"""Final edit: v3 motion piece + Higgsfield cinematic shots.

usage: python3 build_final.py <lang es|en> <shots_dir> [saas_clip.mp4]
Timeline (seconds of output):
  0.0 - 4.0   intro: restaurant owner at night (shot3) + text
  4.0 - 25.0  v3 0.0 - 21.0 (problem, logo, Connect)
  25.0 - 27.9 real product: terminal (shot0) + bartender (shot1) with 'fullsite POS'
  27.9 - 55.0 v3 23.9 - 51.0 (POS demo, together, end)
Audio: muffled intro from the soundtrack, then the v3 soundtrack untouched
(the replaced 21.0-23.9 stretch keeps its own audio, so every hit still lands).
"""
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

LANG = sys.argv[1]
SHOTS = sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(SHOTS, 'edit_' + LANG); os.makedirs(TMP, exist_ok=True)
V3 = os.path.join(HERE, f'fullsite-launch-{LANG}.mp4')
OUT = os.path.join(HERE, f'fullsite-launch-final-{LANG}.mp4')
FONT_B = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FONT_M = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
TXT = {
    'es': ('Sábado. 23:47.', 'El corte de caja no cuadra.'),
    'en': ('Saturday. 11:47 PM.', "The numbers don't add up."),
}[LANG]


def text_png(path, line, size, font, color=(255, 255, 255, 255), w=1920, h=1080, y=None, shadow=True):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(font, size)
    bb = d.textbbox((0, 0), line, font=f)
    x = (w - (bb[2] - bb[0])) // 2
    y = y if y is not None else (h - (bb[3] - bb[1])) // 2
    if shadow:
        sh = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x, y + 4), line, font=f, fill=(0, 0, 0, 150))
        from PIL import ImageFilter
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(im)
    d.text((x, y), line, font=f, fill=color)
    im.save(path)


def pos_title_png(path):
    """white fullsite wordmark (from the mask) + 'POS' + green square, centred low."""
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    wm = Image.open(os.path.join(HERE, 'assets/wordmark.png'))
    W = 520; H = int(wm.height * W / wm.width)
    wm = wm.resize((W, H), Image.LANCZOS)
    f = ImageFont.truetype(FONT_B, int(H * 1.18))
    d = ImageDraw.Draw(im)
    pos_w = d.textbbox((0, 0), 'POS', font=f)[2]
    total = W + 34 + pos_w
    x0 = (1920 - total) // 2; y0 = 820
    from PIL import ImageFilter
    glow = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow); gd.rectangle([x0 - 60, y0 - 50, x0 + total + 60, y0 + H + 60], fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(50)))
    im.alpha_composite(wm, (x0, y0))
    sq = int(.0454 * W); sx = x0 + int(.9546 * W); sy = y0 + int(.7783 * H)
    ImageDraw.Draw(im).rectangle([sx, sy, sx + sq, sy + sq], fill=(16, 185, 129, 255))
    bb = d.textbbox((0, 0), 'POS', font=f)
    ImageDraw.Draw(im).text((x0 + W + 34, y0 + H - bb[3] + 2), 'POS', font=f, fill=(255, 255, 255, 255))
    im.save(path)


def run(args):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + args, check=True)


text_png(f'{TMP}/t1.png', TXT[0], 96, FONT_B, y=760)
text_png(f'{TMP}/t2.png', TXT[1], 52, FONT_M, color=(255, 255, 255, 215), y=885)
pos_title_png(f'{TMP}/pos.png')

V = '-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 60 -an'.split()
GRADE = 'eq=contrast=1.06:saturation=1.08,unsharp=5:5:0.6'
# intro: owner at night, slow push, two text lines fading in
run(['-ss', '0.4', '-t', '4', '-i', f'{SHOTS}/shot3.mp4', '-loop', '1', '-t', '4', '-i', f'{TMP}/t1.png', '-loop', '1', '-t', '4', '-i', f'{TMP}/t2.png',
     '-filter_complex',
     f"[0:v]scale=2112:1188:flags=lanczos,crop=1920:1080:'(iw-ow)/2':'(ih-oh)/2',{GRADE},fps=60,fade=in:st=0:d=0.6,fade=out:st=3.75:d=0.25:color=white[b];"
     "[1:v]format=rgba,fade=in:st=0.7:d=0.6:alpha=1[a1];[2:v]format=rgba,fade=in:st=1.9:d=0.6:alpha=1[a2];"
     "[b][a1]overlay[o1];[o1][a2]overlay,format=yuv420p[v]", '-map', '[v]'] + V + [f'{TMP}/p0.mp4'])
# real product shots (square 960 -> 16:9 crop, upscale)
run(['-ss', '0.5', '-t', '1.6', '-i', f'{SHOTS}/shot0.mp4', '-filter_complex',
     f"[0:v]crop=960:540:0:320,scale=1920:1080:flags=lanczos,{GRADE},fps=60,format=yuv420p[v]",
     '-map', '[v]'] + V + [f'{TMP}/p2.mp4'])
run(['-ss', '1.2', '-t', '1.3', '-i', f'{SHOTS}/shot1.mp4', '-loop', '1', '-t', '1.3', '-i', f'{TMP}/pos.png', '-filter_complex',
     f"[0:v]crop=960:540:0:330,scale=1920:1080:flags=lanczos,{GRADE},fps=60[b];[1:v]format=rgba,fade=in:st=0:d=0.3:alpha=1[t];[b][t]overlay,format=yuv420p[v]",
     '-map', '[v]'] + V + [f'{TMP}/p3.mp4'])
# v3 pieces
run(['-ss', '0', '-t', '21.0', '-i', V3, '-vf', 'fps=60'] + V + [f'{TMP}/p1.mp4'])
run(['-ss', '23.9', '-t', '27.1', '-i', V3, '-vf', 'fps=60'] + V + [f'{TMP}/p4.mp4'])
with open(f'{TMP}/list.txt', 'w') as fh:
    for p in ['p0', 'p1', 'p2', 'p3', 'p4']:
        fh.write(f"file '{TMP}/{p}.mp4'\n")
run(['-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/video.mp4'])
# audio: muffled 4 s intro + full soundtrack
SND = os.path.join(HERE, 'assets/soundtrack.wav')
run(['-i', SND, '-filter_complex',
     "[0:a]atrim=0:4,asetpts=PTS-STARTPTS,lowpass=f=700,volume=0.9,afade=t=in:st=0:d=1.2[i];[0:a]asetpts=PTS-STARTPTS[m];[i][m]concat=n=2:v=0:a=1[a]",
     '-map', '[a]', '-c:a', 'pcm_s16le', f'{TMP}/audio.wav'])
run(['-i', f'{TMP}/video.mp4', '-i', f'{TMP}/audio.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT])
# light version for phones
run(['-i', OUT, '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-level', '4.0', '-b:v', '2400k', '-maxrate', '3200k', '-bufsize', '6400k',
     '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', OUT.replace('.mp4', '-ligero.mp4')])
print('ok', OUT)
