import macro

macro.init_lineage_windows()
macro.init_mouse_x_y()
img = macro.screenshot(hwnd=macro.lineage1_hwnd)
adena = macro.readMp(img=img)
print(f"현재 아데나: {adena}")
