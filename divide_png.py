from PIL import Image
import numpy as np
import os

data_dir = r"C:\Users\eno\test\processed_data"

src_dir = r"C:\Users\eno\test\data2"
dst_dir = r"C:\Users\eno\test\data3"
os.makedirs(dst_dir, exist_ok=True)

removed = []
for fname in os.listdir(src_dir):
    if not fname.lower().endswith(".png"):
        continue
    path = os.path.join(src_dir, fname)
    img = Image.open(path)
    arr = np.array(img)
    cursor_h = img.size[1] - 4

    white = (arr[:,:,0] > 200) & (arr[:,:,1] > 200) & (arr[:,:,2] > 200)
    col_px = white.sum(axis=0)
    active_cols = np.where(col_px > 0)[0]

    if len(active_cols) > 0:
        cmax = int(active_cols[-1])
        if col_px[cmax] == cursor_h and (cmax == 0 or col_px[cmax - 1] < cursor_h // 2):
            arr[:, cmax] = [0, 0, 0]
            removed.append(fname)

    Image.fromarray(arr).save(os.path.join(dst_dir, fname))

print(f"커서 제거: {len(removed)}개")
for f in removed:
    print(f"  {f}")

# data3 -> data4: 한 글자씩 분할
data4_dir = r"C:\Users\eno\test\data4"
os.makedirs(data4_dir, exist_ok=True)

def get_active_x_range(arr):
    white = (arr[:,:,0] > 200) & (arr[:,:,1] > 200) & (arr[:,:,2] > 200)
    col_px = white.sum(axis=0)
    active_cols = np.where(col_px > 0)[0]
    if len(active_cols) == 0:
        return None, None
    return int(active_cols[0]), int(active_cols[-1])

# 1단계: char_w 추정 (여러 파일 샘플링)
char_w_samples = []
for fname in os.listdir(dst_dir):
    if not fname.lower().endswith(".png"):
        continue
    chars = list(os.path.splitext(fname)[0])
    if len(chars) == 0:
        continue
    arr = np.array(Image.open(os.path.join(dst_dir, fname)))
    x0, x1 = get_active_x_range(arr)
    if x0 is None:
        continue
    char_w_samples.append((x1 - x0 + 1) / len(chars))

char_w = round(np.median(char_w_samples))
print(f"추정 글자 너비: {char_w}px (샘플 {len(char_w_samples)}개)")

# 2단계: 분할 저장
total = 0
for fname in sorted(os.listdir(dst_dir)):
    if not fname.lower().endswith(".png"):
        continue
    chars = list(os.path.splitext(fname)[0])
    if len(chars) == 0:
        continue
    img = Image.open(os.path.join(dst_dir, fname))
    arr = np.array(img)
    x0, _ = get_active_x_range(arr)
    if x0 is None:
        print(f"  경고: {fname} 흰 픽셀 없음")
        continue
    for idx, char in enumerate(chars):
        cx0 = x0 + idx * char_w
        cx1 = cx0 + char_w
        char_arr = np.array(img.crop((cx0, 0, cx1, img.height)))
        white = (char_arr[:,:,0] > 200) & (char_arr[:,:,1] > 200) & (char_arr[:,:,2] > 200)
        if white.any():
            active_cols = np.where(white.any(axis=0))[0]
            if active_cols[0] == 0:
                cx0 = max(0, cx0 - 1)
            if active_cols[-1] == char_w - 1:
                cx1 = min(img.width, cx1 + 1)
        crop = img.crop((cx0, 0, cx1, img.height))
        crop.save(os.path.join(data4_dir, f"{char}.png"))
    total += len(chars)
    print(f"{fname}: {len(chars)}글자 분할")

print(f"\n총 {total}개 저장 → {data4_dir}")

def analyze(i):
    arr = np.array(Image.open(os.path.join(data_dir, f"{i}.png")))
    red = (arr[:,:,0] > 200) & (arr[:,:,1] < 50) & (arr[:,:,2] < 50)

    col_px = red.sum(axis=0)
    active_cols = np.where(col_px > 0)[0]
    if len(active_cols) == 0:
        return None

    cmin, cmax = int(active_cols[0]), int(active_cols[-1])

    # 커서 감지: 가장 오른쪽 활성 열이 full-height (12px)이고 바로 왼쪽 열이 비어있음
    cursor_col = None
    if col_px[cmax] >= 11 and (cmax == 0 or col_px[cmax - 1] == 0):
        cursor_col = cmax
        # 커서 열 제거
        char_red = red.copy()
        char_red[:, cursor_col] = False
        active_cols_char = np.where(char_red.any(axis=0))[0]
    else:
        char_red = red
        active_cols_char = active_cols

    if len(active_cols_char) == 0:
        return {"i": i, "cursor": cursor_col is not None, "char_w": 0, "char_h": 0}

    rows_char = np.where(char_red.any(axis=1))[0]
    cmin_c, cmax_c = int(active_cols_char[0]), int(active_cols_char[-1])
    rmin_c, rmax_c = int(rows_char[0]), int(rows_char[-1])
    char_w = cmax_c - cmin_c + 1
    char_h = rmax_c - rmin_c + 1

    return {
        "i": i, "cursor": cursor_col is not None,
        "char_w": char_w, "char_h": char_h,
        "rmin": rmin_c, "rmax": rmax_c
    }

print(f"{'idx':>4} {'cursor':>7} {'char_w':>7} {'char_h':>7}  {'rows':>10}")
print("-" * 50)
for i in range(52):
    r = analyze(i)
    cursor_mark = "YES" if r["cursor"] else "-"
    print(f"[{r['i']:2d}]  {cursor_mark:>6}    w={r['char_w']:2d}    h={r['char_h']:2d}  rows {r['rmin']}-{r['rmax']}")
