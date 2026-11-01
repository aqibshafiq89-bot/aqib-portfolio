# Aqib Shafiq Abbasi — Academic & Professional Portfolio

A fast, accessible single-page portfolio built with semantic HTML, CSS and vanilla JavaScript. It covers research interests, publications (searchable and filterable, with BibTeX export), projects, experience, education, Robootika STEM outreach, certifications and contact details.

## Run locally

```sh
python3 -m http.server 8080 --directory dist
```

Then open http://localhost:8080.

## Edit content

| What | Where |
| --- | --- |
| Publications | `content/publications.json` |
| Projects (cards and detail pop-ups) | `content/projects.json` |
| Research interests, experience, certifications | `content/profile.json` |
| Page copy, hero, education, contact | `templates/index.html` |
| Contact details, profile links, SEO data | top of `scripts/build.py` |
| Styles | `dist/styles.css` |
| Interactions (menu, filters, dialog) | `dist/script.js` |

After editing anything in `content/`, `templates/` or `scripts/`, rebuild:

```sh
python3 scripts/build.py
python3 scripts/validate.py   # optional; needs `pip install pymupdf`
```

## Publish with GitHub Pages

The workflow in `.github/workflows/deploy-pages.yml` builds the site and deploys `dist/` on every push to `main`.

1. Push this project to the `main` branch of https://github.com/aqibshafiq89-bot/aqib-portfolio.
2. In **Settings → Pages → Build and deployment**, set **Source** to **GitHub Actions**.
3. The workflow runs automatically; the site URL appears in the Actions run and in Settings → Pages.

The workflow sets the canonical, Open Graph, sitemap and structured-data URLs to the real GitHub Pages address at deploy time.

## Notes

- Fonts (Inter and Source Serif 4, SIL Open Font License) are self-hosted in `dist/assets/fonts/`, so the site makes no third-party requests.
- Project images are illustrative renderings and are labelled as such on the page. Their provenance is recorded in `content/visual-assets.json`.
- The downloadable CV is a public copy with the passport field and referee details removed.
- Content sources and verification notes are in `SOURCE_NOTES.md`.
