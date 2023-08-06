import os
from abc import ABC
from enum import Enum
from functools import lru_cache
from typing import Type, List, cast

import filetype
import torch
import torchaudio
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.converter import ConverterBase, ConverterParameters
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile

_home = os.path.expanduser('~')
xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')


class SileroModel(str, Enum):
    silero_te = 'silero_te'
    silero_stt = 'silero_stt'


class SileroParameters(ProcessorParameters, ConverterParameters, ABC):
    model: SileroModel = Field(SileroModel.silero_te,
                               description="""The model is published in the repository [silero-models](https://github.com/snakers4/silero-models), can be one of:<br/>
                            <li>`silero_stt`: The Speech-To-Text model (to be used with converter).<br/>
                            <li>`silero_te`: The Text Enhancement model (to be used with processor).""")
    lang: str = Field("en",
                      description="""Name of the [language](https://github.com/snakers4/silero-models)
    supported by Silero model,
    can be one of:<br/>
    <li>`en` English
    <li>`de` German
    <li>`ru` Russian
    <li>`es` Spanish
    """)
    enhance: bool = Field(True, description="Use the Text Enhacement model to restore punctuation and capitalization")


class SileroProcessor(ProcessorBase, ConverterBase, ABC):
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
        for document in documents:
            document.text = self._enhance(document.text, params)
        return documents

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: SileroParameters = \
            cast(SileroParameters, parameters)

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
    return torch.hub.load(repo_or_dir='snakers4/silero-models', model=model)


@lru_cache(maxsize=None)
def get_pipeline_stt(model, lang):
    return torch.hub.load(repo_or_dir='snakers4/silero-models', model=model, language=lang)
