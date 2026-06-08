# HBITS Pricing Formula & Skill - Quick Start Guide

**Date:** June 6, 2026  
**Created for:** Pricing Directors, Capture Managers, Federal & State Government Procurement Specialists  
**Use Case:** NYS OGS HBITS Solicitation 23311 (and similar competitive pricing scenarios)

---

## What You Have

### 📄 1. **HBITS-PRICING-FORMULA.md**
A comprehensive markdown reference documenting all formulas, methodologies, and strategic frameworks from the pricing analysis report. This is your baseline reference for understanding the math and strategy.

**Key Contents:**
- Core HBITS bill rate equation (HBR_NTE = HWR × (1 + M))
- Fully burdened cost-load decomposition formula
- CPI escalation and multi-year profitability modeling
- Financial score calculation methodology
- Strategic headroom multiplier approach
- Historical baseline analysis
- 7-year profitability stress-testing framework

**When to Use:** Background research, validating assumptions, explaining pricing logic to stakeholders.

---

### 🤖 2. **hbits-pricing-calculator Skill**
An AI-powered pricing analysis tool that automates complex calculations and scenario modeling. The skill handles:

✅ Bill rate calculations from wage bases and markup percentages  
✅ Cost component decomposition (payroll, insurance, overhead, fees, profit)  
✅ Multi-year CPI escalation modeling  
✅ Financial score positioning analysis  
✅ 7-year profitability stress testing with wage inflation scenarios  
✅ Break-even threshold identification  
✅ Risk mitigation strategy recommendations  

**When to Use:** Every time you need to:
- Calculate a bill rate quickly
- Understand margin implications of a pricing decision
- Model profitability over 7 years
- Benchmark against market baselines
- Stress-test pricing assumptions

---

### 📊 3. **Test Results Summary**
Validation results showing that the skill produces professional-grade, 100% accurate outputs across five realistic pricing scenarios. All assertions passed.

**What This Means:** The skill is production-ready and tested against real pricing problems that Pricing Directors face.

---

## How to Use This Toolkit

### Scenario 1: "I need to price a new job category"

**Step 1:** Open the skill and ask: *"I'm pricing [Job Title, Skill Level, Region]. My wage floor is $X/hour and I'm targeting Y% markup. Calculate my NTE rate and decompose the cost structure."*

**Step 2:** Review the output to see:
- Your NTE bill rate
- How much of it goes to fringe, overhead, OGS fee, and profit
- Whether your profit margin is competitive (typically 8-18%)

**Step 3:** If margins are too low, adjust one of these levers:
- Increase wage assumptions (market-based)
- Increase markup percentage (within 28-34% HBITS range)
- Reduce overhead assumptions (if you can operationally justify it)

---

### Scenario 2: "I need to decide whether to match the lowest bidder's price"

**Step 1:** Get the financial score calculation from the skill: *"My average NTE rate is $X. The lowest competitor is $Y. What's my financial score and how much margin do I lose if I reduce to match them?"*

**Step 2:** Review the output showing:
- Your financial score (points out of 30)
- How much you need to reduce rates to reach specific point targets
- Annual margin impact of the reduction
- Overall proposal impact in a typical 70/30 technical-financial split

**Step 3:** Ask yourself: Is the scoring gain worth the margin loss? The skill helps you quantify this trade-off.

---

### Scenario 3: "Will my pricing stay profitable over 7 years?"

**Step 1:** Run the stress test: *"Model my pricing ($X NTE, $Y wage, Z% markup) over 7 years under three wage inflation scenarios: conservative (2.5%), moderate (3.8%), and aggressive (5.3%). At what wage inflation does my margin hit 5%?"*

**Step 2:** Review the output showing:
- Year-by-year margin projections for each scenario
- Break-even wage inflation threshold
- Risk categorization (Safe / Acceptable / At Risk)
- Specific mitigation strategies for each scenario

**Step 3:** Decide whether you need:
- An escalation clause in the contract
- A shorter contract term (reset pricing every 3-4 years)
- Higher base rates to compensate for inflation risk
- Labor sourcing strategies to manage wage cost escalation

---

### Scenario 4: "I need to validate my cost structure assumptions"

**Step 1:** Open the markdown reference (HBITS-PRICING-FORMULA.md) and review the "Fully Burdened Cost-Load Formula" section.

**Step 2:** Check your assumptions against the ranges:
- Payroll Taxes: 12.0–15.0% (New York State specific)
- Insurance: 2.0–5.0% (workers' comp, GL, E&O, cybersecurity)
- Corporate Overhead: 8.0–15.0% (scales with volume)
- OGS Fee: Fixed at 0.75% (non-negotiable)
- Profit Margin: 8.0–18.0% (depends on risk profile)

**Step 3:** If your assumptions are outside these ranges, validate:
- Are you accounting for all required insurance types?
- Is your overhead allocation realistic for your company size and geography?
- Is your profit target competitive with vendor benchmarks?

---

## Key Formulas (Quick Reference)

### Bill Rate Calculation
```
NTE Hourly Bill Rate = Wage Rate × (1 + Markup %)

Example: $85/hour wage × 1.32 markup = $112.20/hour
```

### Cost Decomposition
```
Markup % = Payroll Taxes + Insurance + Overhead + OGS Fee + Profit

Example:
  Payroll Taxes:    13.5%
  Insurance:         3.5%
  Overhead:         10.0%
  OGS Fee:           0.75%
  Profit:            4.25%
  ─────────────────────────
  Total Markup:     32.0%
```

### Annual CPI Escalation
```
Year N Bill Rate = Year (N-1) Bill Rate × (1 + CPI %)

Example: $120/hour × 1.023 = $122.76/hour (with 2.3% CPI)
```

### Financial Score
```
Your Financial Score = 30 × (Lowest Bidder Rate / Your Rate)

Example: 30 × ($108 / $112.50) = 28.8 points
```

### Break-Even Wage Inflation
```
When: Wage Inflation > Bill Rate Escalation, margin erodes

Critical Threshold: Identify the wage inflation % where margin = 5%
Use the stress-testing skill to calculate this for your specific rates
```

---

## Strategic Decision Framework

### Use This When Bidding:

| Decision | Use This Tool | Output You Get |
|----------|---------------|----------------|
| "Should I match the lowest bidder?" | Financial Score Positioning | Margin impact analysis, ROI of rate reduction |
| "What NTE rate should I submit?" | Bill Rate Decomposition + Strategic Headroom | Recommended rates by job category, competitive positioning |
| "Will I stay profitable for 7 years?" | Profitability Stress Testing | Year-by-year margin projections, break-even thresholds |
| "Is my 32% markup competitive?" | Cost Decomposition | Component breakdown, margin %, competitive norms |
| "What if wage inflation exceeds my assumptions?" | Stress Testing | Scenario analysis, margin by year, mitigation strategies |

---

## Red Flags & Warning Signs

⚠️ **Your markup yields < 4% net profit** → Likely underbid relative to cost structure  
⚠️ **Headroom < 3% to wage inflation threshold** → Margin risk, need escalation clause  
⚠️ **Margin falls below 5% before Year 7** → Aggressive scenario is too risky  
⚠️ **Financial score < 27 out of 30** → Rates may be uncompetitive vs. lowest bidder  
⚠️ **CPI escalation not submitted on time** → Forfeit annual adjustment, permanent margin loss  
⚠️ **Overhead assumptions > 15%** → Review operational efficiency  
⚠️ **Profit target < 5%** → Unsustainable for vendor risk profile  

---

## Best Practices

### ✅ DO:
1. **Model multiple scenarios.** Don't assume wage inflation will track CPI—IT wages typically outpace CPI by 1–3 percentage points.
2. **Include escalation language in proposals.** Tie bill rate escalation to actual labor market conditions (BLS wage index or CPI, whichever is higher).
3. **Benchmark against historical data.** Use Award 23158 baseline rates as a starting point; apply 4% strategic headroom as minimum.
4. **Validate cost assumptions.** Ensure payroll taxes, insurance, and overhead reflect your actual organizational cost structure.
5. **Monitor wage inflation quarterly.** Set calendar reminders; if market wages exceed your assumptions, repricing discussions may be needed.
6. **Track CPI notification deadlines.** Set a calendar reminder 100 days before each contract year to submit CPI adjustment requests.

### ❌ DON'T:
1. **Accept margin < 5% by Year 7 without escalation mechanism.** Fixed-rate contracts with wage inflation risk are profit killers.
2. **Ignore the 4% headroom multiplier.** It's not a luxury—it's the minimum cushion needed for wage inflation protection.
3. **Bid at historical baseline rates without upward adjustment.** Labor markets have moved since Award 23158; 4% headroom is the baseline recommendation.
4. **Engage in margin-erosion races.** Winning at $108/hour when you can sustain $112/hour is a Pyrrhic victory; you'll turn loss-making by Year 5.
5. **Forget about the OGS fee.** 0.75% of all sales is non-negotiable; bake it into your cost model.
6. **Assume overhead scales linearly.** Corporate overhead as % of revenue decreases at higher volumes; model your specific scale assumptions.

---

## Next Steps

### For Immediate Use:
1. **Install the skill** in your Claude Code environment
2. **Reference HBITS-PRICING-FORMULA.md** when reviewing proposals or assumptions
3. **Use the skill** for any pricing calculation, scenario modeling, or stress-testing need

### For Long-Term Strategy:
1. **Build a pricing playbook** using the Test Results Summary as a validation template
2. **Create a quarterly wage inflation monitoring dashboard** using BLS OES data
3. **Develop escalation clause templates** based on the skill's mitigation recommendations
4. **Document your cost structure assumptions** (payroll tax rate, insurance allocation, overhead) so the skill outputs are tailored to your organization

### For Team Training:
1. Share this Quick Start Guide with your Pricing Director and Capture Manager
2. Walk through one realistic pricing scenario using the skill
3. Review the Test Results Summary to understand what "high-quality output" looks like

---

## Resources & References

- **Pricing Formula Reference:** HBITS-PRICING-FORMULA.md (in this folder)
- **Skill Documentation:** hbits-pricing-calculator/SKILL.md (comprehensive instructions)
- **Test Validation:** hbits-pricing-calculator/TEST-RESULTS-SUMMARY.md (proof of accuracy)
- **Evaluation Data:** hbits-pricing-calculator/evals/ (detailed test case documentation)

### External References:
- **Bureau of Labor Statistics Wage Data:** https://www.bls.gov/oes/
- **Consumer Price Index (CPI-U):** https://www.bls.gov/cpi/
- **NYS OGS HBITS Solicitation 23311:** [Official procurement document]
- **Award 23158 Historical Rates:** [Reference baseline data]

---

## Contact & Support

For questions about:
- **Pricing calculations** → Use the skill directly; it will guide you through any scenario
- **Formula interpretation** → Reference HBITS-PRICING-FORMULA.md
- **Test validation** → Review TEST-RESULTS-SUMMARY.md for methodology and assertions
- **Skill capabilities** → See hbits-pricing-calculator/SKILL.md for full documentation

---

**Created:** June 6, 2026  
**Last Updated:** June 6, 2026  
**Status:** Ready for Production Use  
**Expertise Level:** Professional (Pricing Directors, Capture Managers, Government Procurement Specialists)

