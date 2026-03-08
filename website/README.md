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

1. In repo **Settings → Pages**, set source to **GitHub Actions** or **Deploy from a branch**.
2. If using branch: choose branch `main` and folder `/website` (or put `website` contents in `/docs` and use "Deploy from branch" with docs folder).
3. If using Actions: add a workflow that copies `website/*` to the Pages artifact.

Root of the site should serve `index.html`; `docs.html` is linked from the landing page.
