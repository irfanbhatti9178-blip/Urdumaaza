# Urdumaaza Live News

GitHub Pages based RSS-to-JSON news ticker for Urdumaaza.

Flow:
RSS feeds → GitHub Actions (every 5 minutes) → news.json → GitHub Pages → Blogger ticker.

Files:
- `index.html` — live ticker preview
- `fetch_news.py` — RSS fetcher
- `.github/workflows/update-news.yml` — automatic updater
- `news.json` — generated headlines

Enable GitHub Pages from Settings → Pages → Deploy from branch → main → /(root).
