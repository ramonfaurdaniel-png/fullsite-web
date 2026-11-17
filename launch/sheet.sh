#!/bin/bash
# usage: sheet.sh outdir t1 t2 ...
S="$1"; shift; mkdir -p "$S"; rm -f "${S:?}"/f_*.jpg
node "$(dirname "$0")/stills.js" "$S" "$@"
python3 - "$S" <<'PY'
import sys,glob
from PIL import Image,ImageDraw
S=sys.argv[1]
fs=sorted(glob.glob(S+'/f_*.jpg'),key=lambda f:float(f.split('f_')[1][:-4]))
W,H=480,270
c=Image.new('RGB',(W*4,H*((len(fs)+3)//4)))
for i,f in enumerate(fs):
  im=Image.open(f).resize((W,H)); ImageDraw.Draw(im).text((6,4),f.split('f_')[1][:-4],fill='yellow'); c.paste(im,((i%4)*W,(i//4)*H))
c.save(S+'/sheet.jpg')
PY
