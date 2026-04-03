import easyocr
import numpy as np
from PIL import Image

_reader = None

def get_reader(languages: list[str] = ['ko', 'en']) -> easyocr.Reader:
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(languages, gpu=False)
    return _reader


def ocr_image(image: Image.Image, languages: list[str] = ['ko', 'en']) -> str:
    reader = get_reader(languages)
    img_array = np.array(image)
    results = reader.readtext(img_array)
    return ' '.join(text for _, text, _ in results)
