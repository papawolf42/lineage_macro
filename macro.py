import os
import win32api
import win32con
import win32gui
import win32ui
import time
from ctypes import windll
from datetime import datetime
from PIL import Image

_hwnd = None


def set_hwnd(hwnd: int):
    global _hwnd
    if not win32gui.IsWindow(hwnd):
        raise ValueError(f"유효하지 않은 HWND: {hwnd}")
    _hwnd = hwnd
    print(f"[macro] HWND 설정됨: {hwnd} ({win32gui.GetWindowText(hwnd)})")


def _find_lineage_hwnd() -> int:
    result = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd).startswith("Lineage Classic"):
            result.append(hwnd)
    win32gui.EnumWindows(callback, None)
    if not result:
        raise RuntimeError("'Lineage Classic'으로 시작하는 윈도우를 찾을 수 없습니다.")
    return result[0]


def get_hwnd() -> int:
    global _hwnd
    if _hwnd is None:
        _hwnd = _find_lineage_hwnd()
        print(f"[macro] HWND 자동 설정됨: {_hwnd} ({win32gui.GetWindowText(_hwnd)})")
    return _hwnd


def focus_window():
    hwnd = get_hwnd()
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.05)


def key_down(vk: int):
    win32api.keybd_event(vk, 0, 0, 0)


def key_up(vk: int):
    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)


def key_press(vk: int, duration: float = 0.05):
    key_down(vk)
    time.sleep(duration)
    key_up(vk)


def move_window(x: int, y: int):
    hwnd = get_hwnd()
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    win32gui.MoveWindow(hwnd, x, y, width, height, True)


def screenshot(filename: str = None) -> str:
    hwnd = get_hwnd()
    rect = win32gui.GetWindowRect(hwnd)
    w = int((rect[2] - rect[0]))
    h = int((rect[3] - rect[1]))

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(bitmap)

    windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)
    img = Image.frombuffer("RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)

    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    img = img.crop((0, 0, img.width - 16, img.height - 41))

    if filename is None:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"

    os.makedirs("image", exist_ok=True)
    # path = os.path.join("image", filename)
    # img.save(path)
    # print(f"[macro] 스크린샷 저장됨: {path}")
    return img


def mouse_click_left(x: int, y: int):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def mouse_click_right(x: int, y: int):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


# 두벌식 표준 자판: 단일 자모 → (물리키, shift)
_JAMO_KEY_MAP = {
    'ㄱ': ('R', False), 'ㄲ': ('R', True),  'ㄴ': ('S', False),
    'ㄷ': ('E', False), 'ㄸ': ('E', True),  'ㄹ': ('F', False),
    'ㅁ': ('A', False), 'ㅂ': ('Q', False), 'ㅃ': ('Q', True),
    'ㅅ': ('T', False), 'ㅆ': ('T', True),  'ㅇ': ('D', False),
    'ㅈ': ('W', False), 'ㅉ': ('W', True),  'ㅊ': ('C', False),
    'ㅋ': ('Z', False), 'ㅌ': ('X', False), 'ㅍ': ('V', False),
    'ㅎ': ('G', False),
    'ㅏ': ('K', False), 'ㅐ': ('O', False), 'ㅑ': ('I', False),
    'ㅒ': ('O', True),  'ㅓ': ('J', False), 'ㅔ': ('P', False),
    'ㅕ': ('U', False), 'ㅖ': ('P', True),  'ㅗ': ('H', False),
    'ㅛ': ('Y', False), 'ㅜ': ('N', False), 'ㅠ': ('B', False),
    'ㅡ': ('M', False), 'ㅣ': ('L', False),
}

# 복합 자모 → 단일 자모 시퀀스
_COMPOUND_JAMO = {
    'ㄳ': ['ㄱ', 'ㅅ'], 'ㄵ': ['ㄴ', 'ㅈ'], 'ㄶ': ['ㄴ', 'ㅎ'],
    'ㄺ': ['ㄹ', 'ㄱ'], 'ㄻ': ['ㄹ', 'ㅁ'], 'ㄼ': ['ㄹ', 'ㅂ'],
    'ㄽ': ['ㄹ', 'ㅅ'], 'ㄾ': ['ㄹ', 'ㅌ'], 'ㄿ': ['ㄹ', 'ㅍ'],
    'ㅀ': ['ㄹ', 'ㅎ'], 'ㅄ': ['ㅂ', 'ㅅ'],
    'ㅘ': ['ㅗ', 'ㅏ'], 'ㅙ': ['ㅗ', 'ㅐ'], 'ㅚ': ['ㅗ', 'ㅣ'],
    'ㅝ': ['ㅜ', 'ㅓ'], 'ㅞ': ['ㅜ', 'ㅔ'], 'ㅟ': ['ㅜ', 'ㅣ'],
    'ㅢ': ['ㅡ', 'ㅣ'],
}

_CHOSEONG  = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
_JUNGSEONG = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
_JONGSEONG = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']


def _decompose_hangul(ch: str):
    code = ord(ch) - 0xAC00
    return (
        _CHOSEONG[code // (21 * 28)],
        _JUNGSEONG[(code % (21 * 28)) // 28],
        _JONGSEONG[code % 28],
    )


def _press_key(vk: int, shift: bool = False):
    if shift:
        win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(vk, 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
    if shift:
        win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)


def _send_jamo(jamo: str):
    if jamo in _COMPOUND_JAMO:
        for j in _COMPOUND_JAMO[jamo]:
            _send_jamo(j)
        return
    key, shift = _JAMO_KEY_MAP[jamo]
    _press_key(ord(key), shift)


def _send_char(ch: str):
    if ord(ch) <= 0x7F:
        win32api.PostMessage(get_hwnd(), win32con.WM_CHAR, ord(ch), 0)
    else:
        cho, jung, jong = _decompose_hangul(ch)
        _send_jamo(cho)
        _send_jamo(jung)
        if jong:
            _send_jamo(jong)
        # IME 조합 버퍼 강제 확정 (없으면 다음 자모와 합쳐짐)
        _press_key(win32con.VK_RIGHT)


def _backspace(n: int):
    for _ in range(2 * n):
        win32api.SendMessage(get_hwnd(), win32con.WM_KEYDOWN, win32con.VK_BACK, 0)
        time.sleep(0.01)
        win32api.SendMessage(get_hwnd(), win32con.WM_KEYUP, win32con.VK_BACK, 0)
        time.sleep(0.01)


def send_all_chars(interval: float = 0.2, batch_size: int = 25):
    """a-z, A-Z, 특수문자는 1글자씩, 한글은 batch_size씩 묶어 스크린샷 캡처 및 저장 후 지운다."""
    import sys as _sys; _sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
    import imageProcesser
    from convert_show import all_chars

    os.makedirs("data2", exist_ok=True)
    focus_window()

    ascii_chars   = [ch for ch in all_chars() if ord(ch) <= 0x7F]
    hangul_chars  = [ch for ch in all_chars() if ord(ch) > 0x7F]

    # 1단계: ASCII (a-z, A-Z, 특수문자) — 1글자씩
    # for i, ch in enumerate(ascii_chars):
    #     print("[macro] 문자 전송:", ch)
    #     _send_char(ch)
    #     time.sleep(interval)

    #     img = screenshot()
    #     cropped = imageProcesser.crop(img, 248, 933, 40, 24)
    #     save_path = os.path.join("data2", f"{i}.png")
    #     cropped.save(save_path)
    #     print(f"[macro] 저장됨: {save_path}")

    #     _backspace(1)
    #     time.sleep(1)

    # 2단계: 한글 — batch_size씩
    start_ch = '냢'
    hangul_chars = hangul_chars[hangul_chars.index(start_ch):]
    for batch_idx in range(0, len(hangul_chars), batch_size):
        batch = hangul_chars[batch_idx:batch_idx + batch_size]

        for ch in batch:
            print("[macro] 문자 전송:", ch)
            _send_char(ch)
            time.sleep(interval)

        img = screenshot()
        cropped = imageProcesser.crop(img, 248, 933, 40 * len(batch), 24)
        save_path = os.path.join("data2", f"{''.join(batch)}.png")
        cropped.save(save_path)
        print(f"[macro] 저장됨: {save_path} ({len(batch)}글자)")

        _backspace(len(batch))
        time.sleep(1)
