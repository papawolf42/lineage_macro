import json
import macro
from tools.imageProcesser import crop, read_text, image_to_coord_string

with open("converted_data.json", "r", encoding="utf-8") as f:
    converted_data = json.load(f)

macro.set_hwnd(1117856)
macro.move_window(0, 0)

img = macro.screenshot()
cropped = crop(img, 228, 907, 500, 25)
cropped.save("cropped.png")
cropped2 = crop(cropped, 0, 0, 10, 24)
cropped2.save("cropped2.png")
str = image_to_coord_string(cropped2, (0xAF, 0xEB, 0xEB))
print(str)
if str in converted_data:
    print(converted_data[str])
else:
    print(f"'{str}' not found in converted_data")
text = read_text(cropped, 0, 0, (0xAF, 0xEB, 0xEB))
print(text)

