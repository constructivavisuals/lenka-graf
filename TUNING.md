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

## Batch 2 — Mikrointerakce & detaily
- [ ] Nav: animovaný podtržení odkazů, plynulé objevení nav po načtení
- [ ] Hero: jemné parallax i pro obsah (různé rychlosti vrstev)
- [ ] Jukebox: hlasitost, mute, plynulý fill (rAF interpolace), buffering stav, drag na seekbaru
- [ ] Klávesy A-1/2/3 na fyzické klávesnici (1/2/3, mezerník = play, šipky = prev/next)
- [ ] Tlačítka: jemný press/active stav, ripple-free elegantní feedback
- [ ] Sekční nadpisy: reveal po slovech / clip-path
- [ ] Vstupenky: jemný 3D tilt na hover (desktop)

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
