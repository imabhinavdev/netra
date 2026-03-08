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

**You won’t see a “website” folder in the Pages dropdown.** GitHub only offers **Root** or **/docs** when you use “Deploy from a branch,” and it does not list custom folders like `website/`.

**Use the GitHub Actions source instead:**

1. In the repo go to **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions** (not “Deploy from a branch”).
3. The workflow in `.github/workflows/pages.yml` builds the site from the `website/` folder and deploys it. No folder dropdown is used—the workflow copies `website/*` into the Pages artifact.
4. Push to `main` or run the “Deploy site” workflow; the site will be live at your Pages URL. The root URL serves `index.html`; `docs.html` is linked from the landing page.

If you leave Source on “Deploy from a branch,” GitHub will serve the repo root or `/docs`, so you’ll see the README instead of this website.
