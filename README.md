# WageReality

A single-page "True Hourly Wage Calculator." It reveals a person's real hourly wage — take-home pay minus job-related costs, divided by scheduled hours plus commute, unpaid overtime, and decompression time — versus the naive salary/hours number most people use. Based on the "real hourly wage" concept from *Your Money or Your Life* by Vicki Robin and Joe Dominguez.

Live site (once domain is connected): **https://wagereality.com**

## Stack

Deliberately minimal, per the build spec:

- Single HTML file (`index.html`) — vanilla JS + CSS only, no framework, no build step, no `node_modules`.
- Fonts: Inter (UI) + DM Serif Display (result number) via Google Fonts `<link>`.
- No backend, no database, no login. All calculation is client-side and synchronous.
- Deployable by dragging the one file onto any static host.

## Files

| File | Purpose |
|---|---|
| `index.html` | The entire app — markup, styles, calculator logic, canvas share-card generator |
| `robots.txt` | Crawler rules, explicitly allows AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.) |
| `sitemap.xml` | Single-URL sitemap |
| `llms.txt` | Plain-text site summary for LLM/agentic crawlers |

## Features implemented

- Live, no-button calculator (Doherty threshold) with 3 primary inputs and a collapsed "advanced options" panel (Hick's Law)
- Quick-pick "how do you feel after work" buttons that seed decompression time
- Result card as the single dominant visual element (Von Restorff), with count-up animation on change
- Breakdown grid: real hours/month, real take-home, estimated annual loss
- What-if tabs: Current job / Fully remote / Freelance (custom hours)
- Time-value micro-tool ("what does that purchase really cost you in hours")
- WhatsApp share (prefilled with the user's actual computed numbers) + canvas-generated 1000×1000 PNG share card with download
- Affiliate CTA strip (placeholder remote-job-board link — swap in real affiliate link later)
- Static "How this is calculated" formula + worked example (present at first paint, not JS-injected)
- FAQ accordion (7 Q&As), fully static HTML, keyboard accessible
- `WebApplication` + `FAQPage` JSON-LD (FAQ schema text matches visible copy exactly), plus a placeholder `Organization` schema
- Mobile-first responsive from 375px, `clamp()` fluid type, 44px touch targets

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

## Next steps / TODO

**Domain (Spaceship → Vercel)**
1. In Vercel: Project → Settings → Domains → add `wagereality.com` (and `www.wagereality.com`).
2. In Spaceship DNS: point the domain at Vercel — either change nameservers to Vercel's, or add the A/CNAME records Vercel's domain screen shows you (typically an `A` record for the apex to `76.76.21.21` and a `CNAME` for `www` to `cname.vercel-dns.com`, but use the exact values Vercel displays for this project).
3. Wait for DNS propagation, confirm `https://wagereality.com` serves the site with a valid SSL cert (Vercel issues this automatically).

**SEO / GEO follow-up**
- Replace the placeholder `og-image.png` — create a real 1200×630 social preview image and update the `og:image` / `twitter:image` paths in `index.html`.
- Fill in the placeholder `Organization` JSON-LD block in `index.html` with real name/author details.
- Submit `https://wagereality.com/sitemap.xml` to Google Search Console and Bing Webmaster Tools once the domain is live.
- Verify `robots.txt`, `sitemap.xml`, `llms.txt` are all reachable at the root post-deploy (no host-default blocking).

**Monetization**
- Swap the placeholder affiliate link (currently `remoteok.com`) for a real affiliate/partner link once available.
- Apply for Google AdSense once the domain has been live for a bit and has some traffic history.

**Product**
- Consider adding more "tool" pages later (the sitemap/llms.txt are structured to extend easily).
- Consider a real analytics option that doesn't compromise the "fully private, nothing sent to a server" claim in the FAQ/footer (or drop the claim if analytics are added).
