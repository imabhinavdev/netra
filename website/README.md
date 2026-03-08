# Netra website

Static landing and docs for [Netra](https://github.com/imabhinavdev/netra).

## Local preview

From the repo root:

```bash
cd website
python -m http.server 8080
```

Then open [http://localhost:8080](http://localhost:8080). Or open `index.html` directly in a browser.

## Deploy (e.g. GitHub Pages)

**Important:** In repo **Settings → Pages**, set **Source** to **GitHub Actions** (not "Deploy from a branch"). Otherwise GitHub may serve the repository README instead of this website. The workflow in `.github/workflows/pages.yml` copies `website/*` to the Pages artifact.

1. In repo **Settings → Pages**, set source to **GitHub Actions**.
2. Push to `main` (or trigger the workflow); the Deploy site job will build and publish the site.
3. Root of the site will serve `index.html`; `docs.html` is linked from the landing page.
