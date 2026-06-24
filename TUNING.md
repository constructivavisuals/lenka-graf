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

## Batch 3 — Vizuální vychytávky
- [ ] Hero: lokální fallback foto (frame z hero.mp4) místo závislosti na cizím serveru
- [ ] Plynulé přechody mezi sekcemi, konzistentní vertikální rytmus
- [ ] Jemné dekorativní prvky (hairline ornamenty, čísla sekcí)
- [ ] Preloader / fade-in celé stránky
- [ ] Custom kurzor highlight na interaktivních prvcích (decentní)
- [ ] Lightbox/větší přehrávač pro Featured klip

## Batch 4 — Robustnost & finální QA
- [ ] Self-host kritických assetů (poster, fallbacky) v assets/
- [ ] Cross-check: mobil 360/390, tablet 768, desktop 1440/1920
- [ ] Kontrast textů (WCAG AA) na světlých místech fotky
- [ ] Lighthouse-style pass (meta, alt, lang, headings hierarchie)
- [ ] Závěrečné pročištění CSS/JS, komentáře
- [ ] Aktualizace README/handoff pozn. + finální commit

## Log
- 2026-06-24 15:50 — záloha + roadmapa
