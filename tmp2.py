import macro

macro.set_hwnd(1117856)
macro.move_window(0, 0)

img = macro.screenshot()
cropped = img.crop((249, 933, 269, 957))
cropped.save("cropped.png")
cropped.show()
