"""Generate dist/index.html and supporting files from templates/ and content/.

Uses only the Python standard library. Run: python3 scripts/build.py
"""
from pathlib import Path
from collections import Counter
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
SITE = 'https://example.github.io/portfolio'  # replaced at deploy time by scripts/set-site-url.py
NAME = 'Aqib Shafiq Abbasi'
EMAIL = 'aqib.shafiq89@gmail.com'
PHONE = '+971 56 786 3596'
LINKEDIN = 'https://www.linkedin.com/in/engr-aqib-shafiq-abbasi-355b24179/'
SCHOLAR = 'https://scholar.google.com/citations?user=bwT94LAAAAAJ&hl=en'
GITHUB = 'https://github.com/aqibshafiq89-bot'
CV = 'assets/Aqib-Shafiq-Academic-CV.pdf'

esc = html.escape
papers = json.loads((ROOT / 'content/publications.json').read_text())
projects = json.loads((ROOT / 'content/projects.json').read_text())
profile = json.loads((ROOT / 'content/profile.json').read_text())

PATHS = {
    'arrow': '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    'out': '<path d="M7 17 17 7M7 7h10v10"/>',
    'download': '<path d="M12 3v12m-5-5 5 5 5-5M5 16v4h14v-4"/>',
    'solar': '<path d="m5 10-2 9h18l-2-9ZM8 10l-1 9m9-9 1 9M4 14h16M12 2v2M5 4l2 2m12-2-2 2M9 7a3 3 0 0 1 6 0"/>',
    'grid': '<path d="M12 2 5 22m7-20 7 20M8 11h8M6 17h12M5 7h14M3 7v3m18-3v3"/>',
    'ev': '<path d="m3 12 2-6h10l2 6v7H3ZM3 12h14M6 16h1m6 0h1M5 19v2m10-2v2m3-18 3 3v8a2 2 0 0 1-4 0m3-11v3h2"/>',
    'chip': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4m6-4v4M9 18v4m6-4v4M2 9h4m-4 6h4m12-6h4m-4 6h4M9 9h6v6H9Z"/>',
    'wave': '<path d="M2 13h4l3-8 5 14 3-7h5"/>',
    'chart': '<path d="M4 3v17h17M7 15l4-5 4 2 6-7M17 5h4v4"/>',
    'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 6 10 7L22 6"/>',
    'phone': '<path d="M6 3h3l2 5-3 2c1 3 3 5 6 6l2-3 5 2v3c0 2-2 3-4 3C9 20 4 15 3 7c0-2 1-4 3-4Z"/>',
    'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    'check': '<path d="m5 12 4 4L19 6"/>',
    'award': '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 8 5-3 5 3-1.5-8"/>',
    'copy': '<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V3H3v13h5"/>',
    'search': '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
    'cap': '<path d="m2 9 10-5 10 5-10 5Z"/><path d="M6 11v5c3 2 9 2 12 0v-5M22 9v6"/>',
    'linkedin': '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4m-4-7v7"/>',
    'scholar': '<path d="m2 9 10-6 10 6-10 6Z"/><circle cx="12" cy="16" r="4"/>',
    'github': '<path d="M9 19c-4 1.5-4-2-6-2.5m12 4.5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12 12 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
}


def icon(name, cls=''):
    return (f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{PATHS.get(name, PATHS["chip"])}</svg>')


def tags(items):
    return '<ul class="tags">' + ''.join(f'<li>{esc(x)}</li>' for x in items) + '</ul>'


def ext(href, label, cls='text-link'):
    return f'<a class="{cls}" href="{esc(href)}" target="_blank" rel="noopener noreferrer">{label}{icon("out")}</a>'


# ---------------------------------------------------------------- navigation
nav = ''.join(f'<a href="#{i}">{label}</a>' for i, label in [
    ('about', 'About'), ('research', 'Research'), ('publications', 'Publications'), ('projects', 'Projects'),
    ('experience', 'Experience'), ('education', 'Education'), ('contact', 'Contact')])

# ------------------------------------------------------------------ research
research_html = ''.join(
    f'<li class="interest"><div class="interest-top"><span class="interest-no">{n + 1:02d}</span>{icon(r["icon"])}</div>'
    f'<h3>{esc(r["title"])}</h3><p>{esc(r["text"])}</p>{tags(r["tags"])}</li>'
    for n, r in enumerate(profile['research']))

# -------------------------------------------------------------- publications
types = Counter(p['type'] for p in papers)
years = sorted({p['year'] for p in papers if p['year']}, reverse=True)
topics = sorted({p['topic'] for p in papers})
year_options = ''.join(f'<option value="{y}">{y}</option>' for y in years)
if any(not p['year'] for p in papers):
    year_options += '<option value="undated">Year not listed</option>'
topic_options = ''.join(f'<option>{esc(t)}</option>' for t in topics)


def by_recency(item):
    n, p = item
    return (-(p['year'] or 0), n)


pubs = ''
for n, p in sorted(enumerate(papers), key=by_recency):
    authors = esc(p['authors']).replace('Aqib Shafiq', '<strong>Aqib Shafiq</strong>')
    meta = [f'<em>{esc(p["venue"])}</em>']
    if p.get('volume'):
        meta.append(f'vol. {esc(str(p["volume"]))}')
    if p.get('pages'):
        meta.append(f'pp. {esc(p["pages"])}')
    if p['year']:
        meta.append(str(p['year']))
    links = []
    if p['doi']:
        links.append(ext('https://doi.org/' + p['doi'], 'DOI', 'pub-link'))
    if p['source'].startswith('http'):
        links.append(ext(p['source'], 'Publisher', 'pub-link'))
    if not links:
        links.append(ext(SCHOLAR, 'Google Scholar', 'pub-link'))
    pubs += (
        f'<li class="publication" data-year="{p["year"] or "undated"}" data-type="{p["type"]}" '
        f'data-topic="{esc(p["topic"])}" data-index="{n}">'
        f'<div class="pub-year">{p["year"] or "—"}<span class="badge badge-{p["type"].lower()}">{p["type"]}</span></div>'
        f'<div class="pub-main"><h3>{esc(p["title"])}</h3>'
        f'<p class="authors">{authors}</p>'
        f'<p class="venue">{", ".join(meta[:-1] if p["year"] else meta)}<span class="pub-topic">{esc(p["topic"])}</span></p></div>'
        f'<div class="pub-links">{"".join(links)}</div></li>')

# ------------------------------------------------------------------ projects
project_cards = []
for n, p in enumerate(projects):
    asset = 'hero' if p['kind'] == 'energy' else p['kind']
    cls = 'project-card featured' if n == 0 else 'project-card'
    sizes = '(max-width: 900px) 100vw, 55vw' if n == 0 else '(max-width: 900px) 100vw, 22vw'
    project_cards.append(f'''<article class="{cls}">
 <div class="project-media"><img src="assets/renders/{asset}-960.webp" srcset="assets/renders/{asset}-640.webp 640w, assets/renders/{asset}-960.webp 960w, assets/renders/{asset}-1440.webp 1440w" sizes="{sizes}" alt="Illustrative rendering for {esc(p['title'])}" width="1536" height="1024" loading="lazy"><span class="project-no">{n + 1:02d}</span></div>
 <div class="project-body"><p class="kicker">{esc(p['category'])}</p><h3>{esc(p['title'])}</h3><p>{esc(p['description'])}</p>{tags(p['technologies'])}
 <button class="text-link project-open" type="button" data-project="{p['id']}">Project details {icon('arrow')}</button>
 <noscript><p><strong>Problem:</strong> {esc(p['problem'])}</p><p><strong>Approach:</strong> {esc(p['solution'])}</p><p><strong>Role:</strong> {esc(p['role'])}</p></noscript></div>
</article>''')
project_html = '\n'.join(project_cards)
# Only the fields the public dialog uses are embedded in the page.
public_projects = [{k: p[k] for k in ('id', 'title', 'category', 'problem', 'solution', 'role',
                                      'technologies', 'status', 'link', 'linkLabel', 'image') if k in p}
                   for p in projects]

# ---------------------------------------------------------------- experience
exp = ''.join(
    f'<li class="role"><p class="role-dates">{esc(e["dates"])}</p><div><h3>{esc(e["role"])}</h3>'
    f'<p class="role-org">{esc(e["org"])}</p><p>{esc(e["text"])}</p></div></li>'
    for e in profile['experience'])

# ------------------------------------------------------------ certifications
cert_html = ''.join(
    f'<li>{icon("check")}<div><h3>{esc(c["title"])}</h3><p>{esc(c["detail"])}</p></div></li>'
    for c in profile['certifications'])

# -------------------------------------------------------------------- schema
schema = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'Person', '@id': SITE + '/#person', 'name': NAME,
     'alternateName': ['Aqib Shafiq', 'Engr. Aqib Shafiq Abbasi'], 'url': SITE + '/',
     'image': SITE + '/assets/aqib-shafiq-800.webp',
     'jobTitle': 'Electrical Engineer and Researcher',
     'description': 'Electrical engineer and researcher in renewable energy, EV charging and smart grids; robotics, IoT and STEM educator.',
     'email': 'mailto:' + EMAIL, 'telephone': PHONE.replace(' ', ''),
     'homeLocation': {'@type': 'Place', 'name': 'Dubai, United Arab Emirates'},
     'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'University of Azad Jammu and Kashmir'},
     'sameAs': [LINKEDIN, SCHOLAR, GITHUB],
     'knowsAbout': ['Electrical Engineering', 'Solar Photovoltaic Systems', 'Electric Vehicle Charging',
                    'Smart Grids', 'Robotics', 'Internet of Things', 'STEM Education']},
    {'@type': 'WebSite', '@id': SITE + '/#website', 'name': NAME, 'url': SITE + '/', 'inLanguage': 'en',
     'about': {'@id': SITE + '/#person'}},
    {'@type': 'ProfilePage', '@id': SITE + '/#profile', 'url': SITE + '/', 'mainEntity': {'@id': SITE + '/#person'}}]}

context = {
    'SITE': SITE, 'schema': json.dumps(schema, ensure_ascii=False), 'nav': nav,
    'research_html': research_html, 'project_html': project_html, 'pubs': pubs, 'exp': exp,
    'cert_html': cert_html, 'year_options': year_options, 'topic_options': topic_options,
    'n_pubs': str(len(papers)), 'n_journal': str(types.get('Journal', 0)),
    'n_conf': str(types.get('Conference', 0)), 'n_projects': str(len(projects)),
    'EMAIL': EMAIL, 'PHONE': PHONE, 'PHONE_TEL': PHONE.replace(' ', ''),
    'LINKEDIN': esc(LINKEDIN), 'SCHOLAR': esc(SCHOLAR), 'GITHUB': esc(GITHUB), 'CV': CV,
    'projects_json': json.dumps(public_projects, ensure_ascii=False).replace('</', '<\\/'),
}
for name in PATHS:
    context['icon_' + name] = icon(name)

page = (ROOT / 'templates/index.html').read_text()
page = re.sub(r'\{\{(\w+)\}\}', lambda m: context[m[1]], page)
(OUT / 'index.html').write_text(page)
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text(
    f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    f'<url><loc>{SITE}/</loc></url></urlset>\n')
(OUT / '.nojekyll').touch()

# ------------------------------------------------------------------- BibTeX
bib = []
for n, p in enumerate(papers):
    fields = {'title': p['title'],
              'author': p['authors'].replace(', et al.', ' and others').replace(', ', ' and '),
              'journal' if p['type'] == 'Journal' else 'booktitle': p['venue']}
    for key in ['year', 'doi', 'volume', 'pages']:
        if p.get(key):
            fields[key] = str(p[key])
    if p.get('note'):
        fields['note'] = p['note']
    bib.append('@' + ('article' if p['type'] == 'Journal' else 'inproceedings') + '{aqib'
               + str(p['year'] or 'undated') + '_' + str(n + 1) + ',\n'
               + ',\n'.join('  ' + k + ' = {' + v + '}' for k, v in fields.items()) + '\n}')
(OUT / 'assets/publications.bib').write_text('\n\n'.join(bib) + '\n')

(OUT / '404.html').write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Page not found | Aqib Shafiq Abbasi</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml">'
    '<style>body{margin:0;display:grid;place-content:center;min-height:100vh;background:#f7f6f2;color:#0f1b2d;'
    'font:17px/1.6 system-ui,sans-serif;padding:24px}h1{font:600 44px/1.1 Georgia,serif;margin:.3em 0}'
    'p.k{letter-spacing:.14em;font-size:12px;color:#5b6676;text-transform:uppercase}a{color:#173a6b;font-weight:600}</style></head>'
    '<body><main><p class="k">404 · Page not found</p><h1>This page doesn’t exist.</h1>'
    '<p>The link may be outdated or mistyped.</p><a href="./">Return to the homepage →</a></main></body></html>')

print('Built portfolio with', len(papers), 'publications and', len(projects), 'projects.')
