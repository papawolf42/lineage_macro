from PIL import Image
import numpy as np
import os

TARGET_DIRS = [
    r"C:\Users\eno\test\data",
    r"C:\Users\eno\test\processed_data",
    r"C:\Users\eno\test\tmp_add_processed",
]

def _measure_cursor_height(ref_path: str) -> int:
    """기준 이미지의 높이로부터 커서 높이를 계산한다. (이미지 높이 - 4)"""
    img_h = Image.open(ref_path).size[1]
    cursor_h = img_h - 4
    print(f"[delete_cursor] 이미지 높이: {img_h}px → 커서 높이: {cursor_h}px")
    return cursor_h

CURSOR_HEIGHT = _measure_cursor_height(r"C:\Users\eno\test\data\0.png")

def remove_cursors(data_dir):
    if not os.path.isdir(data_dir):
        print(f"디렉토리 없음: {data_dir}")
        return []

    files = sorted(
        [f for f in os.listdir(data_dir) if f.endswith(".png")],
        key=lambda f: (0, int(f.split(".")[0])) if f.split(".")[0].isdigit() else (1, f)
    )

    removed = []

    for fname in files:
        path = os.path.join(data_dir, fname)
        img = Image.open(path)
        arr = np.array(img)

        white = (arr[:,:,0] > 200) & (arr[:,:,1] > 200) & (arr[:,:,2] > 200)
        col_px = white.sum(axis=0)
        active_cols = np.where(col_px > 0)[0]

        if len(active_cols) == 0:
            continue

        cmax = int(active_cols[-1])

        # 커서 감지: 가장 오른쪽 열의 흰 픽셀 수가 기준 커서 높이와 일치하고 바로 왼쪽 열이 커서보다 훨씬 작음
        if col_px[cmax] == CURSOR_HEIGHT and (cmax == 0 or col_px[cmax - 1] < CURSOR_HEIGHT // 2):
            arr[:, cmax] = [0, 0, 0]  # 커서 열을 배경(검정)으로 덮어씀
            Image.fromarray(arr).save(path)
            removed.append(fname)

    return removed

for d in TARGET_DIRS:
    removed = remove_cursors(d)
    print(f"[{d}] 커서 제거: {len(removed)}개")
    for f in removed:
        print(f"  {f}")
