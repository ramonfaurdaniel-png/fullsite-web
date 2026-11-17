"""Fullsite brand film with voice-over (Marble-style: cinematic real footage, UI cards composited on real shots,
logo reveal on the music lift, human payoff, logo over a storefront).

usage: python3 build_film.py <es|en> <clips_dir> <audio_dir>
audio_dir: music.mp3, vo_<lang>1.mp3, city/chop/wok/rain.mp3
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LANG, CLIPS, AUD = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(CLIPS, 'film_' + LANG); os.makedirs(TMP, exist_ok=True)
BASE = os.path.join(CLIPS, 'film_base'); os.makedirs(BASE, exist_ok=True)
OUT = os.path.join(HERE, f'fullsite-film-{LANG}.mp4')
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
        # (start, end) of each phrase inside vo_es1.mp3 and where it lands in the film
        'vo': [((0.0, 2.86), 8.3), ((3.23, 4.57), 12.4), ((5.01, 6.93), 15.0), ((7.24, 9.14), 18.0),
               ((9.56, 12.48), 21.2), ((12.86, 17.74), 24.3), ((18.23, 20.54), 28.6), ((20.88, 21.46), 31.2),
               ((21.80, 24.60), 36.3), ((24.82, 26.90), 39.7), ((27.14, 28.92), 42.8), ((29.13, 30.80), 46.0),
               ((31.16, 34.08), 50.6)],
    },
    'en': {
        'loss1': ('Waste · avocado', '−$4,380', RED), 'loss2': ('Voids', '−$1,920', RED),
        'sales': ('Sales today', '$84,320', G), 'sales_d': '▲ 12% vs. last Saturday',
        'nf': ('Fullsite AI', 'now', 'Voids +38% at the Valle location.'),
        'feat': ['Connect', 'POS', 'AI Intelligence', 'Inventory', 'Kitchen', 'Invoicing'],
        'tag': 'for the people who live their restaurant',
        'vo': [((0.0, 3.01), 8.3), ((3.59, 4.74), 12.4), ((5.36, 7.17), 15.0), ((7.63, 9.17), 18.0),
               ((9.70, 11.61), 21.4), ((12.14, 17.01), 24.3), ((17.51, 19.48), 28.8), ((19.97, 20.80), 31.1),
               ((21.20, 23.51), 36.3), ((23.87, 25.49), 39.8), ((25.90, 27.80), 42.8), ((28.20, 29.31), 46.2),
               ((29.73, 32.76), 50.6)],
    },
}[LANG]

# (src, src_start, dur, overlays[(png, t_in)])
SHOTS = [
    ('9338.mp4', 4.0, 2.0, []),        # cold open: wok fire
    ('9409.mp4', 12.0, 2.0, []),       # knife
    ('4678.mp4', 6.0, 2.0, []),        # grill
    ('4043.mp4', 8.0, 2.0, []),        # packed bar
    ('30468.mp4', 3.0, 4.0, []),       # sunrise            "antes de que salga el sol"
    ('22660.mp4', 1.0, 2.8, []),       # market             "escogiendo lo mejor"
    ('4118.mp4', 10.0, 2.8, []),       # flambé             "conoces tu cocina por el sonido"
    ('205.mp4', 4.0, 3.4, []),         # waiter, coffee     "y a tus clientes por su nombre"
    ('4331.mp4', 2.0, 3.0, []),        # rainy night        "primero en llegar, último en irse"
    ('6165.mp4', 3.0, 4.2, []),        # exhausted owner    "cada noche… ¿cómo nos fue hoy?"
    ('47627.mp4', 2.0, 2.8, [('card_loss1', 0.3), ('card_loss2', 1.0)]),  # receipts + losses
    ('BLACK', 0, 1.0, []),             # "ya no."
    ('REVEAL', 0, 4.0, []),            # music lift: logo + features
    ('4043.mp4', 2.0, 3.5, [('card_sales', 0.6)]),                    # "fullsite ve tu restaurante…"
    ('14669.mp4', 1.0, 3.0, [('card_nf', 0.3)]),                      # "…y te avisa"
    ('45448.mp4', 2.0, 3.0, []),       # toast              "para que dejes de enterarte al cierre"
    ('23046.mp4', 2.0, 4.0, []),       # family dinner      "y vuelvas a casa a tiempo"
    ('2597.mp4', 1.0, 10.0, [('end_wm', 1.0), ('end_tag', 1.8)]),     # storefront + logo
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


# ---- overlay assets
value_card(f'{TMP}/card_loss1.png', *T['loss1'], x=1230, y=150)
value_card(f'{TMP}/card_loss2.png', *T['loss2'], x=1230, y=350)
value_card(f'{TMP}/card_sales.png', *T['sales'], sub=T['sales_d'], x=1240, y=130)
notif_card(f'{TMP}/card_nf.png')
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
        fc += f"[{last}]fade=out:st={dur - 1.2}:d=1.2[fo];"; last = 'fo'
    run(inputs + ['-filter_complex', fc + f"[{last}]format=yuv420p[v]", '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', '60', out])

with open(f'{TMP}/list.txt', 'w') as fh:
    for p in parts:
        fh.write(f"file '{p}'\n")
run(['-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/video.mp4'])
total = t_cursor

# ---- audio: music (ducked under VO) + VO phrases + ambience
vo = f'{AUD}/vo_{LANG}1.mp3'
ins = ['-i', f'{AUD}/music.mp3']; fc = ''; mix = []
for k, ((a, b), at) in enumerate(T['vo']):
    ins += ['-i', vo]
    fc += f"[{k + 1}:a]atrim={a}:{b + 0.08},asetpts=PTS-STARTPTS,volume=1.5,adelay={int(at * 1000)}|{int(at * 1000)}[v{k}];"
    mix.append(f'[v{k}]')
nv = len(T['vo'])
fc += ''.join(mix) + f"amix=inputs={nv}:normalize=0[vo];[vo]asplit[vo1][vo2];"
sfx = [('wok', 0.0, -6), ('chop', 2.0, -6), ('wok', 4.0, -10), ('city', 8.0, -14), ('wok', cuts[6], -12), ('rain', cuts[8], -10)]
for j, (name, at, g) in enumerate(sfx):
    ins += ['-i', f'{AUD}/{name}.mp3']
    fc += f"[{nv + 1 + j}:a]volume={g}dB,adelay={int(at * 1000)}|{int(at * 1000)}[s{j}];"
fc += (f"[0:a]atrim=0:{total},volume=0.9[m];[m][vo1]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[md];"
       f"[md][vo2]{''.join(f'[s{j}]' for j in range(len(sfx)))}amix=inputs={2 + len(sfx)}:normalize=0,"
       f"alimiter=limit=0.95,afade=t=out:st={total - 2.0}:d=2.0[a]")
run(ins + ['-filter_complex', fc, '-map', '[a]', '-t', f'{total}', '-c:a', 'pcm_s16le', f'{TMP}/audio.wav'])
run(['-i', f'{TMP}/video.mp4', '-i', f'{TMP}/audio.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT])
run(['-i', OUT, '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-level', '4.0', '-b:v', '4500k', '-maxrate', '5500k', '-bufsize', '11000k',
     '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT.replace('.mp4', '-ligero.mp4')])
print('ok', OUT, round(total, 2), [round(c, 1) for c in cuts])
