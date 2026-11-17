"""Manifesto cut: "behind every restaurant there is someone" -> Fullsite. Real footage, piano only, restrained type.
Archival film treatment (grain, warm faded grade, vignette) + stacked lowercase type.

usage: python3 build_story.py <es|en> <clips_dir> <aud_dir>
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

LANG, CLIPS, AUD = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(CLIPS, 'man_' + LANG); os.makedirs(TMP, exist_ok=True)
BASE = os.path.join(CLIPS, 'man_base'); os.makedirs(BASE, exist_ok=True)
OUT = os.path.join(HERE, f'fullsite-manifiesto-{LANG}.mp4')
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FM = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
W = (255, 255, 255, 255); G = (16, 185, 129, 255)

# each shot: key -> lines (list of segments [(text, colour)])
COPY = {
    'es': {
        'a': [[('detrás de cada restaurante', W)]],
        'b': [[('hay alguien que llega antes que todos', W)]],
        'c': [], 'd': [[('que conoce su cocina por el sonido', W)]],
        'e': [[('y a sus clientes por su nombre', W)]], 'f': [],
        'g': [[('que se va después del último', W)]], 'h': [],
        'i': [[('que cierra cansado', W)]],
        'j': [[('y aún así, no sabe cómo le fue', W)]],
        'brand': [[('para ellos hicimos', W)]],
        'k': [[('para que dejes de enterarte al cierre', W)]],
        'l': [[('y llegues a casa a tiempo', W)]],
        'end': [[('para los que viven su restaurante', (255, 255, 255, 230))]],
    },
    'en': {
        'a': [[('behind every restaurant', W)]],
        'b': [[("there's someone who arrives before everyone", W)]],
        'c': [], 'd': [[('who knows their kitchen by its sound', W)]],
        'e': [[('and their guests by name', W)]], 'f': [],
        'g': [[('who leaves after the last guest', W)]], 'h': [],
        'i': [[('who closes up tired', W)]],
        'j': [[("and still doesn't know how the day went", W)]],
        'brand': [[('we built this for them', W)]],
        'k': [[('so you stop finding out at closing time', W)]],
        'l': [[('and make it home on time', W)]],
        'end': [[('for the people who live their restaurant', (255, 255, 255, 230))]],
    },
}[LANG]

# (key, src, src_start, use_seconds, crop, grade)
SHOTS = [  # real footage (Mixkit free licence) + the real Fullsite terminal photo
    ('a', '30468.mp4', 2.0, 9, None, 'warm'),
    ('b', '22660.mp4', 1.0, 9, None, 'warm'),
    ('c', '9409.mp4', 6.0, 9, None, 'warm'),
    ('d', '9338.mp4', 2.0, 9, None, 'warm'),
    ('e', '205.mp4', 4.0, 9, None, 'warm'),
    ('f', '4118.mp4', 10.0, 9, None, 'warm'),
    ('g', '4331.mp4', 2.0, 9, None, 'night'),
    ('h', '46626.mp4', 3.0, 9, None, 'night'),
    ('i', '6165.mp4', 3.0, 9, None, 'night'),
    ('j', '47627.mp4', 2.0, 9, None, 'night'),
    ('brand', 'BLACK', 0, 0, None, 'none'),
    ('k', 'TERMINAL', 0, 0, None, 'warm'),
    ('l', '23046.mp4', 2.0, 9, None, 'warm'),
    ('end', 'BLACK', 0, 0, None, 'none'),
]
# cuts land on the piano notes (1.0, 6.5, 11, 17, 21, 28.5, 36, 44.5, 48.5)
DUR = [6.5, 4.5, 3.0, 3.0, 4.0, 3.7, 3.8, 3.5, 3.5, 4.5, 4.0, 4.0, 4.5, 7.5]
assert len(DUR) == len(SHOTS)

GRADE = {
    'warm': "eq=saturation=0.78:contrast=1.04:gamma=0.98,colorbalance=rs=0.05:gs=0.01:bs=-0.05:rh=0.03:bh=-0.03",
    'night': "eq=saturation=0.7:contrast=1.05:gamma=0.95,colorbalance=rs=0.02:bs=0.01",
    'era': "eq=saturation=0.55:contrast=1.06:gamma=0.97,colorbalance=rs=0.06:gs=0.02:bs=-0.06:rh=0.04:bh=-0.05",
    'now_dark': "eq=saturation=0.8:contrast=1.04,colorbalance=rs=0.03:bs=-0.03",
    'now': "eq=saturation=0.82:contrast=1.03,colorbalance=rs=0.03:bs=-0.03:rh=0.02",
    'none': "null",
}
FILM = "noise=alls=7:allf=t,vignette=angle=PI/4.4"


def run(a):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + a, check=True)


def text_lines(key, size=60):
    """one PNG per line; lines stacked and staggered like the reference."""
    lines = COPY[key]
    f = ImageFont.truetype(FM, size)
    lh = int(size * 1.2)
    total = lh * len(lines)
    y0 = 880 if key not in ('brand', 'end') else (1080 - total) // 2
    paths = []
    for i, segs in enumerate(lines):
        im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        ws = []
        for t, _ in segs:  # tight tracking: draw glyph by glyph
            ws.append(sum(d.textlength(ch, font=f) for ch in t) - size * 0.025 * (len(t) - 1))
        x = (1920 - sum(ws)) / 2
        y = y0 + i * lh
        sh = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        xx = x
        for (t, col), w in zip(segs, ws):
            for ch in t:
                sd.text((xx, y + 4), ch, font=f, fill=(0, 0, 0, 170)); d.text((xx, y), ch, font=f, fill=col)
                xx += d.textlength(ch, font=f) - size * 0.025
        im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), im)
        p = f'{TMP}/{key}_{i}.png'; im.save(p); paths.append(p)
    return paths


def wordmark(path, width, y, color=(255, 255, 255, 255)):
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    m = Image.open(os.path.join(HERE, 'assets/wordmark.png'))
    h = int(m.height * width / m.width); m = m.resize((width, h), Image.LANCZOS)
    solid = Image.new('RGBA', m.size, color); solid.putalpha(m.split()[3])
    x0 = (1920 - width) // 2; im.alpha_composite(solid, (x0, y))
    sq = round(.0454 * width); sx = x0 + round(.9546 * width); sy = y + round(.7783 * h)
    ImageDraw.Draw(im).rectangle([sx, sy, sx + sq - 1, sy + sq - 1], fill=G)
    im.save(path)


def notif(path, y=150):
    app, when, msg = COPY['nf']
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    w, h = 1000, 168; x = (1920 - w) // 2
    sh = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x, y + 18, x + w, y + h + 18], 44, fill=(0, 0, 0, 150))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(30))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + w, y + h], 44, fill=(246, 246, 244, 242))
    ix, iy = x + 34, y + 38
    d.rounded_rectangle([ix, iy, ix + 92, iy + 92], 22, fill=(10, 10, 10, 255))
    fm = Image.open(os.path.join(HERE, 'assets/fmark.png')); fh = 58; fw = int(fm.width * fh / fm.height)
    fm = fm.resize((fw, fh), Image.LANCZOS); im.alpha_composite(fm, (ix + 22, iy + 17)); d = ImageDraw.Draw(im)
    sqx = ix + 22 + int(.679 * fw); sqy = iy + 17 + int(.7675 * fh); sz = int(.321 * fw)
    d.rectangle([sqx, sqy, sqx + sz, sqy + sz], fill=G)
    ft = ImageFont.truetype(FB, 32); fb = ImageFont.truetype(FM, 34); fs = ImageFont.truetype(FM, 28)
    d.text((ix + 122, y + 34), app, font=ft, fill=(17, 17, 17, 255))
    d.text((x + w - 40 - d.textlength(when, font=fs), y + 38), when, font=fs, fill=(130, 130, 130, 255))
    d.text((ix + 122, y + 86), msg, font=fb, fill=(30, 30, 30, 255))
    im.save(path)


wordmark(f'{TMP}/wm_big.png', 640, 450)
# (no notification card in the manifesto)
low = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); ld = ImageDraw.Draw(low)
ld.rectangle([0, 800, 1920, 1080], fill=(0, 0, 0, 120)); low.filter(ImageFilter.GaussianBlur(90)).save(f'{TMP}/lowscrim.png')
# soft dark scrim so white type always reads
scr = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); sd = ImageDraw.Draw(scr)
sd.ellipse([260, 300, 1660, 780], fill=(0, 0, 0, 120)); scr.filter(ImageFilter.GaussianBlur(120)).save(f'{TMP}/scrim.png')

parts = []
for i, ((key, src, ss, use, crop, grade), dur) in enumerate(zip(SHOTS, DUR)):
    out = f'{TMP}/p{i:02d}.mp4'; parts.append(out)
    if src == 'BLACK':
        inputs = ['-f', 'lavfi', '-t', f'{dur:.3f}', '-i', 'color=c=0x0b0b0a:s=1920x1080:r=60']
        base = f"[0:v]{FILM}[b];"
    elif src == 'TERMINAL':  # the real product photo with a slow push-in
        inputs = ['-loop', '1', '-t', f'{dur:.3f}', '-i', os.path.join(HERE, 'assets/img-terminal.jpg')]
        n_fr = int(dur * 60)
        base = (f"[0:v]scale=2400:-1,crop=2400:1350:0:820,zoompan=z='1+0.06*on/{n_fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=60,"
                f"{GRADE[grade]},{FILM}[b];")
    else:
        bp = f"{BASE}/{src.replace('.mp4', '')}_{ss}_{use}_{dur:.3f}.mp4"
        if not os.path.exists(bp):
            k = dur / use
            slow = f"setpts={k:.4f}*PTS,minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," if k > 1.05 else 'fps=60,'
            if k < 0.95:
                slow = 'fps=60,'
            vf = (crop or '') + slow + "scale=1920:1080:flags=lanczos,setsar=1," + f"tpad=stop_mode=clone:stop_duration=3,trim=duration={dur:.3f},format=yuv420p"
            run(['-ss', str(ss), '-t', f'{max(use, dur) if k < 0.95 else use:.3f}', '-i', os.path.join(CLIPS, src), '-vf', vf,
                 '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-r', '60', '-an', bp])
        inputs = ['-i', bp]
        base = f"[0:v]{GRADE[grade]},{FILM}[b];"
    fc = base; last = 'b'; n = 1
    # overlays
    ovl = []
    if key == 'brand':
        ovl.append((f'{TMP}/wm_big.png', 2.0))
    elif key != 'end':
        ovl.append((f'{TMP}/lowscrim.png', 0.0))
    if key == 'end':
        wordmark(f'{TMP}/wm_end.png', 560, 420)
        ovl.append((f'{TMP}/wm_end.png', 0.5))
    lines = text_lines(key, 46 if key == 'end' else (56 if key == 'brand' else 54)) if COPY[key] else []
    if key == 'end':  # small line under the wordmark
        for p in lines:
            im = Image.open(p); moved = Image.new('RGBA', im.size, (0, 0, 0, 0)); moved.paste(im, (0, 190)); moved.save(p)
    t0 = {'a': 1.0, 'brand': 0.4, 'end': 1.4}.get(key, 0.6)
    for j, p in enumerate(lines):
        ovl.append((p, t0 + j * 0.32))
    for p, ti in ovl:
        inputs += ['-loop', '1', '-t', f'{dur:.3f}', '-i', p]
        fade = f"fade=in:st={ti}:d=0.7:alpha=1" if ti > 0 else 'null'
        if key == 'brand' and 'wm_big' not in p:
            fade += ',fade=out:st=1.5:d=0.4:alpha=1'
        fc += f"[{n}:v]format=rgba,{fade}[t{n}];[{last}][t{n}]overlay=x=0:y='8*max(0,1-(t-{ti})/1.0)'[o{n}];"
        last = f'o{n}'; n += 1
    if i == len(SHOTS) - 1:
        fc += f"[{last}]fade=out:st={dur - 1.0:.3f}:d=1.0[fo];"; last = 'fo'
    fc += f"[{last}]format=yuv420p[v]"
    run(inputs + ['-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-r', '60', '-an', out])

with open(f'{TMP}/list.txt', 'w') as fh:
    for p in parts:
        fh.write(f"file '{p}'\n")
run(['-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/video.mp4'])
total = sum(DUR)
run(['-i', f'{TMP}/video.mp4', '-i', f'{AUD}/music_doc.mp3', '-filter_complex',
     f"[1:a]atrim=0:{total:.3f},volume=1.8,alimiter=limit=0.95,afade=t=out:st={total - 3.0:.3f}:d=3.0[a]",
     '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT])
run(['-i', OUT, '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-level', '4.0', '-b:v', '4000k', '-maxrate', '5000k', '-bufsize', '10000k',
     '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT.replace('.mp4', '-ligero.mp4')])
print('ok', OUT, round(total, 2))
