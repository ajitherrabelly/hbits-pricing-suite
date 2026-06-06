# HBITS Pricing Project — Engagement Journal

A chronological record of what was built, the decisions made, and the rationale — captured so future
proposal efforts can reuse the approach. Companion to [PROPOSAL-PLAYBOOK.md](PROPOSAL-PLAYBOOK.md)
(the repeatable method) and [README.md](README.md) (the technical reference).

- **Program:** NYS OGS Group 73012 — Hourly-Based IT Services (HBITS), Award 23158 / Solicitation 23311
- **Our company:** Best Pegasus
- **Goal:** Consolidate every competitor's published rate card, see where we stand, set a defensible bid, and brief a pricing strategist.

---

## Phase 1 — Understand the source data
- **Did:** Read representative vendor pricing schedules (Computer Technology Services @ 11% markup, Sligo @ 47%) from `Pricing document/`.
- **Learned:** Each award-notice PDF (Attachment 1) lays out **3 regions side by side**, each listing Job Title · Skill Level · Hourly Wage · Hourly Bill, for **31 titles × 4 skill levels**. Each PDF contains **multiple effective-date sections** (2019–2025).
- **Decision:** Keep only each vendor's **latest effective date** = their current contracted NTE rate.

## Phase 2 — First app + datasource
- **Did:** Built `index.html` (region/skill/title filters, sortable table, our rates in **bold red**) reading a CSV.
- **Decision:** Start with a hand-built sample CSV (2 vendors) to validate the UI, then automate extraction.
- **Change:** Converted Job Title from a free-text box to a **dropdown** at the user's request.

## Phase 3 — Full extraction (all 32 vendors)
- **Did:** Installed `pdfplumber`; wrote `extract_rates.py` (regex row parser + latest-effective-date filter) and `generate_csv.py`.
- **Validated:** Every one of the **32 vendor cards parsed to exactly 372 rows** (31×4×3) — a strong correctness signal.
- **Fixes along the way:**
  - Vendors use either "Contractor Name:" **or** "Bidder Name:" → handled both.
  - Some markups genuinely **100%** (not a bug — Avenues, Greycell, etc.).
  - Rewrote the JS CSV parser to **RFC-4180** (vendor names like "OST, Inc." contain commas and broke naive `split(',')`).
  - Capped table rendering at 1,500 rows (12k DOM rows froze the page); rank still computed from the full set.
  - Hardened the sort comparator (string/number crash).
- **Result:** `vendors_rates.csv` ≈ 12,264 rows; **33 bidders per role** including Best Pegasus.

## Phase 4 — Positions dashboard
- **Did:** Added a **"Best Pegasus Positions"** tab — one row per Title×Region×Skill (372) with rank badge (#X of N), lowest bid, gap to #1, percentile, color-coded (green top third / amber mid / red bottom third / grey "not bid"), plus search + filters.
- **Insight surfaced:** Under the original baseline, Best Pegasus sat in the **expensive third** (e.g., Programmer/R1/Senior = #26 of 33), largely because many incumbents' rates are pre-2025 and un-escalated.

## Phase 5 — Rank-positioning formula (the strategy change)
- **Request:** Price Best Pegasus to the **19th position** in every role.
- **Did:** `position_best_pegasus.py` — for each combo, sort the 32 competitor bills and place us between the 18th and 19th cheapest ⇒ **rank #19 of 33** (18 below, 14 above).
- **Outcome:** **356/372** roles hit exactly #19; **16/372** land at **#18** because the 18th and 19th cheapest competitors are **tied** (exact #19 mathematically impossible) — nearest, more-competitive rank used.
- **Bonus:** Because the rule only needs competitor data, the **Business Analyst gap was filled** (the baseline estimation doc omitted it).

## Phase 6 — Interactive Bid Builder
- **Did:** Built `positioning.html` — live **Target Rank** input (recomputes all 372 rates instantly), per-role recommended bill/wage/rank, and **CSV export** of the bid sheet.

## Phase 7 — Two preserved versions
- **Request:** Keep the old formula as **Version 1 (baseline)** and the new one as **Version 1.1**, switchable.
- **Did:** Added a `Formula_Version` column; `build_dataset.py` assembles competitors + V1 (baseline doc, 30 titles) + V1.1 (rank-#19, 31 titles). Added **version tabs** to `index.html` so the whole app re-ranks per version.

## Phase 8 — Side-by-side + margin model
- **Did:** Enhanced the Bid Builder with **V1-vs-V1.1 columns + delta** and an **interactive margin/profit estimate** (editable cost build: payroll 13.5%, insurance 3.5%, overhead+G&A 10.5% of wage; OGS fee 0.75% of bill; markup sets wage).
- **Insight:** Net **margin is driven by markup, not the role** (cost loadings are % of wage): ~1–2% at 30% markup, ~11% at 45%.

## Phase 9 — Version control
- **Did:** Wrote `README.md`; committed; (initially pushed to `github.com/ajitherrabelly/memory` baseline branch).
- **Reversed:** User chose **local-only** → deleted the remote branch (repointed the repo default to an empty `main`, then removed `baseline`), removed the `origin` remote. Project is now **local git, never pushed**.

## Phase 10 — Strategy briefing for the pricing strategist
- **Did:** `briefing.html` — a 13-section quality-review page (context, MSP filter, story, formulas, V1/V1.1, data provenance, live snapshot, margin, landscape, **10-item quality-test checklist**, risks, glossary). Fixed a duplicate-`id` bug that wiped a section.

## Phase 11 — Shareable deliverables
- **Did:** `make_deliverables.py` (fpdf2 + python-pptx) → **HBITS_Pricing_Strategy_Briefing.pdf** (6-page handout) and **.pptx** (14-slide deck) for WhatsApp/email sharing.

---

## Key decisions & rationale

| Decision | Rationale |
|----------|-----------|
| Use each vendor's **latest effective date** | That is their current contracted ceiling rate. |
| **Rank-#19** target (mid-field) | Balance margin vs. competitiveness; tunable. |
| Tie fallback to **#18** | Exact #19 impossible when boundary competitors tie; favor the more competitive side. |
| Keep **two versions** | Preserve the cost-up baseline for audit while adopting the market-relative strategy. |
| Margin = markup-driven | Cost loadings are % of wage, so markup is the real lever. |
| **Local-only** git | User preference; no remote. |

## The unresolved strategic question (flagged for the strategist)
**Rank #19 of 33 is in the upper half** of bidders. The MSP forwards only the **lowest ~50%** on high-volume task orders, so a #19 rate could be **filtered out before technical review**. The briefing recommends evaluating a **tiered rank target** (≤16 for commodity/high-supply roles, higher for scarce roles that bypass the filter).

## Artifacts produced
`index.html` · `positioning.html` · `briefing.html` · `vendors_rates.csv` ·
`extract_rates.py` · `generate_csv.py` · `position_best_pegasus.py` · `build_dataset.py` · `make_deliverables.py` ·
`README.md` · `PROJECT-JOURNAL.md` · `PROPOSAL-PLAYBOOK.md` · `HBITS_Pricing_Strategy_Briefing.pdf` / `.pptx`

## Open items / next steps
- Decide target rank **per role tier** (commodity ≤16 to clear the filter).
- **Escalate stale competitor rates** to 2026 equivalents (CPI) before ranking.
- Replace assumed wage / cost loadings with **audited rates**.
- Model **multi-year (5+2) margin decay** (CPI escalation vs. IT wage inflation).
