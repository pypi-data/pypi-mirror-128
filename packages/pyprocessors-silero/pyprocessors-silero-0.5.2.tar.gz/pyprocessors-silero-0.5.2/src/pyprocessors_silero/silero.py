import io
import os
import wave
from abc import ABC
from enum import Enum
from functools import lru_cache
from tempfile import NamedTemporaryFile
from typing import Type, List, cast

import filetype
import torch
import torchaudio
from pydantic import BaseModel, Field
from pydub import AudioSegment
from pymultirole_plugins.v1.converter import ConverterBase, ConverterParameters
from pymultirole_plugins.v1.formatter import FormatterParameters, FormatterBase
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile
from starlette.responses import Response

_home = os.path.expanduser('~')
xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')


class SileroModel(str, Enum):
    auto = 'auto'
    silero_te = 'silero_te'
    silero_stt = 'silero_stt'
    silero_tts = 'silero_tts'


class SileroSpeaker(str, Enum):
    auto = 'auto'
    aidar_v2 = 'aidar_v2'
    baya_v2 = 'baya_v2'
    irina_v2 = 'irina_v2'
    kseniya_v2 = 'kseniya_v2'
    natasha_v2 = 'natasha_v2'
    ruslan_v2 = 'ruslan_v2'
    lj_v2 = 'lj_v2'
    thorsten_v2 = 'thorsten_v2'
    tux_v2 = 'tux_v2'
    gilles_v2 = 'gilles_v2'
    multi_v2 = 'multi_v2'


lang2speaker = {
    'en': [SileroSpeaker.lj_v2],
    'de': [SileroSpeaker.thorsten_v2],
    'ru': [SileroSpeaker.aidar_v2, SileroSpeaker.baya_v2, SileroSpeaker.irina_v2, SileroSpeaker.kseniya_v2,
           SileroSpeaker.natasha_v2, SileroSpeaker.ruslan_v2],
    'es': [SileroSpeaker.tux_v2],
    'fr': [SileroSpeaker.gilles_v2],
}


class SileroParameters(ProcessorParameters, ConverterParameters, FormatterParameters, ABC):
    model: SileroModel = Field(SileroModel.auto,
                               description="""The model is published in the repository [silero-models](https://github.com/snakers4/silero-models), can be one of:<br/>
                            <li>`silero_stt`: The Speech-To-Text model (to be used as converter).<br/>
                            <li>`silero_tts`: The Text-To-Speech model (to be used as formater).<br/>
                            <li>`silero_te`: The Text Enhancement model (to be used with processor).""")
    lang: str = Field("en",
                      description="""Name of the [language](https://github.com/snakers4/silero-models)
    supported by Silero model,
    can be one of:<br/>
    <li>`en` English
    <li>`de` German
    <li>`ru` Russian
    <li>`es` Spanish
    <li>`fr` French (TTS only)
    """)
    speaker: str = Field("auto",
                         description="""Name of the [speaker](https://github.com/snakers4/silero-models)
    supported by Silero TTS model (for formatter only),
    can be one of:<br/>
    <li>`auto` automatically assign a valid speaker according to the language<br/>
    <li>`aidar_v2` Russian<br/>
    <li>`baya_v2` Russian<br/>
    <li>`irina_v2` Russian<br/>
    <li>`kseniya_v2` Russian<br/>
    <li>`natasha_v2` Russian<br/>
    <li>`ruslan_v2` Russian<br/>
    <li>`lj_v2` English<br/>
    <li>`thorsten_v2` German<br/>
    <li>`tux_v2` Spanish<br/>
    <li>`gilles_v2` French<br/>
    <li>`multi_v2` ru, en, de, es, fr, tt
    """)
    enhance: bool = Field(True, description="Use the Text Enhacement model to restore punctuation and capitalization")
    sample_rate: int = Field(8000, description="Sampling rate (formatter only), can be 8000 or 16000")


class SileroProcessor(ProcessorBase, ConverterBase, FormatterBase, ABC):
    """Silero processor or converter .
    """

    def _enhance(self, text, params: SileroParameters) \
            -> str:
        model, example_texts, languages, punct, apply_te = get_pipeline_te(params.model)
        return apply_te(text, lan=params.lang)

    def process(self, documents: List[Document], parameters: ProcessorParameters) \
            -> List[Document]:
        params: SileroParameters = \
            cast(SileroParameters, parameters)
        if params.model == SileroModel.auto:
            params.model = SileroModel.silero_te
        for document in documents:
            document.text = self._enhance(document.text, params)
        return documents

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: SileroParameters = \
            cast(SileroParameters, parameters)

        if params.model == SileroModel.auto:
            params.model = SileroModel.silero_stt
        # Create cached pipeline context with model
        model, decoder, utils = get_pipeline_stt(params.model, params.lang)
        (read_batch, split_into_batches,
         read_audio, prepare_model_input) = utils  # see function signature for details
        doc: Document = None
        try:
            wav = _read_audio(source.file)
            if wav is not None:
                inputs = prepare_model_input([wav])
                outputs = model(inputs)
                text = decoder(outputs[0])
                if params.enhance:
                    params.model = SileroModel.silero_te
                    text = self._enhance(text, params)
                doc = Document(identifier=source.filename,
                               text=text)
                doc.properties = {"fileName": source.filename}
        except BaseException as err:
            raise err
        if doc is None:
            raise TypeError(f"Conversion of audio file {source.filename} failed")
        return [doc]

    def format(self, document: Document, parameters: FormatterParameters) \
            -> Response:
        params: SileroParameters = \
            cast(SileroParameters, parameters)

        if params.model == SileroModel.auto:
            params.model = SileroModel.silero_stt
        if params.speaker == SileroSpeaker.auto:
            params.speaker = lang2speaker[params.lang][0]
        else:
            if params.speaker not in lang2speaker[params.lang]:
                raise TypeError(f"Not a valid speaker {params.speaker.value} for language {params.lang}")
        filename = "file.wav"
        # Create cached pipeline context with model
        model, example_text = get_pipeline_tts(params.model, params.lang, params.speaker)
        # audio_paths = model.save_wav(texts=[document.text],
        #                              sample_rate=params.sample_rate)
        stexts = []
        if not document.sentences:
            stexts.append(document.text)
        else:
            stexts = [document.text[s.start:s.end] for s in document.sentences]

        audios = model.apply_tts(texts=stexts,
                                 sample_rate=params.sample_rate)

        audiodoc = AudioSegment.empty()
        silence = AudioSegment.silent(1000)
        for audio in audios:
            bio = io.BytesIO()
            with wave.open(bio, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(params.sample_rate)
                wf.writeframes((audio * 32767).numpy().astype('int16'))
                seg = AudioSegment.from_file(bio, format="wav")
                audiodoc += (seg + silence)
        with NamedTemporaryFile('w+b', suffix='.wav') as tmp_file:
            audiodoc.export(tmp_file, format="wav")
            tmp_file.seek(0)
            audiobytes = tmp_file.file.read()
            resp = Response(content=audiobytes,
                            media_type="audio/wav")
            resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
            return resp

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SileroParameters


def _read_audio(path,
                target_sr: int = 16000):
    kind = filetype.guess(path)
    path.seek(0)

    if kind is not None and kind.mime.startswith('audio'):
        wav, sr = torchaudio.load(path, format=kind.extension)

        if wav.size(0) > 1:
            wav = wav.mean(dim=0, keepdim=True)

        if sr != target_sr:
            transform = torchaudio.transforms.Resample(orig_freq=sr,
                                                       new_freq=target_sr)
            wav = transform(wav)
            sr = target_sr

        assert sr == target_sr
        return wav.squeeze(0)
    else:
        return None


@lru_cache(maxsize=None)
def get_pipeline_te(model):
    return torch.hub.load(repo_or_dir='snakers4/silero-models', model=model.value)


@lru_cache(maxsize=None)
def get_pipeline_stt(model, lang):
    return torch.hub.load(repo_or_dir='snakers4/silero-models', model=model.value, language=lang)


@lru_cache(maxsize=None)
def get_pipeline_tts(model, lang, speaker):
    return torch.hub.load(repo_or_dir='snakers4/silero-models', model=model.value, language=lang, speaker=speaker.value)
