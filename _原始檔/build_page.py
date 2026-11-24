"""鮮花圖鑑日曆落地頁 v5（2026-11-25）：照幹話曆 v11 的區塊結構，視覺語言換成「植物圖鑑・標本卡」。產出 page.html，432 寬。
字：中文全部凝書體（不加粗、不描邊），英文小標 Helvetica 寬字距。"""
import os, json, math, random
D = os.path.dirname(os.path.abspath(__file__))
V = 'v5'

# 五款底座色（取自 541 實拍底座）
BASE = [('繡球晴藍', '#A9C2DA'), ('紫藤薄霧', '#B9A9D1'), ('亞麻日光', '#C2B39C'), ('葉影晨綠', '#A6CFC1'), ('山茶暮紅', '#8E3D4E')]

P = [
    dict(n='01', who='愛花的人', h='家裡的花，<br>總是開沒幾天就謝了', img='p1', pg='pg080',
         s='每天一朵<mark>手繪花</mark>，桌上的花<mark>一整年都不會謝</mark>。'),
    dict(n='02', who='想對自己好一點', h='每天都好忙，<br>也想留點時間給自己', img='p2', pg='pg007',
         s='早上讀一句<mark>花語</mark>，給自己一分鐘的<mark>溫柔</mark>。'),
    dict(n='03', who='交換禮物', h='預算一千，<br>送一束不會謝的花', img='p3', pg='pg020',
         s='五款花色挑一款，抽到的人<mark>每天都收到一朵花</mark>。'),
    dict(n='04', who='聖誕禮物', h='每天收到一朵花的人，<br>會被寵成什麼樣的公主？', img='p4', pg='pg365',
         s='每天替你送他<mark>一朵花</mark>，連續寵他 <mark>365 天</mark>。'),
]
# 版面：泡泡、內頁卡、貼紙位置（避開臉和手上的日曆）
L = [
    dict(say='right:12px;top:16px', tail='left:34px', card='left:10px;bottom:14px;transform:rotate(-6deg)', tape='#D98C96',
         stk=('flower', '#D98C96', 'left:2px;top:200px;transform:rotate(-8deg)'), rot=-.8),
    dict(say='left:12px;bottom:16px', tail='right:40px', card='right:10px;bottom:14px;transform:rotate(6deg)', tape='#9FC3A8',
         stk=('leaf', '#8FB39A', 'right:22px;top:20px;transform:rotate(10deg)'), rot=.8),
    dict(say='left:12px;top:16px', tail='right:34px', card='right:10px;bottom:14px;transform:rotate(6deg)', tape='#A9C2DA',
         stk=('gift', '#8FAFD0', 'right:20px;top:16px;transform:rotate(8deg)'), rot=-.8),
    dict(say='left:10px;bottom:16px;font-size:16.5px;padding:8px 13px 9px', tail='left:40px', card='right:8px;bottom:20px;transform:rotate(5deg)', tape='#C99AA6',
         stk=('crown', '#9A3E4E', 'left:22px;top:22px;transform:rotate(-10deg)'), rot=.8),
]

ICON = {
    'flower': ''.join(f'<ellipse cx="20" cy="10.5" rx="5.6" ry="8" transform="rotate({a} 20 20)"/>' for a in range(0, 360, 72)) + '<circle cx="20" cy="20" r="4.2" fill="#F3D98E"/>',
    'leaf': '<path d="M20 35 C20 25 20 15 21 6" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
            '<path d="M20.5 14 C13 13 9 8 9 4 C15 4 20 8 20.5 14Z"/><path d="M20.5 14 C27 12 31 8 31 4 C25 4 21 8 20.5 14Z"/>'
            '<path d="M20.3 25 C12 24 7 18 7 13 C14 13 19 18 20.3 25Z"/><path d="M20.3 25 C28 23 33 18 33 13 C26 13 21 18 20.3 25Z"/>',
    'gift': '<rect x="7" y="16" width="26" height="18" rx="2"/><rect x="5" y="11" width="30" height="7" rx="2"/>'
            '<rect x="18" y="11" width="4" height="23" fill="#8FAFD0"/><path d="M20 11 C15 3 9 6 12 10 C14 12 18 11 20 11Z M20 11 C25 3 31 6 28 10 C26 12 22 11 20 11Z"/>',
    'crown': '<path d="M6 30 L8 13 L15 21 L20 8 L25 21 L32 13 L34 30 Z"/><rect x="6" y="31" width="28" height="4" rx="1.5"/>'
             '<circle cx="8" cy="12" r="2.4"/><circle cx="20" cy="7" r="2.4"/><circle cx="32" cy="12" r="2.4"/>',
}

def sticker(kind, color, pos):
    return f'<div class="stk" style="background:{color};{pos}"><svg viewBox="0 0 40 40" width="32" height="32" fill="#fff">{ICON[kind]}</svg></div>'

def rosette(txt, size=132, fill='#F4E2A8', rot=-6, fs=20, n=18):
    pts = []
    for k in range(360):
        a = math.radians(k)
        r = 46 + 3.2 * math.cos(n * a)
        pts.append(f'{50 + r * math.cos(a):.2f},{50 + r * math.sin(a):.2f}')
    return (f'<div class="ros" style="width:{size}px;height:{size}px"><svg viewBox="0 0 100 100" width="{size}" height="{size}">'
            f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#3A332D" stroke-width="1.1"/>'
            f'<circle cx="50" cy="50" r="38" fill="none" stroke="#3A332D" stroke-width=".6" stroke-dasharray="1.6 2.2"/></svg>'
            f'<div class="rt" style="transform:rotate({rot}deg);font-size:{fs}px">{txt}</div></div>')

CSS = '''
@font-face{font-family:Cream;src:url("fonts_cream.otf")}
:root{--paper:#FAF6EE;--ink:#3A332D;--text:#5A5048;--wine:#9A3E4E;--sage:#6F8C72;--deep:#33463B;--gold:#F1D48C;--butter:#F4E2A8;--line:#DCD2C2}
*{box-sizing:border-box;margin:0;padding:0}
body{width:432px;font-family:Cream,serif;color:var(--ink);-webkit-font-smoothing:antialiased;background:var(--paper)}
b,strong,h2,h3{font-weight:normal}
section{position:relative;overflow:hidden;background-color:var(--paper);background-image:linear-gradient(rgba(111,140,114,.075) 1px,transparent 1px),linear-gradient(90deg,rgba(111,140,114,.075) 1px,transparent 1px);background-size:24px 24px;background-position:-1px -1px;padding:36px 22px 40px}
.en{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-weight:500;letter-spacing:.2em}
mark{color:inherit;background:linear-gradient(transparent 60%,rgba(214,140,150,.34) 60%);padding:0 1px}
.eb{font-size:15px;color:var(--wine);letter-spacing:.14em;text-align:center}
h2{font-size:28px;line-height:1.42;text-align:center;margin-top:8px;letter-spacing:.05em}
h2 .u{background:linear-gradient(transparent 62%,rgba(214,140,150,.34) 62%)}
.lead{font-size:14.5px;line-height:1.8;text-align:center;margin-top:12px;color:var(--text);letter-spacing:.04em}
.ros{position:relative;margin:0 auto}.ros svg{position:absolute;inset:0}
.rt{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;line-height:1.25;text-align:center;color:var(--ink);letter-spacing:.04em}
/* 標本卡 panel */
.pn{position:relative;background:#FFFDF8;border:1px solid var(--line);padding:8px;box-shadow:0 8px 20px rgba(60,50,40,.13)}
.tp{position:absolute;width:76px;height:22px;background:rgba(232,221,198,.86);z-index:5;clip-path:polygon(3% 0,97% 4%,100% 50%,96% 100%,2% 96%,0 50%)}
.tp.l{left:-20px;top:6px;transform:rotate(-38deg)}.tp.r{right:-20px;top:6px;transform:rotate(38deg)}
.pic{position:relative;background-size:cover;background-position:center;overflow:hidden}
.tag{position:absolute;left:-10px;top:-18px;z-index:6;background:#FFFDF6;border:1.3px solid var(--ink);border-radius:3px 12px 12px 3px;padding:4px 15px 6px 27px;font-size:22px;transform:rotate(-3deg);box-shadow:2px 3px 0 rgba(58,51,45,.12);letter-spacing:.06em}
.tag:before{content:"";position:absolute;left:9px;top:50%;width:9px;height:9px;margin-top:-4.5px;border:1.3px solid var(--ink);border-radius:50%;background:var(--paper)}
.tag small{font-size:10.5px;color:var(--wine);margin-right:7px;vertical-align:4px;letter-spacing:.14em}
.say{position:absolute;background:#FFFDF8;border:1.3px solid var(--ink);border-radius:18px;padding:9px 15px 10px;font-size:18px;line-height:1.45;z-index:4;white-space:nowrap;letter-spacing:.03em;box-shadow:0 3px 10px rgba(40,30,20,.12)}
.say:after{content:"";position:absolute;width:15px;height:15px;background:#FFFDF8;border-right:1.3px solid var(--ink);border-bottom:1.3px solid var(--ink)}
.say.dn:after{bottom:-8.5px;transform:rotate(45deg)}
.say.up:after{top:-8.5px;transform:rotate(-135deg)}
.card{position:absolute;width:132px;z-index:3}
.card img{display:block;width:100%;border:4px solid #fff;box-shadow:0 6px 16px rgba(0,0,0,.26)}
.card i{position:absolute;width:58px;height:17px;top:-9px;left:37px;transform:rotate(-5deg);opacity:.78}
.stk{position:absolute;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:4;box-shadow:0 0 0 3px #fff,0 4px 10px rgba(0,0,0,.2)}
.nar{background:var(--deep);color:#FBF6EC;padding:12px 16px 13px;font-size:15px;line-height:1.6;letter-spacing:.04em}
.nar mark{background:none;color:var(--gold);padding:0}
/* s03 */
#s03 .ros{margin-top:16px}
#s03 .pn{margin-top:38px}
#s03 .pic{height:438px}
/* s03b */
#s03b{padding:8px 22px 34px}
.xm{position:relative;overflow:hidden;background:#B5423A;border-radius:3px;box-shadow:0 8px 20px rgba(80,30,20,.2);padding:20px 12px 22px;text-align:center;color:#fff;outline:2px solid #E2BE6E;outline-offset:-9px}
.xm .sm{font-size:10px;letter-spacing:.32em;color:#F3D99B}
.xm .big{font-size:34px;letter-spacing:.14em;margin-top:5px;background:linear-gradient(180deg,#FFF6DA 10%,#F1CF7E 55%,#D9A94A 90%);-webkit-background-clip:text;color:transparent}
.xm .sh{position:absolute;top:-30%;bottom:-30%;width:90px;left:-40%;transform:skewX(-22deg);background:linear-gradient(90deg,transparent,rgba(255,236,180,.6),transparent);animation:sweep 2.5s linear infinite}
.xm .sp{position:absolute;width:14px;height:14px;margin:-7px;opacity:0;background:radial-gradient(circle,#FFF4C8 0 18%,transparent 20%),linear-gradient(0deg,transparent 45%,#FFE7A0 45% 55%,transparent 55%),linear-gradient(90deg,transparent 45%,#FFE7A0 45% 55%,transparent 55%);animation:tw 2.5s linear infinite}
@keyframes sweep{0%{left:-40%}55%{left:120%}100%{left:120%}}
@keyframes tw{0%,100%{opacity:0;transform:scale(.4)}12%{opacity:1;transform:scale(1.15) rotate(20deg)}26%{opacity:0;transform:scale(.4)}}
/* s04 */
#s04{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:8px 22px 40px}
#s04>div{background:#FFFDF8;border:1px solid var(--line);box-shadow:0 5px 14px rgba(60,50,40,.1);text-align:center;padding:15px 4px 13px}
#s04>div:nth-child(2){background:#F7EDD2;transform:rotate(1.2deg)}
#s04>div:nth-child(1){transform:rotate(-1.2deg)}
#s04 .n{font-size:40px;line-height:1;color:var(--wine)}
#s04 .n small{font-size:20px;margin-left:2px}
#s04 .c{font-size:13.5px;margin-top:8px;line-height:1.45;color:var(--text)}
/* s05 wall */
#s05 .pn{margin-top:26px;padding:0;border:none;background:var(--deep);height:500px;overflow:hidden}
.wall img{position:absolute;width:74px;box-shadow:0 3px 8px rgba(0,0,0,.4);border:2px solid #fff}
#s05 .ros{position:absolute;right:-14px;top:-30px;margin:0;z-index:6}
/* how */
.how .hd{text-align:center}
.how .no{display:inline-block;background:#FFFDF8;border:1.2px solid var(--wine);color:var(--wine);border-radius:20px;padding:5px 14px 5px 17px;font-size:11px}
.how h3{font-size:26px;line-height:1.42;margin-top:14px;letter-spacing:.05em}
.how p.d{font-size:14.5px;line-height:1.8;color:var(--text);margin-top:10px;letter-spacing:.04em}
.how .pn{margin-top:24px}
.how .ph{height:462px;background-size:cover;background-position:center}
.how .bar{display:flex;align-items:center;gap:10px;background:var(--deep);color:#fff;padding:11px 14px}
.how .bar .st{color:var(--gold);font-size:11.5px}
.how .bar .cn{font-size:16px;flex:1;letter-spacing:.06em}
.how .bar .ee{font-size:10px;color:#BFC9C0}
.how .sfx{position:absolute;z-index:6}
/* s06 */
#s06 .pn{margin-top:24px;padding:0}
#s06 .cap{background:#F7EDD2;border-bottom:1px solid var(--line);height:64px;padding-top:9px;font-size:16px;line-height:1.55;text-align:center;letter-spacing:.06em}
#s06 .cap small{font-size:10.5px;color:var(--wine);letter-spacing:.16em;margin-right:8px}
#s06 .cap i{font-style:normal;font-size:12.5px;color:var(--wine)}
#s06 .pg{position:relative;height:290px}
#s06 .pim{position:absolute;left:105px;top:22px;width:176px;height:246px;background-size:cover;background-position:center;box-shadow:0 5px 14px rgba(30,27,25,.18);outline:1px solid #E3DACB}
#s06 .lb{position:absolute;display:flex;align-items:center;gap:5px;font-size:12.5px;line-height:1.2;letter-spacing:.02em;white-space:nowrap}
#s06 .lb b{flex:none;width:19px;height:19px;border-radius:50%;background:var(--wine);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-family:"Helvetica Neue",Arial,sans-serif;font-weight:500}
#s06 .lb.l{right:292px;flex-direction:row-reverse}
#s06 .lb.r{left:292px}
#s06 .ln{position:absolute;border-top:1.2px dashed var(--ink);height:0;opacity:.7}
/* s09 index plate */
#s09 .pn{margin-top:24px;padding:28px 16px 14px;transform:rotate(-.5deg)}
#s09 .tt{display:flex;justify-content:space-between;align-items:baseline;border-bottom:3px double var(--ink);padding-bottom:9px}
#s09 .tt .a{font-size:21px;letter-spacing:.06em}#s09 .tt .b{font-size:10px;color:var(--wine)}
#s09 .row{display:grid;grid-template-columns:44px repeat(3,1fr);align-items:start;padding:12px 0 10px;border-bottom:1px dashed #D3C8B7}
#s09 .row:last-child{border-bottom:none}
#s09 .se{text-align:center;padding-top:20px}
#s09 .se b{display:block;font-size:26px;line-height:1;color:var(--sage)}
#s09 .se small{display:block;font-size:7.5px;margin-top:6px;color:var(--text);letter-spacing:.14em}
#s09 .fl{text-align:center}
#s09 .fl img{width:84px;height:84px;border-radius:50%;display:block;margin:0 auto;box-shadow:0 0 0 1px #E0D6C6,0 3px 8px rgba(60,50,40,.12)}
#s09 .fl .nm{font-size:13px;margin-top:7px;letter-spacing:.02em;white-space:nowrap}
#s09 .fl .dt{font-size:9px;color:var(--wine);margin-top:3px;letter-spacing:.14em}
#s09 .ft{display:flex;align-items:center;height:78px;border-top:3px double var(--ink);font-size:14px;color:var(--text);letter-spacing:.05em;padding-left:4px}
#s09 .seal{position:absolute;right:-12px;bottom:-14px;width:104px;height:104px;border-radius:50%;border:2px solid var(--wine);color:var(--wine);display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-12deg);background:rgba(250,246,238,.92);z-index:5}
#s09 .seal:before{content:"";position:absolute;inset:5px;border-radius:50%;border:1px solid var(--wine)}
#s09 .seal .s1{font-size:8px;letter-spacing:.18em}
#s09 .seal .s2{font-size:21px;letter-spacing:.08em;margin:3px 0 2px}
#s09 .seal .s3{font-size:11px;letter-spacing:.24em}
/* s10 */
#s10 .pn{margin-top:24px}
#s10 .pic{height:260px}
#s10 .chips{display:grid;grid-template-columns:repeat(5,1fr);margin-top:8px;border-top:1px solid var(--line)}
#s10 .chips div{text-align:center;padding:11px 0 4px;font-size:13.5px;letter-spacing:.02em;border-left:1px dashed var(--line)}
#s10 .chips div:first-child{border-left:none}
#s10 .chips i{display:block;width:34px;height:13px;margin:0 auto 7px;border-radius:3px;box-shadow:inset 0 0 0 1px rgba(58,51,45,.25)}
/* s11 */
#s11 .pn{margin-top:24px;transform:rotate(.5deg)}
#s11 .pic{height:300px}
#s11 table{width:100%;border-collapse:collapse;margin-top:4px}
#s11 td{padding:11px 8px;border-top:1px dashed #D3C8B7;font-size:14px;line-height:1.55;letter-spacing:.03em;vertical-align:top}
#s11 td:first-child{width:62px;color:var(--wine)}
#s11 tr:first-child td{border-top:none}
/* s12 */
#s12 .pn{transform:rotate(-.6deg)}
#s12 .pic{height:457px}
#s12 .say{left:14px;top:16px;font-size:20px}
#s12 .end{position:absolute;right:14px;bottom:16px;z-index:4;background:#F7EDD2;border:1.2px solid var(--ink);padding:6px 14px 8px;font-size:17px;transform:rotate(3deg);text-align:center;letter-spacing:.06em}
#s12 .end .en{font-size:9.5px;letter-spacing:.22em;display:block;color:var(--wine);margin-bottom:2px}
'''

def s03():
    h = '''<section id="s03"><div class="eb">誰適合鮮花圖鑑日曆？</div>
<h2>聖誕禮物 x 交換禮物<br><span class="u">送一整年都不會謝的花</span></h2>''' + rosette('每天<br>收到一朵花')
    for x, l in zip(P, L):
        h += f'''<div class="pn" style="transform:rotate({l['rot']}deg)"><i class="tp r"></i>
<div class="tag"><small class="en">NO.{x['n']}</small>{x['who']}</div>
<div class="pic" style="background-image:url(img/{x['img']}.jpg)">
<div class="say {'dn' if 'top' in l['say'] else 'up'}" style="{l['say']}" data-t="{l['tail']}">{x['h']}</div>
<div class="card" style="{l['card']}"><i style="background:{l['tape']}"></i><img src="img/{x['pg']}.jpg"></div>
{sticker(*l['stk'])}</div>
<div class="nar">{x['s']}</div></div>'''
    return h + '</section>'

def s03b():
    sp = ''.join(f'<i class="sp" style="left:{x}%;top:{y}%;animation-delay:{d}s"></i>' for x, y, d in
                 [(8, 18, 0), (90, 22, .5), (93, 74, 1.0), (6, 78, 1.5), (50, 8, 2.0)])
    return f'<section id="s03b"><div class="xm"><div class="sh"></div>{sp}<div class="en sm">CHRISTMAS DELIVERY</div><div class="big">聖誕節前到貨</div></div></section>'

def s04():
    return '''<section id="s04"><div><div class="n">365</div><div class="c">朵手繪花卉</div></div>
<div><div class="n">365</div><div class="c">則花語與語錄</div></div>
<div><div class="n">5<small>款</small></div><div class="c">花色底座</div></div></section>'''

def s05():
    random.seed(7)
    imgs = ''; k = 1
    for r in range(6):
        for c in range(5):
            if k > 44: break
            x = c * 80 - 14 + (r % 2) * 30 + random.uniform(-5, 5)
            y = r * 88 - 26 + random.uniform(-6, 6)
            imgs += f'<img src="img/wall/{k:03d}.jpg" style="left:{x:.0f}px;top:{y:.0f}px;transform:rotate({random.uniform(-8,8):.1f}deg)">'
            k += 1
    return f'''<section id="s05"><div class="eb">從臘梅到羅莎公主</div>
<h2>365 天，<br><span class="u">天天都有一朵花</span></h2>
<div class="lead">每一頁都是不同的花，<br>翻開就是一整年的花園。</div>
<div style="position:relative"><div class="pn"><div class="wall">{imgs}</div></div>{rosette('365 朵<br>不重複', 104, '#F4E2A8', 8, 17)}</div></section>'''

def how(n, sid, h, d, clip, cn, ee, sfx, sfx_pos):
    return f'''<section id="{sid}" class="how"><div class="hd"><span class="no en">HOW TO USE {n:02d}</span>
<h3>{h}</h3><p class="d">{d}</p></div>
<div class="pn"><i class="tp l"></i><i class="tp r"></i><div class="ph" data-clip="{clip}" style="background-image:url(gif/clips/{clip}/001.jpg)"></div>
<div class="sfx" style="{sfx_pos}">{sfx}</div>
<div class="bar"><span class="st en">STEP {n:02d}</span><span class="cn">{cn}</span><span class="ee en">{ee}</span></div></div></section>'''

def s06():
    caps = json.load(open(f'{D}/gif/caps_f_days.json'))
    # 標籤 y 位置對應印刷檔版面（頁面 176×246，上緣 22）
    T = 22
    lab = [('l', 1, '日期・星期', T + 40), ('l', 2, '農曆・節日', T + 80), ('l', 3, '花名・學名', T + 124),
           ('r', 4, '手繪水彩花', T + 118), ('r', 5, '花語', T + 187), ('r', 6, '暖心語錄', T + 214)]
    h = ''
    for side, k, t, y in lab:
        h += f'<span class="lb {side}" style="top:{y-10}px"><b>{k}</b>{t}</span>'
        if side == 'l': h += f'<i class="ln" style="left:96px;width:24px;top:{y}px"></i>'
        else: h += f'<i class="ln" style="left:266px;width:22px;top:{y}px"></i>'
    return f'''<section id="s06"><div class="eb">一頁有什麼？</div>
<h2>一天一朵花，<br><span class="u">一頁一段溫柔</span></h2>
<div class="pn"><div class="cap" data-caps="f_days">{caps[0]}</div>
<div class="pg"><div class="pim" data-clip="f_days" style="background-image:url(gif/clips/f_days/001.jpg)"></div>{h}</div></div></section>'''

def s09():
    rows = [('春', 'SPRING', [(37, '吉野櫻', 'FEB. 6'), (80, '單瓣鬱金香', 'MAR. 21'), (95, '香豌豆', 'APR. 5')]),
            ('夏', 'SUMMER', [(157, '無盡夏繡球', 'JUN. 6'), (163, '香水百合', 'JUN. 12'), (188, '巧克力向日葵', 'JUL. 7')]),
            ('秋', 'AUTUMN', [(252, '中秋桂', 'SEP. 9'), (266, '奏鳴曲波斯菊', 'SEP. 23'), (300, '單瓣木芙蓉', 'OCT. 27')]),
            ('冬', 'WINTER', [(1, '臘梅', 'JAN. 1'), (346, '高加索雪花蓮', 'DEC. 12'), (356, '蟹爪蘭', 'DEC. 22')])]
    body = ''
    for se, en, fl in rows:
        body += f'<div class="row"><div class="se"><b>{se}</b><small class="en">{en}</small></div>'
        body += ''.join(f'<div class="fl"><img src="img/ix/{d:03d}.png"><div class="nm">{nm}</div><div class="dt en">{dt}</div></div>' for d, nm, dt in fl)
        body += '</div>'
    return f'''<section id="s09" style="padding-bottom:44px"><div class="eb">鮮花圖鑑・四季索引</div>
<h2>春夏秋冬的花，<br><span class="u">一本全部收齊</span></h2>
<div class="pn"><i class="tp l"></i><i class="tp r"></i><div class="tt"><span class="a">鮮花圖鑑日曆 2027</span><span class="b en">FLORA INDEX</span></div>
{body}<div class="ft">還有 353 朵，等你每天翻開</div><div class="seal"><span class="s1 en">LAST EDITION</span><span class="s2">最後一年</span><span class="s3 en">2027</span></div></div></section>'''

def s10():
    chips = ''.join(f'<div><i style="background:{c}"></i>{n}</div>' for n, c in BASE)
    return f'''<section id="s10"><div class="eb">底座款式</div>
<h2>五款花色，<br><span class="u">挑一抹喜歡的顏色</span></h2>
<div class="pn"><i class="tp l"></i><i class="tp r"></i><div class="pic" style="background-image:url(img/s10.jpg)"></div>
<div class="chips">{chips}</div></div></section>'''

def s11():
    rows = [('尺寸', '10 × 14 公分，直式手撕'), ('內容', '365 頁，正面花卉與花語，<br>背面花期、產地與花卉簡史'),
            ('底座', '五款花色底座，立在桌上剛剛好'), ('外盒', '附厚磅外盒，撕下的花卡可以收進去'), ('重量', '623 g（含外盒 850 g）')]
    tr = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in rows)
    return f'''<section id="s11"><div class="eb">規格</div>
<h2>一本小小的花園，<br><span class="u">桌上剛剛好</span></h2>
<div class="pn"><i class="tp l"></i><i class="tp r"></i><div class="pic" style="background-image:url(img/s11.jpg)"></div><table>{tr}</table></div></section>'''

def s12():
    return '''<section id="s12" style="padding-bottom:48px"><div class="pn"><i class="tp l"></i><i class="tp r"></i><div class="pic" style="background-image:url(img/s12.jpg)">
<div class="say dn" data-t="left:34px">瓶裡的花總會謝，<br>紙上的花，陪你一整年</div>
<div class="end"><span class="en">SEE YOU TOMORROW</span>明天，還有一朵花</div></div></div></section>'''

def build():
    body = (s03() + s03b() + s04() + s05()
        + how(1, 's05a', '早上撕一頁，<br>收下今天的那朵花', '撕下今天這頁，一朵手繪花配一句花語，<br>一天就從溫柔開始。', 'f_tear', '撕下今天', 'TEAR', rosette('嘶～', 88, '#FFFDF8', -8, 20), 'right:-14px;top:-30px')
        + s06()
        + how(2, 's06a', '翻到背面，<br>讀一朵花的故事', '花期、產地、花卉簡史都寫在背面，<br>每天認識一種花。', 'f_back', '翻到背面', 'FLIP', rosette('翻面', 88, '#F4E2A8', 6, 20), 'left:-14px;top:-30px')
        + how(3, 's07', '撕下來的每一頁，<br>都是一張花卡', '夾進書裡、寫給朋友，<br>或收進外盒，留住這一年的花。', 'f_collect', '收藏花卡', 'COLLECT', rosette('收好', 88, '#FFFDF8', -6, 20), 'right:-14px;top:-30px')
        + how(4, 's08', '放在床頭，<br>醒來第一眼就是花', '365 天不重複，<br>每天都期待明天會是哪一朵。', 'f_bed', '翻開今天', 'BLOOM', rosette('早安', 88, '#F4E2A8', 6, 20), 'left:-14px;top:-30px')
        + s09() + s10() + s11() + s12())
    js = '''<script>document.querySelectorAll('.say[data-t]').forEach((e,i)=>{const c='t'+i;e.classList.add(c);const s=document.createElement('style');s.textContent=`.${c}:after{${e.dataset.t}}`;document.head.appendChild(s)})</script>'''
    html = f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=432"><title>鮮花圖鑑日曆落地頁 {V}</title><style>{CSS}</style></head><body>{body}{js}</body></html>'
    open(f'{D}/page.html', 'w').write(html)
    print('ok')

if __name__ == '__main__':
    build()
