"""v5 edit: AI-rendered 3D shots (Higgsfield / Kling) cut to an ElevenLabs score.

usage: python3 build_v5.py <es|en> <clips_dir> <audio_dir>
clips_dir holds c0..c9.mp4 (3D shots), owner.mp4 and bartender.mp4.
audio_dir holds music.mp3 and the sound effects.
Cuts land on 4-beat boundaries of the 112 BPM score (drop at 17.5 s).
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LANG, CLIPS, AUD = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(CLIPS, 'v5_' + LANG); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(HERE, f'fullsite-launch-v5-{LANG}.mp4')
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FM = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
G = (16, 185, 129, 255); W_ = (255, 255, 255, 255); K = (10, 10, 10, 255)
BAR = 60 / 112.34 * 8  # 8 beats = one cut

C = {
    'es': {
        'owner': [('Sábado. ', W_), ('23:47.', G)],
        'r1': [('Tu POS sabe cuánto vendiste.', W_)],
        'r2': [('No sabe cuánto ', W_), ('perdiste.', (239, 68, 68, 255))],
        'pre': 'PRESENTA',
        'orbit': [('Todo tu restaurante, ', W_), ('conectado.', G)],
        'cards': [('La IA vigila ', W_), ('cada peso.', G)],
        'phone': [('Te avisa ', W_), ('antes del cierre.', G)],
        'tablet': [('Cobra en ', K), ('segundos.', G)],
        'bar': [('Hecho para el ', W_), ('servicio real.', G)],
        'helix': [('Comandas, cocina, inventario ', K), ('y caja.', G)],
        'dash': [('Un solo sistema para ', K), ('operar y crecer.', G)],
        'tag': [('Deja de enterarte ', K), ('al cierre.', G)],
        'cta': 'Agenda tu demo  ·  fullsite.mx',
        'nf': ('Fullsite IA', 'ahora', 'Cancelaciones +38% en Sucursal Valle.'),
    },
    'en': {
        'owner': [('Saturday. ', W_), ('11:47 PM.', G)],
        'r1': [('Your POS knows what you sold.', W_)],
        'r2': [("It doesn't know what ", W_), ('you lost.', (239, 68, 68, 255))],
        'pre': 'INTRODUCING',
        'orbit': [('Your whole restaurant, ', W_), ('connected.', G)],
        'cards': [('AI watches ', W_), ('every peso.', G)],
        'phone': [('It tells you ', W_), ('before closing.', G)],
        'tablet': [('Charge in ', K), ('seconds.', G)],
        'bar': [('Built for ', W_), ('real service.', G)],
        'helix': [('Orders, kitchen, inventory ', K), ('and cash.', G)],
        'dash': [('One system to ', K), ('run and grow.', G)],
        'tag': [('Stop finding out ', K), ('at closing time.', G)],
        'cta': 'Book a demo  ·  fullsite.mx',
        'nf': ('Fullsite AI', 'now', 'Voids +38% at the Valle location.'),
    },
}[LANG]


def line_png(path, segs, size=84, font=FB, y=None, shadow=None):
    """centred multi-colour line on a transparent 1920x1080 canvas."""
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    f = ImageFont.truetype(font, size)
    d = ImageDraw.Draw(im)
    widths = [d.textlength(t, font=f) for t, _ in segs]
    x = (1920 - sum(widths)) / 2
    asc, desc = f.getmetrics()
    y = (1080 - asc) / 2 if y is None else y
    if shadow:
        sh = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); xx = x
        for (t, _), w in zip(segs, widths):
            sd.text((xx, y + 3), t, font=f, fill=shadow); xx += w
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(18))); d = ImageDraw.Draw(im)
    for (t, col), w in zip(segs, widths):
        d.text((x, y), t, font=f, fill=col); x += w
    im.save(path)


def wordmark_png(path, width=720, y=420, color=(10, 10, 10, 255), extra=None):
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    m = Image.open(os.path.join(HERE, 'assets/wordmark.png'))
    h = int(m.height * width / m.width); m = m.resize((width, h), Image.LANCZOS)
    solid = Image.new('RGBA', m.size, color); solid.putalpha(m.split()[3])
    x0 = (1920 - width) // 2; im.alpha_composite(solid, (x0, y))
    sq = round(.0454 * width); sx = x0 + round(.9546 * width); sy = y + round(.7783 * h)
    ImageDraw.Draw(im).rectangle([sx, sy, sx + sq - 1, sy + sq - 1], fill=G)
    im.save(path)
    return x0, y, width, h


def notif_png(path, y=110):
    app, when, msg = C['nf']
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    w, h = 1000, 168; x = (1920 - w) // 2
    sh = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x, y + 18, x + w, y + h + 18], 44, fill=(0, 0, 0, 150))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + w, y + h], 44, fill=(246, 246, 244, 245))
    ix, iy = x + 34, y + 38
    d.rounded_rectangle([ix, iy, ix + 92, iy + 92], 22, fill=(10, 10, 10, 255))
    fm = Image.open(os.path.join(HERE, 'assets/fmark.png')); fh = 58; fw = int(fm.width * fh / fm.height)
    fm = fm.resize((fw, fh), Image.LANCZOS); im.alpha_composite(fm, (ix + 22, iy + 17))
    d = ImageDraw.Draw(im)
    sqx = ix + 22 + int(.679 * fw); sqy = iy + 17 + int(.7675 * fh); sz = int(.321 * fw)
    d.rectangle([sqx, sqy, sqx + sz, sqy + sz], fill=G)
    ft = ImageFont.truetype(FB, 32); fb = ImageFont.truetype(FM, 34); fs = ImageFont.truetype(FM, 28)
    d.text((ix + 122, y + 34), app, font=ft, fill=(17, 17, 17, 255))
    d.text((x + w - 40 - d.textlength(when, font=fs), y + 38), when, font=fs, fill=(130, 130, 130, 255))
    d.text((ix + 122, y + 86), msg, font=fb, fill=(30, 30, 30, 255))
    im.save(path)


def run(a):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + a, check=True)


# ---------- text cards ----------
SH = (0, 0, 0, 160)
line_png(f'{TMP}/owner.png', C['owner'], 92, y=800, shadow=SH)
line_png(f'{TMP}/r1.png', C['r1'], 76, y=140, shadow=SH)
line_png(f'{TMP}/r2.png', C['r2'], 76, y=240, shadow=SH)
wordmark_png(f'{TMP}/wm_dark.png', 560, 760, (255, 255, 255, 255))
line_png(f'{TMP}/pre.png', [(C['pre'], (255, 255, 255, 170))], 22, FM, y=880)
line_png(f'{TMP}/orbit.png', C['orbit'], 72, y=900, shadow=SH)
line_png(f'{TMP}/cards.png', C['cards'], 80, y=880, shadow=SH)
line_png(f'{TMP}/phone.png', C['phone'], 80, y=880, shadow=SH)
# POS title: white-on-light needs dark ink
wordmark_png(f'{TMP}/wm_pos.png', 420, 120, (10, 10, 10, 255))
line_png(f'{TMP}/tablet.png', C['tablet'], 84, y=110, shadow=(255, 255, 255, 200))
line_png(f'{TMP}/bar.png', C['bar'], 80, y=880, shadow=SH)
line_png(f'{TMP}/helix.png', C['helix'], 72, y=110, shadow=(255, 255, 255, 230))
line_png(f'{TMP}/dash.png', C['dash'], 80, y=100, shadow=(255, 255, 255, 230))
wordmark_png(f'{TMP}/wm_end.png', 640, 330, (10, 10, 10, 255))
line_png(f'{TMP}/tag.png', C['tag'], 60, y=520)
line_png(f'{TMP}/cta.png', [(C['cta'], (60, 60, 60, 255))], 30, FM, y=640)
notif_png(f'{TMP}/notif.png')
line_png(f'{TMP}/connect.png', [('Connect', W_), ('.', G)], 150, y=420, shadow=SH)
line_png(f'{TMP}/pos.png', [('POS', K), ('.', G)], 110, y=230)

# ---------- shot list: (src, src_start, dur, overlays[(png, t_in, t_out)], grade) ----------
b = BAR
SHOTS = [  # (src, start, use, dur, overlays)
    ('owner.mp4', 0.3, 4.4, 4.4, [('owner', 0.6, 99)]),
    ('c0.mp4', 0.1, 3.4, 4.2, [('r1', 0.3, 99), ('r2', 1.9, 99)]),
    ('c1.mp4', 0.0, 2.7, 4.4, [('wm_dark', 1.6, 99), ('pre', 2.6, 99)]),
    ('c2.mp4', 0.2, 3.6, 4.5, [('connect', 0.3, 2.6), ('orbit', 2.0, 99)]),
    ('c3.mp4', 0.1, 2.7, b, [('cards', 0.4, 99)]),
    ('c4.mp4', 0.1, 3.2, b, [('notif', 0.5, 99), ('phone', 1.1, 99)]),
    ('c5.mp4', 0.1, 3.6, b, [('wm_pos', 0.3, 99), ('pos', 0.5, 99)]),
    ('c6.mp4', 0.1, 3.0, b, [('tablet', 0.4, 99)]),
    ('bartender.mp4', 0.6, 3.4, b, [('bar', 0.4, 99)]),
    ('c7.mp4', 0.1, 2.5, b, [('helix', 0.4, 99)]),
    ('dashreal.mp4', 0.2, 3.8, b, [('dash', 0.4, 99)]),
    ('c9.mp4', 0.0, 5.0, 55.0 - (17.5 + 7 * b), [('wm_end', 0.5, 99), ('tag', 1.3, 99), ('cta', 2.1, 99)]),
]
FADE = 0.45
parts = []
for i, (src, ss, use, dur, ovs) in enumerate(SHOTS):
    p = f'{TMP}/s{i}.mp4'; parts.append(p)
    inputs = ['-ss', str(ss), '-t', f'{use:.3f}', '-i', os.path.join(CLIPS, src)]
    crop = {'bartender.mp4': 'crop=960:540:0:330,', 'dashreal.mp4': 'crop=960:540:0:180,'}.get(src, '')
    k = dur / use
    slow = f"setpts={k:.4f}*PTS,minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if k > 1.05 else 'fps=60,'
    base = crop + slow + "scale=1920:1080:flags=lanczos,setsar=1,unsharp=5:5:0.45,eq=contrast=1.03:saturation=0.97"
    if src == 'c4.mp4':  # hide the model's gibberish notification text
        base += ",split[m][bb];[bb]crop=1300:380:310:50,gblur=sigma=28[bl];[m][bl]overlay=310:50"

    # slow-down guard: if the source is shorter than needed, hold the last frame
    base += f",tpad=stop_mode=clone:stop_duration=2,trim=duration={dur:.3f}"
    fc = f"[0:v]{base}[v0];"
    last = 'v0'
    for j, (png, ti, to) in enumerate(ovs):
        inputs += ['-loop', '1', '-t', f'{dur:.3f}', '-i', f'{TMP}/{png}.png']
        k = j + 1
        fade = f"fade=in:st={ti}:d={FADE}:alpha=1"
        if to < dur:
            fade += f",fade=out:st={to}:d=0.3:alpha=1"
        # text drifts up 18px while fading in
        fc += f"[{k}:v]format=rgba,{fade}[t{k}];[{last}][t{k}]overlay=x=0:y='18*max(0,1-(t-{ti})/0.8)'[o{k}];"
        last = f'o{k}'
    fc += f"[{last}]format=yuv420p[v]"
    run(inputs + ['-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', '60', '-an', p])

# join with short dissolves on the intro beats, hard cuts on the drop section
with open(f'{TMP}/list.txt', 'w') as fh:
    for p in parts:
        fh.write(f"file '{p}'\n")
run(['-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/video.mp4'])

# ---------- audio: score + sound design ----------
cuts = [0]
for (_, _, _, d, _) in SHOTS:
    cuts.append(cuts[-1] + d)
sfx = [  # (file, time, gain dB)
    ('impact', cuts[2] - 0.05, -6), ('glass', cuts[3], -14), ('whoosh', cuts[4] - 0.35, -12),
    ('glass', cuts[5], -14), ('whoosh', cuts[6] - 0.35, -14), ('click', cuts[7] + 1.4, -8),
    ('paid', cuts[7] + 1.7, -10), ('whoosh', cuts[8] - 0.35, -14), ('whoosh', cuts[10] - 0.35, -14),
    ('impact', cuts[11] - 0.05, -8),
]
if os.path.exists(f'{AUD}/notif.mp3'):
    sfx.append(('notif', cuts[5] + 0.6, -6))
ins = ['-i', f'{AUD}/music.mp3']; fc = ''
for i, (f, t, g) in enumerate(sfx):
    ins += ['-i', f'{AUD}/{f}.mp3']
    fc += f"[{i + 1}:a]volume={g}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{i}];"
fc += '[0:a]' + ''.join(f'[s{i}]' for i in range(len(sfx))) + f"amix=inputs={len(sfx) + 1}:normalize=0,alimiter=limit=0.95,afade=t=out:st=53.6:d=1.4[a]"
run(ins + ['-filter_complex', fc, '-map', '[a]', '-t', '55', '-c:a', 'pcm_s16le', f'{TMP}/audio.wav'])
run(['-i', f'{TMP}/video.mp4', '-i', f'{TMP}/audio.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT])
run(['-i', OUT, '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-level', '4.0', '-b:v', '3500k', '-maxrate', '4500k', '-bufsize', '9000k',
     '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT.replace('.mp4', '-ligero.mp4')])
print('cuts', [round(c, 2) for c in cuts])
print('ok', OUT)
