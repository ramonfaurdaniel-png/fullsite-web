"""Fullsite brand film v2: story + a clear explainer section (what Fullsite is), voice-over (Marble-style: cinematic real footage, UI cards composited on real shots,
logo reveal on the music lift, human payoff, logo over a storefront).

usage: python3 build_film.py <es|en> <clips_dir> <audio_dir>
audio_dir: music.mp3, vo_<lang>1.mp3, city/chop/wok/rain.mp3
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LANG, CLIPS, AUD = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(CLIPS, 'film2_' + LANG); os.makedirs(TMP, exist_ok=True)
BASE = os.path.join(CLIPS, 'film_base'); os.makedirs(BASE, exist_ok=True)
OUT = os.path.join(HERE, f'fullsite-film2-{LANG}.mp4')
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FM = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
FR = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
G = (16, 185, 129, 255); W = (255, 255, 255, 255); RED = (248, 113, 113, 255)

T = {
    'es': {
        'loss1': ('Merma · aguacate', '−$4,380', RED), 'loss2': ('Cancelaciones', '−$1,920', RED),
        'sales': ('Ventas hoy', '$84,320', G), 'sales_d': '▲ 12% vs. sábado pasado',
        'nf': ('Fullsite IA', 'ahora', 'Cancelaciones +38% en Sucursal Valle.'),
        'feat': ['Connect', 'POS', 'Inteligencia IA', 'Inventario', 'Cocina', 'Facturación'],
        'tag': 'para los que viven su restaurante',
        'ticket': ('Mesa 12 · Luis', [('2× Tacos rib eye', '$380'), ('1× Mezcal', '$160'), ('1× Agua de jamaica', '$55')], 'Total', '$595'),
        'paid': ('Pago', '$595', 'Tarjeta · aprobado ✓'), 'kds': ('Cocina · #0482', 'Mesa 12', 'Nueva comanda · 00:04'),
        'off': ('Sin conexión', '14 órdenes en cola'), 'on': ('Conexión restaurada', '14 órdenes sincronizadas ✓'),
        'chat_q': '¿Cómo vamos hoy?', 'chat_a': 'Ventas $84,320 (+12%). Ticket promedio $412. 3 de 4 sucursales en orden.',
        # middle VO (mid_es.mp3) phrase starts, relative to its first word
        'mid_cuts': [0, 4.5, 8.45, 10.0, 11.65, 15.7, 20.8, 23.8, 26.3, 30.0],
        # (start, end) of each phrase inside vo_es1.mp3 and where it lands in the film
        'vo': [((0.0, 2.86), 8.3), ((3.23, 4.57), 12.4), ((5.01, 6.93), 15.0), ((7.24, 9.14), 18.0),
               ((9.56, 12.48), 21.2), ((12.86, 17.74), 24.3), ((18.23, 20.54), 29.5), ((20.88, 21.46), 32.15),
               ((27.14, 28.92), 'OUT1'), ((29.13, 30.80), 'OUT2'), ((31.16, 34.08), 'OUT3')],
    },
    'en': {
        'loss1': ('Waste · avocado', '−$4,380', RED), 'loss2': ('Voids', '−$1,920', RED),
        'sales': ('Sales today', '$84,320', G), 'sales_d': '▲ 12% vs. last Saturday',
        'nf': ('Fullsite AI', 'now', 'Voids +38% at the Valle location.'),
        'feat': ['Connect', 'POS', 'AI Intelligence', 'Inventory', 'Kitchen', 'Invoicing'],
        'tag': 'for the people who live their restaurant',
        'ticket': ('Table 12 · Luis', [('2× Rib eye tacos', '$380'), ('1× Mezcal', '$160'), ('1× Hibiscus water', '$55')], 'Total', '$595'),
        'paid': ('Payment', '$595', 'Card · approved ✓'), 'kds': ('Kitchen · #0482', 'Table 12', 'New order · 00:04'),
        'off': ('Offline', '14 orders queued'), 'on': ('Back online', '14 orders synced ✓'),
        'chat_q': 'How are we doing today?', 'chat_a': 'Sales $84,320 (+12%). Avg. ticket $412. 3 of 4 locations on track.',
        'mid_cuts': [0, 3.45, 7.9, 9.35, 11.0, 14.6, 18.6, 21.65, 24.1, 28.0],
        'vo': [((0.0, 3.01), 8.3), ((3.59, 4.74), 12.4), ((5.36, 7.17), 15.0), ((7.63, 9.17), 18.0),
               ((9.70, 11.61), 21.4), ((12.14, 17.01), 24.3), ((17.51, 19.48), 29.5), ((19.97, 20.80), 32.15),
               ((25.90, 27.80), 'OUT1'), ((28.20, 29.31), 'OUT2'), ((29.73, 32.76), 'OUT3')],
    },
}[LANG]

# (src, src_start, dur, overlays[(png, t_in)])
MC = T['mid_cuts']; MD = [MC[i + 1] - MC[i] for i in range(len(MC) - 1)]; MD[0] += 0.4
SHOTS = [
    ('9338.mp4', 4.0, 2.0, []), ('9409.mp4', 12.0, 2.0, []), ('4678.mp4', 6.0, 2.0, []), ('4043.mp4', 8.0, 2.0, []),
    ('30468.mp4', 3.0, 4.0, []), ('22660.mp4', 1.0, 2.8, []), ('4118.mp4', 10.0, 2.8, []), ('205.mp4', 4.0, 3.4, []),
    ('4331.mp4', 2.0, 3.0, []), ('6165.mp4', 3.0, 5.3, []),
    ('47627.mp4', 2.0, 2.7, [('card_loss1', 0.3), ('card_loss2', 1.0)]),
    ('BLACK', 0, 1.0, []),
    # ---- what Fullsite is (middle VO starts 0.4 s into the first of these)
    ('24405.mp4', 6.0, MD[0], [('card_ticket', 0.8)]),          # punto de venta con IA
    ('REVEAL', 0, MD[1], []),                                    # en un solo sistema
    ('6367.mp4', 3.0, MD[2], [('card_paid', 0.2)]),              # cobras en segundos
    ('4678.mp4', 2.0, MD[3], [('card_kds', 0.15)]),              # llega a cocina
    ('4043.mp4', 2.0, MD[4], [('card_off', 0.2), ('card_on', MD[4] - 1.6)]),  # sin internet
    ('4296.mp4', 1.0, MD[5], [('card_loss1', 0.6)]),             # la IA vigila cada peso
    ('9409.mp4', 4.0, MD[6], [('card_loss2', 0.2)]),             # mermas, cancelaciones, fugas
    ('14669.mp4', 1.0, MD[7], [('card_nf', 0.2)]),               # te avisa al celular
    ('6161.mp4', 3.0, MD[8], [('card_q', 0.3), ('card_a', 1.4)]),  # pregúntale
    # ---- payoff
    ('23046.mp4', 2.0, 6.0, []),
    ('2597.mp4', 1.0, 10.0, [('end_wm', 1.0), ('end_tag', 1.8)]),
]

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
    im = canvas(); w, h = 1000, 168; x = (1920 - w) // 2
    im = glass(im, [x, y, x + w, y + h], 44, (244, 244, 242, 238)); d = ImageDraw.Draw(im)
    ix, iy = x + 34, y + 38
    d.rounded_rectangle([ix, iy, ix + 92, iy + 92], 22, fill=(10, 10, 10, 255)); fmark(im, ix + 22, iy + 17, 58); d = ImageDraw.Draw(im)
    d.text((ix + 122, y + 34), app, font=ImageFont.truetype(FB, 32), fill=(17, 17, 17, 255))
    fs = ImageFont.truetype(FM, 28); d.text((x + w - 40 - d.textlength(when, font=fs), y + 38), when, font=fs, fill=(130, 130, 130, 255))
    d.text((ix + 122, y + 86), msg, font=ImageFont.truetype(FM, 34), fill=(30, 30, 30, 255))
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
value_card(f'{TMP}/card_sales.png', *T['sales'], sub=T['sales_d'], x=1240, y=130)
notif_card(f'{TMP}/card_nf.png')
tk = T['ticket']; list_card(f'{TMP}/card_ticket.png', tk[0], tk[1], tk[2], tk[3])
value_card(f'{TMP}/card_paid.png', T['paid'][0], T['paid'][1], G, sub=T['paid'][2], x=1240, y=140)
value_card(f'{TMP}/card_kds.png', T['kds'][0], T['kds'][1], W, sub=T['kds'][2], x=1240, y=140)
status_card(f'{TMP}/card_off.png', *T['off'], (245, 158, 11, 255))
status_card(f'{TMP}/card_on.png', *T['on'], G, y=320)
bubble(f'{TMP}/card_q.png', T['chat_q'], True, 150)
bubble(f'{TMP}/card_a.png', T['chat_a'], False, 290)
im = canvas(); wm_w = 640; h = wordmark(im, wm_w, (1920 - wm_w) // 2, 430); im.save(f'{TMP}/end_wm.png')
im = canvas(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FM, 44)
d.text(((1920 - d.textlength(T['tag'], font=f)) / 2, 430 + h + 50), T['tag'], font=f, fill=(255, 255, 255, 235)); im.save(f'{TMP}/end_tag.png')
# reveal: central tile + feature pills (each pill its own layer so they can stagger in)
im = canvas(); tile = 420; tx, ty = (1920 - tile) // 2, (1080 - tile) // 2
sh = canvas(); ImageDraw.Draw(sh).rounded_rectangle([tx, ty + 20, tx + tile, ty + tile + 20], 60, fill=(0, 0, 0, 170))
im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(40)))
ImageDraw.Draw(im).rounded_rectangle([tx, ty, tx + tile, ty + tile], 60, fill=(10, 10, 10, 255), outline=(16, 185, 129, 120), width=3)
wordmark(im, 300, tx + 60, ty + tile // 2 - 34); im.save(f'{TMP}/rv_tile.png')
pill_pos = [(260, 330), (260, 500), (260, 670), (1360, 330), (1360, 500), (1360, 670)]
for i, (name, (px, py)) in enumerate(zip(T['feat'], pill_pos)):
    im = canvas(); im = glass(im, [px, py, px + 300, py + 84], 42); d = ImageDraw.Draw(im)
    d.ellipse([px + 26, py + 34, px + 42, py + 50], fill=G)
    d.text((px + 58, py + 22), name, font=ImageFont.truetype(FM, 32), fill=(240, 240, 240, 255)); im.save(f'{TMP}/rv_pill{i}.png')

# ---- shots
parts = []; t_cursor = 0.0; cuts = []
for i, (src, ss, dur, ovs) in enumerate(SHOTS):
    cuts.append(t_cursor); t_cursor += dur
    out = f'{TMP}/p{i:02d}.mp4'; parts.append(out)
    if src == 'BLACK':
        run(['-f', 'lavfi', '-t', f'{dur}', '-i', 'color=c=black:s=1920x1080:r=60', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out]); continue
    if src == 'REVEAL':
        bg = os.path.join(CLIPS, '4678.mp4')
        inputs = ['-ss', '2', '-t', f'{dur}', '-i', bg, '-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/rv_tile.png']
        fc = (f"[0:v]fps=60,scale=1920:1080,setsar=1,gblur=sigma=26,eq=brightness=-0.22:saturation=0.6,{GRADE}[b];"
              "[1:v]format=rgba,fade=in:st=0:d=0.5:alpha=1[t];[b][t]overlay=y='20*max(0,1-t/0.6)'[o0];")
        last = 'o0'
        for j in range(6):
            inputs += ['-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/rv_pill{j}.png']
            ti = 0.7 + j * 0.18
            fc += f"[{j + 2}:v]format=rgba,fade=in:st={ti}:d=0.4:alpha=1[q{j}];[{last}][q{j}]overlay=x='{-40 if j < 3 else 40}*max(0,1-(t-{ti})/0.6)'[o{j + 1}];"
            last = f'o{j + 1}'
        run(inputs + ['-filter_complex', fc + f"[{last}]format=yuv420p[v]", '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', '60', out])
        continue
    bp = f"{BASE}/{src.replace('.mp4', '')}_{ss}_{dur}.mp4"
    if not os.path.exists(bp):
        run(['-ss', str(ss), '-t', f'{dur + 0.5}', '-i', os.path.join(CLIPS, src), '-vf',
             f"fps=60,scale=1920:1080:flags=lanczos,setsar=1,trim=duration={dur},format=yuv420p",
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-an', bp])
    inputs = ['-i', bp]; fc = f"[0:v]{GRADE}[b];"; last = 'b'
    for j, (png, ti) in enumerate(ovs):
        inputs += ['-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/{png}.png']
        fc += f"[{j + 1}:v]format=rgba,fade=in:st={ti}:d=0.5:alpha=1[t{j}];[{last}][t{j}]overlay=y='16*max(0,1-(t-{ti})/0.7)'[o{j}];"
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
mid_start = cuts[12] + 0.4
mid_len = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{AUD}/mid_{LANG}.mp3'], capture_output=True, text=True).stdout)
place = {'OUT1': cuts[21] + 0.6, 'OUT2': cuts[21] + 3.4, 'OUT3': cuts[22] + 1.0}
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
ins += ['-i', f'{AUD}/mid_{LANG}.mp3']
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
