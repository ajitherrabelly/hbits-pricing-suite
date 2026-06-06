# Web Suite Pattern — the executive app we built (reusable)

Companion to [PROPOSAL-PLAYBOOK.md](PROPOSAL-PLAYBOOK.md) (the pricing method). This documents the **multi-page
executive web suite** so it can be reproduced for the next RFP. Also captured as the user-level Claude skill
**`idiq-pricing-capture`** (with `rfp-pricing-warmup` for session orientation).

## The 10 pages (shared nav, one design system)
| File | Page | Purpose |
|------|------|---------|
| `index.html` | Overview | Executive landing: market KPIs, top-3 takeaways, top roles/vendors, launch cards (default entry) |
| `compare.html` | Rate Comparison | Our price vs the full field per role; KPI strip, sortable table, price bars, vs-lowest, vendor search, CSV |
| `positioning.html` | Bid Builder | Live target-rank + markup → recommended rates, V1-vs-V1.1 delta, margin; CSV |
| `analytics.html` | Market Analytics | 3-yr placements/$ by year, leaders, share, momentum, top roles/buyers (Chart.js local) |
| `vendors.html` | Vendor Detail | Per-vendor per-year closures + contract drill-down; CSV |
| `briefing.html` | Strategy Briefing | Full methodology + quality-test checklist (sticky TOC) |
| `expert.html` | Expert Session | Dense working page; assumptions table + capturable decision worksheet for senior analysts |
| `formulas.html` | How It Works | Plain-English lemonade-stand analogy of both formulas |
| `factors.html` | Factors & Inputs | Factors/variables/parameters behind each formula + effect on price |
| `resources.html` | Resources | Official reference links, grouped, open in new tab |

Nav order (every page, append-only): Overview · Rate Comparison · Bid Builder · Strategy Briefing · Market Analytics · Vendor Detail · How It Works · Factors & Inputs · Expert Session · Resources.

## Design system
Navy top-nav `#11203a` (current = `#2a64c4`) · hero gradient `#11203a→#1f5a8a` · canvas `#eef1f6` · white cards r12 ·
KPI cards with colored top border · navy sortable tables (▲▼), zebra rows · our row red + "YOU" badge ·
green=competitive, amber=mid, red=expensive.

## Build → verify → commit loop
1. Write/edit a page (append nav link; never disturb existing links).
2. Serve (`python -m http.server`) and **verify via browser preview/eval** — assert KPIs, ranks, row counts, no console errors.
3. Fix the usual suspects: comma-in-name CSV parsing (use quote-aware parser), duplicate element IDs, 10k-row render freeze (cap ~1500), cold-start fetch race.
4. **Local git commit** per milestone — **no remote** (see memory: local-only).

## Data + deliverables
- Data: `vendors_rates.csv` (Formula_Version: ""/v1/v1.1), `analytics_data.js`, `vendor_detail.js`.
- Pipeline: `extract_rates.py` → `generate_csv.py` → `position_best_pegasus.py` → `build_dataset.py`; `make_analytics.py`, `make_vendor_detail.py`, `make_charts.py`.
- Deliverables: `make_deliverables.py` → PDF + PPTX briefing.

## Reuse
- New RFP: invoke the **`idiq-pricing-capture`** skill (method + `references/` for pricing, data pipeline, this suite pattern).
- New session on this project: invoke **`rfp-pricing-warmup`** to orient before working.
