"""
client.py - Pickup 클라이언트
  - 서버에 TCP 연결 후 명령 수신
  - "pickup" 명령에 따라 lineage1_hwnd / lineage2_hwnd 픽업 실행
  - 소켓 끊김 시 자동 재연결 시도
"""

import socket
import json
import time
import sys

import macro

SERVER_HOST = '192.168.0.1'  # ← 서버 IP로 변경
SERVER_PORT = 9999
RECONNECT_DELAY = 5  # 재연결 대기 시간(초)

running = True


def _send_json(conn: socket.socket, obj: dict) -> bool:
    try:
        conn.sendall((json.dumps(obj) + '\n').encode())
        return True
    except OSError:
        return False


def _recv_json(conn: socket.socket) -> dict | None:
    buf = b''
    try:
        while b'\n' not in buf:
            chunk = conn.recv(4096)
            if not chunk:
                return None
            buf += chunk
        return json.loads(buf.split(b'\n')[0].decode())
    except (OSError, json.JSONDecodeError):
        return None


def _handle_command(msg: dict) -> bool:
    """
    수신된 명령 처리. True 반환 시 ack 필요.
    """
    cmd = msg.get("cmd")

    if cmd == "ping":
        return False  # ack 불필요

    if cmd == "pickup":
        target = msg.get("target")
        print(f"[client] 픽업 명령 수신: {target}")
        if target == "lineage1":
            macro.pickup_lineage1()
        elif target == "lineage2":
            macro.pickup_lineage2()
        else:
            print(f"[client] 알 수 없는 target: {target}")
        return True

    print(f"[client] 알 수 없는 명령: {msg}")
    return False


def _run(conn: socket.socket):
    print("[client] 서버 연결됨")
    while running:
        msg = _recv_json(conn)
        if msg is None:
            print("[client] 서버 연결 끊김")
            break

        needs_ack = _handle_command(msg)
        if needs_ack:
            if not _send_json(conn, {"status": "ok"}):
                print("[client] ack 전송 실패")
                break


def main():
    macro.init_lineage_windows("client")
    macro.init_mouse_x_y()

    while running:
        try:
            print(f"[client] 서버에 연결 시도 중: {SERVER_HOST}:{SERVER_PORT}")
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((SERVER_HOST, SERVER_PORT))
            _run(conn)
        except (ConnectionRefusedError, OSError) as e:
            print(f"[client] 연결 실패: {e}")
        finally:
            try:
                conn.close()
            except OSError:
                pass

        if running:
            print(f"[client] {RECONNECT_DELAY}초 후 재연결...")
            time.sleep(RECONNECT_DELAY)


if __name__ == "__main__":
    print("명령어: q=종료 (별도 입력창 없음, Ctrl+C로 종료)")
    try:
        main()
    except KeyboardInterrupt:
        running = False
        print("[client] 종료")
