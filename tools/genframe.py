#!/usr/bin/env python3
"""
Generátor zdobného (barokního) rámu jako SVG pro CSS border-image.

Dvě vrstvy, každá jinou technikou — protože každá řeší něco jiného:
  1) PROFIL LIŠTY: čtyři lichoběžníky s pokosem, každý s vlastním gradientem
     napříč profilem. Gradient drží tvar lišty (oblounek → výžlabek → plocha
     → perlovec → polodrážka) a správné nasvícení zleva shora.
  2) ŘEZBA: ornamenty jako ploché siluety, které teprve SVG filtr
     (rozostřená alfa → feSpecularLighting) změní v reliéf. Filtr běží jen
     na ornamentech, ne na podkladu — jinak by vymyl kov do běla.
"""
import math, os

OUT = "/Users/misak/Projects/lenka-graf-demo/assets/frames"
SIZE = 600
B = 168                 # rámová zóna = border-image slice
RAIL = SIZE - 2 * B     # délka opakovaného pásu

METALS = {
    "gold": dict(
        # profil lišty zvenku dovnitř
        prof=[(0.00, "#241905"), (0.06, "#6d5220"), (0.13, "#b8934a"), (0.18, "#e8d29c"),
              (0.26, "#a8813a"), (0.40, "#c9a75f"), (0.50, "#eadaa8"), (0.60, "#bd9950"),
              (0.72, "#7d5c22"), (0.83, "#b5924a"), (0.92, "#dcc794"), (1.00, "#2b1e07")],
        orn="#c4a05a", ornHi="#eddfb4", ornLo="#5c421414",
        spec="#fff4d8", diff="#d8bd82", dark="#1a1204",
    ),
    "silver": dict(
        prof=[(0.00, "#14171b"), (0.06, "#4e565f"), (0.13, "#a9b2bd"), (0.18, "#f0f5fa"),
              (0.26, "#7e868f"), (0.40, "#bcc4ce"), (0.50, "#f7fafd"), (0.60, "#aab3bd"),
              (0.72, "#565e67"), (0.83, "#a4adb7"), (0.92, "#e4eaf1"), (1.00, "#181c21")],
        orn="#b9c2cc", ornHi="#f4f8fc", ornLo="#3a424b14",
        spec="#ffffff", diff="#dde4ec", dark="#0f1216",
    ),
}


# ───────────────────────────── ornamentální prvky ─────────────────────────────

def pts(seq):
    return " L ".join(f"{x:.2f},{y:.2f}" for x, y in seq)


def volute(cx, cy, r0, r1, a0, a1, w0, w1, steps=52):
    """C-voluta: spirálový pás s proměnnou šířkou."""
    o, i = [], []
    for k in range(steps + 1):
        t = k / steps
        a = math.radians(a0 + (a1 - a0) * t)
        r = r0 + (r1 - r0) * (t ** 1.3)
        w = (w0 + (w1 - w0) * t) / 2
        ca, sa = math.cos(a), math.sin(a)
        o.append((cx + ca * (r + w), cy + sa * (r + w)))
        i.append((cx + ca * (r - w), cy + sa * (r - w)))
    return f"M {pts(o)} L {pts(list(reversed(i)))} Z"


def acanthus(x, y, ang, length, width, curl=30, lobes=4, flip=1):
    """
    Akantový list: podél osy se stáčí (curl), po vnější hraně má laloky,
    špička se zatáčí. Vnitřní hrana je hladká, aby list „ležel" na liště.
    """
    outer, inner = [], []
    n = lobes * 8
    for k in range(n + 1):
        t = k / n
        # osa listu se postupně stáčí
        a = math.radians(ang + curl * (t ** 1.6))
        # poloha na ose
        seg = length * t
        px = x + math.cos(a) * seg
        py = y + math.sin(a) * seg
        nx, ny = -math.sin(a) * flip, math.cos(a) * flip
        # obálka: rychle naroste, ke špičce se ztenčí
        env = math.sin(math.pi * min(1.0, t * 1.04)) ** 0.62
        # laloky po vnější hraně
        lob = 1 + 0.42 * math.sin(t * lobes * 2 * math.pi - 1.1) * (1 - t * 0.35)
        outer.append((px + nx * width * 0.5 * env * lob, py + ny * width * 0.5 * env * lob))
        inner.append((px - nx * width * 0.22 * env, py - ny * width * 0.22 * env))
    return f"M {pts(outer)} L {pts(list(reversed(inner)))} Z"


def palmette(cx, cy, r, ang=0, rays=7):
    """Vějíř / mušle — plní roh a středové kartuše."""
    parts = [f'<path d="M {cx-r:.2f},{cy:.2f} A {r:.2f} {r:.2f} 0 0 1 {cx+r:.2f},{cy:.2f} Z" '
             f'transform="rotate({ang} {cx} {cy})"/>']
    for i in range(rays):
        a = math.radians(-180 + (i + 0.5) * 180 / rays)
        x1, y1 = cx + math.cos(a) * r * 0.22, cy + math.sin(a) * r * 0.22
        x2, y2 = cx + math.cos(a) * r * 0.94, cy + math.sin(a) * r * 0.94
        parts.append(f'<path d="M {x1:.2f},{y1:.2f} L {x2:.2f},{y2:.2f}" stroke-width="{r*0.16:.2f}" '
                     f'stroke-linecap="round" transform="rotate({ang} {cx} {cy})"/>')
    return "".join(parts)


def rosette(cx, cy, r, petals=8):
    p = [f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r*0.3:.2f}"/>']
    for i in range(petals):
        a = 2 * math.pi * i / petals
        px, py = cx + math.cos(a) * r * 0.6, cy + math.sin(a) * r * 0.6
        p.append(f'<ellipse cx="{px:.2f}" cy="{py:.2f}" rx="{r*0.33:.2f}" ry="{r*0.19:.2f}" '
                 f'transform="rotate({math.degrees(a):.1f} {px:.2f} {py:.2f})"/>')
    return "".join(p)


# ───────────────────────── běhy podél lišty (vodorovně) ─────────────────────────

def bead_reel(x0, y, length, unit, r):
    """Perlovec: kulička – váleček – kulička."""
    out = []
    n = max(2, round(length / unit))
    s = length / n
    for i in range(n):
        cx = x0 + s * (i + 0.5)
        out.append(f'<circle cx="{cx:.2f}" cy="{y:.2f}" r="{r:.2f}"/>')
        out.append(f'<ellipse cx="{cx + s/2:.2f}" cy="{y:.2f}" rx="{r*0.34:.2f}" ry="{r*1.1:.2f}"/>')
    return "".join(out)


def egg_dart(x0, y, length, unit, h):
    """Vejcovec se šipkami."""
    out = []
    n = max(2, round(length / unit))
    s = length / n
    for i in range(n):
        cx = x0 + s * (i + 0.5)
        # objímka
        out.append(f'<path d="M {cx-s*0.40:.2f},{y-h*0.52:.2f} Q {cx:.2f},{y+h*0.80:.2f} '
                   f'{cx+s*0.40:.2f},{y-h*0.52:.2f} L {cx+s*0.30:.2f},{y-h*0.52:.2f} '
                   f'Q {cx:.2f},{y+h*0.55:.2f} {cx-s*0.30:.2f},{y-h*0.52:.2f} Z"/>')
        # vejce
        out.append(f'<ellipse cx="{cx:.2f}" cy="{y-h*0.04:.2f}" rx="{s*0.255:.2f}" ry="{h*0.46:.2f}"/>')
        # šipka mezi vejci
        dx = cx + s / 2
        out.append(f'<path d="M {dx:.2f},{y-h*0.54:.2f} L {dx+s*0.075:.2f},{y+h*0.10:.2f} '
                   f'L {dx:.2f},{y+h*0.52:.2f} L {dx-s*0.075:.2f},{y+h*0.10:.2f} Z"/>')
    return "".join(out)


def gadroon(x0, y, length, unit, h):
    """Prýtovec — šikmé lalokované klínky, typické pro vnější výžlabek."""
    out = []
    n = max(2, round(length / unit))
    s = length / n
    for i in range(n):
        cx = x0 + s * (i + 0.5)
        out.append(f'<path d="M {cx-s*0.46:.2f},{y+h*0.5:.2f} '
                   f'C {cx-s*0.46:.2f},{y-h*0.72:.2f} {cx+s*0.46:.2f},{y-h*0.72:.2f} '
                   f'{cx+s*0.46:.2f},{y+h*0.5:.2f} Z"/>')
    return "".join(out)


def rinceau(x0, y, length, unit):
    """Vlnovka s akantovými lístky — hlavní běh v širokém výžlabku."""
    out = []
    n = max(2, round(length / unit))
    s = length / n
    for i in range(n):
        cx = x0 + s * i
        up = (i % 2 == 0)
        out.append(f'<path d="{volute(cx + s*0.5, y, s*0.30, s*0.07, 180 if up else 0, (180 if up else 0) + (300 if up else -300), 9, 3)}"/>')
        out.append(f'<path d="{acanthus(cx + s*0.5, y, -30 if up else 30, s*0.46, 15, curl=48 if up else -48, lobes=2, flip=1 if up else -1)}"/>')
    return "".join(out)


# ───────────────────────────── nároží ─────────────────────────────

def corner():
    """
    Nárožní kartuše pro levý horní roh (ostatní vzniknou rotací celého rámu).

    Kreslí se jen polovina nad úhlopříčkou a ta se zrcadlí maticí (0 1 1 0),
    tj. překlopením přes osu y=x. Bez té symetrie čte shluk voluty a akantu
    jako zvířecí hlava — symetrie z toho udělá rozvilinu.
    """
    half = []
    # velký akant stékající do vodorovné lišty
    half.append(f'<path d="{acanthus(70, 34, 6, 98, 42, curl=24, lobes=4, flip=1)}"/>')
    # voluta, kterou akant vyrůstá
    half.append(f'<path d="{volute(96, 62, 34, 11, 195, 425, 17, 6)}"/>')
    # protivoluta na přechodu kartuše do lišty
    half.append(f'<path d="{volute(152, 56, 25, 8, 150, 395, 12, 4)}"/>')
    # menší akant vyplňující plochu blíž k obrazu
    half.append(f'<path d="{acanthus(104, 118, 22, 54, 24, curl=26, lobes=3, flip=1)}"/>')
    half.append(rosette(150, 104, 10))
    h = "".join(half)

    g = [h, f'<g transform="matrix(0 1 1 0 0 0)">{h}</g>']
    # prvky ležící přímo na úhlopříčce (samy o sobě symetrické)
    g.append(palmette(42, 42, 33, ang=45, rays=9))
    g.append(rosette(42, 42, 12))
    g.append(f'<path d="{acanthus(96, 96, 45, 46, 26, curl=0, lobes=2, flip=1)}"/>')
    g.append(f'<path d="{acanthus(96, 96, 45, 46, 26, curl=0, lobes=2, flip=-1)}"/>')
    g.append(rosette(126, 126, 12))
    return "".join(g)


def crest(w, h):
    """Středová kartuše na lištu."""
    cx = w / 2
    g = []
    g.append(f'<path d="{volute(cx-34, 74, 24, 8, 175, 455, 14, 5)}"/>')
    g.append(f'<path d="{volute(cx+34, 74, 24, 8, 5, -275, 14, 5)}"/>')
    g.append(palmette(cx, 82, 42, ang=0, rays=11))
    g.append(f'<path d="{acanthus(cx-14, 96, 108, 44, 22, curl=-30, lobes=2, flip=-1)}"/>')
    g.append(f'<path d="{acanthus(cx+14, 96, 72, 44, 22, curl=30, lobes=2, flip=1)}"/>')
    g.append(rosette(cx, 34, 17))
    return "".join(g)


def rail():
    """Opakovaný pás mezi nárožími (kreslí se pro horní lištu)."""
    g = []
    g.append(f'<g>{gadroon(B, 26, RAIL, 40, 30)}</g>')          # vnější výžlabek
    g.append(f'<g>{rinceau(B, 82, RAIL, 93)}</g>')              # hlavní běh rozvilin
    g.append(f'<g>{egg_dart(B, 130, RAIL, 56, 27)}</g>')        # vejcovec u polodrážky
    g.append(f'<g>{bead_reel(B, 158, RAIL, 20, 5.0)}</g>')      # perlovec na polodrážce
    return "".join(g)


# ───────────────────────── profil lišty (podklad) ─────────────────────────

def plates(m):
    """Čtyři lichoběžníky s pokosem; gradient jde napříč profilem lišty."""
    S, b = SIZE, B
    quads = {
        "t": [(0, 0), (S, 0), (S - b, b), (b, b)],
        "b": [(b, S - b), (S - b, S - b), (S, S), (0, S)],
        "l": [(0, 0), (b, b), (b, S - b), (0, S)],
        "r": [(S - b, b), (S, 0), (S, S), (S - b, S - b)],
    }
    # nasvícení zleva shora
    bright = {"t": 1.06, "l": 0.97, "r": 0.80, "b": 0.70}
    out = []
    for k, q in quads.items():
        out.append(f'<path d="M {pts(q)} Z" fill="url(#prof-{k})" '
                   f'style="filter:brightness({bright[k]})"/>')
    return "".join(out)


def build(metal):
    m = METALS[metal]

    # gradienty profilu — pro každou stranu jiný směr (vnější hrana → vnitřní)
    dirs = {"t": (0, 0, 0, 1), "b": (0, 1, 0, 0), "l": (0, 0, 1, 0), "r": (1, 0, 0, 0)}
    grads = []
    for k, (x1, y1, x2, y2) in dirs.items():
        stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in m["prof"])
        grads.append(f'<linearGradient id="prof-{k}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{stops}</linearGradient>')

    ornaments = []
    for rot in (0, 90, 180, 270):
        t = f'rotate({rot} {SIZE/2} {SIZE/2})'
        ornaments.append(f'<g transform="{t}">{rail()}</g>')
        ornaments.append(f'<g transform="{t}">{corner()}</g>')
        ornaments.append(f'<g transform="{t} translate({B} 0)">{crest(RAIL, B)}</g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" width="{SIZE}" height="{SIZE}">
<defs>
  {''.join(grads)}
  <linearGradient id="ornFill" x1="0" y1="0" x2="0.6" y2="1">
    <stop offset="0" stop-color="{m['ornHi']}"/>
    <stop offset="0.5" stop-color="{m['orn']}"/>
    <stop offset="1" stop-color="{m['prof'][8][1]}"/>
  </linearGradient>

  <!-- řezba: rozostřená alfa slouží jako výšková mapa -->
  <filter id="carve" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="3.4" result="h"/>
    <feSpecularLighting in="h" surfaceScale="4.0" specularConstant="0.72"
                        specularExponent="28" lighting-color="{m['spec']}" result="sp">
      <feDistantLight azimuth="230" elevation="52"/>
    </feSpecularLighting>
    <feComposite in="sp" in2="SourceAlpha" operator="in" result="spc"/>
    <feDiffuseLighting in="h" surfaceScale="4.0" diffuseConstant="0.92"
                       lighting-color="{m['diff']}" result="df">
      <feDistantLight azimuth="230" elevation="52"/>
    </feDiffuseLighting>
    <feComposite in="df" in2="SourceAlpha" operator="in" result="dfc"/>
    <!-- vlastní barva ornamentu × difúzní světlo, pak přičíst odlesk -->
    <feBlend in="dfc" in2="SourceGraphic" mode="multiply" result="body"/>
    <feComposite in="spc" in2="body" operator="arithmetic" k1="0" k2="0.9" k3="1" k4="0" result="lit"/>
    <feDropShadow in="lit" dx="1.5" dy="2" stdDeviation="1.8"
                  flood-color="{m['dark']}" flood-opacity="0.55"/>
  </filter>
</defs>

<!-- 1) profil lišty -->
{plates(m)}

<!-- 2) řezba -->
<g fill="url(#ornFill)" stroke="url(#ornFill)" stroke-width="0" filter="url(#carve)">
  {''.join(ornaments)}
</g>
</svg>
'''


os.makedirs(OUT, exist_ok=True)
for metal in METALS:
    p = os.path.join(OUT, f"frame-{metal}.svg")
    open(p, "w", encoding="utf-8").write(build(metal))
    print(f"{p}  {os.path.getsize(p)/1024:.1f} kB")
