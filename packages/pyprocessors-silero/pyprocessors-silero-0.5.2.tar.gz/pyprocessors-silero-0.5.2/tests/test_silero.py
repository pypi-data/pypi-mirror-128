import json
from pathlib import Path
from typing import List

from starlette.responses import Response

from pyprocessors_silero.silero import SileroProcessor, SileroParameters, SileroModel
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile


def test_silero_te():
    model = SileroProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == SileroParameters
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/test.txt')
    with source.open("r") as fin:
        doc = Document(text=fin.read())
    original_text = doc.text
    processor = SileroProcessor()
    parameters = SileroParameters(model=SileroModel.silero_te)
    docs: List[Document] = processor.process([doc], parameters)
    doc0 = docs[0]
    assert original_text != doc0.text


def test_silero_stt():
    converter = SileroProcessor()
    parameters = SileroParameters(model=SileroModel.silero_stt, enhance=False)
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/160628_news_report_brexit_download.mp3')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/mpeg'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'british' in doc0.text
        assert 'david cameron' in doc0.text
        assert 'David Cameron' not in doc0.text
        assert ',' not in doc0.text

        fin.seek(0)
        parameters = SileroParameters(model=SileroModel.silero_stt, enhance=True)
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/mpeg'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'david cameron' not in doc0.text
        assert 'David Cameron' in doc0.text
        assert ',' in doc0.text


def test_silero_tts():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/test.txt')
    with source.open("r") as fin:
        doc = Document(text=fin.read())
    processor = SileroProcessor()
    parameters = SileroParameters(model=SileroModel.silero_tts, lang='en')
    resp: Response = processor.format(doc, parameters)
    assert resp.status_code == 200
    assert resp.media_type == "audio/wav"
    result = Path(testdir, 'data/test.wav')
    with result.open("wb") as fout:
        fout.write(resp.body)


def test_silero_tts_french():
    testdir = Path(__file__).parent
    json_file = Path(testdir, 'data/french.json')
    with json_file.open("r") as fin:
        doc = json.load(fin)
    doc = Document(**doc)
    processor = SileroProcessor()
    parameters = SileroParameters(model=SileroModel.silero_tts, lang='fr')
    resp: Response = processor.format(doc, parameters)
    assert resp.status_code == 200
    assert resp.media_type == "audio/wav"
    result = Path(testdir, 'data/french.wav')
    with result.open("wb") as fout:
        fout.write(resp.body)
