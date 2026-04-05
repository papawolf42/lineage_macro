from PIL import Image
import numpy as np
import os
import json


_SPECIAL_CHARS = r"""`~!@#$%^&*()_+-=[]{}\|;:'",<.>/?"""

def all_chars():
    """a-z, A-Z, 특수문자, 한글 음절(가~힣) 순서로 모든 문자를 yield한다."""
    for c in range(ord('a'), ord('z') + 1):
        yield chr(c)
    for c in range(ord('A'), ord('Z') + 1):
        yield chr(c)
    for ch in _SPECIAL_CHARS:
        yield ch
    for c in range(ord('0'), ord('9') + 1):
        yield chr(c)
    for c in range(0xAC00, 0xD7A4):
        yield chr(c)


def pixels_to_string(arr):
    mask = (arr[:,:,0] == 255) & (arr[:,:,1] == 255) & (arr[:,:,2] == 255)
    ys, xs = np.where(mask)
    coords = sorted(zip(xs, ys))
    return ''.join(f"{x}{y}" for x, y in coords)


BASE = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE, "data2")
OUTPUT_JSON   = os.path.join(BASE, "converted_data.json")

chars = list(all_chars())

def sort_key(f):
    stem = f.replace(".png", "")
    return (0, int(stem)) if stem.isascii() and stem.lstrip('-').isdigit() else (1, ord(stem[0]))

files = sorted(os.listdir(PROCESSED_DIR), key=sort_key)

lookup = {}
for fname in files:
    if not fname.endswith(".png"):
        continue
    stem = fname.replace(".png", "")
    if stem.isascii() and stem.lstrip('-').isdigit():
        char = chars[int(stem)]
    else:
        char = stem
    arr = np.array(Image.open(os.path.join(PROCESSED_DIR, fname)).convert("RGB"))
    s = pixels_to_string(arr)
    lookup[s] = char

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(lookup, f, ensure_ascii=False, indent=2)

print(f"저장 완료: {OUTPUT_JSON} ({len(lookup)}개)")
