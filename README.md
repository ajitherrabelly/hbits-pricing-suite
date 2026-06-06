# HBITS Vendor Rate Comparison & Bid Builder

Competitive pricing-analysis tooling for **NYS OGS Group 73012 — Hourly-Based IT Services (HBITS)**, Solicitation 23311.
It consolidates every competitor's published rate card into one datasource and provides an interactive web app to
compare rates, see Best Pegasus's competitive position, and build a recommended bid sheet positioned against the field.

---

## What's in here

| File | Purpose |
|------|---------|
| `index.html` | Main web app — two formula-version tabs (V1 / V1.1) × two view tabs (Rate Comparison / Best Pegasus Positions). |
| `positioning.html` | **Bid Builder** — interactive page that recomputes Best Pegasus's recommended rate for any target rank, with V1-vs-V1.1 comparison and margin/profit estimates. |
| `vendors_rates.csv` | Consolidated datasource: competitors + both Best Pegasus formula versions. |
| `extract_rates.py` | Parses each vendor PDF (latest effective date) into rate rows. |
| `generate_csv.py` | Builds the competitor CSV and holds the V1 baseline rates from the estimation doc. |
| `position_best_pegasus.py` | Computes the V1.1 rank-#19 positioning per role. |
| `build_dataset.py` | Assembles `vendors_rates.csv` = competitors + V1 + V1.1 Best Pegasus rows. |

---

## Data pipeline

```
Pricing document/*.pdf  ──extract_rates.py──►  competitor rows (latest effective date)
NYS OGS IT Vendor Rate Estimation.pdf  ──►  V1 baseline Best Pegasus rates
competitor field  ──position_best_pegasus.py──►  V1.1 rank-#19 Best Pegasus rates
                                  └──► build_dataset.py ──► vendors_rates.csv
```

- **32 vendor cards** parse to exactly **372 rows** each (31 job titles × 4 skill levels × 3 regions).
- Each vendor PDF contains several effective-date sections; only each vendor's **latest** effective date is kept
  (their current contracted Award 23158 rate).
- `vendors_rates.csv` columns:
  `Contractor_Name, Federal_ID, Region, Job_Title, Skill_Level, Hourly_Wage_Rate, Hourly_Bill_Rate, Markup_Percent, Is_Our_Rate, Formula_Version`

### Regenerate the data
```bash
pip install pdfplumber
python generate_csv.py          # extract competitors + embed V1 baseline
python build_dataset.py         # produce vendors_rates.csv with V1 + V1.1
```

### Run the app
```bash
python -m http.server 8000
# open http://localhost:8000/index.html
```

---

## Pricing formula versions

Both versions coexist in the CSV via the `Formula_Version` column and are selectable via tabs in `index.html`.

### Version 1 — Baseline (`v1`)
Best Pegasus rates from the original **NYS OGS IT Vendor Rate Estimation** (Bid Year 2026 bill rates).
Covers **30 titles** (the source doc omits *Business Analyst*). These rates tend to sit in the **expensive third**
of the field (e.g., Programmer / Region 1 / Senior ranks **#26 of 33**).

### Version 1.1 — Rank #19 Positioning (`v1.1`) — current strategy
For every Title × Region × Skill, competitor bill rates are ranked ascending (rank #1 = lowest). Best Pegasus's
rate is set to land at **rank #19 of 33** — **18 competitors below, 14 above** (mid-field, ~58th percentile).

- **356 / 372** combos hit exactly #19.
- **16 / 372** land at #18 — these are combos where the 18th and 19th cheapest competitors are **tied**, so #19 is
  mathematically impossible; the nearest (more competitive) rank is used.
- Because the formula only needs competitor data, **all 31 titles are covered**, including Business Analyst.
- Change the target by editing `TARGET_RANK` in `position_best_pegasus.py` and re-running `build_dataset.py`,
  or use the live **Target Rank** input on the Bid Builder page.

---

## Web app features

**index.html**
- **Version tabs:** V1 Baseline ↔ V1.1 Rank #19 (re-ranks the whole app; banner explains the active formula).
- **Rate Comparison:** filter by Region / Skill Level / Job Title (dropdowns), sort ascending/descending by bill rate.
  Best Pegasus row highlighted **bold red** with its live rank ("#19 of 33").
- **Best Pegasus Positions:** one row per Title × Region × Skill (372) with color-coded rank badges
  (green = top third, amber = middle, red = bottom third, grey = not bid), lowest bid, gap to #1, percentile;
  has title search + region/skill filters + sort (best/worst rank, by title).

**positioning.html (Bid Builder)**
- Live **Target Rank** input (default 19) — recomputes all recommended rates instantly from the competitor field.
- Side-by-side **V1 Baseline vs V1.1 Recommended** with delta per role.
- **Margin/profit estimate** with editable cost-build inputs:
  payroll taxes 13.5%, insurance 3.5%, overhead + G&A 10.5% (% of wage), OGS fee 0.75% (% of bill), markup % (sets wage).
  Columns: Wage, Net Profit/hr, Net Margin % (color-coded).
- **CSV export** of the full bid sheet for the chosen rank.

---

## Key findings & caveats

- **Margin is driven by markup, not the role.** Cost loadings are a % of wage, so at the rank-#19 bill rates net
  margin is ~uniform across roles: **~1–2% at a 30% markup**, **~11% at a 45% markup**. Rank-#19 pricing requires a
  ~40–45% markup to clear a healthy (~10%) margin.
- **Incumbent rates can look artificially cheap.** Many competitors' latest contracted effective date is pre-2025 and
  un-escalated under Award 23158, so the field's low end reflects stale rates.
- **Business Analyst** is absent from the V1 estimation doc but fully covered under V1.1.
- The Best Pegasus **wage** shown is derived from the bill rate at an assumed 30% markup (display only); set your real
  markup on the Bid Builder to refine.
- Rates reflect **public OGS award-notice pricing schedules** (Group 73012 / Award 23158).

---

*Persona context: Federal & State Government Pricing / Capture analysis for IT staff-augmentation RFPs.*
