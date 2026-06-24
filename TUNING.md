# Tuning roadmap — Lenka Graf demo

Autonomní vylepšování (~2h loop). Záloha: `backups/index.backup-*.html` + git tag `pre-tuning-backup`.
**Pravidlo:** nerozbít schválený vzhled (světlý → tmavý Adele-style hero, jukebox, vstupenky). Jen vrstvit kvalitu.

## Batch 1 — Základ profesionality (SEO, a11y, perf, UX) ✅
- [x] SEO meta: OG/Twitter cards, canonical, theme-color, author, robots, og:locale
- [x] JSON-LD strukturovaná data (Person + MusicGroup + 2× MusicEvent + 3× MusicRecording)
- [x] Favicon (inline SVG monogram LG) + apple-touch-icon
- [x] Preconnect na lenkagraf.com (mp3/foto host)
- [x] Hero img: fetchpriority/decoding/async + onerror fallback (gradient)
- [x] A11y: aria-labels na icon buttons, role=slider na seekbaru, landmarky
- [x] :focus-visible zlatý outline
- [x] Anchor scroll-offset pod fixní nav (scroll-margin-top)
- [x] Scrollspy — aktivní odkaz v navigaci se zvýrazní
- [x] Jazyk se pamatuje (localStorage)
- [x] Reduced-motion: vypnout parallax/marquee/spin
- [x] Tenký zlatý scroll-progress proužek nahoře
- [x] Seekbar ovladatelný klávesnicí (šipky)

## Batch 2 — Mikrointerakce & detaily ✅
- [x] Nav: animované podtržení odkazů + objevení nav po načtení (navIn)
- [x] Hero: jemné mizení + posun obsahu při scrollu
- [x] Jukebox: plynulý 60fps fill (rAF), drag na seekbaru (pointer)
- [x] Klávesy 1/2/3 = výběr skladby, Esc = zavřít menu (prev/next/play přístupné nativně přes focus)
- [x] Tlačítka: press/active stavy
- [~] Sekční nadpisy reveal po slovech — vynecháno (data-reveal fade stačí, nešahat na vzhled)
- [~] Vstupenky 3D tilt — vynecháno (kolize se style-hover liftem; hover lift ponechán)

## Batch 3 — Self-hosting & vizuál ✅
- [x] Self-host assetů: portrét, 3× nahrávka, obal lokálně + optimalizace (mp3 160k, foto 1800px)
- [x] Nezávislost na cizím serveru (vč. odebrání preconnectu)
- [x] Preload LCP fotky (fetchpriority high)
- [x] Gradient fallback hero + onerror na <img>
- [~] Custom kurzor / lightbox klipu — vynecháno (drželo by to víc rušení než užitku pro demo)

## Batch 4 — Robustnost & QA ✅
- [x] QA v reálném headless prohlížeči (browse): 0 console chyb, 3 skladby OK
- [x] Cross-check screenshoty: mobil 390, tablet 768, desktop 1440 — hero/jukebox/klip/vstupenky OK
- [x] Mobil: hamburger funguje, vstupenky se skládají, jukebox full-width
- [x] Reveal = progressive enhancement (bez JS obsah viditelný)
- [x] Heading hierarchie h1→h2→h3, alt texty, lang přepínání
- [ ] (volitelné) self-host fontů, absolutní og:image po nasazení na doménu

## Batch 5 — Self-host fontů & funkční QA ✅
- [x] Self-host Google Fonts lokálně (assets/fonts/, 18 woff2, 368K) + přepojení @font-face
- [x] Odebrána závislost na fonts.googleapis/gstatic — 0 externích requestů (GDPR-friendly)
- [x] Re-QA: 0 console chyb, Playfair Display loaded lokálně, vzhled 1:1
- [x] Funkční QA: jukebox (přepnutí skladby + play + pill), přepnutí jazyka (EN, lang=en), mobilní menu — vše OK

## Batch 6-9 — Vizuální vlna (gradienty, animace, footer, loading) ✅
- [x] Loading animace (preloader: LG monogram + progress bar + failsafe + reduced-motion)
- [x] Ambientní struktura pozadí (3 driftující glow vrstvy, screen blend)
- [x] Radiální gradienty v sekcích (jukebox/klip/koncerty) — víc hloubky
- [x] Jukebox: halo glow kolem skříně + světelný sweep přes kupoli
- [x] Footer: zlatý divider, back-to-top tlačítko, hover na socials, marquee pauza na hover
- [x] Ken-burns na portrétu (jemné dýchání), shimmer na číslech sekcí (01/02/03)
- [x] Kurzorový glow (desktop), hover glow na zlatých CTA, focus glow na inputu
- [x] Newsletter: děkovný stav po odeslání (CS/EN)
- [x] Jemnější reveal (translateY + scale)
- [x] QA: 0 chyb, ověřeno mobil/desktop, vše cohezní

## Batch 11 — Cross-browser & finiš ✅
- [x] -webkit-backdrop-filter prefixy pro Safari (nav, badge, reel, klip, toTop, mobilní menu) — 7×
- [x] Fade-in bočních hero popisků (Soprán·Crossover, IG/YT/SP)
- [x] Tablet (1024) ověřen — dvousloupcový jukebox s halem OK
- [~] 3D tilt vstupenek / volume / lightbox — VYNECHÁNO (riziko kolize se schváleným chováním, nejde spolehlivě QA screenshotem)

## Log
- 2026-06-24 15:50 — záloha + roadmapa
- 2026-06-24 15:53 — Batch 1 (SEO, a11y, scrollspy, progress, perzistence)
- 2026-06-24 15:56 — Batch 2 (plynulý progress, drag seek, klávesy, hero fade)
- 2026-06-24 15:59 — Batch 3 (self-hosting assetů)
- 2026-06-24 16:03 — Batch 4 (QA screenshoty, 0 chyb) + preload LCP
- 2026-06-24 16:35 — Batch 5 (self-host fontů, funkční QA) — roadmapa vyčerpána, loop ukončen
