#!/usr/bin/env python3
"""Videografie: převod videí pro web, nahrání na Cloudflare R2 a vygenerování karet ve videografie.html.

  python3 tools/videografie.py encode   # převede videa z tools/videa.json (co už je hotové, přeskočí)
  python3 tools/videografie.py upload   # nahraje mp4 + poster do R2 bucketu (co už je nahrané, přeskočí)
  python3 tools/videografie.py html     # přegeneruje karty ve videografie.html

Nové video = nový řádek v tools/videa.json a spustit všechny tři kroky.
Webové verze se ukládají na disk do složky „LENKA GRAF WEB VERZE“ (originály zůstávají beze změny).
"""
import json, os, subprocess, sys, html, threading, concurrent.futures as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, 'tools', 'videa.json'), encoding='utf-8'))
DISK = CFG['disk']
OUT = os.path.join(DISK, 'LENKA GRAF WEB VERZE')
BUCKET = 'lenka-graf-media'
STATE = os.path.join(OUT, 'nahrano.json')

def src_path(v): return v['zdroj'] if v['zdroj'].startswith('/') else os.path.join(DISK, v['zdroj'])
def out_base(v): return os.path.join(OUT, v['kat'], v['id'])

def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration',
                        '-of', 'json', path], capture_output=True, text=True)
    d = json.loads(r.stdout); s = d['streams'][0]
    return s['width'], s['height'], float(d['format']['duration'])

def encode_one(v):
    src, base = src_path(v), out_base(v)
    mp4, jpg = base + '.mp4', base + '.jpg'
    if os.path.exists(mp4) and os.path.exists(jpg): return v['id'], 'hotovo dříve'
    os.makedirs(os.path.dirname(base), exist_ok=True)
    w, h, dur = probe(src)
    # na výšku zůstane výška max 1920, na šířku šířka max 1920; H.264 + AAC, přehratelné hned (faststart)
    scale = "scale='min(1920,iw)':-2:flags=lanczos" if w >= h else "scale=-2:'min(1920,ih)':flags=lanczos"
    tmp = mp4 + '.part.mp4'
    cmd = ['ffmpeg', '-hide_banner', '-v', 'error', '-y', '-i', src, '-map', '0:v:0', '-map', '0:a:0?',
           '-vf', scale + ',format=yuv420p', '-fpsmax', '50',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-maxrate', '6M', '-bufsize', '12M', '-profile:v', 'high', '-g', '100',
           '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
           '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-ar', '48000', '-movflags', '+faststart', tmp]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: return v['id'], 'CHYBA: ' + r.stderr[-300:]
    os.replace(tmp, mp4)
    make_poster(mp4, jpg, w, h, dur)
    return v['id'], f'{os.path.getsize(mp4)/1048576:.0f} MB'

def make_poster(mp4, jpg, w, h, dur):
    """Poster = nejostřejší dost světlý snímek z 12 kandidátů mezi 8 % a 70 % délky (ne rozmazaný ani tmavý)."""
    import numpy as np
    best = (-1, dur * 0.25)
    for i in range(12):
        t = dur * (0.08 + 0.62 * i / 11)
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', mp4, '-frames:v', '1', '-vf', 'scale=320:-2,format=gray',
                              '-f', 'rawvideo', '-'], capture_output=True).stdout
        if not raw: continue
        a = np.frombuffer(raw, np.uint8).astype(np.float32)
        hh = len(a) // 320; a = a[:hh * 320].reshape(hh, 320)
        lap = np.abs(4 * a[1:-1, 1:-1] - a[:-2, 1:-1] - a[2:, 1:-1] - a[1:-1, :-2] - a[1:-1, 2:])
        sharp, bright = float(lap.var()), float(a.mean())
        score = sharp * min(1.0, bright / 70) * (0.3 if bright < 25 else 1)
        if score > best[0]: best = (score, t)
    pw = 960 if w >= h else 540
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{best[1]:.2f}', '-i', mp4, '-vf', f'scale={pw}:-2',
                    '-frames:v', '1', '-q:v', '3', jpg], check=True)

def posters():
    for v in CFG['videa']:
        mp4, jpg = out_base(v) + '.mp4', out_base(v) + '.jpg'
        if not os.path.exists(mp4):
            old = os.path.join(OUT, 'kratka', v['id']) + '.mp4'
            if not os.path.exists(old): continue
            mp4, jpg = old, old[:-4] + '.jpg'
        w, h, dur = probe(mp4); make_poster(mp4, jpg, w, h, dur); print('poster', v['id'], flush=True)

def encode():
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for vid, msg in ex.map(encode_one, CFG['videa']):
            print(f'{vid:32s} {msg}', flush=True)

def upload():
    for v in CFG['videa']:
        old = os.path.join(OUT, 'kratka', v['id'])
        for ext in ('.mp4', '.jpg'):
            if os.path.exists(old + ext) and not os.path.exists(out_base(v) + ext):
                os.makedirs(os.path.dirname(out_base(v)), exist_ok=True); os.replace(old + ext, out_base(v) + ext)
    done = json.load(open(STATE)) if os.path.exists(STATE) else {}
    jobs = []
    for v in CFG['videa']:
        for ext, ctype in (('.mp4', 'video/mp4'), ('.jpg', 'image/jpeg')):
            f = out_base(v) + ext; key = f"{v['kat']}/{v['id']}{ext}"
            if not os.path.exists(f): print('chybí', f); continue
            sig = f'{os.path.getsize(f)}:{int(os.path.getmtime(f))}'
            if done.get(key) != sig: jobs.append((f, key, ctype, sig))
    lock = threading.Lock()
    def put(job):
        f, key, ctype, sig = job
        r = subprocess.run(['npx', '--yes', 'wrangler', 'r2', 'object', 'put', f'{BUCKET}/{key}', '--file', f, '--remote',
                            '--content-type', ctype, '--cache-control', 'public, max-age=31536000'],
                           capture_output=True, text=True, cwd=OUT)
        ok = r.returncode == 0
        with lock:
            print(('OK   ' if ok else 'CHYBA') + f' {key}  {os.path.getsize(f)/1048576:.1f} MB' + ('' if ok else '  ' + r.stderr[-300:]), flush=True)
            if ok:
                done[key] = sig; json.dump(done, open(STATE, 'w'), indent=1)
    # wrangler nahrává jedním spojením (~1 MB/s) — víc souborů najednou využije linku
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(put, jobs))

def fmt_dur(s):
    s = int(round(s)); return f'{s//60}:{s%60:02d}'

def html_cards():
    base = CFG['base_url'].rstrip('/')
    done = json.load(open(STATE)) if os.path.exists(STATE) else {}
    live = lambda v: f"{v['kat']}/{v['id']}.mp4" in done and f"{v['kat']}/{v['id']}.jpg" in done
    parts = []
    for k in CFG['kategorie']:
        vids = [v for v in CFG['videa'] if v['kat'] == k['id'] and live(v)]
        cards = []
        for v in vids:
            mp4 = out_base(v) + '.mp4'
            dur = fmt_dur(probe(mp4)[2]) if os.path.exists(mp4) else ''
            url = f"{base}/{v['kat']}/{v['id']}"
            ver = lambda ext: done.get(f"{v['kat']}/{v['id']}{ext}", '').split(':')[-1]
            kick_cs = k['kick_cs'] + (f" · {v['rok']}" if v.get('rok') else '')
            kick_en = k['kick_en'] + (f" · {v['rok']}" if v.get('rok') else '')
            cards.append(
                f'''        <button type="button" class="vcard{' vcard--svisle' if v.get('svisle') else ''}" data-src="{url}.mp4?v={ver('.mp4')}" data-poster="{url}.jpg?v={ver('.jpg')}"{' data-vertical' if v.get('svisle') else ''}>
          <span class="vcard-media"><img src="{url}.jpg?v={ver('.jpg')}" alt="" loading="lazy" decoding="async"><span class="vcard-play" aria-hidden="true"></span>{f'<span class="vcard-dur">{dur}</span>' if dur else ''}</span>
          <span class="vcard-txt"><span class="vcard-kick" data-cs="{html.escape(kick_cs)}" data-en="{html.escape(kick_en)}">{html.escape(kick_cs)}</span><span class="vcard-title" data-cs="{html.escape(v['cs'])}" data-en="{html.escape(v['en'])}">{html.escape(v['cs'])}</span></span>
        </button>''')
        n = len(vids)
        parts.append(f'''    <section id="{k['id']}" class="vp-cat">
      <div class="vp-cat-head"><span class="vp-cat-num">{len(parts)+1:02d}</span><h2 data-cs="{k['cs']}" data-en="{k['en']}">{k['cs']}</h2><span class="vp-cat-count" data-count-label="{k['id']}"></span></div>
      <div class="vp-grid">
{chr(10).join(cards)}
      </div>
    </section>''')
    tabs = '\n'.join(f'''        <a href="#{k['id']}" class="vp-tab{' active' if i == 0 else ''}"><span data-cs="{k['cs']}" data-en="{k['en']}">{k['cs']}</span> <b data-count="{k['id']}"></b></a>'''
                     for i, k in enumerate(CFG['kategorie']))
    return tabs, '\n\n'.join(parts)

def replace_between(s, start, end, new):
    a = s.index(start) + len(start); b = s.index(end, a)
    return s[:a] + '\n' + new + '\n' + s[b:]

def gen_html():
    p = os.path.join(ROOT, 'videografie.html')
    s = open(p, encoding='utf-8').read()
    tabs, sections = html_cards()
    s = replace_between(s, '<!-- TABS:START -->', '        <!-- TABS:END -->', tabs)
    s = replace_between(s, '<!-- VIDEA:START (generuje tools/videografie.py html) -->', '    <!-- VIDEA:END -->', sections)
    open(p, 'w', encoding='utf-8').write(s)
    print('videografie.html: karty přegenerovány')

if __name__ == '__main__':
    {'encode': encode, 'posters': posters, 'upload': upload, 'html': gen_html}[sys.argv[1]]()
