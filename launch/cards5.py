"""Cards for film v5 (manifesto): giant kinetic type + 'Fullsite understands' insight cards.
Reuses the design system from cards4."""
import cards4
from cards4 import page, fm, ic, svg

TYPE_CSS = """
.ty{position:absolute;left:0;width:1920px;text-align:center;font-family:'Inter Display';font-weight:700;color:#fff;
  letter-spacing:-4px;line-height:1.02;text-shadow:0 10px 60px rgba(0,0,0,.55)}
.ty .g{color:#34d399}
.ins .q{font-size:24px;color:rgba(255,255,255,.62);margin-top:18px}
.ins .ans{font-size:38px;font-weight:600;line-height:1.22;letter-spacing:-.6px;margin-top:10px}
.ins .chips{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
.ins .chip{font-size:21px;font-weight:600;padding:9px 16px;border-radius:20px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);color:rgba(255,255,255,.85)}
.ins .chip.r{color:#fca5a5;border-color:rgba(252,165,165,.35);background:rgba(248,113,113,.10)}
.ins .chip.g{color:#6ee7b7;border-color:rgba(52,211,153,.35);background:rgba(16,185,129,.10)}
"""


def tpage(body):
    return page(f'<style>{TYPE_CSS}</style>' + body)


def build(lang):
    es = lang == 'es'
    L = lambda a, b: a if es else b
    base = {c['name']: c for c in cards4.build(lang)}
    C = [base[k] for k in ('pred', 'rec', 'rec_ok', 'pos_sales')]
    add = lambda name, body: C.append({'name': name, 'html': tpage(body)})

    # giant type (no glass): size, vertical position
    types = {
        'ty_rec': (L('Registramos todo.', 'We record everything.'), 132, 440),
        'ty_nada': (L('No entendemos nada.', 'We understand nothing.'), 132, 440),
        'ty_hoy': (L('Hasta hoy.', 'Until now.'), 150, 450),
        'ty_noreg': (L('Fullsite no registra<br>tu restaurante.', 'Fullsite doesn\'t record<br>your restaurant.'), 104, 380),
        'ty_ent': (L('Lo <span class=g>entiende.</span>', 'It <span class=g>understands</span> it.'), 140, 690),
        'ty_num': (L('No más números.', 'No more numbers.'), 132, 440),
        'ty_resp': (L('<span class=g>Respuestas.</span>', '<span class=g>Answers.</span>'), 150, 440),
    }
    for name, (txt, size, top) in types.items():
        add(name, f'<div class="ty" style="top:{top}px;font-size:{size}px">{txt}</div>')

    # "Fullsite understands" insight cards: question → answer → evidence
    def ins(name, icon, cls, color, q, a, chips):
        ch = ''.join(f'<span class="chip {c}">{t}</span>' for t, c in chips)
        add(name, f'<div class="card ins" style="left:1100px;top:120px;width:700px"><div class="hd">{fm()}<span style="color:#fff;font-weight:600">Fullsite</span>'
            f'<div class="live">{L("ENTIENDE","UNDERSTANDS")}</div></div>'
            f'<div class="q">{q}</div><div class="ans">{a}</div><div class="chips">{ch}</div></div>')
    ins('q_martes', 'trend', '', '', L('¿Por qué el martes vendiste menos?', 'Why was Tuesday slow?'),
        L('Llovió y la terraza no abrió: 8 mesas sin activar.', 'It rained and the terrace stayed closed: 8 tables never seated.'),
        [(L('−14% vs. martes promedio', '−14% vs. avg. Tuesday'), 'r'), (L('Clima', 'Weather'), ''), (L('Mesas', 'Tables'), '')])
    ins('q_plat', '', '', '', L('¿Qué platillo se vende mucho y deja poco?', 'Which dish sells a lot and earns little?'),
        L('Guacamole: #2 en ventas, pero el aguacate subió 22%.', 'Guacamole: #2 in sales, but avocado is up 22%.'),
        [('Food cost 31% → 38%', 'r'), (L('Receta', 'Recipe'), ''), (L('Compras', 'Purchasing'), '')])
    ins('q_prov', '', '', '', L('¿Qué proveedor te subió el precio?', 'Which supplier raised your prices?'),
        L('Pollo: de $157 a $185/kg esta semana.', 'Chicken: from $157 to $185/kg this week.'),
        [('+18%', 'r'), (L('3 alzas en 6 meses', '3 increases in 6 months'), ''), (L('Proveedor', 'Supplier'), '')])
    ins('q_cancel', '', '', '', L('¿Quién cancela de más?', 'Who voids too much?'),
        L('Brayan B.: 3 cancelaciones en una hora ($1,240).', 'Brayan B.: 3 voids in one hour ($1,240).'),
        [(L('Fuera de su patrón', 'Out of his pattern'), 'r'), (L('Turno vespertino', 'Evening shift'), ''), (L('Mesero', 'Server'), '')])
    ins('q_falta', '', '', '', L('¿Qué va a faltar?', 'What will you run out of?'),
        L('Aguacate: se agota en ~2 horas.', 'Avocado: runs out in ~2 hours.'),
        [(L('Pide antes de las 17:00', 'Order before 5 PM'), 'g'), (L('Inventario teórico', 'Theoretical inventory'), ''), (L('Receta', 'Recipe'), '')])
    add('why', f'<div class="card ins" style="left:1060px;top:200px;width:740px;border-radius:34px 34px 34px 10px"><div class="hd">{fm()}<span style="color:#fff;font-weight:600">Fullsite</span>'
        f'<div class="live">{L("POR QUÉ","WHY")}</div></div>'
        f'<div class="ans" style="font-size:33px;margin-top:20px">{L("Vas <span class=g>12% arriba</span>: la terraza llenó 8 mesas más.", "You\'re <span class=g>up 12%</span>: the terrace filled 8 more tables.")}</div>'
        f'<div class="ans" style="font-size:33px;margin-top:14px">{L("Bebidas va <span class=r>18% abajo</span>: activa la promo de 6 a 8.", "Drinks are <span class=r>down 18%</span>: run the 6–8 PM promo.")}</div></div>')
    return C


if __name__ == '__main__':
    import json, sys
    json.dump(build(sys.argv[1]), open(sys.argv[2], 'w'))
