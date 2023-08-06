from pathlib import Path
from typing import List

from pyconverters_speech.speech import SpeechConverter, SpeechParameters, TrfModel
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile


def test_speech_wav():
    model = SpeechConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == SpeechParameters
    converter = SpeechConverter()
    parameters = SpeechParameters()
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/2.wav')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/wav'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert doc0.text.startswith('on bed seven')


def test_speech_mp3():
    model = SpeechConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == SpeechParameters
    converter = SpeechConverter()
    parameters = SpeechParameters(model=TrfModel.hubert_large_ls960_ft)
    parameters = SpeechParameters()
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/160628_news_report_brexit_download.mp3')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/mpeg'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'british' in doc0.text
