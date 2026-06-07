# Best Pegasus — Pricing Model V2 (Margin-First / KBI-Aligned)

**Status:** ✅ Adopted — supersedes V1 (cost-up) and V1.1 (rank-#19 positioning).
**Program:** NYS OGS Group 73012 — HBITS, Award 23158 / Solicitation 23311.
**Basis:** Decoded from the market leader (Knowledge Builders, "KBI") and validated by a
counterfactual backtest over 1,488 real HBITS awards (2023–2025). See [Evidence](#evidence).

---

## 1. The one-line model

> **Set the wage as low as you can source it, apply a fat fixed markup, and let the bill rate
> land where it lands. Do _not_ price to a target rank.**

```
bill = sourced_wage × (1 + markup)         markup ≈ 100–110%   (fixed)
```

Wage is the **only** variable you optimize. Markup is a constant. Rank is an *output* we ignore.

---

## 2. Why we changed (the decision)

| | V1.1 — OLD (rank #19) | **V2 — NEW (margin-first)** |
|---|---|---|
| Independent variable | **Rank** (target #19) | **Wage** (lowest sourced) |
| Markup | 30% (assumed) | **~100–110% (fixed)** |
| Bill rate | solved to hit rank #19 | output of wage × markup |
| Net margin | **~1%** | **~38%** |
| Profit/hr | $0.76 | $25.50 |

V1.1 solved for the wrong variable. It chased a market position that **the data proves buys
no extra wins**, and in doing so collapsed margin to ~1%. V2 fixes margin first — the way the
perennial winner (KBI) actually prices.

---

## 3. Evidence

Backtest over **1,488 real HBITS awards** (`build_db.py` → `hbits.db` → `backtest.py`):

**A. Price does not drive winning.**
- Only **0.2%** of winners were the cheapest bidder (a price-driven market would be ~100%).
- Winners split **49.6% cheap half / 50.4% expensive half** — a coin flip.
- KBI wins from the **expensive half** (median bill-rank **#17 of 32**).

**B. No price model explains KBI — their moat is non-price.**
- Price position justifies **≤68** of KBI's wins; KBI actually won **295**.
- The ~227-win gap = incumbency + recruiter bench + fulfillment speed + agency relationships.

**C. Wins are flat across rank; profit swings ~30×.**

| Strategy | Sim. wins (empirical) | Margin | Expected profit |
|---|---|---|---|
| KBI actual (benchmark) | 295 | 38.5% | $44.8M |
| V1.1 rank19 / 30% | 73 | 1.2% | $0.3M |
| rank16 / 45% | 68 | 11.3% | $2.9M |
| **KBI-clone — wage / 110%** | 65 | **38.5%** | **$9.4M** |
| KBI-undercut — wage / 100% | 53 | 35.5% | $6.9M |

Same wins, ~30× the profit. **Discounting buys nothing; margin is the only lever that pays.**

---

## 4. How to apply V2 (per role: Title × Region × Skill)

1. **Source the wage.** Establish the lowest defensible pay rate you can recruit at for the role.
   Target the **bottom ~quartile** of the competitor wage field (KBI sits ~#6 of 32 on wage).
   *This is the real work — a sourcing/recruiting capability, not a spreadsheet input.*
2. **Apply the fixed markup.** `bill = wage × (1 + markup)`, **markup = 110%** (default).
3. **Sanity-check the bill, don't target it.** Confirm the resulting bill is **≤ ~rank #21**
   of the field (KBI's neighborhood). If it lands more expensive than that, the fix is a
   **lower wage**, *never* a thinner markup.
4. **Confirm margin.** Net margin should clear **~35%** at the default cost build (§5).
   If it doesn't, the wage or markup is wrong — re-source, don't discount.

### Default parameters

| Parameter | Default | Notes |
|---|---|---|
| Markup | **110%** | Fixed, contract-life constant (matches KBI). Floor 100%. |
| Wage target | bottom ~quartile of field | The competitive weapon. |
| Bill guardrail | ≤ ~rank #21 of 32 | Output check, not a target. |
| Min net margin | ~35% | Below this, re-source the wage. |

---

## 5. Margin / cost model (unchanged from the Bid Builder)

% of **wage**: payroll taxes **13.5%**, insurance **3.5%**, overhead + G&A **10.5%**.
% of **bill**: OGS fee **0.75%**.

```
cost      = wage × (0.135 + 0.035 + 0.105) + bill × 0.0075
net_profit = (bill − wage) − cost
net_margin = net_profit / bill
```

Because cost loadings are a % of wage, **margin is driven by markup, not the role** — which is
exactly why a low wage × fat markup wins the economics.

---

## 6. Year-over-year escalation

Markup is a **contracted constant**, so the annual price change is driven **only** by the wage:

```
Δbill (year N→N+1) = Δwage × (1 + markup)
```

Escalate the wage (CPI / IT-wage index); re-apply the same multiplier. Do not re-derive a rank.

---

## 7. What this model does NOT solve

Price gets us **margin parity** with KBI, but not their **win volume**. KBI's ~227 unexplained
wins come from non-price strengths. To rival their volume, invest in:
- **Sourcing** — a cheaper, faster recruiter bench (lets the wage go lower → guardrail holds).
- **Fulfillment** — speed and fill-rate on task orders.
- **Incumbency / relationships** — agency presence that bypasses price entirely.

**V2 makes every win profitable; closing the volume gap is an operations program, not a pricing one.**

---

## 8. Tooling

| File | Role |
|---|---|
| `build_db.py` → `hbits.db` | Builds the DB (closures/wins + rate cards + contacts + titles). |
| `hbits_db.py` | Consumer API over the DB. |
| `backtest.py` | Validates strategy vs KBI on real awards (wins + profit, 3 win-models). |
| `positioning.html` | Bid Builder — set markup ~110% and drive from wage to operate V2. |

Re-validate any change with: `python build_db.py && python backtest.py`.

---

## 9. Decision log

- **2026-06-07** — Adopted V2 (margin-first). Decoded KBI = low wage (rank ~#6) × fixed 110%
  markup → ~38% margin. Backtest confirmed price doesn't drive wins; V1.1's rank-#19/30%-markup
  yields ~1% margin for the same wins. Switched the independent variable from **rank → wage**.

*Persona: Federal & State Government Pricing / Capture analysis, IT staff-augmentation RFPs.*
