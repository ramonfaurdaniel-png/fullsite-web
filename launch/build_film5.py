"""Fullsite film v5: manifesto. "We record everything and understand nothing. Until now. Fullsite understands your restaurant."
Desaturated 'old way' intro -> black 'Hasta hoy' -> colour reveal on the music lift -> one insight card per question -> close.

usage: python3 build_film5.py <es|en> <clips_dir> <audio_dir>
audio_dir: music.mp3, man_<lang>.mp3 (full voice-over)
env: RERENDER=3,5 re-renders only those shots; AUDIO_ONLY=1 remixes sound on an existing render.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

LANG, CLIPS, AUD = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cards5
TMP = os.path.join(CLIPS, 'film5_' + LANG); os.makedirs(TMP, exist_ok=True)
BASE = os.path.join(CLIPS, 'film_base'); os.makedirs(BASE, exist_ok=True)
OUT = os.path.join(HERE, f'fullsite-film5-{LANG}.mp4')
FM = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
G = (16, 185, 129, 255); W = (255, 255, 255, 255)
AUDIO_ONLY = os.environ.get('AUDIO_ONLY') == '1'; ONLY = os.environ.get('RERENDER')

# phrase starts inside man_<lang>.mp3 (see silencedetect), named by what is said
P = {
    'es': dict(cien=0.0, igual=1.72, instinto=4.24, libretas=5.52, cortes=6.76, registramos=9.18, nada=10.80, nada_end=12.16,
               hoy=12.83, hoy_end=13.53, noreg=14.12, entiende=16.86, entiende_end=17.67,
               martes=18.14, platillo=20.80, proveedor=23.45, cancela=25.50, faltar=26.97, cerrar=29.45,
               numeros=33.43, respuestas=34.89, hacer=36.22, pos=37.86, porque=40.08, perseguir=42.32, dirigir=44.73, dirigir_end=46.21,
               fullsite=46.76, end=49.19, tag='Entiende tu restaurante.'),
    'en': dict(cien=0.18, igual=1.90, instinto=4.50, libretas=5.77, cortes=6.97, registramos=9.16, nada=11.08, nada_end=12.40,
               hoy=13.44, hoy_end=14.33, noreg=15.05, entiende=17.60, entiende_end=18.67,
               martes=19.08, platillo=21.51, proveedor=24.08, cancela=26.15, faltar=27.61, cerrar=30.00,
               numeros=33.32, respuestas=35.20, hacer=36.64, pos=38.25, porque=40.44, perseguir=42.55, dirigir=44.74, dirigir_end=45.71,
               fullsite=46.19, end=48.71, tag='Understands your restaurant.'),
}[LANG]

# the voice is cut into chunks with extra breathing room at the big moments
START = 1.2
CHUNKS = [  # (from, to, extra pause before)
    (0.0, P['nada_end'], 0.0),
    (P['hoy'] - 0.05, P['hoy_end'], 1.1),          # beat of black before "Hasta hoy"
    (P['noreg'] - 0.05, P['entiende_end'], 0.7),
    (P['martes'] - 0.05, P['dirigir_end'], 1.5),   # reveal breathes on the music lift
    (P['fullsite'] - 0.05, P['end'] + 0.15, 1.0),
]
_off = []; acc = START
for i, (a, b, gap) in enumerate(CHUNKS):
    acc += gap
    _off.append((a, b, acc - a))
    acc += (b - a)
VO_END = acc


def f(t):
    """voice-file time -> film time"""
    for a, b, o in _off:
        if t <= b + 0.01:
            return max(t, a) + o
    return t + _off[-1][2]


T_END = VO_END + 4.6
# shots: (start film time, src, src_in, overlays[(png, t_in_rel, fade, t_out_rel)], look)
OLD = 'old'; DIM = 'dim'
S = [
    (0.0, '22660.mp4', 1.0, [], OLD),
    (f(P['igual']), '9338.mp4', 4.0, [], OLD),
    (f(P['instinto']), '4118.mp4', 10.0, [], OLD),
    (f(P['libretas']), '22855.mp4', 3.0, [], OLD),
    (f(P['cortes']), '47627.mp4', 2.0, [], OLD),
    (f(P['registramos']), '20847.mp4', 0.3, [('ty_rec', 0.15, 0.4)], OLD + DIM),
    (f(P['nada']), '6165.mp4', 3.0, [('ty_nada', 0.15, 0.4)], OLD + DIM),
    (f(P['nada_end']) + 0.35, 'BLACK', 0, [('ty_hoy', None, 0.5)], ''),
    (f(P['noreg']) - 0.1, '4043.mp4', 8.0, [('ty_noreg', 0.2, 0.5)], DIM),
    (f(P['entiende']) - 0.1, 'REVEAL', 0, [('rv_tile', 0.0, 0.6), ('ty_ent', 0.35, 0.6)], ''),
    (f(P['martes']) - 0.15, '4331.mp4', 2.0, [('q_martes', 0.3)], ''),
    (f(P['platillo']) - 0.1, '9409.mp4', 3.0, [('q_plat', 0.25)], ''),
    (f(P['proveedor']) - 0.1, '4678.mp4', 9.0, [('q_prov', 0.25)], ''),
    (f(P['cancela']) - 0.1, '24405.mp4', 16.0, [('q_cancel', 0.2)], ''),
    (f(P['faltar']) - 0.1, '22660.mp4', 8.0, [('q_falta', 0.2)], ''),
    (f(P['cerrar']) - 0.1, '205.mp4', 10.0, [('pred', 0.25)], ''),
    (f(P['numeros']) - 0.1, 'BLUR', 0, [('ty_num', 0.1, 0.35, f(P['respuestas']) - f(P['numeros']) - 0.42), ('ty_resp', f(P['respuestas']) - f(P['numeros']) - 0.05, 0.3)], ''),
    (f(P['hacer']) - 0.1, '6161.mp4', 3.0, [('rec', 0.15, 0.3), ('rec_ok', f(P['pos']) - f(P['hacer']) - 0.55, 0.2)], ''),
    (f(P['pos']) - 0.1, '6367.mp4', 3.0, [('pos_sales', 0.2, 0.3)], ''),
    (f(P['porque']) - 0.1, '14669.mp4', 5.0, [('why', 0.2, 0.35)], ''),
    (f(P['perseguir']) - 0.1, '4296.mp4', 1.0, [], ''),
    (f(P['dirigir']) - 0.1, '23046.mp4', 2.0, [], ''),
    (f(P['fullsite']) - 0.6, '2597.mp4', 1.0, [('end_wm', 0.5, 0.8), ('end_tag', 1.3, 0.8)], 'end'),
]

GRADE = ("eq=contrast=1.12:saturation=0.88:gamma=0.92,"
         "colorbalance=rs=-0.04:gs=0.0:bs=0.06:rm=0.02:bm=-0.02:rh=0.06:gh=0.01:bh=-0.06,"
         "vignette=angle=PI/4.2,noise=alls=5:allf=t")
OLDLOOK = "eq=saturation=0.35:contrast=1.08,colorbalance=rm=0.05:gm=0.02:bm=-0.05:rh=0.05:bh=-0.05,"


def run(a):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + a, check=True)


def wordmark(im, width, x0, y, color=W):
    m = Image.open(os.path.join(HERE, 'assets/wordmark.png'))
    h = int(m.height * width / m.width); m = m.resize((width, h), Image.LANCZOS)
    solid = Image.new('RGBA', m.size, color); solid.putalpha(m.split()[3]); im.alpha_composite(solid, (x0, y))
    sq = round(.0454 * width); sx = x0 + round(.9546 * width); sy = y + round(.7783 * h)
    ImageDraw.Draw(im).rectangle([sx, sy, sx + sq - 1, sy + sq - 1], fill=G)
    return h


# ---- overlays
if not AUDIO_ONLY and not ONLY:
    cards = cards5.build(LANG)
    json.dump(cards, open(f'{TMP}/cards.json', 'w'))
    subprocess.run(['node', os.path.join(HERE, 'cards_render.js'), f'{TMP}/cards.json', TMP], check=True)
cv = lambda: Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
im = cv(); h = wordmark(im, 680, (1920 - 680) // 2, 420); im.save(f'{TMP}/end_wm.png')
im = cv(); d = ImageDraw.Draw(im); fnt = ImageFont.truetype(FM, 54)
d.text(((1920 - d.textlength(P['tag'], font=fnt)) / 2, 420 + h + 54), P['tag'], font=fnt, fill=(255, 255, 255, 240)); im.save(f'{TMP}/end_tag.png')
im = cv(); tile = 300; tx, ty = (1920 - tile) // 2, 250
from PIL import ImageFilter
sh = cv(); ImageDraw.Draw(sh).rounded_rectangle([tx, ty + 24, tx + tile, ty + tile + 24], 70, fill=(0, 0, 0, 180))
im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(40)))
ImageDraw.Draw(im).rounded_rectangle([tx, ty, tx + tile, ty + tile], 70, fill=(10, 10, 10, 255), outline=(16, 185, 129, 130), width=3)
wordmark(im, 200, tx + 50, ty + tile // 2 - 24); im.save(f'{TMP}/rv_tile.png')

# ---- shots
parts = []
for i, (t0, src, ss, ovs, look) in enumerate(S):
    t1 = S[i + 1][0] if i + 1 < len(S) else T_END
    dur = round((t1 - t0) * 60) / 60
    out = f'{TMP}/p{i:02d}.mp4'; parts.append(out)
    if AUDIO_ONLY or (ONLY and str(i) not in ONLY.split(',') and os.path.exists(out)):
        continue
    if src == 'BLACK':
        bp = f'{TMP}/black_{dur:.3f}.mp4'
        run(['-f', 'lavfi', '-t', f'{dur}', '-i', 'color=c=black:s=1920x1080:r=60', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', bp])
        pre = '[0:v]null[b];'
    else:
        clip, cs = {'REVEAL': ('4043.mp4', 9.0), 'BLUR': ('4043.mp4', 3.0)}.get(src, (src, ss))
        bp = f"{BASE}/{clip.replace('.mp4', '')}_{cs}_{dur:.4f}.mp4"
        if not os.path.exists(bp):
            run(['-ss', str(cs), '-t', f'{dur + 0.5}', '-i', os.path.join(CLIPS, clip), '-vf',
                 f"fps=60,scale=1920:1080:flags=lanczos,setsar=1,trim=duration={dur},format=yuv420p",
                 '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-an', bp])
        if src in ('REVEAL', 'BLUR'):
            pre = f"[0:v]gblur=sigma=28,eq=brightness=-0.26:saturation=0.7,{GRADE}[b];"
        else:
            pre = f"[0:v]{OLDLOOK if OLD in look else ''}{GRADE}{',eq=brightness=-0.13' if DIM in look else ''}[b];"
    inputs = ['-i', bp]; fc = pre; last = 'b'; k = 1
    for j, ov in enumerate(ovs):
        png, ti = ov[0], ov[1]; fd = ov[2] if len(ov) > 2 else 0.5; to = ov[3] if len(ov) > 3 else None
        if ti is None:                       # BLACK title: land with the word
            ti = f(P['hoy']) - t0 - 0.05
        dy = f"y='18*pow(max(0,1-(t-{ti})/({fd}+0.25)),2)'"
        fade = f"fade=in:st={ti}:d={fd}:alpha=1" + (f",fade=out:st={to}:d=0.25:alpha=1" if to else '')
        mp = f'{TMP}/{png}_m.png'
        if os.path.exists(mp) and Image.open(mp).getbbox():   # frosted glass under real cards only
            inputs += ['-loop', '1', '-t', f'{dur}', '-i', mp]
            mfade = f"fade=in:st={ti}:d={fd}" + (f",fade=out:st={to}:d=0.25" if to else '')
            fc += (f"[{last}]split[a{j}][c{j}];[c{j}]gblur=sigma=30,eq=brightness=-0.03:saturation=1.15[bb{j}];"
                   f"[{k}:v]format=rgba,alphaextract,{mfade}[mk{j}];[bb{j}][mk{j}]alphamerge[bm{j}];[a{j}][bm{j}]overlay={dy}[f{j}];")
            last = f'f{j}'; k += 1
        inputs += ['-loop', '1', '-t', f'{dur}', '-i', f'{TMP}/{png}.png']
        fc += f"[{k}:v]format=rgba,{fade}[t{j}];[{last}][t{j}]overlay={dy}[o{j}];"
        last = f'o{j}'; k += 1
    if look == 'end':
        fc += f"[{last}]eq=brightness=-0.1,fade=out:st={dur - 1.4}:d=1.4[fo];"; last = 'fo'
    if i == 0:
        fc += f"[{last}]fade=in:st=0:d=0.8[fi];"; last = 'fi'
    run(inputs + ['-filter_complex', fc + f"[{last}]format=yuv420p[v]", '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', '60', out])

with open(f'{TMP}/list.txt', 'w') as fh:
    for p in parts:
        fh.write(f"file '{p}'\n")
if not AUDIO_ONLY:
    run(['-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/video.mp4'])
total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{TMP}/video.mp4'],
                             capture_output=True, text=True).stdout)

# ---- music: bar-aligned (8 s bars); start so the big lift (32 s) lands on the reveal, repeat 40-56 as needed, end on 54-60
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{AUD}/music.mp3', '-ac', '2', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
mu = np.frombuffer(raw, np.float32).reshape(-1, 2).copy(); SR = 48000; sec = lambda t: int(t * SR)
reveal = S[9][0]
m0 = 32 - reveal                                  # music offset at film t=0
def xf(x, y, d=0.08):
    n = sec(d); r = np.linspace(0, 1, n)[:, None]
    return np.concatenate([x[:-n], x[-n:] * (1 - r) + y[:n] * r, y[n:]])
body = mu[sec(m0):sec(56)]
while len(body) < sec(total - 6 + 1):
    body = xf(body, mu[sec(40):sec(56)])
body = body[:sec(total - 6 + 1)]
music = xf(body, mu[sec(54):sec(60)], 1.0)[:sec(total)]
env = np.ones(len(music))                          # dip under the black "Hasta hoy" beat, slam back on the reveal
b0, b1 = sec(S[7][0] - 0.3), sec(reveal)
env[b0:b1] = 0.35
env[:sec(1.5)] *= np.linspace(0, 1, sec(1.5))
music *= env[:, None]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', '-', '-c:a', 'pcm_s16le', f'{TMP}/music.wav'],
               input=music.astype(np.float32).tobytes(), check=True)

# ---- voice chunks + mix
vo = f'{AUD}/man_{LANG}.mp3'
ins = ['-i', f'{TMP}/music.wav']; fc = ''; mix = []
for n, (a, b, o) in enumerate(_off, start=1):
    at = a + o; d_ = b - a
    ins += ['-i', vo]
    fc += (f"[{n}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={d_ - 0.05:.3f}:d=0.05,"
           f"volume=1.5,adelay={int(at * 1000)}|{int(at * 1000)}[v{n}];")
    mix.append(f'[v{n}]')
fc += ''.join(mix) + f"amix=inputs={len(mix)}:normalize=0,apad=whole_dur={total}[vo];[vo]asplit[vo1][vo2];"
fc += (f"[0:a]volume=0.95,apad=whole_dur={total}[m];[m][vo1]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=450[md];"
       f"[md][vo2]amix=inputs=2:normalize=0,alimiter=limit=0.95,afade=t=out:st={total - 1.8}:d=1.8[a]")
run(ins + ['-filter_complex', fc, '-map', '[a]', '-t', f'{total}', '-c:a', 'pcm_s16le', f'{TMP}/audio.wav'])
run(['-i', f'{TMP}/video.mp4', '-i', f'{TMP}/audio.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT])
run(['-i', OUT, '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-level', '4.0', '-b:v', '4500k', '-maxrate', '5500k', '-bufsize', '11000k',
     '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT.replace('.mp4', '-ligero.mp4')])
print('ok', OUT, round(total, 2), 'reveal', round(reveal, 2), 'music offset', round(m0, 2), [round(s[0], 1) for s in S])
