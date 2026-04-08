import threading
import macro
import ocr
import imageProcesser
from http.server import BaseHTTPRequestHandler, HTTPServer

running = True

def _serve():
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            global running
            if self.path == "/end":
                running = False
            self.send_response(200)
            self.end_headers()
        log_message = lambda *a: None
    HTTPServer(("", 8765), H).serve_forever()

threading.Thread(target=_serve, daemon=True).start()

if __name__ == "__main__":
    macro.init_lineage_windows()
    macro.init_mouse_x_y()

    print("\n명령어: q=종료  /end → http://localhost:8765/end")
    while True:
        cmd = input("> ").strip()
        if cmd == "q":
            break
        if cmd == "1":
            macro.force_set_foreground_window(macro.lineage1_hwnd)
            running = True
            while running:
                macro.accept_exchange_and_track_adena()
        if cmd == "2":
            img = macro.screenshot()
            img.save("screenshot.png")
        if cmd == "3":
            img = macro.screenshot()
            cropped = imageProcesser.crop(img, 717, 667, 100, 21)
            results = ocr.ocr(cropped, ['en'])
            text = ' '.join(t for _, t, _ in results)
            before_slash = text.split('/')[0].strip()
            mp = int(''.join(c for c in before_slash if c.isdigit()) or 0)
            print(mp)
