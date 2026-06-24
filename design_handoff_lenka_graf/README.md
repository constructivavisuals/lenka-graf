# Handoff: Lenka Graf — single-page demo web

## Overview
Single-page demo (one-page marketing/landing) pro sopranistku Lenku Graf — crossover umělkyni (klasika × moderna) a filantropku (NF Energie pomáhá). Cíl: prémiový, filmový, tmavý web v „operní eleganci". Sekce v pořadí: HERO → HUDBA (jukebox + medailonek) → FEATURED KLIP → KONCERTY (vstupenky) → NADACE → NEWSLETTER/FOOTER. Obsah dvojjazyčný (CS výchozí, EN přepínač — pouze vizuální přepnutí textů).

## About the Design Files
Soubory v tomto balíčku (`Lenka Graf.dc.html`) jsou **design reference vytvořené v HTML** — prototyp ukazující zamýšlený vzhled a chování, **ne produkční kód k přímému zkopírování**. Úkol je **znovu vytvořit tento design v cílovém prostředí** (klient plánuje **Next.js / React**) s použitím jeho zavedených vzorů, komponent a knihoven. HTML neposílat do produkce 1:1 — slouží jako přesná vizuální a behaviorální specifikace.

Pozn. k formátu: `.dc.html` je „Design Component" — celé tělo je mezi `<x-dc>…</x-dc>`, logika je v `<script data-dc-script>` jako třída `Component extends DCLogic` (React-like: `state`, `renderVals()`, lifecycle). Styly jsou **inline**. Pro implementaci ignorujte runtime `DCLogic`/`support.js` — přepište do běžných React komponent + CSS/Tailwind/styled.

## Fidelity
**High-fidelity (hifi).** Finální barvy, typografie, spacing, animace i interakce. Rekonstruujte UI pixel-perfect pomocí knihoven v cílovém codebase. Jediná výjimka: ilustrační „placeholdery" nejsou — vše je hotový vizuál.

---

## Design Tokens

### Barvy
| Token | Hex | Použití |
|---|---|---|
| bg-base | `#0a0908` | hlavní pozadí |
| bg-panel-1 | `#0d0a08` | sekce (gradient spodek) |
| bg-panel-2 | `#100c08` / `#16110c` | karty, lístky |
| bg-nadace | `#140b0d → #0d0809` | sekce nadace (vínový nádech) |
| text-primary | `#f5f1ea` | nadpisy |
| text-warm-white | `#ece7de` | běžný text na tmavé |
| text-body | `#b3ada2` / `#c6bfb4` | odstavce |
| text-muted | `#8a857c` | popisky |
| text-faint | `#6b665d` / `#5c574f` | mikro-popisky |
| gold | `#d8b97a` | primární kovový akcent |
| gold-light | `#f0dcae` | světlé zlato (světla, neony) |
| gold-deep | `#9a7c4a` | tmavé zlato (mono labels) |
| burgundy | `#7e2a38` / `#150,46,63` (`#962e3f`) | sekundární akcent (vínová) |
| burgundy-light | `#c98a96` | vínový text (nadace, 2. lístek) |
| chrome | `#cfc6b8 / #8a8074 / #6f665b` | chromové plochy (gradient) |

Akcenty definované v oklch ladění; všechny akcenty drží stejnou chroma/lightness, mění se hue (zlatá ↔ vínová).

### Typografie
- **Display / nadpisy / citáty:** `Playfair Display` (Google Font), weight 500–700, často `italic`. Negative tracking u velkých (~ -0.01em). line-height 0.86–1.0 u XL.
- **Body:** `Hanken Grotesk` (Google Font), weight 300–600.
- **Mono / labels / kódy / čísla:** `Space Mono` (Google Font), letter-spacing 0.1–0.28em, `text-transform:uppercase` u labelů.
- Měřítka: hero name `clamp(58px,13vw,178px)`; section h2 `clamp(34px,5.5vw,64px)`; velký citát `clamp(26px,3.6vw,40px)`; body `clamp(16px,1.9vw,19px)`; mono labels 9–12px.

### Spacing & tvar
- Section vertical padding: `clamp(54–90px, 7–12vw, 92–160px)`, horizontal `6vw`.
- Max šířka obsahu: 1100–1200px, centered.
- Border-radius: karty/lístky 14px, tlačítka pill 40px, malé prvky 6–12px.
- Stíny: velké `0 30–70px 70–130px rgba(0,0,0,.5–.78)`; inset hairline `inset 0 0 0 1px rgba(216,185,122,.14–.2)`.
- Hairline dělič sekcí: `height:1px; background:linear-gradient(90deg,rgba(216,185,122,.45),transparent 60%)`.

### Animace (jemné, „operní klid")
- **Scroll reveal:** elementy `[data-reveal]` start `opacity:0; translateY(28px)`, na intersekci → `opacity:1; none`, `transition: 1s cubic-bezier(.2,.6,.2,1)`. IntersectionObserver threshold 0.1, rootMargin `0px 0px -7%`.
- **Hero parallax:** media wrapper `translateY(scrollY*0.16)`.
- **Equalizer bars (jukebox):** `@keyframes eq { 0%,100%{scaleY(.18)} 50%{scaleY(1)} }`, různé durations 0.7–1.4s, `animation-play-state` přepínané podle přehrávání.
- **Otáčející deska:** `@keyframes spin` 5s linear, play-state dle přehrávání.
- **Neon glow:** `@keyframes glowPulse` 3.6s opacity .55↔.9.
- **Marquee (footer wordmark):** `@keyframes marqueeMove` translateX 0→-50%, 28s linear.
- **Bulbs / ndot:** drobné pulzy 0.8–1.6s.
- Hover karet/lístků: `translateY(-4 až -5px)` + zesílení stínu/borderu, 0.35–0.4s.

---

## Screens / Views (jedna stránka, sekce shora dolů)

### 0. Nav (fixed)
- Fixed top, `padding:20px 6vw`, gradient pozadí `rgba(10,9,8,.8)→0`, `backdrop-filter:blur(3px)`, z-index 60.
- Vlevo wordmark „LENKA GRAF" (Playfair, letter-spacing .18em, uppercase, 19px).
- Vpravo: odkazy Hudba / Koncerty / Nadace (mono 12px, .2em, uppercase, `#b3ada2`), pak CS/EN přepínač (pill, border `#3a352d`, gold text).
- Když hraje hudba: malý „now playing" pill (3 pulzující proužky + název skladby).

### 1. HERO (`#hero`)
- `height:100vh; min-height:680px; overflow:hidden`.
- **Pozadí = portrét přes celou plochu** (`GRAF_DEFDEF-scaled.jpg`), `object-fit:cover; object-position:50% 22%`, grade `grayscale(.42) contrast(1.05) brightness(.74) sepia(.14)`. V parallax wrapperu (`top:-7%; height:114%`).
- Vrstvy overlay: teplý radial (champagne) vpravo nahoře; vertikální gradient (tmavý nahoře+dole); horizontální gradient zleva pro čitelnost textu; inset vignette `inset 0 0 240px rgba(0,0,0,.7)`.
- **Showreel:** druhý prvek `<video>` (b&w `lenka_graf-pozadi_video-bw.mp4`, muted loop, `opacity:0`), tlačítko „Přehrát ukázku" přepne `opacity:1` a `play()` → klid přejde v pohyb. Ikona/štítek se mění (▶ ↔ ❚❚, „Přehrát ukázku" ↔ „Zastavit ukázku").
- Nahoře tour teaser (mezi hairlines): „O2 Arena · 15.05.2026  ·  Žofín · 13.12.2026" (mono, `#b89b6a`).
- Vlevo svislý label „Soprán · Crossover" (writing-mode vertical, rotate 180); vpravo svislé socials IG/YT/SP s dělíčky.
- **Obsah dole vlevo (editorial):** badge „● Nový singl · Křídla snů" (pill, 3 pulzující proužky), pak obří jméno „Lenka Graf" (Playfair 500, `clamp(58px,13vw,178px)`, line-height .86), pod ním řádek: claim „Soprán mezi operou a současností" (Playfair italic) + showreel tlačítko.
- Vpravo dole scroll indikátor „Poslechnout ↓" (svislý, plave).

### 2. HUDBA / JUKEBOX (`#hudba`)
Sekce = **header + dvousloupcová kompozice** (flex wrap, gap `clamp(34px,5vw,72px)`, align center, justify center).
- Header: hairline + „01 — Jukebox" (mono index gold-deep + Playfair h2).
- Lead mono `music.sub`.
- **Levý sloupec (editorial text, BEZ fotky):** `flex:1 1 300px; max-width:480px`.
  - kicker „O ZPĚVAČCE" (mono, gold-deep).
  - velký citát (Playfair italic 500, `clamp(26px,3.6vw,40px)`): „Hudba je most mezi tím, co bylo, a tím, co teprve přijde." — vizuální těžiště sloupce.
  - hairline 64px gold.
  - bio odstavec (`about.body`).
  - „POSLECHNOUT TAKÉ" + 3 pill odkazy: Spotify / Apple Music / YouTube (border gold .3, hover gold .7 + text gold-light).
- **Pravý sloupec = JUKEBOX SKŘÍŇ** (`flex:0 0 auto`, `width:min(430px,100%)`, ústřední prvek). Stavba shora:
  1. **Skříň**: arch silueta `border-radius:210px 210px 20px 20px`, dřevěný gradient `#3a2616→#2a1a0d→#1c1208`, jemná „wood grain" (repeating-linear-gradient), velký stín.
  2. **Dvojité neonové trubice** (arch + boky): vnější šampaňská `border:5px rgba(240,220,170,.92)` (jen top/left/right, `border-radius:185px…0 0`), vnitřní vínová `border:3px rgba(150,46,63,.85)`; obě `glowPulse`, glow box-shadow.
  3. **Chromové boční spony** (left/right, gradient chrome + vínové proužky).
  4. **Prosklená kupole** (`height:118px`, `border-radius:150px…`), uvnitř barevné mdlé glowy (zelená/fialová/zlatá) a **otáčející se deska** (`84px`, repeating-radial vinyl, ve středu obal skladby nebo monogram „LG"), sklo reflex.
  5. **Chromový štítek** „Jukebox" (Playfair italic 700, kovový gradient, po stranách dvě LED tečky).
  6. **Jantarový displej**: `{code} · NOW PLAYING` + `{subtitle}` vpravo; název skladby (Playfair `clamp(17px,2.4vw,21px)`); **equalizer** (16 proužků, gold gradient, animace `eq`).
  7. **Selektor (3 klávesy)**: kód-chip „A-1/A-2/A-3" (mono bold; aktivní = plné zlato/tmavý text), název (Playfair 15px), trvání (mono). Aktivní řádek: gold bg .07 + border gold .45.
  8. **Chromová ovládací lišta**: ◀◀ / ▶(48px gold radiál) / ▶▶ + čas `{cur}` + progress „trubice" (gold gradient fill, kulatý úchyt) + `{dur}`. Klik na progress = seek.
  9. **Mřížka** (`height:96px`): diamantový vzor (dvě křížené repeating-linear-gradient gold .42) + radial vínový glow + **medailon** (zlatý disk, Playfair „LG").
  10. **Podstavec** (tmavý proužek).

**Datová logika jukeboxu (klíčové):** 3 skladby s reálnými MP3 (viz Assets). Stav: `current`, `playing`, `time`, `dur`, `durs{}`. Jeden `Audio()` element; `timeupdate`/`loadedmetadata`/`ended`→next. `selectTrack(i)` přepne src (zachová play), `prev/next` cyklicky, `togglePlay`, `seek` (zlomek z kliku × duration). Při hraní: spin desky + equalizer `animation-play-state:running`. Obal má jen „I Dare" (ostatní → monogram „LG").

### 3. FEATURED KLIP
- Header „02 — Featured klip".
- **Filmový přehrávač** `aspect-ratio:16/9`, radius 6px. Uvnitř `<video>` (b&w pozadí, muted loop, poster = portrét), grade grayscale; letterbox pruhy 7% nahoře/dole; vlevo nahoře „● REC · 04:12" (pulzující vínová tečka), vpravo „NEW WORLD · 4K"; uprostřed velké kruhové play (`toggleKlip`); dole popisová lišta: „MUSIC VIDEO" + „Křídla snů" (Playfair italic `clamp(26px,3.6vw,42px)`) + pill „Sledovat na YouTube ↗".
- **Kredity** (grid auto-fit): Na motivy — Dvořákova Novosvětská · Produkce — Michal Dvořák (Lucie) · Sólové violoncello — Jodok Vuille. (mono label gold-deep + Playfair 19px hodnota.)

### 4. KONCERTY (`#koncerty`)
- Header „03 — Nadcházející koncerty".
- **Dvě prémiové vstupenky** (flex column, gap 26px). Každý lístek = horizontální flex (wrap), radius 14px, gradient pozadí, inset gold hairline, hover lift -5px. Levý gold/vínový svislý proužek 5px. Jemný gilošový bezpečnostní vzor (repeating-radial-gradient).
  - **Hlavní část:** horní řádek kategorie (mono) + kulatá pečeť „LG"; pak blok: den v týdnu (mono) + obří datum (Playfair `clamp(54px,8vw,80px)`, gold-light) + měsíc/rok; svislý dělič; název venue (Playfair `clamp(26px,3.6vw,38px)`) + „Praha, CZ"; grid 4 polí: Host/Program · Začátek · Sekce · Místo (mono label + hodnota).
  - **Perforace:** svislá tečkovaná linka (`background:linear-gradient` 6px on/off) s vyseknutými kruhy nahoře/dole (barva pozadí sekce).
  - **Útržek (stub):** „ADMIT ONE" (mono), **QR kód** (bílý čtverec 62px, mřížka + 3 rohové „finder" čtverce), číslo lístku „No. 2026-0515", cena „od 890 Kč" (Playfair), CTA „Vstupenky" (zlaté tlačítko).
  - Lístek 1: O2 arena, 15.05.2026, host Štefan Margita, 19:30, Parter A, Ř.7/12, od 890 Kč. **Zlatý** akcent.
  - Lístek 2: Palác Žofín, 13.12.2026, Adventní árie, 19:00, Velký sál, Stůl 4, od 690 Kč. **Vínový** akcent.

### 5. NADACE (`#nadace`)
- Vínově laděná sekce (gradient `#140b0d→#0d0809`, vínový radial glow vpravo nahoře).
- Centrováno: kicker „NADAČNÍ FOND" (vínová), h2 „Energie pomáhá" (Playfair `clamp(38px,6.5vw,80px)`), mise (Playfair italic): „Podporujeme vzdělávání, zdravý životní styl a umělecké aktivity dětí v České republice."
- **3 pilíře** (grid auto-fit minmax 220px): 01 Vzdělávání · 02 Zdravý životní styl · 03 Umělecké aktivity (Playfair číslo gold + nadpis + popis). Karty hover lift -4px + zesvětlení.
- CTA pill „O nadaci" (zlaté tlačítko).

### 6. NEWSLETTER + FOOTER
- Centrováno: h3 „Zůstaňte v kontaktu" + podtitul + řádek e-mail input (pill) + „Odebírat" (zlaté).
- Spodní řádek: socials Instagram/Facebook/YouTube/Spotify/Apple Music (mono) + „© 2026 · Demo".
- **Obří wordmark marquee**: „Lenka Graf · Lenka Graf ·" (Playfair `clamp(70px,16vw,200px)`, barva `#15110d` = sotva nad pozadím), nekonečné posouvání, mask fade po stranách.

---

## Interactions & Behavior
- **CS/EN přepínač:** přepíná textContent všech `[data-i18n]` (a placeholder `[data-i18n-ph]`) podle slovníku. Výchozí CS je přímo v markupu (okamžitý paint), EN se aplikuje až po přepnutí. V Reactu: i18n slovník + stav jazyka, podmíněné texty.
- **Jukebox:** výběr skladby, play/pause, prev/next (cyklicky), seek klikem na progress, auto-next po `ended`. Vizuál reaguje (spin + equalizer).
- **Hero showreel:** přepnutí portrét → b&w video.
- **Featured klip:** play/pause videa.
- **Scroll reveal** na všech `[data-reveal]`; **parallax** hero média.
- **Hover:** karty/lístky lift; pill odkazy mění border+barvu.
- Responsivita bez media queries je řešená flex-wrap + `clamp()` + grid `auto-fit/minmax`. V cílovém kódu klidně použijte standardní breakpointy.

## State Management
- `lang: 'cs'|'en'`
- Jukebox: `current:int`, `playing:bool`, `time:number`, `dur:number`, `durs:{}` (cache délek), jeden Audio element.
- `reel:bool` (hero showreel), `klip:bool` (featured klip přehrávání).
- Refs: hero media wrapper (parallax), hero/klip video, jukebox deska, equalizer kontejner, obal aktuální skladby.

## Assets (reálná aktiva — použít stejná)
- Hero/portrét (jpg): `https://www.lenkagraf.com/wp-content/uploads/2026/02/GRAF_DEFDEF-scaled.jpg`
- B&W pozadí video (mp4): `https://www.lenkagraf.com/wp-content/uploads/2022/05/lenka_graf-pozadi_video-bw.mp4`
- MP3 — Křídla snů: `https://www.lenkagraf.com/wp-content/uploads/2026/02/KRIDLA-SNU-CZ-Jodok-RadioCut.mp3`
- MP3 — Everything Is Part Of One: `https://www.lenkagraf.com/wp-content/uploads/2024/03/L.Graf_Everything-SHORT-MASTER-FINAL_6-1.mp3`
- MP3 — I Dare: `https://www.lenkagraf.com/wp-content/uploads/2022/08/lenka_graf-i_dare.mp3`
- Obal I Dare (jpg): `https://www.lenkagraf.com/wp-content/uploads/2022/08/lenka-graf_cover_i-dare.jpg`
- Fonty: Google Fonts — Playfair Display, Hanken Grotesk, Space Mono.
- Pozn.: v demu byla média přímo linkovaná na lenkagraf.com; v produkci doporučeno hostovat lokálně / přes CDN a doplnit reálné obaly skladeb + skutečný music-video soubor pro Featured klip (teď používá b&w pozadí jako placeholder pohybu).

## Files
- `Lenka Graf.dc.html` — kompletní hi-fi design (markup inline-styled + logika ve třídě `Component`). Hlavní referenční soubor.
- (V projektu existuje i `Lenka Graf v1.dc.html` — starší jednodušší verze, není součástí handoffu.)

## Doporučení pro implementaci (Next.js/React)
- Rozbít na komponenty: `<Nav>`, `<Hero>`, `<MusicSection>` (`<EditorialIntro>` + `<Jukebox>`), `<FeaturedClip>`, `<Shows>` (`<Ticket>`), `<Foundation>`, `<Footer>`.
- Jukebox: jeden `useRef<HTMLAudioElement>` + stav; equalizer/spin přes CSS `animation-play-state` vázaný na `playing`.
- i18n: `next-intl` nebo jednoduchý slovník + context.
- Styly: Tailwind nebo CSS Modules; tokeny výše přenést do theme.
- Zachovat „jemné" animace (žádný pop/overload), tmavé pozadí + prostor + teplé zlato.
