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

## Batch 12 — Přechod na Jannon Sans ✅
- [x] Celý web převeden z Playfair Display / Space Mono / Hanken Grotesk na **Jannon Sans Light**
      (Storm Type Foundry, © František Štorm) — 105 deklarací sjednoceno do `var(--font)`
- [x] JannonSans-Light.otf → podmnožina latin + latin-ext (celá česká diakritika) → WOFF2, 32 kB
      (dřív 18 souborů Google fontů, ~350 kB → 1 soubor)
- [x] `font-synthesis: none` — jen řez Light, prohlížeč nesmí kreslit faux-bold/kurzívu
- [x] Tabulkové číslice (`tnum`) na čas stopy, délky a kód stopy — Jannon není monospace,
      bez toho by čísla za běhu poskakovala
- [x] `<link rel=preload>` na woff2
- [ ] **Dokoupit další řezy** (Regular / Medium / Bold / Italic) na stormtype.com —
      hierarchie teď stojí jen na velikosti, prostrkání a barvě. Po nákupu stačí přidat
      `@font-face` bloky do `assets/fonts/fonts.css`, index.html se nemění.
      Pozor: webfont licence je zvlášť od desktopové.

## Batch 13 — Sekce Aftermovies (03) a TV reportáže (04) ✅
- [x] Dvě nové sekce, každá 2×2 mřížka v ozdobných rámech — zlaté aftermovies, stříbrné reportáže
- [x] Rám = 4 lišty s pravým pokosem (clip-path trapézy), gradient napříč profilem lišty
      (oblounek → výžlabek → plochý pás → vnitřní perlička), světlo zleva shora,
      polodrážka a odlesk skla přes náhledovku
- [x] Vlastní video lightbox: play/pauza, tažení po ose, čas, ztlumení, hlasitost, fullscreen,
      buffering spinner, zámek scrollu, focus trap, návrat fokusu
- [x] Klávesy: mezerník/K, ←/→ ±5 s, ↑/↓ hlasitost, M, F, Esc; Tab cyklí uvnitř dialogu
- [x] Otevření videa zastaví hudbu z jukeboxu (jinak by hrály dvě stopy přes sebe)
- [x] Tabulkové číslice v časech; `af-meta` délky odpovídají skutečné stopáži
- [x] Videa: 6× H.264 2-pass, reportáže 960×540, aftermovies 1280×720, ~9,3 MB/kus (celkem 54 MB),
      keyframe po 2 s kvůli plynulému přetáčení, `+faststart` kvůli okamžitému startu
- [x] Zdrojové složky `Reportaze/` a `Aftermovies/` (7,6 GB) v .gitignore
- [x] i18n CS/EN pro obě sekce + nav odkaz „Video"
- [x] QA přes CDP ve skutečném prohlížeči: 49/49 (mobil 390 / tablet 768 / desktop 1440)
- [ ] Aftermovies 3 a 4 — zatím placeholdery „Připravujeme"
- [ ] Zvážit R2 storage, až přibudou další videa (viz Log)

## Batch 14 — Zdobné (barokní) rámy ✅
- [x] Původní profilované lišty nahrazeny skutečnou řezbou — akant, voluty, vejcovec,
      prýtovec, perlovec, mušle, rozety, nárožní kartuše a středové kartuše na lištách
- [x] Předloha se generuje skriptem `tools/genframe.py` do `assets/frames/frame-{gold,silver}.svg`
- [x] Technika: profil lišty dělají gradienty na 4 lichoběžnících s pokosem, ŘEZBU dělá
      SVG lighting filtr (rozostřená alfa jako výšková mapa → feSpecularLighting +
      feDiffuseLighting) nad plochými siluetami. Filtr běží jen na ornamentech —
      na podkladu by vymyl kov do běla.
- [x] Nárožní kartuše symetrická podle úhlopříčky (kreslí se polovina + zrcadlo);
      bez toho shluk voluty a akantu četl jako zvířecí hlava
- [x] Nasazeno přes `border-image ... 168 / var(--fw) / 0 round` — nároží se nedeformují,
      lišty se opakují; odpadly 4 rozpěry v markupu na každý rám (32 elementů pryč)
- [x] Lišta rozšířena na clamp(26px, 3.6vw, 52px) — pod 26 px se řezba slévá
- [x] Zlato ztlumeno do hlubšího odstínu, na skoro černém pozadí bylo křiklavé
- [x] 129 kB SVG → 10 kB po gzipu; QA 51/51

## Batch 15 — Zúžení rámů ✅
- [x] Lišta z clamp(26px,3.6vw,52px) na **clamp(18px,2.2vw,32px)** — původní byla moc tlustá
- [x] Nešlo jen zúžit CSS: při zmenšení předlohy by se řezba slila. Zúžena i rámová
      zóna v předloze (B 168 → 112) a ornament přestavěn na **3 běhy místo 4**
      (prýtovec, rozviliny, vejcovec) — vnitřní perlovec by po zmenšení zmizel
- [x] Rozměry běhů jsou teď zlomky šířky lišty B, ne pevná čísla — na užší liště
      musí být ornamentu MÍŇ a být VĚTŠÍ, ne jen zmenšený
- [x] Nárožní a středová kartuše se kreslí v 168 prostoru a proporčně se zmenší
- [x] Na mobilu spodní hranice 18 px (při 16 px už byl rám jen zlatý proužek)
- [x] QA 52/52 (přibyl test na horní i dolní mez šířky lišty)

## Batch 16 — Jedna sekce Video se záložkami ✅
- [x] Featured klip, Aftermovies a TV reportáže sloučeny do sekce **02 — Video**
      se záložkami Videoklipy · Aftermovies · Reportáže (role=tablist, šipky/Home/End)
- [x] Počty videí v záložkách se dopočítávají z obsahu panelu
- [x] Zdobné rámy odstraněny (SVG předlohy i `tools/genframe.py`) — klipy ohraničuje
      světlá svítivá linka v tónu oblouku jukeboxu (240,220,170)
- [x] Stříbrná varianta lightboxu zrušena, vše jednotně zlaté
- [x] Přepnutí záložky zastaví smyčku featured klipu; Koncerty přečíslovány na 03

## Batch 17 — Nové pořadí sekcí ✅
- [x] 01 O Lence (medailonek + kariéra, 4 milníky + rozbalení), 02 Hudba (jukebox),
      03 Nadační fond (Energie pomáhá, čísla, galerie), 04 Koncerty, 05 Videografie, 06 Press
- [x] Press: fotogalerie + karta „CV pro novináře“ (stahování zatím neaktivní — `data-soon`)
- [x] Fotky zatím placeholdery `.ph` s popiskem, co tam patří (portrét, Lenka s dětmi, tisková foto)
- [x] Navigace 7 položek: od 1320 px užší mezery, pod 1100 px hamburger (i na eshop.html)
- [x] Hero bez řádku s termíny, JSON-LD bez koncertů
- [ ] Text sekce Hudba je provizorní (složený z dodaných faktů) — čeká na text od klienta

## Batch 18 — Videografie ve stylu adele.com ✅
- [x] 3 celoobrazovkové smyčky (Videoklip · Aftermovie · Reportáž) ve sticky „reelu“; slide se
      přepíná podle scrollu, `html{scroll-snap-type:y proximity}` + kotvy `.vg-snap` dotáhnou na další video
- [x] Smyčky jsou krátké výřezy bez zvuku (`assets/video/loop-*.mp4`, 7–11 s, ~1,3 MB, fade na švu)
- [x] Hraje jen aktivní smyčka a jen když je sekce vidět; při otevření přehrávače se pauzne
- [x] „Přehrát video“ otevře celé video ve stávajícím přehrávači, pozadí se rozmaže (blur 22px)
- [x] Zámek scrollu přehrávače přes `overflow:hidden` na <html> (position:fixed na body odsouvalo sticky video)
- [x] `#root` má `overflow-x:clip` — s `hidden` by byl scroll kontejner a sticky by nefungoval
- [x] Pás dalších videí: 9 karet (3 z každé kategorie, chystaná na konci), šipky, tažení myší, posuvník
- [x] Pás se při scrollu připne: svislý scroll posouvá karty do strany (výška sekce = obrazovka + délka pásu),
      po poslední kartě stránka pokračuje; tažení, horizontální swipe, šipky i posuvník jen posouvají stránku

## Log
- 2026-06-24 15:50 — záloha + roadmapa
- 2026-06-24 15:53 — Batch 1 (SEO, a11y, scrollspy, progress, perzistence)
- 2026-06-24 15:56 — Batch 2 (plynulý progress, drag seek, klávesy, hero fade)
- 2026-06-24 15:59 — Batch 3 (self-hosting assetů)
- 2026-06-24 16:03 — Batch 4 (QA screenshoty, 0 chyb) + preload LCP
- 2026-06-24 16:35 — Batch 5 (self-host fontů, funkční QA) — roadmapa vyčerpána, loop ukončen
- 2026-08-09 12:20 — Batch 12 (celý web na Jannon Sans Light, self-hosted WOFF2 32 kB)
- 2026-08-09 13:30 — Batch 13 (sekce Aftermovies + TV reportáže, ozdobné rámy, vlastní video přehrávač)
- 2026-08-09 14:50 — Batch 14 (zdobné barokní rámy generované do SVG, border-image)
- 2026-08-09 15:05 — Batch 15 (užší rámy, ornament přestavěn na 3 běhy)
- 2026-09-16 — Hero: portrét oddálený na střed, studiové pozadí do stran, menší texty
- 2026-09-16 — Batch 16 (sekce Video se záložkami, svítivá linka místo rámů)
- 2026-09-16 — Video: sekce se vejde na jednu obrazovku (šířka podle výšky okna), Videoklipy jako 4 karty, bez credits
- 2026-09-16 — E-shop: položka v navigaci + stránka eshop.html „Připravujeme“ (footer z hlavní stránky, CS/EN, noindex)
- 2026-09-16 — Koncerty: vstupenky odstraněny, místo nich blok „Připravujeme“ s odkazem na newsletter
- 2026-09-16 — Batch 17 (přeskládání sekcí, O Lence, Nadační fond, Press, texty CS/EN)
- 2026-09-16 — Batch 18 (Videografie: celoobrazovkové smyčky + pás dalších videí, styl adele.com)
- 2026-09-16 — Videografie: připnutý pás dalších videí řízený svislým scrollem
