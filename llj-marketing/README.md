# LLJ Marketing website

Static site (HTML/CSS/JS, no build step). Everything that gets deployed is in `public/`.

## Images (already installed — re-export from Figma only if the design changes)
Export these from Figma (PNG, 2x) and overwrite the files in `public/images/`:

| File | Figma layer | Size |
|---|---|---|
| logo.png | Logo | 352 x 122 |
| hero-phone.png | Hero / Phone Image | 2048 x 1536 (transparent) |
| about-phone.png | About / Phone Image | 2482 x 1862 (transparent) |
| map.png | Location / Map Image | 506 x 506 |

Optional: add `favicon.png` (512x512) and `og-image.png` (1200x630), then add the matching
`<link rel="icon">` / `<meta property="og:image">` tags in each page's `<head>`.

## Replace the domain
`https://lljmarketing.com` is a placeholder used in canonical links, sitemap.xml and robots.txt.
After buying the domain, replace it in all files (e.g. `grep -rl lljmarketing.com public | xargs sed -i 's#https://lljmarketing.com#https://YOUR-DOMAIN.com#g'`).

## Deploy on Cloudflare
Cloudflare dashboard > Workers & Pages > Create > connect your GitHub repo.
Build command: leave empty. Output / assets directory: `public` (already set in `wrangler.jsonc`).
Then add the custom domain under the project's Domains tab.

## Edit prices
Prices live in `public/pricelist.html`. They are generated from the arrays in `build.py`
(not included here). Edit build.py and re-run it, or edit the numbers directly in the HTML.
