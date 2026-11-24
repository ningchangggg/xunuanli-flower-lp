"""鮮花圖鑑日曆落地頁實拍動圖片段（2026-11-25）。丁丁用「調色對齊麻豆」版本，彩度 1.45、對比 1.05（規範）；裁 4:5。"""
import subprocess, os, shutil, sys
from concurrent.futures import ThreadPoolExecutor
M = "/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○煦暖曆/01_廣告投放/鮮花圖鑑日曆/毛片/"
DD = M + '丁丁_Log_0912_調色對齊麻豆/'
FPS = 15
C = {  # name: (src, t0, t1, speed, crop_y(0-1) or crop_x for landscape, landscape)
 'f_tear':    (DD + 'C0074.mp4', 1.9, 6.4, 1.1, 0.42, False),
 'f_back':    (DD + 'C0072.mp4', 3.0, 9.6, 1.25, 0.45, False),
 'f_collect': (DD + 'C0083.mp4', 0.3, 7.6, 1.2, 0.50, True),
 'f_bed':     (DD + 'C0076.mp4', 1.8, 9.8, 1.5, 0.40, False),
}
def run(item):
    n, (src, t0, t1, sp, c, land) = item
    od = os.path.dirname(os.path.abspath(__file__)) + f'/clips/{n}'; shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
    crop = f"crop=ih*0.8:ih:(iw-ih*0.8)*{c}:0" if land else f"crop=iw:iw*1.25:0:(ih-iw*1.25)*{c}"
    vf = f"setpts=PTS/{sp},fps={FPS},{crop},scale=930:1163:flags=lanczos,eq=saturation=1.45:contrast=1.05"
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', src, '-vf', vf, '-q:v', '2', f'{od}/%03d.jpg'], check=True, stdin=subprocess.DEVNULL)
    return n, len(os.listdir(od))
sel = sys.argv[1:] or list(C)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(run, [(k, C[k]) for k in sel]): print(r)
