"""Fullsite brand film v4: story + the current core (home copy: one system, AI watching during the shift), HTML/frosted-glass UI cards, voice-over (Marble-style: cinematic real footage, UI cards composited on real shots,
logo reveal on the music lift, human payoff, logo over a storefront).

usage: python3 build_film.py <es|en> <clips_dir> <audio_dir>
audio_dir: music.mp3, vo_<lang>1.mp3, city/chop/wok/rain.mp3
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LANG, CLIPS, AUD = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(CLIPS, 'film4_' + LANG); os.makedirs(TMP, exist_ok=True)
BASE = os.path.join(CLIPS, 'film_base'); os.makedirs(BASE, exist_ok=True)
OUT = os.path.join(HERE, f'fullsite-film4-{LANG}.mp4')
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FM = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
FR = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
G = (16, 185, 129, 255); W = (255, 255, 255, 255); RED = (248, 113, 113, 255)

T = {
    'es': {
        'tag': 'para los que viven su restaurante',
        # phrase starts inside mid3_es.mp3 (one per shot), last value = end of the file
        'beats': [0, 2.59, 5.46, 7.98, 9.05, 10.09, 11.13, 12.13, 12.85, 13.70, 14.57, 15.56, 22.73, 26.56, 30.16, 33.66, 37.13, 41.64, 43.77, 46.8],
        'mods': [18.58, 19.55, 20.34, 20.91, 21.85],   # punto de venta, cocina, caja, inventario, personal
        'approve': 40.34, 'online': 45.30,
        'vo': [((0.0, 2.86), 8.3), ((3.23, 4.57), 12.4), ((5.01, 6.93), 15.0), ((7.24, 9.14), 18.0),
               ((9.56, 12.48), 21.2), ((12.86, 17.74), 24.3), ((18.23, 20.54), 29.5), ((20.88, 21.46), 32.15),
               ((27.14, 28.92), 'OUT1'), ((29.13, 30.80), 'OUT2'), ((31.16, 34.08), 'OUT3')],
    },
    'en': {
        'tag': 'for the people who live their restaurant',
        'beats': [0, 2.66, 5.02, 7.32, 8.38, 9.38, 10.42, 11.36, 12.12, 13.00, 13.89, 14.93, 21.62, 24.65, 27.63, 30.90, 34.20, 38.44, 40.86, 44.0],
        'mods': [17.53, 18.50, 19.13, 19.75, 20.55],
        'approve': 37.25, 'online': 42.54,
        'vo': [((0.0, 3.01), 8.3), ((3.59, 4.74), 12.4), ((5.36, 7.17), 15.0), ((7.63, 9.17), 18.0),
               ((9.70, 11.61), 21.4), ((12.14, 17.01), 24.3), ((17.51, 19.48), 29.5), ((19.97, 20.80), 32.15),
               ((25.90, 27.80), 'OUT1'), ((28.20, 29.31), 'OUT2'), ((29.73, 32.76), 'OUT3')],
    },
}[LANG]

# (src, src_start, dur, overlays[(png, t_in[, fade])]); every overlay sits on frosted glass (blurred footage under its mask)
BT = T['beats']; MD = [BT[i + 1] - BT[i] for i in range(len(BT) - 1)]; MD[0] += 0.4; MD[-1] += 0.7
q = lambda k: ('chip%d' % k, 0.04, 0.18)
SHOTS = [
    ('9338.mp4', 4.0, 2.0, []), ('9409.mp4', 12.0, 2.0, []), ('4678.mp4', 6.0, 2.0, []), ('4043.mp4', 8.0, 2.0, []),
    ('30468.mp4', 3.0, 4.0, []), ('22660.mp4', 1.0, 2.8, []), ('4118.mp4', 10.0, 2.8, []), ('205.mp4', 4.0, 3.4, []),
    ('4331.mp4', 2.0, 3.0, []), ('6165.mp4', 3.0, 5.3, []),
    ('47627.mp4', 2.0, 2.7, [('loss1', 0.3), ('loss2', 1.0)]),
    ('BLACK', 0, 1.0, []),
    # ---- the core (mid3 VO starts 0.4 s into the first of these)
    ('6367.mp4', 3.0, MD[0], [('pos_sales', 0.6)]),              # tu punto de venta sabe cuánto vendiste
    ('4296.mp4', 1.0, MD[1], [('leaks', 0.3)]),                  # dónde se te va el dinero
    ('20847.mp4', 0.2, MD[2], [('ticket', 0.5)]),                # una venta no es solo un ticket
    ('4118.mp4', 20.0, MD[3], [q(0)]), ('9409.mp4', 3.0, MD[4], [q(1)]), ('22660.mp4', 5.0, MD[5], [q(2)]),
    ('1737.mp4', 5.0, MD[6], [q(3)]), ('4533.mp4', 5.0, MD[7], [q(4)]), ('4533.mp4', 13.0, MD[8], [q(5)]),
    ('24405.mp4', 6.0, MD[9], [q(6)]), ('9338.mp4', 8.0, MD[10], [q(7)]),
    ('SYS', 9.0, MD[11], [('sys_tile', 0.15, 0.6), ('sys_cap', 0.9, 0.6)] + [('mod%d' % k, t - BT[11] - 0.1, 0.3) for k, t in enumerate(T['mods'])]),
    ('4043.mp4', 1.0, MD[12], [('live', 0.4)]),                  # una IA lo vigila durante el turno
    ('24405.mp4', 16.0, MD[13], [('alert', 0.3), ('alert2', 1.7)]),  # detecta fugas, mermas, cancelaciones
    ('14669.mp4', 1.0, MD[14], [('notif', 0.25)]),               # te avisa al celular
    ('205.mp4', 10.0, MD[15], [('pred', 0.3)]),                  # desde las 2 pm, cómo vas a cerrar
    ('6161.mp4', 3.0, MD[16], [('rec', 0.2), ('rec_ok', T['approve'] - BT[16] - 0.05, 0.2)]),  # explica, recomienda, tú apruebas
    ('14669.mp4', 5.0, MD[17], [('ask_q', 0.15), ('ask_a', 0.9)]),  # pregúntale
    ('4678.mp4', 9.0, MD[18], [('off', 0.15), ('on', T['online'] - BT[18] - 0.05)]),  # se cae el internet... tu restaurante no
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


# ---- overlay assets: HTML cards (+ masks) rendered by cards_render.js
import json, cards4
json.dump(cards4.build(LANG), open(f'{TMP}/cards.json', 'w'))
subprocess.run(['node', os.path.join(HERE, 'cards_render.js'), f'{TMP}/cards.json', TMP], check=True)
im = canvas(); wm_w = 640; h = wordmark(im, wm_w, (1920 - wm_w) // 2, 430); im.save(f'{TMP}/end_wm.png')
im = canvas(); d = ImageDraw.Draw(im); f = ImageFont.truetype(FM, 44)
d.text(((1920 - d.textlength(T['tag'], font=f)) / 2, 430 + h + 50), T['tag'], font=f, fill=(255, 255, 255, 235)); im.save(f'{TMP}/end_tag.png')

# ---- shots
parts = []; t_cursor = 0.0; cuts = []
for i, (src, ss, dur, ovs) in enumerate(SHOTS):
    dur = round(dur * 60) / 60
    cuts.append(t_cursor); t_cursor += dur
    out = f'{TMP}/p{i:02d}.mp4'; parts.append(out)
    if src == 'BLACK':
        run(['-f', 'lavfi', '-t', f'{dur}', '-i', 'color=c=black:s=1920x1080:r=60', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out]); continue
    sys_bg = src == 'SYS'
    if sys_bg:
        src = '4043.mp4'
    bp = f"{BASE}/{src.replace('.mp4', '')}_{ss}_{dur:.4f}.mp4"
    if not os.path.exists(bp):
        run(['-ss', str(ss), '-t', f'{dur + 0.5}', '-i', os.path.join(CLIPS, src), '-vf',
             f"fps=60,scale=1920:1080:flags=lanczos,setsar=1,trim=duration={dur},format=yuv420p",
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-an', bp])
    inputs = ['-i', bp]
    fc = (f"[0:v]gblur=sigma=26,eq=brightness=-0.24:saturation=0.6,{GRADE}[b];" if sys_bg else f"[0:v]{GRADE}[b];"); last = 'b'; k = 1
    for j, ov in enumerate(ovs):
        png, ti = ov[0], ov[1]; fd = ov[2] if len(ov) > 2 else 0.5
        dy = f"y='18*pow(max(0,1-(t-{ti})/({fd}+0.25)),2)'"
        if os.path.exists(f'{TMP}/{png}_m.png'):          # frosted glass: blur the footage under the card's shape
            inputs += ['-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/{png}_m.png']
            fc += (f"[{last}]split[a{j}][c{j}];[c{j}]gblur=sigma=30,eq=brightness=-0.03:saturation=1.15[bb{j}];"
                   f"[{k}:v]format=rgba,alphaextract,fade=in:st={ti}:d={fd}[mk{j}];[bb{j}][mk{j}]alphamerge[bm{j}];[a{j}][bm{j}]overlay={dy}[f{j}];")
            last = f'f{j}'; k += 1
        inputs += ['-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/{png}.png']
        fc += f"[{k}:v]format=rgba,fade=in:st={ti}:d={fd}:alpha=1[t{j}];[{last}][t{j}]overlay={dy}[o{j}];"
        last = f'o{j}'; k += 1
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
mid_len = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{AUD}/mid3_{LANG}.mp3'], capture_output=True, text=True).stdout)
place = {'OUT1': cuts[FAM] + 0.6, 'OUT2': cuts[FAM] + 3.4, 'OUT3': cuts[FAM + 1] + 1.0}
vo = f'{AUD}/vo_{LANG}1.mp3'
# music: the score is built on 8 s bars; play 0-56, repeat the full-energy bars 40-56 (seamless, bar-aligned), end on 54-60
import numpy as np
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{AUD}/music.mp3', '-ac', '2', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
mu = np.frombuffer(raw, np.float32).reshape(-1, 2); SR = 48000; sec = lambda t: int(t * SR)
def xf(x, y, d=0.08):
    n = sec(d); r = np.linspace(0, 1, n)[:, None]
    return np.concatenate([x[:-n], x[-n:] * (1 - r) + y[:n] * r, y[n:]])
body = mu[:sec(56)]
while len(body) < sec(total - 6 + 1):
    body = xf(body, mu[sec(40):sec(56)])
body = body[:sec(total - 6 + 1)]
music = xf(body, mu[sec(54):sec(60)], 1.0)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', '-', '-c:a', 'pcm_s16le', f'{TMP}/music_ext.wav'],
               input=music.astype(np.float32).tobytes(), check=True)

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
ins += ['-i', f'{AUD}/mid3_{LANG}.mp3']
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
