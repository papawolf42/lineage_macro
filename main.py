import threading
import time
import win32gui
import win32con
import macro
import ocr


def enum_windows_callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            windows.append((hwnd, title))


def get_open_windows():
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows


def select_hwnd():
    windows = get_open_windows()
    print(f"{'#':<4} {'HWND':<12} {'Title'}")
    print("-" * 60)
    for i, (hwnd, title) in enumerate(windows):
        print(f"{i:<4} {hwnd:<12} {title}")

    idx = int(input("\n번호 선택: "))
    hwnd, title = windows[idx]
    macro.set_hwnd(hwnd)


if __name__ == "__main__":
    macro.init_lineage_windows()
    macro.init_mouse_x_y((726, 402), (1321, 402))

    print("\n명령어: 1=클릭, 2=스크린샷, 3=모든 문자 전송, q=종료")
    while True:
        cmd = input("> ").strip()
        if cmd == "q":
            break
        elif cmd == "0":
            mp = macro.readMp()
            print(f"현재 MP: {mp}")
        elif cmd == "1":
            adena = macro.readAdena()
            print(f"현재 아데나: {adena}")
        elif cmd == "2":
            time.sleep(3)
            img = macro.screenshot()
            img.save("image/screenshot.png")
        elif cmd == "3":
            macro.accept_exchange_and_track_adena()
        elif cmd == "4":
            # 교환창 마지막 슬롯 좌표 보정 확인
            macro.calibrate_exchange_slot()
        elif cmd == "5":
            # 상대 교환 확인 여부 단발 체크
            confirmed = macro.checkExchangeConfirmed()
            print(f"상대 확인 여부: {'YES' if confirmed else 'NO'}")
