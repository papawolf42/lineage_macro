import easyocr
import numpy as np
from PIL import Image

_reader = None

def ocr(image, lang=['ko', 'en']):
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(lang)
    if isinstance(image, Image.Image):
        image = np.array(image)
    results = _reader.readtext(image)
    return [(bbox, text, conf) for bbox, text, conf in results]

def extract_color(image, target_rgb: tuple, diff_thresh=30, brightness_min=0):
    """특정 색상(target_rgb)에 가까운 픽셀만 남기고 나머지는 검은색으로 처리."""
    if isinstance(image, str):
        image = Image.open(image)
    img = image.convert('RGB')
    arr = np.array(img, dtype=int)
    tr, tg, tb = target_rgb

    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    diff = np.max([np.abs(r - tr), np.abs(g - tg), np.abs(b - tb)], axis=0)
    brightness = (r + g + b) / 3
    mask = (diff < diff_thresh) & (brightness >= brightness_min)

    result = np.zeros_like(arr)
    result[mask] = arr[mask]

    return Image.fromarray(result.astype(np.uint8))


def extract_gray(image, diff_thresh=20, brightness_min=50):
    """회색 픽셀(R≈G≈B)만 남기고 나머지는 검은색으로 처리."""
    if isinstance(image, str):
        image = Image.open(image)
    img = image.convert('RGB')
    arr = np.array(img, dtype=int)

    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    diff = np.max([np.abs(r-g), np.abs(g-b), np.abs(r-b)], axis=0)
    brightness = (r + g + b) / 3
    gray_mask = (diff < diff_thresh) & (brightness >= brightness_min)

    result = np.zeros_like(arr)
    result[gray_mask] = arr[gray_mask]

    return Image.fromarray(result.astype(np.uint8))
