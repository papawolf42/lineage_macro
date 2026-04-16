import time

import macro
import imageProcesser


def main() -> None:
    macro.init_setting("server")
    text = macro.readExchangeNickname()
    print(text)
    macro.force_set_foreground_window(macro.lineage1_hwnd)
    time.sleep(1)
    macro.acceptExchange()
if __name__ == "__main__":
    main()
