# WageReality

A small suite of free "real hourly wage" tools, built around the concept from *Your Money or Your Life* by Vicki Robin and Joe Dominguez: your true hourly wage is take-home pay minus job-related costs, divided by scheduled hours plus commute, unpaid overtime, and decompression time — not just salary ÷ scheduled hours.

Live site: **https://wagereality.com**

Two pages currently:
- **`/`** — the single-offer real hourly wage calculator
- **`/compare-job-offers`** — compares two offers side by side and declares a winner by real hourly wage

## Stack

Deliberately minimal, per the original build spec:

- Static HTML pages — vanilla JS + CSS only, no framework, no build step, no `node_modules`.
- Fonts: Inter (UI) + DM Serif Display (result numbers) via Google Fonts `<link>`.
- No backend, no database, no login. All calculation is client-side and synchronous.
- One `vercel.json` rewrite gives `/compare-job-offers` a clean URL (maps to `compare-job-offers.html`); everything else is deployable by dragging the files onto any static host.

## Files

| File | Purpose |
|---|---|
| `index.html` | Single-offer calculator — markup, styles, calculator logic, canvas share-card generator |
| `compare-job-offers.html` | Two-offer comparison tool — same calc engine applied twice, verdict banner, its own share card |
| `vercel.json` | Rewrite so `/compare-job-offers` serves without the `.html` extension |
| `og-image.png` | Social preview image for `index.html` |
| `og-image-compare.png` | Social preview image for `compare-job-offers.html` |
| `robots.txt` | Crawler rules, explicitly allows AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.) |
| `sitemap.xml` | Lists both pages |
| `llms.txt` | Plain-text site summary for LLM/agentic crawlers, lists both pages |

## Features implemented

**`index.html` (single-offer calculator)**
- Live, no-button calculator (Doherty threshold) with 3 primary inputs and a collapsed "advanced options" panel (Hick's Law)
- Quick-pick "how do you feel after work" buttons that seed decompression time
- Result card as the single dominant visual element (Von Restorff), with count-up animation on change
- Breakdown grid: real hours/month, real take-home, estimated annual loss
- What-if tabs: Current job / Fully remote / Freelance (custom hours)
- Time-value micro-tool ("what does that purchase really cost you in hours")
- Affiliate CTA strip (placeholder remote-job-board link — swap in real affiliate link later)

**`compare-job-offers.html` (two-offer comparison)**
- Same real-wage engine applied independently to two named offers, shared currency selector
- Verdict banner naming the winner with $ and % delta, winner badge on the leading result card
- Own worked example: a 12.5% raise that actually pays *less* per real hour once commute/decompression/costs are counted

**Shared across both pages**
- WhatsApp share (prefilled with the user's actual computed numbers) + canvas-generated PNG share card with download
- Static "how this is calculated" formula + worked example (present at first paint, not JS-injected)
- FAQ accordion, fully static HTML, keyboard accessible (7 Q&As each, page-specific)
- `WebApplication` + `FAQPage` JSON-LD per page (FAQ schema text verified word-for-word against visible copy), plus a placeholder `Organization` schema
- Google Analytics (GA4, `G-1118XN41HK`) on both pages
- Mobile-first responsive from 375px, `clamp()` fluid type, 44px touch targets
- Cross-links: header nav on each page links to the other

## Local preview

No build step — just open the file, or serve it statically:

```bash
python3 -m http.server 8933
```

Then visit `http://localhost:8933`.

## Deployment

Deployed as a static site on **Vercel**. Repo is pushed to GitHub and connected to Vercel for auto-deploys on push to `main`.

```bash
vercel --prod
```

## Done

- Domain connected: Spaceship DNS → Vercel (`A` records on `@` and `www`, both resolving with valid SSL)
- Google Search Console: domain property verified via DNS TXT record, sitemap submitted
- Google Analytics (GA4) wired into both pages; footer/FAQ privacy copy updated to stay accurate now that visit analytics are collected
- `og-image.png` and `og-image-compare.png` both real, both live (no more 404 placeholders)
- Second tool shipped: `/compare-job-offers`, cross-linked from the homepage, registered in `sitemap.xml` and `llms.txt`

## Next steps / TODO

**SEO / GEO follow-up**
- **Bing Webmaster Tools — not yet done.** Submit `https://wagereality.com/sitemap.xml` there too (separate from Google Search Console).
- In Search Console, confirm the updated 2-URL sitemap has been re-crawled (Sitemaps report), and consider using URL Inspection → Request Indexing on `/compare-job-offers` directly to speed up its first crawl.
- Fill in the placeholder `Organization` JSON-LD block (still a stub in both pages) with real name/author details.

**Monetization**
- Swap the placeholder affiliate link (currently `remoteok.com`) for a real affiliate/partner link once available.
- Apply for Google AdSense once the domain has more traffic history.

**Product**
- More tool pages are easy to add — `sitemap.xml`/`llms.txt` and the two-page cross-link pattern already support it.
- The GA4 Data API (programmatic access to visits/sessions) was discussed but never set up — still open if useful.

**Ops**
- Watch for domain/project mismatches in Vercel: on 2026-09-13, `wagereality.com`'s production deployment briefly served an unrelated project's ("kompound") build even though the domain→project mapping in Vercel was correct the whole time — root cause was traced to a deploy run from outside this repo, not anything in this codebase. If it recurs, check `vercel ls wagereality` for deploys you don't recognize and re-deploy from this repo to restore it.
