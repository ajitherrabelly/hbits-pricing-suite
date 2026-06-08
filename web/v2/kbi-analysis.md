# HBITS Pricing — KBI Decode & V2 Model: Full Session Handoff

**Date:** 2026-06-07
**Repo:** `github.com/ajitherrabelly/hbits-pricing-suite` (cloned to
`C:\Users\ramat\OneDrive\Documents\hbits-pricing-suite`)
**Program:** NYS OGS Group 73012 — Hourly-Based IT Services (HBITS), Award 23158 / Solicitation 23311
**Our company:** Best Pegasus  ·  **Benchmark competitor:** Knowledge Builders Inc. ("KBI")

> **Purpose of this doc:** a complete, self-contained record of everything done in this session so
> anyone can pick it up cold — the objective, the analysis, the numbers, the decisions, the tools
> built, and the open items. Read top-to-bottom once; thereafter use the section index.

---

## 0. Index
1. Objective & how it evolved
2. The existing project (what we inherited): V1 & V1.1 models
3. Decoding KBI's pricing formula
4. V1.1 vs KBI — the formula difference
5. The 2019-history question (and why it's blocked)
6. The database we built from RFP 23311 (`hbits.db`)
7. The backtest: testing our model against KBI on real wins
8. The decision: adopt the V2 (margin-first) model
9. V2 quotes produced (Programmer-Expert, full Expert sheet)
10. Rate-trajectory CSVs (2021 / 2026 / 2029) — V1 and V2
11. Project Manager spot-check vs KBI
12. All files created/modified this session
13. Open items / next steps
14. How to reproduce everything

---

## 1. Objective & how it evolved
The session walked through a chain of asks, each building on the last:

1. Look at the repo → understand it.
2. Run the service.
3. **Truly understand the logic** (pricing formulas + win data).
4. Focus the objective: **tail the market leader KBI** — decode their pricing model, see how we compare.
5. Decode KBI's formula precisely; quantify the formula difference vs ours.
6. Attempt a 2019→2025 history of KBI (blocked — see §5).
7. Ingest a new data drop (RFP 23311 zip) → **build a database**.
8. **Test our model against KBI** on real award data (backtest).
9. **Adopt a new model (V2)** and document it.
10. Produce **2026 quotes** and **2021/2026/2029 rate trajectories** as CSVs.
11. Spot-check a role (Project Manager) vs KBI.

**The throughline:** move pricing from "pick a rank and hope" to a deliberate, data-validated,
margin-protecting model reverse-engineered from the proven winner.

---

## 2. The existing project (inherited): V1 & V1.1

The repo is a static web suite (HTML/JS + Chart.js) over a consolidated rate CSV, plus a Python
data pipeline. Served with `python -m http.server 8000` (pages: `index.html`, `compare.html`,
`positioning.html` (Bid Builder), `briefing.html`, `analytics.html`, `formulas.html`, etc.).

**Data unit:** a *combo* = Job Title × Region × Skill. 31 titles × 4 skills (Junior/Mid-Level/
Senior/Expert) × 3 regions = **372 combos**, **33 bidders** each (32 competitors + Best Pegasus).
`vendors_rates.csv` ≈ 12,264 rows. Columns: `Contractor_Name, Federal_ID, Region, Job_Title,
Skill_Level, Hourly_Wage_Rate, Hourly_Bill_Rate, Markup_Percent, Is_Our_Rate, Formula_Version`.

**Pipeline:** `extract_rates.py` (pdfplumber + regex; keeps each vendor's *latest effective date*) →
`generate_csv.py` (competitors + hard-coded V1 baseline) → `position_best_pegasus.py` (V1.1 rank
math) → `build_dataset.py` (assembles CSV with `Formula_Version`).

### Two pricing formulas
- **V1 — Baseline (cost-up):** Best Pegasus bill rates hard-coded from the *NYS OGS IT Vendor Rate
  Estimation* doc (`BASELINE_2026_BILL` in `generate_csv.py`). **30 titles** (omits Business
  Analyst). Region 1 values applied to all 3 regions. Tends to land in the **expensive third**
  (e.g., Programmer/R1/Senior ≈ #26 of 33).
- **V1.1 — Rank-#19 positioning (the "current" strategy before this session):** for each combo,
  sort the 32 competitor bills ascending and place Best Pegasus to land at **rank #19 of 33** (18
  below, 14 above). Implemented in **integer cents** with a **tie-aware exact-rank** search
  (`find_clean` / `target_cents`), duplicated in JS in `positioning.html` for live recompute.
  **356/372 hit exactly #19; 16/372 land at #18** (boundary ties make #19 impossible). Covers all
  31 titles (fills the Business Analyst gap).

### Margin/cost model (used everywhere, unchanged through V2)
% of **wage**: payroll **13.5%**, insurance **3.5%**, overhead+G&A **10.5%**.
% of **bill**: OGS fee **0.75%**.
```
wage       = bill / (1 + markup/100)            (for rank-driven pricing)
cost       = wage*(0.135+0.035+0.105) + bill*0.0075
net_profit = (bill - wage) - cost
net_margin = net_profit / bill
```
**Key inherited insight:** because cost loadings are a % of wage, **margin is driven by markup,
not the role**: ~1–2% net at 30% markup, ~11% at 45%.

---

## 3. Decoding KBI's pricing formula

**KBI = "Knowledge Builders Inc."**, Federal ID `20-3057365`. They are the **perennial #1 winner**:

| Year | KBI placements | KBI $ |
|---|---|---|
| 2023 | 107 | $78.0M |
| 2024 | 81 | $26.8M |
| 2025 | 129 | $55.7M |
| **Total** | **317** | **$160.5M** |

That's **~2× the #2 vendor** (MVP, 161). KBI wins every year.

### KBI's formula (decoded from the rate data)
```
bill = sourced_wage × 2.10            (a FIXED 110% markup)
```
- **Markup = 110%, dead constant** across all 372 rows (stdev 0.025%).
- **Wage rank ≈ #6 of 32** — KBI pays among the **lowest wages** in the field. *This is their weapon.*
- **Bill rank ≈ #21 of 32 (median)** — i.e. KBI sits in the **upper/expensive half** on price.
- **Net margin ≈ 38.5%** (~$25.50/hr profit) under our cost model.

### The bombshell
KBI **does not win on price.** Concrete example — Programmer / Region 1 / Senior:
- KBI: wage **$34.11** (lowest on the board) → bill **$71.63**, rank **#16**.
- Cheapest bidder RMS: wage $42.37 → bill $61.44.

KBI pays the lowest wage but bills mid-pack, because of the 2.1× markup. **The "MSP forwards only
the cheapest 50%, so be cheap" premise behind V1.1 does not explain the actual winner.** KBI wins on
**incumbency + recruiter bench + fulfillment volume + relationships**, while charging mid-pack and
pocketing a fat margin.

### KBI vs Best Pegasus V1.1 (same bill lane, opposite economics)
| | KBI | BP V1.1 |
|---|---|---|
| Bill rank | #21 | #19 |
| Markup | 110% | 30% (assumed) |
| **Net margin** | **38.5%** | **1.2%** |
| **Profit/hr** | **$25.50** | **$0.76** |

**KBI makes ~33× more profit per hour at a similar bill rank.**

---

## 4. V1.1 vs KBI — the formula difference (one idea)

The two models run in **opposite directions** — same equation `bill = wage × (1+markup)`, different
term held constant:

| | BP V1.1 (OLD) | KBI (decoded) |
|---|---|---|
| **Independent variable** | **Rank** (target #19) | **Wage** (lowest sourced) |
| Markup | 30% (assumed, derived) | **110% (fixed rule)** |
| Bill | solved to hit the rank | output of wage × markup |
| Rank | the input | output (~#21, ignored) |
| **Margin** | leftover ≈ **1%** | locked in ≈ **38%** |

- BP **fixes market position, lets margin float** → right lane, no profit.
- KBI **fixes margin, lets market position float** → same lane, with profit.

**The fix: flip the independent variable from rank → wage.**

---

## 5. The 2019-history question (blocked)

Asked: how did KBI price 2019→2025 and how is the YoY diff computed? **Not answerable from the repo:**
1. **Source PDFs are gitignored** (`.gitignore`: `Pricing document/`, `NYS OGS IT Vendor Rate
   Estimation.pdf`). They're the only artifacts with the 2019–2025 effective-date sections.
2. **The pipeline discards history** — `extract_rates.py` keeps only `latest = max(valid)` effective date.
3. **`vendors_rates.csv` has no date/year column** — every KBI row is one 2025 snapshot.

**What we can still infer about the mechanism:** since the **110% markup is a contracted constant**,
KBI's year-over-year price change is driven **only** by the wage:
```
Δbill (year N→N+1) = Δwage × 2.10
```
To actually chart it, re-add the KBI source PDF and modify `extract_rates.py` to keep *all*
effective-date sections (remove the latest-only filter, add a date column).

---

## 6. The database we built — `hbits.db`

**Input:** `C:\Users\ramat\Downloads\RFP 23311-20260607T152111Z-3-001.zip` (127 workbooks) —
the **win/closure side** of the market (complements the pricing side). Extracted to
`rfp_data/RFP 23311/`.

**What's in the zip:** per-vendor per-year "closure" pulls from *Open Book New York* (State
Comptroller award records); consolidated "All companies" files; a master
`Final Data of Jan 2023 to Dec 2025.xlsx` (1,664 records); `HBITS_31_Sheets_Complete_Data_Final.xlsx`
(bill-rate matrix, 31 title sheets); vendor contacts; old (31) + new Attachment-7 job titles.

Each closure record = one **task-order win**: vendor, agency, **$ amount**, dates, and a
`CONTRACT DESCRIPTION` that encodes **job title + skill level + county**.

### Build: `build_db.py` → `hbits.db` (SQLite)
**Tables**
- `vendors` (33; canonical_name + `norm_key`) · `vendor_aliases` · `vendor_contacts` (55)
- `job_titles` (49: 31 old + 18 new) 
- `closures` (1,663 wins; parsed `job_title/skill_level/county`, `year`, `is_hbits` flag)
- `rate_cards` (12,636; wage/bill/markup/is_our_rate/formula_version, from `vendors_rates.csv`)
- `bill_matrix` (11,904; from the 31-sheet workbook)

**Views:** `v_vendor_year_wins`, `v_title_demand`, `v_vendor_pricing_vs_wins`.

**Validation (all green):**
- Closures per year **560 / 506 / 597**; **KBI = 317** (matches the app's analytics exactly).
- **0 vendor keys unmatched** between wins and pricing (fixed Genesys "INC"-truncation + TEKsystems).
- `is_hbits`: **1,556 HBITS** awards, **107 non-HBITS** flagged out (e.g. "Google Cloud", amendments).
- Top demand roles (3 yrs): **Software Architect 336, IT Specialist 231, Software Developer 195**.

### Consumer API: `hbits_db.py`
```python
import hbits_db as h
h.vendor_wins()                 # wins + pricing per vendor (view-backed)
h.wins_by_year(h.vendor_key("Knowledge Builders"))
h.query("SELECT * FROM closures WHERE is_hbits=1 AND norm_key=?", ("KNOWLEDGE BUILDERS",))
```
`python hbits_db.py` prints the headline proof: **KBI wins most while being the most expensive /
highest-markup of the top winners** — wins are not driven by low price.

---

## 7. The backtest — `backtest.py`

Counterfactual replay over **1,488 real HBITS awards** (those with parsed title+skill that place
into a 32-vendor field; KBI = 295 of them). Field model: per (title,skill), each vendor's bill =
mean of its 3 regional NTE bills.

> **Caveats (built in):** we see only *winners*, not the full bid set, and rates are **NTE ceilings**;
> the field is approximated by the 32 contracted vendors. So absolute simulated win counts are
> directional, not literal forecasts.

### Layer 2 — does PRICE predict winning?
```
Winner's bill-rank among ~32 vendors:  median #17 (mean 16.1)
Winners who were the CHEAPEST bidder:   0.2%    (price-only market would be ~100%)
Winners in the cheapest 50%:           49.6%    (MSP-filter premise needs ~100%)
Winners in the EXPENSIVE half:         50.4%    (a coin flip)
KBI wins (295) at median bill-rank #17  (from the EXPENSIVE half)
=> VERDICT: PRICE IS NOT THE DRIVER. The V1.1 "be in the cheap half" premise is falsified.
```

### Layer 3 — insert Best Pegasus; score wins + profit (3 win-models)
Win-models: **H1** lowest-price wins · **H2** cheapest-50% forwarded (then uniform) · **H3**
empirical P(win | price-percentile) fit from real winners.

**Calibration (can each reproduce KBI's 295 real wins?)** — none can:
```
H1 lowest:  predicts KBI ~  0     H2 filter: ~ 37     H3 empirical: ~ 68     (actual 295)
```
→ The **~227-win gap is KBI's non-price moat** (incumbency / sourcing / fulfillment), unexplainable
by price.

**Scorecard (over the same 1,488 awards):**
| Strategy | H1 | H2 | H3 wins | Margin | Expected profit (H3) |
|---|--:|--:|--:|--:|--:|
| **KBI actual (benchmark)** | — | — | **295** | 38.5% | **$44.8M** |
| V1.1  rank19 / 30% markup | 0 | 0 | 73 | 1.2% | $0.3M |
| rank16 / 45% markup | 0 | 88 | 68 | 11.3% | $2.9M |
| **KBI-clone  wage / 110%** | 0 | 44 | 65 | **38.5%** | **$9.4M** |
| KBI-undercut  wage / 100% | 0 | 69 | 53 | 35.5% | $6.9M |

**Reading:** wins are roughly flat (~53–73) regardless of rank — *because price barely matters* —
but **profit swings ~30×**. The KBI-clone economics make ~30× the profit of V1.1 for the same wins.

---

## 8. The decision — adopt **V2 (margin-first)**  → `PRICING-MODEL.md`

**One line:** *Set the wage as low as you can source it, apply a fat fixed markup, and let the bill
land where it lands. Do not price to a target rank.*
```
bill = sourced_wage × (1 + markup)        markup ≈ 100–110% (fixed)
```
- **Independent variable = WAGE** (was: rank). Markup is a constant. Rank is an ignored output.
- **Defaults:** markup **110%** (floor 100%); wage in the **bottom quartile / ≈ KBI-floor**; bill
  **guardrail ≤ ~rank #21**; **min net margin ~35%**.
- **Guardrail rule:** *if the bill lands too expensive, lower the WAGE — never thin the markup.*
- **YoY escalation:** markup constant ⇒ `Δbill = Δwage × (1+markup)` — escalate the wage, re-apply markup.
- **What V2 does NOT solve:** KBI's ~227 non-price wins. Matching their *volume* is a sourcing /
  fulfillment / incumbency program, not a pricing change. V2 buys **margin parity**, not win-count parity.

Full spec, parameters, evidence, and decision log are in **`PRICING-MODEL.md`** (the authoritative
go-forward document).

---

## 9. V2 quotes produced

### Programmer — Expert (worked example)
Using KBI-floor wage as the sourced-wage proxy, +3% to 2026, markup 110% (R3→100% to hold the lane):

| Region | Sourced wage 2026 | Markup | **Quoted bill 2026** | Rank | Margin |
|---|--:|--:|--:|:--:|--:|
| R1 | $39.66 | 110% | **≈ $83.30** | ~#18/33 | 38.5% |
| R2 | $38.60 | 110% | **≈ $81.05** | ~#16/33 | 38.5% |
| R3 | $45.32 | 100% | **≈ $90.65** | ~#19/33 | 35.5% |

vs old V1.1 (~$85 at rank #19, **30% markup → ~1% margin**). **Same lane, ~30× the margin.**

### Full Expert bid sheet — `V2_2026_Expert_bid_sheet.csv`
All 31 titles × 3 regions (93 rows). Columns: `Job_Title, Skill, Region, Sourced_Wage_2026,
Markup_%, Quoted_Bill_2026, Bill_Rank, Field, Net_Margin_%`. Every role nets **~35–38%**. The
`Markup_%` column shows **110** (default) or **100** (guardrail pulled it down to hold rank ≤ #21).

> **Methodology note (important):** rank is judged at **parity** — BP's wage and the competitor field
> are compared on the same year basis (assume uniform escalation). An earlier first pass escalated
> only BP's wage against an un-escalated field, which falsely worsened rank; that was corrected.

---

## 10. Rate-trajectory CSVs (2021 / 2026 / 2029)

The user supplied the target table shape (example row: **Programmer / Junior → $35.74 / $44.08 /
$47.23**). The 2026 anchor = V1 baseline ($44.08 confirms it). Escalation factors reverse-engineered
from that row and applied uniformly:
```
2021 = 2026 × 0.8108   (≈ +4.29%/yr, 2021→2026)
2029 = 2026 × 1.0715   (≈ +2.33%/yr, 2026→2029)
```

### `Rate_Trajectory_2021_2026_2029.csv`  — **V1 baseline** trajectory
- 120 rows (30 titles × 4 skills; **no Business Analyst** — baseline omits it).
- Columns: `Job_Title, Skill_Level, Historical_2021_Rate, Bid_Year_2026_Rate, Target_Year_2029_Rate`.
- **This is V1 (cost-up), NOT the V2 model** — reproduces the user's example exactly.

### `V2_Rate_Trajectory_2021_2026_2029.csv`  — **V2 margin-first** trajectory
- 124 rows (**31 titles** incl. Business Analyst × 4 skills), Region 1 basis.
- 2026 = V2 quote (`KBI_wage × markup`; 110% default, 100% where rank would exceed #21); same
  escalation factors for 2021/2029.
- Extra columns: `Markup_Pct, Net_Margin_Pct, Bill_Rank_2026` — margins all **~35–38%** (vs ~1% in V1).

---

## 11. Project Manager spot-check vs KBI

(User gave our bills: **Senior $77.60, Expert $98.12.** Note: "Program Manager" → mapped to the
existing title **Project Manager**.)

| | Your bill | KBI bill | Gap | Your rank | KBI rank |
|---|--:|--:|--:|:--:|:--:|
| Senior R1 | $77.60 | $81.48 | −$3.88 (cheaper) | #14/33 | #25/32 |
| Senior R2 | $77.60 | $81.48 | −$3.88 | #16/33 | #27/32 |
| Senior R3 | $77.60 | $86.82 | −$9.22 | #4/33 | #27/32 |
| Expert R1 | $98.12 | $103.02 | −$4.90 (cheaper) | #27/33 | #29/32 |
| Expert R2 | $98.12 | $96.64 | +$1.48 (above) | #28/33 | #24/32 |
| Expert R3 | $98.12 | $103.02 | −$4.90 | #12/33 | #25/32 |

**On price you are NOT missing** — within ~$4–5 of KBI, often cheaper and better-ranked (Senior #14
vs KBI #25). KBI's wages here: **$38.80 (Sr) / $49.06 (Exp)** → 38.5% margin.

**The real gap is margin and depends on YOUR wage (still unknown):**
| If your wage is… | Your margin at $77.60 (Sr) | Verdict |
|---|--:|---|
| = KBI's $38.80 (the floor) | **35.5%** | ✅ matched the leader |
| = $59.69 (old V1 30%-markup) | **~1%** | ❌ gave the margin away |

**To finalize this comparison we need the wage your $77.60 / $98.12 are built on.**

---

## 12. Files created / modified this session

**New code/data (in repo root unless noted):**
- `build_db.py` — builds `hbits.db` from `rfp_data/` + `vendors_rates.csv`.
- `hbits.db` — the SQLite database (generated; gitignored).
- `hbits_db.py` — consumer API + demo over `hbits.db`.
- `backtest.py` — Layer-2 calibration + Layer-3 simulation vs KBI.
- `PRICING-MODEL.md` — **authoritative V2 model spec** (go-forward).
- `V2_2026_Expert_bid_sheet.csv` — V2 Expert quotes, 31 titles × 3 regions.
- `Rate_Trajectory_2021_2026_2029.csv` — V1 trajectory (120 rows).
- `V2_Rate_Trajectory_2021_2026_2029.csv` — V2 trajectory (124 rows).
- `SESSION-HANDOFF-KBI-ANALYSIS.md` — this document.
- `rfp_data/RFP 23311/...` — extracted source workbooks (gitignored).

**Modified:** `.gitignore` — added `rfp_data/` and `hbits.db` (heavy/generated).

**Inherited (unchanged) key sources:** `vendors_rates.csv`, `generate_csv.py`
(`BASELINE_2026_BILL`), `position_best_pegasus.py`, `positioning.html`.

---

## 13. Open items / next steps
1. **Real sourced wages** — the single most important missing input. All V2 numbers use KBI-floor
   wage as a proxy. Replace with audited recruiter costs to finalize bids.
2. **Real escalation rate** — `+3%` (Expert sheet) and `0.8108 / 1.0715` (trajectories) are
   derived/placeholder. Substitute the contracted Award-23158 escalation (or chosen CPI/IT index).
3. **Project Manager finalize** — supply the wage behind $77.60 / $98.12 to compute the true margin
   gap to KBI.
4. **Business Analyst** — absent from the V1 baseline (30 titles); present in V2 (31).
5. **KBI 2019→2025 history** — re-add the source PDF + un-gate `extract_rates.py` (keep all
   effective dates) to chart KBI's wage escalation (markup is constant).
6. **Non-price moat (~227 wins)** — quantify how much sourcing/fulfillment/incumbency improvement
   would close KBI's volume gap; this is an operations program, not a pricing change.
7. **Optional tooling:** wire V2 ("drive from wage", markup default 110%) into `positioning.html`;
   add a rank×markup profit-frontier sweep to `backtest.py`; produce an all-3-regions V2 trajectory.

---

## 14. How to reproduce everything
```bash
# 0. environment
pip install openpyxl            # (pdfplumber only needed to regenerate vendors_rates.csv from PDFs)

# 1. (source data) extract the RFP zip to rfp_data/RFP 23311/  — see §6

# 2. build the database
python build_db.py              # -> hbits.db  (prints validation: KBI=317, etc.)

# 3. explore wins vs pricing
python hbits_db.py              # demo: top vendors, KBI by year, demand by role

# 4. test our model against KBI
python backtest.py              # Layer 2 calibration + Layer 3 scorecard

# 5. run the web suite
python -m http.server 8000      # open http://localhost:8000/positioning.html (set markup ~110% for V2)
```
**Key constants** (in `backtest.py` / `build_db.py` / `PRICING-MODEL.md`): cost build payroll 13.5%,
insurance 3.5%, overhead+G&A 10.5% (% wage), OGS 0.75% (% bill); V2 markup 110% (floor 100%);
escalation 2021=×0.8108, 2029=×1.0715; KBI key in DB = `KNOWLEDGE BUILDERS`.

---
*End of handoff. The authoritative go-forward pricing spec is `PRICING-MODEL.md`; this file is the
narrative + evidence behind it.*
