"""受眾卡與各區照片裁切。box 用比例 (x0,y0,w)，高度依輸出比例算。"""
import os
from PIL import Image, ImageEnhance
D = os.path.dirname(os.path.abspath(__file__))
M = "/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○煦暖曆/01_廣告投放/鮮花圖鑑日曆/毛片/麻豆_照片_0809/"
C = {
 # name: (src, x0, y0, w(frac of width), out_w, out_h, sat)
 'p1': (D + '/src/zj_36.2.jpg', 0.0, 0.035, 1.0, 930, 1100, 1.06),
 'p2': (D + '/src/d77_18.2.jpg', 0.0, 0.24, 1.0, 930, 1100, 1.25),
 'p3': (M + '台灣模特兒與日曆/2027煦暖曆系列_毛片-574.jpg', 0.0, 0.0, 1.0, 930, 1100, 1.0),
 'p4': (M + '台灣模特兒與日曆/2027煦暖曆系列_毛片-600.jpg', 0.0, 0.06, 1.0, 930, 1100, 1.0),
 's10': (M + '五本花日曆/2027煦暖曆系列_毛片-541.jpg', 0.023, 0.0, 0.954, 930, 650, 1.0),
 's11': (M + '單本花日曆/2027煦暖曆系列_毛片-527.jpg', 0.06, 0.0, 0.827, 930, 750, 1.0),
 's12': (M + '台灣模特兒與日曆/2027煦暖曆系列_毛片-565.jpg', 0.0, 0.08, 1.0, 930, 1150, 1.0),
}
def run(sel=None):
    os.makedirs(D + '/img', exist_ok=True)
    for k, (src, x0, y0, w, ow, oh, sat) in C.items():
        if sel and k not in sel: continue
        im = Image.open(src).convert('RGB'); W, H = im.size
        cw = W * w; ch = cw * oh / ow
        bx, by = W * x0, H * y0
        if by + ch > H: by = H - ch
        c = im.crop((round(bx), round(by), round(bx + cw), round(by + ch))).resize((ow, oh), Image.LANCZOS)
        if sat != 1: c = ImageEnhance.Color(c).enhance(sat)
        c.save(f'{D}/img/{k}.jpg', quality=90)
        print(k, im.size, (round(bx), round(by), round(cw), round(ch)))
if __name__ == '__main__':
    import sys; run(sys.argv[1:])
