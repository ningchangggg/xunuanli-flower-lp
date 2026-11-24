"""鮮花圖鑑日曆落地頁：從印刷檔轉內頁（第 N 天正面＝第 2N 頁，3mm 出血裁掉）。"""
import subprocess, os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
D = os.path.dirname(os.path.abspath(__file__))
PDF = "/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○煦暖曆/03_設計規範/鮮花圖鑑日曆/印刷檔/印刷檔_2027花卉圖鑑曆_3mm出血.pdf"
TMP = D + '/pdf/tmp'; os.makedirs(TMP, exist_ok=True)

def page(day, dpi=200, back=False):
    p = 2 * day + (1 if back else 0)
    out = f'{TMP}/p{p}_{dpi}'
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-f', str(p), '-l', str(p), '-r', str(dpi), '-png', '-singlefile', PDF, out], check=True)
    im = Image.open(out + '.png').convert('RGB')
    w, h = im.size
    bx, by = round(w * 3 / 106), round(h * 3 / 146)
    return im.crop((bx, by, w - bx, h - by))

def ellipse_box(im):
    a = np.asarray(im).astype(int)
    bright = (a.min(axis=2) > 236)
    h, w = bright.shape
    sub = bright[int(h * .15):int(h * .8), int(w * .28):]
    ys, xs = np.nonzero(sub)
    # use rows/cols where white run is substantial
    cols = sub.sum(axis=0); rows = sub.sum(axis=1)
    cx = np.nonzero(cols > cols.max() * .08)[0]; ry = np.nonzero(rows > rows.max() * .08)[0]
    x0, x1 = cx[0] + int(w * .28), cx[-1] + int(w * .28)
    y0, y1 = ry[0] + int(h * .15), ry[-1] + int(h * .15)
    return x0, y0, x1, y1

if __name__ == '__main__':
    os.makedirs(D + '/img/wall', exist_ok=True); os.makedirs(D + '/img/ix', exist_ok=True)
    # persona inner pages
    for d in [80, 7, 20, 365]:
        im = page(d, 200); im.thumbnail((640, 900), Image.LANCZOS); im.save(f'{D}/img/pg{d:03d}.jpg', quality=92)
    # wall: 44 days spread over the year
    days = sorted(set(round(1 + k * 364 / 43) for k in range(44)))
    for i, d in enumerate(days):
        im = page(d, 72); im.thumbnail((260, 400), Image.LANCZOS); im.save(f'{D}/img/wall/{i+1:03d}.jpg', quality=88)
    print('wall', len(days))
    # index circles
    IX = [37, 80, 95, 157, 163, 188, 252, 266, 300, 1, 346, 356]
    for d in IX:
        im = page(d, 300)
        x0, y0, x1, y1 = ellipse_box(im)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; r = min(x1 - x0, y1 - y0) / 2 * .97
        c = im.crop((round(cx - r), round(cy - r), round(cx + r), round(cy + r))).resize((300, 300), Image.LANCZOS)
        m = Image.new('L', (1200, 1200), 0); ImageDraw.Draw(m).ellipse((0, 0, 1199, 1199), fill=255); m = m.resize((300, 300), Image.LANCZOS)
        c.putalpha(m); c.save(f'{D}/img/ix/{d:03d}.png')
        print(d, (x0, y0, x1, y1), im.size)
