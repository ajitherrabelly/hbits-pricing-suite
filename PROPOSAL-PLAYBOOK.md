# Government IDIQ Pricing Playbook — Competitive Rate Positioning

A repeatable method for pricing a fixed-bill-rate, price-filtered government staff-augmentation vehicle (built for
NYS OGS HBITS, but generalizable). Use this to stand up a competitive pricing model and stakeholder briefing for the
next proposal. Companion to [PROJECT-JOURNAL.md](PROJECT-JOURNAL.md) (what we did) and [README.md](README.md) (the tooling).

---

## 0 · When this applies
- The vehicle publishes **competitor pricing** (award notices / pricing schedules).
- Bill rates are **fixed/NTE** and **non-negotiated** at task-order level.
- A **price filter** (MSP or evaluator) screens candidates by rate **before** technical review.
- Pricing spans a **matrix** (job titles × skill levels × regions).

If those hold, competitive position — not absolute cost — usually decides win rate.

---

## 1 · Gather the field
- Collect every awarded competitor's **pricing schedule** (Attachment 1 or equivalent) + your own baseline estimate.
- Note the **matrix dimensions** (titles, skill levels, regions) and any **markup %** disclosed.
- **Watch for multiple effective dates** in each file — keep only each vendor's **latest** (their current ceiling).

## 2 · Extract to a single datasource
- Parse the PDFs to rows: `Contractor, Federal_ID, Region, Job_Title, Skill_Level, Wage, Bill, Markup, Is_Our_Rate, Formula_Version`.
- Tooling: `pdfplumber` + a regex row parser (see `extract_rates.py`).
- **Correctness check:** every vendor should yield the same row count (titles × skills × regions). A mismatch means a parse error.
- Handle real-world quirks: label variants ("Contractor Name" vs "Bidder Name"), commas inside names (use an **RFC-4180** CSV parser everywhere), genuinely high markups (e.g. 100%).

## 3 · Understand the evaluation mechanics (the most important step)
Document exactly how candidates get screened. For HBITS the **MSP price filter** is:
| Pool size | What's forwarded |
|-----------|------------------|
| 10–40 candidates | lowest **50%** of bill rates (+ any within 1% of the cutoff) |
| 6–10 candidates | the **5 lowest** bill rates |
| ≤5 candidates | **all** (filter bypassed) |

**Implication:** to survive a high-volume task order you must be in the **lower half** of the field. This is the constraint your target rank must respect.

## 4 · Choose a positioning strategy
Two complementary models (keep both — version them with a `Formula_Version` column):
- **V1 — Cost-up baseline:** your internal estimate (labor benchmarks × escalation). Good for audit/floor, but blind to the field.
- **V1.1 — Market-relative rank target:** place each rate at a chosen **rank** among all bidders.

### The rank-positioning formula
For each combo, sort competitor bills ascending `c(1) … c(n)`. To land at **rank R** (R−1 competitors below you):
```
choose B*  such that  c(R-1) < B* < c(R)
B* = midpoint( c(R-1), c(R) ), at whole cents, nudged so exactly R-1 are strictly below and none tie.
```
If `c(R-1) == c(R)` (tie), exact R is impossible → fall back to the **nearest, more-competitive** rank. (Implemented in `position_best_pegasus.py`; `TARGET_RANK` is the single knob.)

### Pick R against the filter, not by gut
- **Commodity / high-supply roles** (Business Analyst, Tester, Technical Writer, Graphic Designer): pools exceed 10 → must be in the **lowest ~50%** → choose **R ≤ ~n/2**.
- **Scarce roles** (Cloud Engineer, Architects, Security Manager): pools often ≤5 → filter bypassed → you can sit higher and **protect margin**.
- A single flat R (e.g. #19 of 33) is simple but **risks being filtered on commodity roles** — prefer a **tiered R by role scarcity**.

## 5 · Core pricing math
```
HBR_NTE = HWR × (1 + Markup/100)              # bill = wage grossed up by markup
CPI escalation %: (CPI_t − CPI_t-12)/CPI_t-12 × 100   # file manually each anniversary or forfeit
```
Escalation is **not automatic** — build a workflow to file within the window (e.g. 90 days pre-anniversary) with index sheets.

## 6 · Margin / cost-build check
```
Net profit  = (bill − wage) − wage×(payroll + insurance + overhead+G&A) − bill×OGSfee
Net margin% = Net profit / bill × 100
```
Reference loadings (replace with **audited** rates): payroll 13.5%, insurance 3.5%, overhead+G&A 10.5% (of wage); OGS fee 0.75% (of bill).
- **Key property:** because loadings are % of wage, **margin is set by markup, not the role**.
- Rules of thumb at market-positioned rates: ~30% markup → ~1–2% net; ~45% markup → ~11% net.
- **Trade-off:** higher markup = healthier margin **but** lower payable wage (recruiting risk) **and** higher bill (filter risk). Solve consciously.

## 7 · Quality-test checklist (hand to the strategist)
1. **Does the target rank survive the price filter?** (must be in the lowest ~50% for high-volume roles)
2. **Are competitor benchmarks current?** Escalate stale/un-escalated rates to bid-year equivalents before ranking.
3. **Flat vs tiered rank** by role scarcity.
4. **Margin vs recruiting** trade-off validated against real wage data.
5. **Audited cost build** (replace assumptions).
6. **Multi-year margin decay** (escalation usually trails IT wage inflation).
7. **Tie-affected roles** acceptable?
8. **Data completeness** — full awarded pool?
9. **Region modeling** — per-region competitor sets distinct?
10. **Escalation compliance** workflow in place?

## 8 · Brief stakeholders
- Build a transparent briefing (context → mechanics → formula → data → margins → **checklist** → risks). See `briefing.html`.
- Produce shareable **PDF + PPTX** (`make_deliverables.py`) for team/strategist distribution.

---

## Pitfalls & lessons learned
- **Naive CSV parsing breaks on vendor names with commas** — always use a quote-aware parser.
- **Rendering 10k+ rows freezes the browser** — cap rendering; compute ranks from the full set.
- **"Latest effective date" ≠ same year across vendors** — un-escalated incumbents look artificially cheap; this distorts ranking.
- **A flat rank target ignores the filter** — mid-field can mean filtered-out on commodity roles.
- **Margin is a markup decision**, not a per-role one.
- **Don't trust a source estimate's title coverage** — ours omitted Business Analyst; the market-relative method filled it.

## Tooling & commands
```bash
pip install pdfplumber fpdf2 python-pptx
python generate_csv.py          # extract competitors + embed V1 baseline
python position_best_pegasus.py # (optional) reprice V1.1 to TARGET_RANK in place
python build_dataset.py         # assemble vendors_rates.csv with V1 + V1.1
python make_deliverables.py     # PDF + PPTX briefing
python -m http.server 8000      # then open index.html / positioning.html / briefing.html
```

## Reusable assets
| File | Reuse for |
|------|-----------|
| `extract_rates.py` | Parsing any OGS-style Attachment 1 pricing schedule |
| `position_best_pegasus.py` | Rank-targeting against any competitor field (`TARGET_RANK`) |
| `build_dataset.py` | Versioned multi-formula datasource |
| `index.html` / `positioning.html` / `briefing.html` | Comparison, bid building, stakeholder briefing |
| `make_deliverables.py` | One-command PDF + PPTX briefing |
