# Fullsite — Launch video (Connect + POS)

- `fullsite-launch.mp4` — final 1920×1080, 30 fps, 51 s, with soundtrack.
- `fullsite-launch.html` — the live, code-driven version (open it in a browser and click play; space = pause, scrub bar at the bottom). Every frame is computed from the time `t`, so it renders the same way every time.
- `build_audio.py` — synthesizes the 120 BPM soundtrack (`python3 build_audio.py assets/soundtrack.wav`).
- `render.js` — renders the HTML to MP4 (`node render.js 30 fullsite-launch.mp4`; needs Playwright + ffmpeg).
- `stills.js` / `sheet.sh` — grab frames at specific seconds for checking.

To change copy, edit the strings in the `BUILD` section of the HTML and run `render.js` again.
