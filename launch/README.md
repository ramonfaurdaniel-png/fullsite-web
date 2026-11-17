# Fullsite — Launch video (Connect + POS)

- `fullsite-launch-es.mp4` / `fullsite-launch-en.mp4`: final cuts, 1920×1080, 30 fps with real motion blur (rendered at 60 fps, every two frames blended into one), 51 s, with soundtrack.
- `fullsite-launch.html`: the live, code-driven version. Open it in a browser and press play. Space pauses, there's a scrub bar at the bottom, and the button in the corner switches language (`?lang=en` / `?lang=es`).
- All the copy lives in the `COPY` object (ES / EN) at the top of the script.
- `build_audio.py`: synthesizes the 120 BPM soundtrack (`python3 build_audio.py assets/soundtrack.wav`).
- `render.js`: renders to MP4 (`node render.js es` / `node render.js en`). Needs Playwright and ffmpeg, and takes about 8 minutes per language.
- `stills.js` / `sheet.sh`: grab frames at specific seconds for checking (`LANG_V=en ./sheet.sh out_dir 3.2 19.5`).
