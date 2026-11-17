"""Fullsite brand film v2: story + a clear explainer section (what Fullsite is), voice-over (Marble-style: cinematic real footage, UI cards composited on real shots,
logo reveal on the music lift, human payoff, logo over a storefront).

usage: python3 build_film.py <es|en> <clips_dir> <audio_dir>
audio_dir: music.mp3, vo_<lang>1.mp3, city/chop/wok/rain.mp3
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LANG, CLIPS, AUD = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(CLIPS, 'film3_' + LANG); os.makedirs(TMP, exist_ok=True)
BASE = os.path.join(CLIPS, 'film_base'); os.makedirs(BASE, exist_ok=True)
OUT = os.path.join(HERE, f'fullsite-film3-{LANG}.mp4')
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FM = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
FR = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
G = (16, 185, 129, 255); W = (255, 255, 255, 255); RED = (248, 113, 113, 255)

T = {
    'es': {
        'loss1': ('Merma · aguacate', '−$4,380', RED), 'loss2': ('Cancelaciones raras', '−$1,920', RED),
        'chain': ['Venta', 'Platillo', 'Receta', 'Inventario', 'Costo', 'Margen'],
        'chips': [('VENTA', 'Mesa 12 · $595'), ('PLATILLO', 'Crepas suzette · margen 68%'), ('RECETA', '120 g cebolla morada'),
                  ('INGREDIENTE', 'Aguacate +18% este mes'), ('MESERO', 'Luis · 34 mesas hoy'), ('TURNO', 'Cena · 18:00 – 00:00')],
        'agents': ['Anti-fraude', 'Predicción de cierre', 'Merma', 'Ingeniería de menú', 'Staffing', 'Briefing 7 AM'],
        'agents_t': '26 agentes de IA · 24/7',
        'pred': ('Cierre estimado · 14:00', '$74,000', 'rango $71,200 – $76,800 · confianza 87%'),
        'rec': ('Recomendación', ['El pollo subió 18% con tu proveedor.', 'Sube $15 el Pollo al chipotle.', 'Recuperas ~$9,200 al mes.'], '✓  Aprobar', '✓  Aprobado'),
        'nf': ('Fullsite IA', '7:00', 'Buenos días. Ayer vendiste $84,320 (+12%). 2 alertas y 1 recomendación.'),
        'chat_q': '¿Cómo vamos hoy?', 'chat_a': 'Ventas $41,900 (+9%). Ticket promedio $412. Vas para cerrar en ~$74,000.',
        'connect': ('Fullsite Connect', 'Conectado a tu punto de venta actual ✓', 'Instalado en 4 horas · sin cambiar nada'),
        'pos': ('Fullsite POS', ['Cobro', 'Cocina', 'Inventario']),
        'kds': ('Cocina · #0482', 'Mesa 12', 'Nueva comanda · 00:04'),
        'off': ('Sin conexión', '14 órdenes en cola'), 'on': ('Conexión restaurada', '14 órdenes sincronizadas ✓'),
        'tag': 'para los que viven su restaurante',
        # phrase starts inside mid2_es.mp3 (beats), last value = end of the file
        'beats': [0, 2.97, 4.01, 5.13, 6.33, 7.61, 8.70, 9.85, 15.34, 20.82, 24.63, 27.67, 30.95, 33.21, 38.17, 43.46, 46.24],
        'vo': [((0.0, 2.86), 8.3), ((3.23, 4.57), 12.4), ((5.01, 6.93), 15.0), ((7.24, 9.14), 18.0),
               ((9.56, 12.48), 21.2), ((12.86, 17.74), 24.3), ((18.23, 20.54), 29.5), ((20.88, 21.46), 32.15),
               ((27.14, 28.92), 'OUT1'), ((29.13, 30.80), 'OUT2'), ((31.16, 34.08), 'OUT3')],
    },
    'en': {
        'loss1': ('Waste · avocado', '−$4,380', RED), 'loss2': ('Odd voids', '−$1,920', RED),
        'chain': ['Sale', 'Dish', 'Recipe', 'Inventory', 'Cost', 'Margin'],
        'chips': [('SALE', 'Table 12 · $595'), ('DISH', 'Crêpes suzette · 68% margin'), ('RECIPE', '120 g red onion'),
                  ('INGREDIENT', 'Avocado +18% this month'), ('SERVER', 'Luis · 34 tables today'), ('SHIFT', 'Dinner · 6 PM – 12 AM')],
        'agents': ['Anti-fraud', 'Close prediction', 'Waste', 'Menu engineering', 'Staffing', '7 AM briefing'],
        'agents_t': '26 AI agents · 24/7',
        'pred': ('Projected close · 2:00 PM', '$74,000', 'range $71,200 – $76,800 · 87% confidence'),
        'rec': ('Recommendation', ['Chicken went up 18% at your supplier.', 'Raise Chipotle Chicken by $15.', 'You recover ~$9,200 a month.'], '✓  Approve', '✓  Approved'),
        'nf': ('Fullsite AI', '7:00 AM', 'Good morning. Yesterday you sold $84,320 (+12%). 2 alerts, 1 recommendation.'),
        'chat_q': 'How are we doing today?', 'chat_a': 'Sales $41,900 (+9%). Avg. ticket $412. On track to close at ~$74,000.',
        'connect': ('Fullsite Connect', 'Connected to your current POS ✓', 'Live in 4 hours · nothing to replace'),
        'pos': ('Fullsite POS', ['Payments', 'Kitchen', 'Inventory']),
        'kds': ('Kitchen · #0482', 'Table 12', 'New order · 00:04'),
        'off': ('Offline', '14 orders queued'), 'on': ('Back online', '14 orders synced ✓'),
        'tag': 'for the people who live their restaurant',
        'beats': [0, 3.80, 4.82, 5.79, 6.85, 8.08, 9.23, 10.31, 14.38, 18.98, 22.29, 25.40, 28.76, 31.07, 36.57, 42.41, 45.52],
        'vo': [((0.0, 3.01), 8.3), ((3.59, 4.74), 12.4), ((5.36, 7.17), 15.0), ((7.63, 9.17), 18.0),
               ((9.70, 11.61), 21.4), ((12.14, 17.01), 24.3), ((17.51, 19.48), 29.5), ((19.97, 20.80), 32.15),
               ((25.90, 27.80), 'OUT1'), ((28.20, 29.31), 'OUT2'), ((29.73, 32.76), 'OUT3')],
    },
}[LANG]

# (src, src_start, dur, overlays[(png, t_in[, fade])])
BT = T['beats']; MD = [BT[i + 1] - BT[i] for i in range(len(BT) - 1)]; MD[0] += 0.4; MD[-1] += 0.7
CH = [(f'chain{k}', 0.5 + 0.22 * k, 0.35) for k in range(6)]
SHOTS = [
    ('9338.mp4', 4.0, 2.0, []), ('9409.mp4', 12.0, 2.0, []), ('4678.mp4', 6.0, 2.0, []), ('4043.mp4', 8.0, 2.0, []),
    ('30468.mp4', 3.0, 4.0, []), ('22660.mp4', 1.0, 2.8, []), ('4118.mp4', 10.0, 2.8, []), ('205.mp4', 4.0, 3.4, []),
    ('4331.mp4', 2.0, 3.0, []), ('6165.mp4', 3.0, 5.3, []),
    ('47627.mp4', 2.0, 2.7, [('card_loss1', 0.3), ('card_loss2', 1.0)]),
    ('BLACK', 0, 1.0, []),
    # ---- the core (mid2 VO starts 0.4 s into the first of these)
    ('4043.mp4', 1.0, MD[0], CH),                                   # Fullsite ve cada dato
    ('6367.mp4', 3.0, MD[1], [('chip0', 0.05, 0.25)]),             # cada venta
    ('4118.mp4', 20.0, MD[2], [('chip1', 0.05, 0.25)]),            # cada platillo
    ('9409.mp4', 3.0, MD[3], [('chip2', 0.05, 0.25)]),             # cada receta
    ('22660.mp4', 5.0, MD[4], [('chip3', 0.05, 0.25)]),            # cada ingrediente
    ('24405.mp4', 6.0, MD[5], [('chip4', 0.05, 0.25)]),            # cada mesero
    ('4678.mp4', 8.0, MD[6], [('chip5', 0.05, 0.25)]),             # cada turno
    ('AGENTS', 0, MD[7], []),                                       # 26 agentes, 24/7
    ('4296.mp4', 1.0, MD[8], [('card_loss1', 0.4), ('card_loss2', 1.6)]),  # detectan fugas
    ('205.mp4', 10.0, MD[9], [('card_pred', 0.3)]),                # predicen el cierre
    ('6161.mp4', 3.0, MD[10], [('card_rec', 0.2), ('card_ok', MD[10] - 1.3, 0.2)]),  # tú apruebas
    ('14669.mp4', 1.0, MD[11], [('card_nf', 0.3)]),                # briefing 7 AM
    ('14669.mp4', 5.0, MD[12], [('card_q', 0.2), ('card_a', 1.1)]),  # pregúntale
    ('20847.mp4', 0.2, MD[13], [('card_connect', 0.4)]),           # Connect
    ('4043.mp4', 6.0, MD[14] * 0.55, [('card_pos', 0.3)]),         # POS
    ('4678.mp4', 9.0, MD[14] * 0.45, [('card_kds', 0.1)]),
    ('3456.mp4', 0.5, MD[15], [('card_off', 0.1), ('card_on', MD[15] - 1.6)]),  # sin internet
    # ---- payoff
    ('23046.mp4', 2.0, 6.0, []),
    ('2597.mp4', 1.0, 10.0, [('end_wm', 1.0), ('end_tag', 1.8)]),
]
MID0 = 12; FAM = len(SHOTS) - 2

GRADE = ("eq=contrast=1.12:saturation=0.88:gamma=0.92,"
         "colorbalance=rs=-0.04:gs=0.0:bs=0.06:rm=0.02:bm=-0.02:rh=0.06:gh=0.01:bh=-0.06,"
         "vignette=angle=PI/4.2,noise=alls=5:allf=t")


def run(a):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + a, check=True)


def canvas():
    return Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))


def glass(im, box, r=26, fill=(14, 14, 14, 190)):
    x0, y0, x1, y1 = box
    sh = canvas(); ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 14, x1, y1 + 14], r, fill=(0, 0, 0, 140))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, r, fill=fill, outline=(255, 255, 255, 46), width=2)
    return im


def fmark(im, x, y, h, color=(255, 255, 255, 255)):
    m = Image.open(os.path.join(HERE, 'assets/fmark.png')); w = int(m.width * h / m.height)
    m = m.resize((w, h), Image.LANCZOS); solid = Image.new('RGBA', m.size, color); solid.putalpha(m.split()[3])
    im.alpha_composite(solid, (x, y))
    sz = int(.321 * w); ImageDraw.Draw(im).rectangle([x + int(.679 * w), y + int(.7675 * h), x + int(.679 * w) + sz, y + int(.7675 * h) + sz], fill=G)


def wordmark(im, width, x0, y, color=W):
    m = Image.open(os.path.join(HERE, 'assets/wordmark.png'))
    h = int(m.height * width / m.width); m = m.resize((width, h), Image.LANCZOS)
    solid = Image.new('RGBA', m.size, color); solid.putalpha(m.split()[3]); im.alpha_composite(solid, (x0, y))
    sq = round(.0454 * width); sx = x0 + round(.9546 * width); sy = y + round(.7783 * h)
    ImageDraw.Draw(im).rectangle([sx, sy, sx + sq - 1, sy + sq - 1], fill=G)
    return h


def value_card(path, label, value, col, sub=None, x=1240, y=130):
    im = canvas(); w, h = 560, 170 if not sub else 196
    im = glass(im, [x, y, x + w, y + h]); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x + 28, y + 30, x + 76, y + 78], 12, fill=(255, 255, 255, 26))
    fmark(im, x + 41, y + 37, 34); d = ImageDraw.Draw(im)
    d.text((x + 96, y + 36), label, font=ImageFont.truetype(FR, 28), fill=(220, 220, 220, 255))
    d.text((x + 30, y + 92), value, font=ImageFont.truetype(FB, 62), fill=col)
    if sub:
        d.text((x + 30, y + 160), sub, font=ImageFont.truetype(FR, 24), fill=(16, 185, 129, 255))
    im.save(path)


def notif_card(path, y=120):
    app, when, msg = T['nf']
    import textwrap
    lines = textwrap.wrap(msg, 42)
    im = canvas(); w, h = 1060, 130 + 46 * len(lines); x = (1920 - w) // 2
    im = glass(im, [x, y, x + w, y + h], 44, (244, 244, 242, 238)); d = ImageDraw.Draw(im)
    ix, iy = x + 34, y + 38
    d.rounded_rectangle([ix, iy, ix + 92, iy + 92], 22, fill=(10, 10, 10, 255)); fmark(im, ix + 22, iy + 17, 58); d = ImageDraw.Draw(im)
    d.text((ix + 122, y + 34), app, font=ImageFont.truetype(FB, 32), fill=(17, 17, 17, 255))
    fs = ImageFont.truetype(FM, 28); d.text((x + w - 40 - d.textlength(when, font=fs), y + 38), when, font=fs, fill=(130, 130, 130, 255))
    for k, l in enumerate(lines):
        d.text((ix + 122, y + 84 + 46 * k), l, font=ImageFont.truetype(FM, 32), fill=(30, 30, 30, 255))
    im.save(path)


def list_card(path, title, rows, tl, tv, x=1180, y=110):
    im = canvas(); w = 600; h = 120 + 52 * len(rows) + 80
    im = glass(im, [x, y, x + w, y + h]); d = ImageDraw.Draw(im)
    fmark(im, x + 30, y + 28, 36); d = ImageDraw.Draw(im)
    d.text((x + 80, y + 30), title, font=ImageFont.truetype(FB, 30), fill=W)
    fr = ImageFont.truetype(FR, 28); yy = y + 96
    for a, b in rows:
        d.text((x + 32, yy), a, font=fr, fill=(215, 215, 215, 255)); d.text((x + w - 32 - d.textlength(b, font=fr), yy), b, font=fr, fill=(215, 215, 215, 255)); yy += 52
    d.line([x + 32, yy + 6, x + w - 32, yy + 6], fill=(255, 255, 255, 50), width=2)
    fb = ImageFont.truetype(FB, 40); d.text((x + 32, yy + 22), tl, font=fb, fill=W); d.text((x + w - 32 - d.textlength(tv, font=fb), yy + 22), tv, font=fb, fill=G)
    im.save(path)


def status_card(path, title, sub, color, x=1240, y=140):
    im = canvas(); w, h = 560, 150
    im = glass(im, [x, y, x + w, y + h]); d = ImageDraw.Draw(im)
    d.ellipse([x + 32, y + 46, x + 56, y + 70], fill=color)
    d.text((x + 76, y + 32), title, font=ImageFont.truetype(FB, 36), fill=W)
    d.text((x + 76, y + 84), sub, font=ImageFont.truetype(FR, 28), fill=(210, 210, 210, 255))
    im.save(path)


def bubble(path, text, me, y):
    im = canvas(); f = ImageFont.truetype(FM, 34); d = ImageDraw.Draw(im)
    import textwrap
    lines = textwrap.wrap(text, 34); w = max(d.textlength(l, font=f) for l in lines) + 64; h = 48 * len(lines) + 44
    x = 1840 - w if me else 1060
    im = glass(im, [x, y, x + w, y + h], 30, (16, 185, 129, 230) if me else (14, 14, 14, 210)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        d.text((x + 32, y + 22 + 48 * i), l, font=f, fill=W)
    im.save(path)


# ---- overlay assets
value_card(f'{TMP}/card_loss1.png', *T['loss1'], x=1230, y=150)
value_card(f'{TMP}/card_loss2.png', *T['loss2'], x=1230, y=350)
value_card(f'{TMP}/card_pred.png', T['pred'][0], T['pred'][1], G, sub=T['pred'][2], x=1120, y=140)
notif_card(f'{TMP}/card_nf.png')
value_card(f'{TMP}/card_kds.png', T['kds'][0], T['kds'][1], W, sub=T['kds'][2], x=1240, y=140)
status_card(f'{TMP}/card_off.png', *T['off'], (245, 158, 11, 255))
status_card(f'{TMP}/card_on.png', *T['on'], G, y=320)
bubble(f'{TMP}/card_q.png', T['chat_q'], True, 150)
bubble(f'{TMP}/card_a.png', T['chat_a'], False, 290)

# data chain: six pills joined by lines along the bottom, each its own layer
cw, gap = 230, 40; x0 = (1920 - (6 * cw + 5 * gap)) // 2; cy = 860
for k, name in enumerate(T['chain']):
    im = canvas(); px = x0 + k * (cw + gap)
    if k:
        ImageDraw.Draw(im).line([px - gap, cy + 40, px, cy + 40], fill=(16, 185, 129, 220), width=3)
    im = glass(im, [px, cy, px + cw, cy + 80], 40); d = ImageDraw.Draw(im)
    d.ellipse([px + 24, cy + 32, px + 40, cy + 48], fill=G)
    f = ImageFont.truetype(FM, 30); d.text((px + 54, cy + 21), name, font=f, fill=(240, 240, 240, 255))
    im.save(f'{TMP}/chain{k}.png')

# label chips (lower left) for the fast "every ..." cuts
for k, (lab, val) in enumerate(T['chips']):
    im = canvas(); d = ImageDraw.Draw(im); fl = ImageFont.truetype(FB, 26); fv = ImageFont.truetype(FM, 40)
    w = int(max(d.textlength(lab, font=fl) + 60, d.textlength(val, font=fv))) + 70
    x, y = 110, 820
    im = glass(im, [x, y, x + w, y + 150], 28); d = ImageDraw.Draw(im)
    d.ellipse([x + 34, y + 36, x + 50, y + 52], fill=G)
    d.text((x + 64, y + 28), lab, font=fl, fill=(16, 185, 129, 255))
    d.text((x + 34, y + 76), val, font=fv, fill=W)
    im.save(f'{TMP}/chip{k}.png')

# recommendation card + approved button state
def rec_card(path, done):
    title, lines, btn, ok = T['rec']
    im = canvas(); x, y, w = 1080, 130, 720; h = 130 + 50 * len(lines) + 120
    im = glass(im, [x, y, x + w, y + h]); d = ImageDraw.Draw(im)
    fmark(im, x + 32, y + 30, 36); d = ImageDraw.Draw(im)
    d.text((x + 84, y + 32), title, font=ImageFont.truetype(FB, 30), fill=W)
    f = ImageFont.truetype(FR, 30)
    for k, l in enumerate(lines):
        d.text((x + 34, y + 100 + 50 * k), l, font=f, fill=(225, 225, 225, 255) if k < 2 else (16, 185, 129, 255))
    by = y + 100 + 50 * len(lines) + 24; bw = 300
    if done:
        d.rounded_rectangle([x + 34, by, x + 34 + bw, by + 70], 35, fill=G)
        d.text((x + 34 + (bw - d.textlength(ok, font=ImageFont.truetype(FB, 30))) / 2, by + 17), ok, font=ImageFont.truetype(FB, 30), fill=(8, 8, 8, 255))
    else:
        d.rounded_rectangle([x + 34, by, x + 34 + bw, by + 70], 35, outline=G, width=3)
        d.text((x + 34 + (bw - d.textlength(btn, font=ImageFont.truetype(FB, 30))) / 2, by + 17), btn, font=ImageFont.truetype(FB, 30), fill=G)
    im.save(path)
rec_card(f'{TMP}/card_rec.png', False); rec_card(f'{TMP}/card_ok.png', True)

# Connect card
def connect_card(path):
    name, l1, l2 = T['connect']
    im = canvas(); x, y, w, h = 1060, 150, 740, 230
    im = glass(im, [x, y, x + w, y + h]); d = ImageDraw.Draw(im)
    hh = wordmark(im, 230, x + 34, y + 38); d = ImageDraw.Draw(im)
    d.text((x + 34 + 250, y + 34), name.split()[-1], font=ImageFont.truetype(FB, 44), fill=W)
    d.text((x + 34, y + 104), l1, font=ImageFont.truetype(FM, 32), fill=(16, 185, 129, 255))
    d.text((x + 34, y + 156), l2, font=ImageFont.truetype(FR, 28), fill=(215, 215, 215, 255))
    im.save(path)
connect_card(f'{TMP}/card_connect.png')

# POS card with three module pills
def pos_card(path):
    name, mods = T['pos']
    im = canvas(); x, y, w, h = 1080, 150, 720, 230
    im = glass(im, [x, y, x + w, y + h]); d = ImageDraw.Draw(im)
    wordmark(im, 230, x + 34, y + 38); d = ImageDraw.Draw(im)
    d.text((x + 34 + 250, y + 34), 'POS', font=ImageFont.truetype(FB, 44), fill=W)
    px = x + 34; f = ImageFont.truetype(FM, 28)
    for m in mods:
        mw = d.textlength(m, font=f) + 70
        d.rounded_rectangle([px, y + 128, px + mw, y + 188], 30, fill=(255, 255, 255, 22), outline=(255, 255, 255, 60), width=2)
        d.ellipse([px + 22, y + 151, px + 36, y + 165], fill=G); d.text((px + 46, y + 141), m, font=f, fill=W); px += mw + 16
    im.save(path)
pos_card(f'{TMP}/card_pos.png')

im = canvas(); wm_w = 640; h = wordmark(im, wm_w, (1920 - wm_w) // 2, 430); im.save(f'{TMP}/end_wm.png')
im = canvas(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FM, 44)
d.text(((1920 - d.textlength(T['tag'], font=f)) / 2, 430 + h + 50), T['tag'], font=f, fill=(255, 255, 255, 235)); im.save(f'{TMP}/end_tag.png')
# agents reveal: central tile + agent pills + caption
im = canvas(); tile = 400; tx, ty = (1920 - tile) // 2, (1080 - tile) // 2 - 40
sh = canvas(); ImageDraw.Draw(sh).rounded_rectangle([tx, ty + 20, tx + tile, ty + tile + 20], 60, fill=(0, 0, 0, 170))
im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(40)))
ImageDraw.Draw(im).rounded_rectangle([tx, ty, tx + tile, ty + tile], 60, fill=(10, 10, 10, 255), outline=(16, 185, 129, 120), width=3)
wordmark(im, 290, tx + 55, ty + tile // 2 - 34); im.save(f'{TMP}/rv_tile.png')
im = canvas(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FB, 46)
d.text(((1920 - d.textlength(T['agents_t'], font=f)) / 2, ty + tile + 60), T['agents_t'], font=f, fill=W); im.save(f'{TMP}/rv_cap.png')
pill_pos = [(170, 290), (170, 460), (170, 630), (1370, 290), (1370, 460), (1370, 630)]
for i, (name, (px, py)) in enumerate(zip(T['agents'], pill_pos)):
    im = canvas(); f = ImageFont.truetype(FM, 32); pw = int(ImageDraw.Draw(im).textlength(name, font=f)) + 100
    if i >= 3:
        px = 1920 - 170 - pw
    im = glass(im, [px, py, px + pw, py + 84], 42); d = ImageDraw.Draw(im)
    d.ellipse([px + 26, py + 34, px + 42, py + 50], fill=G)
    d.text((px + 58, py + 22), name, font=f, fill=(240, 240, 240, 255)); im.save(f'{TMP}/rv_pill{i}.png')

# ---- shots
parts = []; t_cursor = 0.0; cuts = []
for i, (src, ss, dur, ovs) in enumerate(SHOTS):
    dur = round(dur * 60) / 60
    cuts.append(t_cursor); t_cursor += dur
    out = f'{TMP}/p{i:02d}.mp4'; parts.append(out)
    if src == 'BLACK':
        run(['-f', 'lavfi', '-t', f'{dur}', '-i', 'color=c=black:s=1920x1080:r=60', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out]); continue
    if src == 'AGENTS':
        bg = os.path.join(CLIPS, '4043.mp4')
        inputs = ['-ss', '9', '-t', f'{dur}', '-i', bg, '-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/rv_tile.png']
        fc = (f"[0:v]fps=60,scale=1920:1080,setsar=1,gblur=sigma=26,eq=brightness=-0.22:saturation=0.6,{GRADE}[b];"
              "[1:v]format=rgba,fade=in:st=0:d=0.5:alpha=1[t];[b][t]overlay=y='20*max(0,1-t/0.6)'[o0];")
        last = 'o0'
        for j in range(6):
            inputs += ['-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/rv_pill{j}.png']
            ti = 0.5 + j * 0.16
            fc += f"[{j + 2}:v]format=rgba,fade=in:st={ti}:d=0.4:alpha=1[q{j}];[{last}][q{j}]overlay=x='{-40 if j < 3 else 40}*max(0,1-(t-{ti})/0.6)'[o{j + 1}];"
            last = f'o{j + 1}'
        inputs += ['-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/rv_cap.png']
        fc += f"[8:v]format=rgba,fade=in:st=1.6:d=0.5:alpha=1[cp];[{last}][cp]overlay=y='14*max(0,1-(t-1.6)/0.6)'[o7];"; last = 'o7'
        run(inputs + ['-filter_complex', fc + f"[{last}]format=yuv420p[v]", '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', '60', out])
        continue
    bp = f"{BASE}/{src.replace('.mp4', '')}_{ss}_{dur}.mp4"
    if not os.path.exists(bp):
        run(['-ss', str(ss), '-t', f'{dur + 0.5}', '-i', os.path.join(CLIPS, src), '-vf',
             f"fps=60,scale=1920:1080:flags=lanczos,setsar=1,trim=duration={dur},format=yuv420p",
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-an', bp])
    inputs = ['-i', bp]; fc = f"[0:v]{GRADE}[b];"; last = 'b'
    for j, ov in enumerate(ovs):
        png, ti = ov[0], ov[1]; fd = ov[2] if len(ov) > 2 else 0.5
        inputs += ['-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/{png}.png']
        fc += f"[{j + 1}:v]format=rgba,fade=in:st={ti}:d={fd}:alpha=1[t{j}];[{last}][t{j}]overlay=y='16*max(0,1-(t-{ti})/({fd}+0.2))'[o{j}];"
        last = f'o{j}'
    if i == len(SHOTS) - 1:
        fc += f"[{last}]eq=brightness=-0.08,fade=out:st={dur - 1.2}:d=1.2[fo];"; last = 'fo'
    run(inputs + ['-filter_complex', fc + f"[{last}]format=yuv420p[v]", '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', '60', out])

with open(f'{TMP}/list.txt', 'w') as fh:
    for p in parts:
        fh.write(f"file '{p}'\n")
run(['-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/video.mp4'])
total = t_cursor

# ---- audio
mid_start = cuts[MID0] + 0.4
mid_len = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{AUD}/mid2_{LANG}.mp3'], capture_output=True, text=True).stdout)
place = {'OUT1': cuts[FAM] + 0.6, 'OUT2': cuts[FAM] + 3.4, 'OUT3': cuts[FAM + 1] + 1.0}
vo = f'{AUD}/vo_{LANG}1.mp3'
# music: original 0-56 s, then the energy section (36-56) looped with crossfades, then its ending (56-60)
need = total - 56 - 4
loops = int(need // 19) + 1
mus_in = ['-i', f'{AUD}/music.mp3']; mf = "[0:a]atrim=0:56,asetpts=PTS-STARTPTS[m0];"
for k in range(loops):
    mf += f"[0:a]atrim=36:56,asetpts=PTS-STARTPTS[l{k}];"
mf += "[0:a]atrim=56:60,asetpts=PTS-STARTPTS[me];"
chain = 'm0'
for k in range(loops):
    mf += f"[{chain}][l{k}]acrossfade=d=1:c1=tri:c2=tri[c{k}];"; chain = f'c{k}'
mf += f"[{chain}]atrim=0:{total - 4 + 1},asetpts=PTS-STARTPTS[mb];[mb][me]acrossfade=d=1[mus]"
run(mus_in + ['-filter_complex', mf, '-map', '[mus]', '-c:a', 'pcm_s16le', f'{TMP}/music_ext.wav'])

ins = ['-i', f'{TMP}/music_ext.wav']; fc = ''; mix = []; n = 1
prev_end = 0.0
for (a_, b_), at in T['vo']:
    at = place.get(at, at)
    if at == place['OUT1']:
        prev_end = max(prev_end, mid_start + mid_len)
    at = max(at, prev_end + 0.3)            # never let two phrases overlap
    d_ = b_ + 0.1 - a_; prev_end = at + d_
    ins += ['-i', vo]
    fc += (f"[{n}:a]atrim={a_}:{b_ + 0.1},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={d_ - 0.06:.3f}:d=0.06,"
           f"volume=1.5,adelay={int(at * 1000)}|{int(at * 1000)}[v{n}];")
    print('vo', round(at, 2), '->', round(prev_end, 2))
    mix.append(f'[v{n}]'); n += 1
ins += ['-i', f'{AUD}/mid2_{LANG}.mp3']
fc += f"[{n}:a]volume=1.5,adelay={int(mid_start * 1000)}|{int(mid_start * 1000)}[v{n}];"; mix.append(f'[v{n}]'); n += 1
fc += ''.join(mix) + f"amix=inputs={len(mix)}:normalize=0[vo];[vo]asplit[vo1][vo2];"
sfx = [('wok', 0.0, -6), ('chop', 2.0, -6), ('wok', 4.0, -10), ('city', 8.0, -14), ('wok', cuts[6], -12), ('rain', cuts[8], -10)]
s0 = n
for j, (name, at, g) in enumerate(sfx):
    ins += ['-i', f'{AUD}/{name}.mp3']
    fc += f"[{s0 + j}:a]volume={g}dB,adelay={int(at * 1000)}|{int(at * 1000)}[s{j}];"
fc += (f"[0:a]atrim=0:{total},volume=0.9[m];[m][vo1]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[md];"
       f"[md][vo2]{''.join(f'[s{j}]' for j in range(len(sfx)))}amix=inputs={2 + len(sfx)}:normalize=0,"
       f"alimiter=limit=0.95,afade=t=out:st={total - 2.0}:d=2.0[a]")
run(ins + ['-filter_complex', fc, '-map', '[a]', '-t', f'{total}', '-c:a', 'pcm_s16le', f'{TMP}/audio.wav'])
run(['-i', f'{TMP}/video.mp4', '-i', f'{TMP}/audio.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT])
run(['-i', OUT, '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-level', '4.0', '-b:v', '4500k', '-maxrate', '5500k', '-bufsize', '11000k',
     '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT.replace('.mp4', '-ligero.mp4')])
print('ok', OUT, round(total, 2), [round(c, 1) for c in cuts])
