"""UI cards for film v4, written as HTML (rendered by cards_render.js).
build(lang) -> list of {name, html}; every card has class "card" so the renderer can also produce its shape mask."""
import base64, os

HERE = os.path.dirname(os.path.abspath(__file__))
_b64 = lambda p: base64.b64encode(open(os.path.join(HERE, p), 'rb').read()).decode()
FMARK = _b64('assets/fmark.png'); WMARK = _b64('assets/wordmark.png')

I = {  # lucide-style line icons (24x24 viewBox)
    'monitor': '<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>',
    'utensils': '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    'book': '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    'carrot': '<path d="M2.27 21.7s9.87-3.5 12.73-6.36a4.5 4.5 0 0 0-6.36-6.37C5.77 11.84 2.27 21.7 2.27 21.7zM8.64 14l-2.05-2.04M15.34 15l-2.46-2.46"/><path d="M22 9s-1.33-2-3.5-2C16.86 7 15 9 15 9s1.33 2 3.5 2S22 9 22 9z"/><path d="M15 2s-2 1.33-2 3.5S15 9 15 9s2-1.84 2-3.5C17 3.33 15 2 15 2z"/>',
    'package': '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    'dollar': '<line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    'percent': '<line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    'user': '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    'flame': '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3 0 1.38 1.12 2.5 2.5 2.5z"/>',
    'wallet': '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    'receipt': '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
    'alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    'trend': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    'eye': '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'wifioff': '<path d="M12 20h.01"/><path d="M8.5 16.43a5 5 0 0 1 7 0"/><path d="M2 8.82a15 15 0 0 1 4.17-2.65"/><path d="M10.66 5c4.01-.36 8.14.9 11.34 3.76"/><path d="M16.85 11.25a10 10 0 0 1 2.22 1.68"/><path d="M5 13a10 10 0 0 1 5.24-2.76"/><path d="m2 2 20 20"/>',
    'wifi': '<path d="M12 20h.01"/><path d="M2 8.82a15 15 0 0 1 20 0"/><path d="M5 12.86a10 10 0 0 1 14 0"/><path d="M8.5 16.43a5 5 0 0 1 7 0"/>',
    'down': '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
}


def svg(name, color='#34d399', size=24, sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>')


CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1920px;height:1080px;background:transparent;overflow:hidden}}
body{{font-family:'Inter';color:#fff;-webkit-font-smoothing:antialiased;position:relative}}
.card{{position:absolute;border-radius:30px;background:linear-gradient(180deg,rgba(44,44,48,.50),rgba(12,12,14,.62));
  border:1px solid rgba(255,255,255,.16);box-shadow:0 34px 90px rgba(0,0,0,.42),inset 0 1px 0 rgba(255,255,255,.20);padding:30px 34px}}
.card.light{{background:linear-gradient(180deg,rgba(250,250,248,.80),rgba(236,236,234,.78));color:#111;border-color:rgba(255,255,255,.6)}}
body.mask .card{{background:#fff!important;box-shadow:none!important;border-color:#fff!important}}
body.mask .card *{{visibility:hidden}}
body.mask .nomask{{visibility:hidden}}
.hd{{display:flex;align-items:center;gap:14px;font-size:23px;font-weight:500;color:rgba(255,255,255,.74);letter-spacing:.1px}}
.light .hd{{color:#222}}
.ic{{width:46px;height:46px;flex:none;border-radius:13px;display:grid;place-items:center;background:rgba(16,185,129,.14);border:1px solid rgba(52,211,153,.38)}}
.ic.red{{background:rgba(248,113,113,.14);border-color:rgba(252,165,165,.38)}}
.ic.amb{{background:rgba(245,158,11,.14);border-color:rgba(252,211,77,.40)}}
.ic.gry{{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.20)}}
.fm{{width:46px;height:46px;flex:none;border-radius:13px;background:#0b0b0c;border:1px solid rgba(255,255,255,.16);position:relative}}
.fm i{{position:absolute;left:12px;top:9px;width:21px;height:28px;background:#fff;-webkit-mask:url(data:image/png;base64,{FMARK}) center/contain no-repeat}}
.fm b{{position:absolute;left:28px;top:30px;width:7px;height:7px;background:#10b981}}
.big{{font-family:'Inter Display';font-weight:700;font-size:66px;letter-spacing:-1.6px;line-height:1;margin-top:20px;font-variant-numeric:tabular-nums}}
.sub{{font-size:22px;color:rgba(255,255,255,.62);margin-top:12px}}
.g{{color:#34d399}} .r{{color:#fca5a5}} .a{{color:#fcd34d}}
.row{{display:flex;justify-content:space-between;align-items:baseline;gap:30px;font-size:25px;padding:15px 0;border-top:1px solid rgba(255,255,255,.09)}}
.row span:first-child{{color:rgba(255,255,255,.80)}}
.row b{{font-weight:600;font-variant-numeric:tabular-nums}}
.lab{{font-size:19px;font-weight:700;letter-spacing:2.2px;color:#34d399}}
.live{{margin-left:auto;display:flex;align-items:center;gap:9px;font-size:17px;font-weight:700;letter-spacing:1.8px;color:#34d399}}
.live i{{width:10px;height:10px;border-radius:50%;background:#34d399;box-shadow:0 0 0 6px rgba(52,211,153,.18)}}
.btn{{margin-top:24px;display:inline-flex;align-items:center;gap:12px;height:62px;padding:0 30px;border-radius:31px;font-size:24px;font-weight:600;border:2px solid #34d399;color:#34d399}}
.btn.on{{background:#10b981;border-color:#10b981;color:#06110c}}
.k{{font-size:17px;font-weight:700;letter-spacing:1.6px;color:rgba(255,255,255,.45);margin-bottom:4px}}
"""


def page(body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


def fm():
    return '<div class="fm"><i></i><b></b></div>'


def ic(name, cls='', color='#34d399'):
    return f'<div class="ic {cls}">{svg(name, color)}</div>'


def build(lang):
    es = lang == 'es'
    L = lambda a, b: a if es else b
    C = []
    add = lambda name, body: C.append({'name': name, 'html': page(body)})
    R = 'left:1180px;top:120px;width:600px'

    # story: losses on the receipts shot (left blank in v3 style, now in the new system)
    add('loss1', f'<div class="card" style="left:1200px;top:150px;width:520px"><div class="hd">{ic("alert","red","#fca5a5")}{L("Merma · aguacate","Waste · avocado")}</div><div class="big r">−$4,380</div></div>')
    add('loss2', f'<div class="card" style="left:1200px;top:370px;width:520px"><div class="hd">{ic("alert","red","#fca5a5")}{L("Cancelaciones","Voids")}</div><div class="big r">−$1,920</div></div>')

    # 1 · your POS knows how much you sold (deliberately plain)
    add('pos_sales', f'<div class="card" style="{R}"><div class="hd">{ic("monitor","gry","#d4d4d4")}{L("Tu punto de venta","Your POS")}</div>'
        f'<div class="big">$38,400</div><div class="sub">{L("Ventas de hoy. Y ya.","Today\'s sales. That\'s it.")}</div></div>')
    # 2 · where the money leaks
    rows = [(L('Merma de aguacate', 'Avocado waste'), '−$4,380'), (L('Cancelaciones fuera de patrón', 'Out-of-pattern voids'), '−$1,240'),
            (L('Cortesías sin autorizar', 'Unauthorized comps'), '−$860')]
    add('leaks', f'<div class="card" style="left:1120px;top:110px;width:660px"><div class="hd" style="margin-bottom:14px">{fm()}{L("Dónde se te va el dinero","Where your money leaks")}'
        f'<div class="live"><i></i>{L("HOY","TODAY")}</div></div>'
        + ''.join(f'<div class="row"><span>{a}</span><b class="r">{b}</b></div>' for a, b in rows) +
        f'<div class="row" style="border-top:1px solid rgba(255,255,255,.22);font-size:28px"><span style="color:#fff;font-weight:600">{L("Fuga detectada","Leak detected")}</span><b class="r" style="font-size:34px">−$6,480</b></div></div>')
    # 3 · a sale is not just a ticket
    add('ticket', f'<div class="card" style="left:110px;top:800px;width:auto;padding:24px 34px 24px 26px"><div class="hd" style="color:#fff;font-size:30px;font-weight:600">{ic("receipt")}'
        f'<span>{L("Ticket #4821","Ticket #4821")} <span style="color:rgba(255,255,255,.55);font-weight:500"> · {L("Mesa 7","Table 7")} · $285</span></span></div></div>')
    # 4 · chips for the fast cuts
    chips = [('utensils', L('PLATILLO', 'DISH'), 'Chicken Bowl · $185'),
             ('book', L('RECETA', 'RECIPE'), L('180 g pollo · 60 g aguacate', '180 g chicken · 60 g avocado')),
             ('carrot', L('INGREDIENTES', 'INGREDIENTS'), L('Aguacate $48 → $59/kg', 'Avocado $48 → $59/kg')),
             ('package', L('INVENTARIO', 'INVENTORY'), L('Aguacate · se agota en ~2 h', 'Avocado · runs out in ~2 h')),
             ('dollar', L('COSTO', 'COST'), L('Food cost 25.3% → 29.8%', 'Food cost 25.3% → 29.8%')),
             ('percent', L('MARGEN', 'MARGIN'), L('Objetivo 72%', 'Target 72%')),
             ('user', L('MESERO', 'SERVER'), L('Omar · ticket promedio $412', 'Omar · avg. ticket $412')),
             ('clock', L('TURNO', 'SHIFT'), L('Vespertino · 14:00 – 22:00', 'Evening · 2 PM – 10 PM'))]
    for k, (icn, lab, val) in enumerate(chips):
        add(f'chip{k}', f'<div class="card" style="left:110px;top:806px;padding:24px 36px 24px 24px;display:flex;align-items:center;gap:20px">'
            f'<div class="ic" style="width:64px;height:64px;border-radius:18px">{svg(icn, size=32)}</div>'
            f'<div><div class="lab">{lab}</div><div style="font-size:36px;font-weight:600;margin-top:6px;letter-spacing:-.3px">{val}</div></div></div>')
    # 5 · one system: module pills (each its own layer, row under the tile)
    mods = [('monitor', L('Punto de venta', 'Point of sale')), ('flame', L('Cocina', 'Kitchen')), ('wallet', L('Caja', 'Cash')),
            ('package', L('Inventario', 'Inventory')), ('users', L('Personal', 'Staff'))]
    widths = [300, 210, 180, 250, 230] if es else [290, 210, 170, 250, 200]
    gap = 22; x = (1920 - (sum(widths) + gap * 4)) // 2
    for k, ((icn, name), w) in enumerate(zip(mods, widths)):
        add(f'mod{k}', f'<div class="card" style="left:{x}px;top:790px;width:{w}px;height:86px;padding:0 0 0 20px;border-radius:43px;display:flex;align-items:center;gap:14px">'
            f'<div class="ic" style="width:48px;height:48px;border-radius:24px">{svg(icn, size=24)}</div><span style="font-size:26px;font-weight:600">{name}</span></div>')
        x += w + gap
    add('sys_tile', f'<div class="card" style="left:810px;top:250px;width:300px;height:300px;border-radius:70px;background:#0b0b0c;border-color:rgba(16,185,129,.45);'
        f'box-shadow:0 40px 120px rgba(0,0,0,.6),0 0 0 1px rgba(16,185,129,.2),0 0 80px rgba(16,185,129,.18)">'
        f'<div style="position:absolute;left:62px;top:116px;width:176px;height:52px;background:#fff;-webkit-mask:url(data:image/png;base64,{WMARK}) left center/contain no-repeat"></div>'
        f'<div style="position:absolute;left:230px;top:153px;width:9px;height:9px;background:#10b981"></div></div>')
    add('sys_cap', f'<div class="nomask" style="position:absolute;top:600px;width:1920px;text-align:center;font-family:\'Inter Display\';font-weight:700;font-size:58px;letter-spacing:-1.2px;text-shadow:0 6px 40px rgba(0,0,0,.6)">{L("Un solo sistema.","One system.")}</div>'
        '<div class="card" style="left:-9999px;top:0;width:1px;height:1px"></div>')
    # 6 · AI watching during the shift
    checks = [(L('Ventas', 'Sales'), '✓', 'g'), (L('Inventario', 'Inventory'), '✓', 'g'), (L('Excepciones', 'Exceptions'), L('1 por revisar', '1 to review'), 'a')]
    add('live', f'<div class="card" style="{R}"><div class="hd">{fm()}<span style="color:#fff;font-weight:600">Fullsite {L("IA","AI")}</span><div class="live"><i></i>{L("EN VIVO","LIVE")}</div></div>'
        f'<div class="big">1,284</div><div class="sub" style="margin-bottom:16px">{L("movimientos revisados en este turno","transactions checked this shift")}</div>'
        + ''.join(f'<div class="row"><span>{a}</span><b class="{c}">{b}</b></div>' for a, b, c in checks) + '</div>')
    # 7 · exception detected
    add('alert', f'<div class="card" style="{R}"><div class="hd">{ic("alert","red","#fca5a5")}<span style="color:#fff;font-weight:600">{L("Excepción detectada","Exception detected")}</span><span style="margin-left:auto;font-size:20px;color:rgba(255,255,255,.5)">15:42</span></div>'
        f'<div class="big r">$1,240</div><div class="sub" style="color:rgba(255,255,255,.85);font-size:25px;margin-top:16px">{L("3 cancelaciones · Brayan B. · última hora","3 voids · Brayan B. · last hour")}</div>'
        f'<div class="sub">{L("Patrón inusual vs. su promedio histórico","Unusual vs. his historical average")}</div></div>')
    add('alert2', f'<div class="card" style="left:1180px;top:520px;width:600px;padding:22px 30px"><div class="hd">{ic("trend","amb","#fcd34d")}<span>{L("Merma · aguacate","Waste · avocado")}</span><b class="a" style="margin-left:auto;font-size:30px">+22%</b></div></div>')
    # 8 · phone notification (light, iOS-like)
    add('notif', f'<div class="card light" style="left:450px;top:110px;width:1020px;border-radius:40px;padding:28px 34px;display:flex;gap:24px">'
        f'<div style="width:84px;height:84px;flex:none;border-radius:20px;background:#0b0b0c;position:relative"><i style="position:absolute;left:23px;top:16px;width:38px;height:50px;background:#fff;-webkit-mask:url(data:image/png;base64,{FMARK}) center/contain no-repeat"></i><b style="position:absolute;left:52px;top:56px;width:12px;height:12px;background:#10b981"></b></div>'
        f'<div style="flex:1"><div style="display:flex;font-size:25px;font-weight:700">Fullsite<span style="margin-left:auto;font-weight:500;color:#888;font-size:22px">{L("ahora","now")}</span></div>'
        f'<div style="font-size:27px;font-weight:600;margin-top:6px">{L("Cancelaciones fuera de patrón","Out-of-pattern voids")}</div>'
        f'<div style="font-size:25px;color:#333;margin-top:4px;line-height:1.35">{L("Brayan B. lleva 3 en la última hora ($1,240). Revísalo con el supervisor.","Brayan B. has 3 in the last hour ($1,240). Check with the supervisor.")}</div></div></div>')
    # 9 · close prediction with a chart (actual to 2 PM, projected band after)
    pts = [(0, 150), (40, 140), (80, 128), (120, 120), (160, 100), (200, 92), (240, 70)]
    path = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    chart = (f'<svg width="532" height="170" viewBox="0 0 532 170" style="margin-top:22px;overflow:visible">'
             f'<defs><linearGradient id="gf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#10b981" stop-opacity=".35"/><stop offset="1" stop-color="#10b981" stop-opacity="0"/></linearGradient></defs>'
             f'<path d="{path} L240,170 L0,170 Z" fill="url(#gf)"/>'
             f'<path d="M240,70 L532,6 L532,40 Z" fill="rgba(52,211,153,.18)"/>'
             f'<path d="M240,70 L532,22" stroke="#34d399" stroke-width="3" stroke-dasharray="8 8" fill="none"/>'
             f'<path d="{path}" stroke="#34d399" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<line x1="240" x2="240" y1="0" y2="170" stroke="rgba(255,255,255,.25)" stroke-dasharray="3 6"/>'
             f'<circle cx="240" cy="70" r="8" fill="#0b0b0c" stroke="#34d399" stroke-width="4"/>'
             f'<text x="252" y="164" fill="rgba(255,255,255,.55)" font-size="18" font-family="Inter">{L("14:00","2 PM")}</text></svg>')
    add('pred', f'<div class="card" style="{R}"><div class="hd">{ic("trend")}{L("Proyección al cierre","Projected close")}</div>'
        f'<div class="big" style="font-size:58px">$71,200 – $76,800</div><div class="sub">{L("Ventas a las 14:00: $38,400 · ","Sales at 2 PM: $38,400 · ")}<span class="g">+12% {L("vs. martes","vs. Tuesday")}</span></div>{chart}</div>')
    # 10 · recommendation → approve
    def rec(done):
        rows = [(L('Qué pasó', 'What happened'), L('Pollo +18% · $157 → $185/kg', 'Chicken +18% · $157 → $185/kg'), ''),
                (L('Impacto', 'Impact'), L('−$4,200 / semana en margen', '−$4,200 / week in margin'), 'r'),
                (L('Acción', 'Action'), 'Chicken Bowl $185 → $215', 'g')]
        b = (f'<div class="btn on">{svg("check", "#06110c", 26, 3)}{L("Aprobado · ejecutando","Approved · executing")}</div>' if done else
             f'<div class="btn">{svg("check", "#34d399", 26, 3)}{L("Aprobar ajuste","Approve change")}</div>')
        return (f'<div class="card" style="left:1080px;top:110px;width:700px"><div class="hd" style="margin-bottom:12px">{fm()}<span style="color:#fff;font-weight:600">{L("Recomendación","Recommendation")}</span></div>'
                + ''.join(f'<div class="row" style="font-size:24px"><span style="color:rgba(255,255,255,.55)">{a}</span><b class="{c}">{v}</b></div>' for a, v, c in rows) + b + '</div>')
    add('rec', rec(False)); add('rec_ok', rec(True))
    # 11 · ask
    add('ask_q', f'<div class="card" style="left:auto;right:140px;top:150px;padding:22px 34px;border-radius:34px 34px 10px 34px;background:linear-gradient(180deg,rgba(16,185,129,.92),rgba(5,150,105,.92));border-color:rgba(255,255,255,.25)">'
        f'<span style="font-size:32px;font-weight:600">{L("¿Cómo vamos hoy?","How are we doing today?")}</span></div>')
    add('ask_a', f'<div class="card" style="left:1020px;top:290px;width:760px;border-radius:34px 34px 34px 10px"><div class="hd" style="margin-bottom:14px">{fm()}<span style="color:#fff;font-weight:600">Fullsite</span></div>'
        f'<div style="font-size:28px;line-height:1.45;color:rgba(255,255,255,.92)">{L("Ventas 14:30: <b>$38,400</b> <span class=g>(+12% vs. martes)</span>.<br>Proyección al cierre: <b>$71,200 – $76,800</b>.","Sales at 2:30 PM: <b>$38,400</b> <span class=g>(+12% vs. Tuesday)</span>.<br>Projected close: <b>$71,200 – $76,800</b>.")}</div></div>')
    # 12 · offline → restored
    add('off', f'<div class="card" style="{R}"><div class="hd">{ic("wifioff","amb","#fcd34d")}<span style="color:#fff;font-weight:600">{L("Sin conexión","Offline")}</span><div class="live" style="color:#fcd34d"><i style="background:#fcd34d;box-shadow:0 0 0 6px rgba(252,211,77,.18)"></i>{L("LOCAL","LOCAL")}</div></div>'
        f'<div class="big">18</div><div class="sub">{L("órdenes en cola local · cocina e impresión OK","orders queued locally · kitchen & printing OK")}</div></div>')
    add('on', f'<div class="card" style="left:1180px;top:430px;width:600px"><div class="hd">{ic("wifi")}<span style="color:#fff;font-weight:600">{L("Restaurado","Back online")}</span></div>'
        f'<div class="big g">18/18</div><div class="sub">{L("órdenes sincronizadas · 0 pérdidas","orders synced · 0 lost")}</div></div>')
    return C


if __name__ == '__main__':
    import json, sys
    json.dump(build(sys.argv[1]), open(sys.argv[2], 'w'))
