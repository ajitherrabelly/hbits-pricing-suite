# HBITS Pricing Model — Version 2.0
## Margin-First Strategy (V2) vs. Legacy Rank-Based Model (V1)

**Document Date:** June 7, 2026  
**Status:** APPROVED - Production Ready  
**Applies to:** NYS OGS Group 73012 (HBITS), Solicitation 23311, Awards 23158+  
**Analysis Source:** Reverse-engineered from KBI ("Knowledge Builders Inc.") — 317 wins, $160.5M (2023-2025)

---

## Executive Summary

**V1 (Legacy):** Rank-based pricing targeting position #19 in market → **~1.2% net margin**, thin profitability  
**V2 (NEW):** Margin-first pricing with fixed 110% markup, wage-driven billing → **35-38% net margin**, 30× more profit

### The Model Switch

| Dimension | V1.1 (Old) | V2 (New) |
|-----------|-----------|---------|
| **Independent Variable** | Market rank (target #19) | Sourced wage (lowest quartile) |
| **Markup** | ~30% (derived, thin) | **110% fixed** (proven winner) |
| **Bill Rate** | Solved to hit rank | Output of wage × markup |
| **Net Margin** | ~1.2% (leftover) | **35-38% (locked in)** |
| **Profit per Hour** | ~$0.76/hr | **~$25.50/hr** |
| **Competitiveness** | Rank #19 (transparent rank) | Rank #21 (median, competitive) |

**Key Insight:** KBI wins not on price, but on incumbency + fulfillment while keeping massive margins. V2 adopts KBI's economics while maintaining competitive bill positioning.

---

## V2 Core Formula

### Standard Bill Rate Calculation

$$\text{Bill Rate} = \text{Sourced Wage} \times (1 + \text{Markup\%})$$

**Where:**
- **Sourced Wage** = lowest-cost recruiter rate for the role in that region/year
- **Markup** = 110% (fixed constant, floor 100% to hold rank guardrail)
- **Bill Rate** = Not-To-Exceed rate submitted to customer

### Example: Programmer, Expert, Region 1 (2026)

| Component | Value | Notes |
|-----------|-------|-------|
| Sourced Wage 2026 | $39.66/hr | KBI-floor proxy; assume +3% YoY from baseline |
| Markup % | 110% | Fixed constant; 100% if rank would exceed #21 |
| **Bill Rate 2026** | **$83.30/hr** | $39.66 × 2.10 |
| Bill Rank | ~#18/33 | Competitive (not cheap, not expensive) |
| **Net Margin %** | **38.5%** | Gross profit divided by bill |

---

## Cost-Load Model (Unchanged from V1)

This cost decomposition applies to both V1 and V2:

$$\text{Cost} = \text{Wage} \times (13.5\% + 3.5\% + 10.5\%) + \text{Bill} \times 0.75\%$$

### Cost Components

| Component | % of Wage | Notes |
|-----------|-----------|-------|
| **Payroll Taxes** | 13.5% | FICA, FUTA, SUTA (NY-specific) |
| **Insurance** | 3.5% | Workers' comp, GL, E&O, cybersecurity |
| **Overhead + G&A** | 10.5% | Recruiting, applicant tracking, admin |
| **Total Wage Burden** | 27.5% | Cost as % of wage |
| **OGS Fee** | 0.75% of bill | Pass-through (fixed, mandated) |

### Margin Calculation

$$\text{Net Margin \%} = \frac{\text{Bill} - \text{Wage} - \text{Cost}}{\text{Bill}}$$

#### V1.1 Example (30% markup)
- Bill: $100.00
- Wage: $76.92 (derived: bill / 1.30)
- Cost: $30.13 (27.5% wage + OGS)
- **Net Margin: 1.2%** ← **Thin profitability**

#### V2 Example (110% markup, same $83.30 bill)
- Bill: $83.30
- Wage: $39.66 (known, externally sourced)
- Cost: $18.93 (27.5% wage + OGS)
- **Net Margin: 38.5%** ← **Healthy profitability**

---

## KBI's Discovered Formula (Benchmark)

**Federal ID:** 20-3057365  
**Market Performance:** 317 wins, $160.5M (2023-2025), #1 vendor every year

### KBI's Pricing Law

$$\text{Bill} = \text{Sourced Wage} \times 2.10 \quad (\text{fixed 110\% markup})$$

### KBI's Competitive Position

- **Wage Rank:** #6 of 32 (among the lowest — their sourcing advantage)
- **Bill Rank:** #21 of 32 (median, not cheap, but profitable)
- **Net Margin:** 38.5% (~$25.50 profit per hour at typical rates)

### Why KBI Wins

**Not on price** — KBI sits at median rank #21, yet:
1. Incumbency + customer relationships
2. Recruiter bench (stable, fast fulfillment)
3. Volume scale (wins attract more wins)
4. Fat margins fund the above three

**V1.1 premise is falsified:** The "MSP awards to the cheapest bidders" assumption does not hold. 50.4% of winners come from the *expensive half* of the market.

---

## V2 Implementation Rules

### 1. Wage Rule (Independent Variable)

**Source your wage from the lowest-cost recruiter floor** for that role/region. 

- **Proxy:** Use KBI's demonstrated wage as a floor benchmark (they're the #1 winner, so their sourcing is proven)
- **Escalation:** Year-over-year wage change is your primary P&L driver
  ```
  bill(year N) = bill(year N-1) × (1 + wage_escalation%)
  ```
  (Markup constant ⇒ bill changes exactly as wage changes)

### 2. Markup Rule (Fixed, Defended)

**Default: 110% (1.10 multiplier)**  
**Floor: 100% (1.00 multiplier)** — only if rank guardrail triggers

**Never thin the markup.** If your bill lands too expensive:
- Lower the wage estimate, do not lower the markup
- If you can't source cheaper, don't bid the role

### 3. Rank Guardrail (Defensive)

**If bill rank would exceed #21 after applying 110% markup:**
- Drop markup to 100% and re-solve
- If rank still > #21, reject the pricing (don't force it)

**Guardrail logic:** Stay competitive but not cut-rate; 100% markup still yields 35.5% net margin (vs 1.2% in V1).

### 4. Year-over-Year Escalation

$$\text{bill}(year N) = \text{wage}(year N) \times (1 + 1.10)$$

- Escalate the wage (based on recruiter cost inflation + BLS wage index)
- Re-apply the fixed 110% markup
- Bill automatically escalates with wage; no separate escalation assumption

**Example:**
- 2026: wage $39.66 → bill = $39.66 × 2.10 = $83.30
- 2027: wage $40.85 (+3% inflation) → bill = $40.85 × 2.10 = $85.79

---

## V2 Bid Sheet Example (All Titles, Region 1, 2026)

### Excerpt: Programmer (all skills)

| Job Title | Skill | Sourced Wage 2026 | Markup % | Quoted Bill 2026 | Rank | Net Margin % |
|-----------|-------|-----|--------|---------|------|------|
| Programmer | Junior | $23.40 | 110% | $49.14 | #8 | 38.5% |
| Programmer | Mid-Level | $31.20 | 110% | $65.52 | #12 | 38.5% |
| Programmer | Senior | $39.66 | 110% | $83.30 | #18 | 38.5% |
| Programmer | Expert | $49.65 | 110% | $104.27 | #26 | 38.5% |

**Key:** All roles yield **35-38% net margin** (110% markup default, 100% only if guardrail triggers).

**Compare to V1.1:** All roles at ~1.2% margin.

---

## V1 vs V2: The Shift

### What V2 Solves
✅ **Margin parity with KBI** — locked-in 35-38% profit per hour  
✅ **Competitive bill positioning** — rank #21 (median), not cheap but not expensive  
✅ **Scalable profitability** — margin doesn't erode with volume; grows with wage escalation control  
✅ **Simple decision rule** — "source the cheapest wage, apply 110%, ship it" — no ranking math  

### What V2 Does NOT Solve
❌ **Win volume vs KBI** — KBI wins 295 real awards; V2 pricing captures maybe ~65-73 under neutral H3 win-model. The ~227-win gap is **non-price moat** (incumbency, fulfillment, relationships). That's an **operations program**, not pricing.

---

## Financial Impact: V2 vs V1.1

**Scenario: 100 FTEs over 3 years at Programmer/Senior rates**

| Metric | V1.1 | V2 | Delta |
|--------|------|----|----|
| Bill Rate (2026) | $85.00 | $83.30 | −$1.70 (cheaper) |
| Wage (implied) | $65.38 | $39.66 | −$25.72 (V2 sources cheaper) |
| Net Margin % | 1.2% | 38.5% | +3,708 bps |
| Profit/hour | $0.76 | $25.50 | ×33.6 |
| **3-Year Profit (100 FTEs)** | **$0.5M** | **$16.8M** | **+$16.3M** |

*Assumptions: 2,080 hrs/FTE/yr, bill constant/year (no escalation), 100% utilization, same bill rank.*

---

## Open Items & Next Steps

1. **Real Sourced Wages** — Replace KBI-floor proxy with audited recruiter cost data
2. **Escalation Rate Confirmation** — Lock in the exact wage inflation rate (current assumption: +3% YoY)
3. **All-Regions Bid Sheet** — Extend V2 to Regions 2 and 3 (current: Region 1 basis)
4. **Business Analyst Inclusion** — Add the missing title (present in V2, absent from V1 baseline)
5. **Website Migration** — Update positioning.html to default markup 110% (V2 mode); add V2 bid sheet

---

## Key Data Files (V2.0)

- **`V2_2026_Expert_bid_sheet.csv`** — All 31 titles, 3 regions, 2026 quotes, markup/margin columns
- **`V2_Rate_Trajectory_2021_2026_2029.csv`** — 124 rows (31 titles × 4 skills), wage-indexed escalation
- **`backtest_scorecard.json`** — Simulation results (H1/H2/H3 win-models, profit by strategy)
- **`hbits.db`** — SQLite database: vendor wins, closures, rate cards, demand by role

---

## References & Validation

- **KBI Analysis:** Reverse-engineered from 12,264 rate-card rows + 1,663 closure wins  
- **Backtest Data:** 1,488 real HBITS awards, 295 KBI wins (matched)
- **Cost Model:** Inherited from V1; validated against OGS budget guidelines (13.5% payroll, etc.)

---

**Version:** 2.0  
**Last Updated:** June 7, 2026  
**Status:** Production Ready  
**Next Review:** Q3 2026 (post-Award-23311 first year)
