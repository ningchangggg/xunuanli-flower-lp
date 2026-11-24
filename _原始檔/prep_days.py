"""06 一頁拆解：8 天正面輪播，每天 1.2 秒（15fps×18 格），上方日期句跟著換。"""
import os, json, shutil
from PIL import Image
from prep_pdf import page
D = os.path.dirname(os.path.abspath(__file__))
F = {o['d']: o for o in json.load(open(D + '/pdf/flowers.json'))}
DAYS = [1, 37, 80, 95, 157, 220, 258, 356]
MON = {'JANUARY': 'JAN.', 'FEBRUARY': 'FEB.', 'MARCH': 'MAR.', 'APRIL': 'APR.', 'MAY': 'MAY', 'JUNE': 'JUN.', 'JULY': 'JUL.', 'AUGUST': 'AUG.', 'SEPTEMBER': 'SEP.', 'OCTOBER': 'OCT.', 'NOVEMBER': 'NOV.', 'DECEMBER': 'DEC.'}
od = D + '/gif/clips/f_days'; shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
caps = []; k = 0
for d in DAYS:
    o = F[d]
    im = page(d, 200).resize((440, 616), Image.LANCZOS)
    fest = ' '.join(o['mid'][1:]).replace(' ', '').replace('•', '・')
    fest = '正月初一' if d == 37 else fest.split('正月')[0]
    en = f"{MON[o['month']]} {o['day']}"
    cap = f'<small class="en">{en}</small>{("<i>" + fest + "</i>") if fest else ""}<br>{o["name"]}・{o["hy"].replace(" ", "")}'
    for _ in range(18):
        k += 1; im.save(f'{od}/{k:03d}.jpg', quality=92); caps.append(cap)
json.dump(caps, open(D + '/gif/caps_f_days.json', 'w'), ensure_ascii=False)
print(k, [c for c in caps[::18]])
