---
name: hbits-pricing-calculator
description: Calculate bill rates, markup decomposition, and 7-year profitability for NYS OGS HBITS bids. Use this skill whenever you're preparing a competitive pricing proposal for Solicitation 23311, analyzing vendor bids, modeling cost structure, forecasting margin decay, or stress-testing pricing assumptions against labor inflation. Supports HBR_NTE calculations, fully burdened cost-load decomposition, CPI escalation modeling, financial score evaluation, strategic headroom multiplier application, and multi-year profitability stress tests. Essential for Pricing Directors and Capture Managers evaluating HBITS contract strategy.
---

# HBITS Pricing Calculator

## What This Skill Does

This skill automates the mathematical frameworks for NYS OGS HBITS (Hourly-Based Information Technology Services) competitive pricing. It implements the formulas and methodologies from the **Comprehensive Competitive Pricing and Bidding Strategy Report for NYS OGS HBITS Solicitation 23311**, translating strategic pricing intent into executable calculations.

### Core Capabilities

1. **Bill Rate Calculation** – Apply the core HBITS equation (HBR_NTE = HWR × (1 + M)) to compute not-to-exceed hourly rates from wage bases and markup percentages
2. **Cost-Load Decomposition** – Break down markup percentages into their statutory and operational components (payroll taxes, insurance, G&A, OGS admin fee, profit)
3. **Multi-Year Escalation** – Model annual CPI-U adjustments over the 7-year contract lifecycle and forecast margin erosion under wage inflation scenarios
4. **Financial Score Modeling** – Evaluate competitive positioning by calculating financial proposal scores relative to market basket benchmarks
5. **Strategic Headroom Analysis** – Apply the 4.0% strategic multiplier to historical baseline rates and analyze the sensitivity to wage inflation assumptions
6. **Profitability Stress Testing** – Simulate contract performance across 7 years under varying wage inflation, candidate churn, and labor market scenarios; identify break-even wage escalation thresholds

## When to Use This Skill

**Use this skill when:**
- Preparing a master contract pricing proposal for Solicitation 23311
- Analyzing a competitor's pricing strategy from their awarded rates
- Building or validating a fully burdened cost model for an IT staffing organization
- Forecasting margin decay under different wage inflation scenarios
- Determining whether a submitted markup percentage is defensible over 7 years
- Reverse-engineering vendor bid strategy from historical award data
- Evaluating the sensitivity of profitability to labor market tightness or candidate retention

**Example scenarios:**
- "We're bidding a 30% markup. Under what wage inflation rate does our margin fall below 5%?"
- "The historical baseline for Senior Java Developer in NYC was $95/hour. What's our recommended NTE rate using the 4% headroom multiplier?"
- "We've identified three subcontractors at $52/hour. What's the blended bill rate if we apply a 32% markup?"
- "The lowest bidder's average NTE rate was $110/hour. What financial score does our $115/hour average earn?"

## Core Formulas

### Bill Rate Equation

$$HBR_{NTE} = HWR \times (1 + M)$$

Where:
- **HBR_NTE** = Not-To-Exceed Hourly Bill Rate (the ceiling rate charged to agencies)
- **HWR** = Hourly Wage Rate (minimum wage floor, legally binding)
- **M** = Markup Percentage (as decimal; e.g., 0.30 for 30%)

### Fully Burdened Markup Decomposition

$$M = T_{payroll} + I_{insurance} + O_{overhead} + A_{fee} + P_{profit}$$

Where:
- **T_payroll** = Statutory Payroll Taxes (FICA, FUTA, SUTA) — typically 12.0% to 15.0%
- **I_insurance** = Workers' comp, GL, professional liability, cybersecurity — typically 2.0% to 5.0%
- **O_overhead** = Corporate G&A, recruiting, applicant tracking, background checks — typically 8.0% to 15.0%
- **A_fee** = OGS Administrative Fee — fixed at 0.75% (0.0075 as decimal)
- **P_profit** = Target Net Profit Margin — typically 8.0% to 18.0%

**Key insight:** The OGS fee is non-negotiable; all other components are cost-driven. Profitability depends entirely on controlling overhead and defending against wage inflation erosion.

### CPI Escalation Over Contract Years

$$HBR_t = HBR_{t-1} \times (1 + \Delta CPI_t)$$

Where:
- **HBR_t** = Bill rate for contract year *t*
- **HBR_{t-1}** = Bill rate for prior contract year
- **ΔCPI_t** = Percentage change in CPI-U for year *t* (published by Bureau of Labor Statistics)

**Critical compliance note:** Contractors must notify OGS no earlier than 90 calendar days and no later than the first day of the month prior to the contract year start date. Missing this window forfeits the adjustment for that year.

### Financial Score Calculation

$$FS_i = 30 \times \left(\frac{\text{Lowest Avg NTE HBR}}{\text{Avg NTE HBR}_i}\right)$$

Where:
- **FS_i** = Financial score awarded to bidder *i* (out of 30 points)
- **Lowest Avg NTE HBR** = The average rate of the lowest bidder in the market basket
- **Avg NTE HBR_i** = This bidder's average rate in the market basket

The market basket is pre-determined by OGS and consists of specific combinations of Job Titles, Skill Levels, and Regions. Bidders don't know the exact composition during bid preparation.

### Strategic Headroom Multiplier

$$NTE_{Recommended} = \text{Historical Avg} \times 1.04$$

The 4.0% headroom multiplier (1.04 scaling factor) is applied to predecessor contract historical baseline rates. This provides:
- Margin buffer for wage escalation above baseline
- Flexibility to discount at Task Order level to win placements
- Competitive protection while maintaining operational defensibility

## How to Use This Skill

### Scenario 1: Calculate Bill Rates from Cost Components

**Task:** Determine an appropriate NTE rate for a Senior Systems Administrator position given cost structure and profit targets.

**Provide:**
- Submitted minimum hourly wage rate (HWR)
- Desired markup percentage (M), or cost components to decompose

**What the skill will do:**
1. Apply HBR_NTE = HWR × (1 + M) to calculate the rate
2. Optionally, decompose the markup into components (payroll taxes, insurance, overhead, OGS fee, profit) to show where each dollar goes
3. Validate that the markup is within strategic range (28%–34% for HBITS)
4. Flag if overhead or profit assumptions are unrealistic given contract volume

**Example:**
```
HWR: $85/hour
Markup: 32% (0.32)
Calculation: $85 × 1.32 = $112.20/hour NTE

Cost Decomposition:
  Payroll Taxes:     13.5% ($11.48)
  Insurance:          3.5% ($2.97)
  Overhead:          10.0% ($8.50)
  OGS Fee:            0.75% ($0.64)
  Profit:             4.25% ($3.61)
  ─────────────────────────────
  Total Markup:      32.0% ($27.20)
```

### Scenario 2: Apply Strategic Headroom Multiplier to Baseline Rates

**Task:** Given historical baseline rates from the predecessor HBITS contract, calculate recommended NTE rates with 4% strategic headroom.

**Provide:**
- Historical average bill rate for specific job title + skill level + region (from Award 23158 data)
- Optionally, wage inflation assumptions for validation

**What the skill will do:**
1. Apply the 4.0% multiplier: NTE_Recommended = Historical_Avg × 1.04
2. Show the absolute headroom (dollars and cents)
3. Estimate the implied wage inflation "cushion" (how much wage inflation this headroom can absorb before margin erosion begins)
4. Recommend regional adjustments if labor market tightness varies by geography

**Example:**
```
Historical Baseline (Senior Java Developer, Level 4, NYC):  $95.00/hour
Strategic Multiplier:                                        1.04 (4%)
Recommended NTE Rate:                                        $98.80/hour
Headroom (Absolute):                                         $3.80/hour
Headroom (Percentage):                                       4.0%

Wage Inflation Cushion Analysis (assuming 32% fixed markup):
  If wage inflation averages 2.5% annually:                  Margin remains healthy
  If wage inflation averages 4.0% annually:                  Margin erodes ~2% per year
  If wage inflation exceeds 5.0% annually:                   Profitability at risk
```

### Scenario 3: Model CPI Escalation and Margin Decay

**Task:** Forecast contract revenue and margin over the 7-year cycle, accounting for annual CPI adjustments and wage inflation.

**Provide:**
- Starting NTE rate (from Year 1 master bid)
- Starting cost (wage + fully burdened markup)
- Annual CPI escalation rates (or average assumption, e.g., 2.5% annually)
- Wage inflation rates (often diverge from CPI; e.g., IT wages inflate faster)
- Whether you plan to submit CPI adjustments annually (important: missing the notification window forfeits the year)

**What the skill will do:**
1. Project Year 1–7 bill rates using CPI-U adjustments
2. Project Year 1–7 wage costs using wage inflation assumptions
3. Calculate realized gross margin in each year
4. Identify the year where margin falls below acceptable threshold (e.g., 5%)
5. Calculate cumulative margin erosion and present the risk profile

**Example:**
```
Year 1 (2026):   NTE $120.00,  Wage $85.00,  Margin 41.2% ($35.00),  Profitable ✓
Year 2 (2027):   NTE $122.88,  Wage $87.20,  Margin 40.9% ($35.68),  Profitable ✓
Year 3 (2028):   NTE $125.84,  Wage $89.52,  Margin 40.5% ($36.32),  Profitable ✓
Year 4 (2029):   NTE $128.87,  Wage $91.97,  Margin 40.0% ($36.90),  Profitable ✓
Year 5 (2030):   NTE $131.99,  Wage $94.53,  Margin 39.5% ($37.46),  Profitable ✓
Year 6 (2031):   NTE $135.19,  Wage $97.22,  Margin 39.0% ($37.97),  Profitable ✓
Year 7 (2032):   NTE $138.49,  Wage $100.04, Margin 38.4% ($38.45),  Profitable ✓

⚠️  Wage inflation exceeded CPI by 2.0% average (wage +3.5%, CPI +2.3%)
    Monitor candidate retention; premium wages may narrow margin faster than forecast
```

### Scenario 4: Calculate Financial Score vs. Market Basket

**Task:** Evaluate your competitive position by estimating your financial proposal score relative to the lowest bidder in the master evaluation.

**Provide:**
- Your average NTE rate across the OGS market basket (if known or estimated from selected job categories)
- Lowest competitor's average NTE rate (from market intelligence or historical benchmark)
- Number of categories you're bidding (for sensitivity analysis)

**What the skill will do:**
1. Calculate your financial score using FS_i = 30 × (Lowest / Yours)
2. Show the score delta and what the difference means in terms of overall bid competitiveness
3. Estimate how much you'd need to lower rates to reach specific score targets (27, 28, 29 points)
4. Assess whether the gap is worth closing via rate reduction vs. accepting a lower financial score

**Example:**
```
Your Average NTE Rate:           $112.50/hour
Lowest Competitor Average:       $108.00/hour
Your Financial Score:            30 × (108 / 112.5) = 28.8 points

Score Assessment:
  If financial score weights 30 points total:         You earn 28.8 of 30 (96%)
  Gap to perfect score:                               1.2 points
  To earn 29.0 points, you'd need average:            $111.72/hour (reduce by $0.78)
  Margin impact of $0.78 reduction at 32% markup:     ~$0.55 margin per hour

Recommendation: The 1.2-point gap is likely NOT worth the 0.55/hour margin compression.
Maintain your rate unless technical scoring is weak and financial is your differentiator.
```

### Scenario 5: Stress-Test Profitability Against Wage Inflation

**Task:** Identify the wage inflation threshold above which your submitted pricing becomes unprofitable.

**Provide:**
- NTE rate (from master bid)
- Starting wage cost
- Markup percentage
- Minimum acceptable profit margin (e.g., 5%)
- 7-year contract horizon with or without annual CPI adjustments

**What the skill will do:**
1. Calculate the implied wage inflation "break-even" rate (the annual wage escalation where margin = minimum threshold)
2. Show year-by-year profitability under three scenarios:
   - Conservative (wage inflation = CPI-U)
   - Moderate (wage inflation = CPI-U + 1.5%)
   - Aggressive (wage inflation = CPI-U + 3.0%)
3. Recommend risk mitigation strategies if wage inflation sensitivity is high

**Example:**
```
Base Case (NTE $120, Wage $85, 32% Markup, Min Margin 5%):

Break-Even Analysis:
  Wage inflation threshold (margin falls to 5%):      ~4.8% annually
  Historical IT wage inflation (BLS data):            ~3.5% annually
  Your margin cushion:                                ~1.3 percentage points

Scenario Results (Year 7):
  Conservative (2.3% CPI, wages +2.3%):              Margin 37.8% ✓ Safe
  Moderate (2.3% CPI, wages +3.8%):                  Margin 32.5% ✓ Acceptable
  Aggressive (2.3% CPI, wages +5.3%):                Margin 27.2% ⚠  At Risk

Risk Assessment:
  Wage inflation > 4.8% annually puts profitability at risk.
  Mitigation: Consider billing at Task Order level below ceiling to compress costs,
  or build subcontractor network to diversify labor sourcing.
```

## Input Format Guide

When you use this skill, provide information in one of these formats:

### For Bill Rate Calculations
```
Job Title: Senior Java Developer
Location: New York City
Wage Rate: $95/hour
Markup Percentage: 32%
```

### For Cost Decomposition
```
Target Bill Rate: $120/hour
Desired Profit Margin: 10%
Payroll Taxes: 13.5%
Insurance: 3.5%
Corporate Overhead: 10.0%
(OGS Fee is fixed at 0.75%)
```

### For CPI Escalation Models
```
Starting NTE Rate: $120/hour
Starting Wage: $85/hour
Markup: 32%
Years: 7
Average Annual CPI-U: 2.3%
Average Annual Wage Inflation: 3.5%
Submit CPI Adjustments Annually: Yes
```

### For Financial Score Analysis
```
Your Average NTE Rate: $112.50
Market Basket Categories: 15
Lowest Competitor Rate (estimated): $108.00
```

### For Profitability Stress Testing
```
NTE Rate: $120/hour
Base Wage: $85/hour
Markup: 32%
Minimum Acceptable Profit Margin: 5%
Contract Years: 7
Wage Inflation Scenarios: 2.5%, 3.5%, 5.0%
```

## Key Assumptions and Constraints

### Statutory Constraints (Non-Negotiable)

- **OGS Administrative Fee:** Fixed at 0.75% (0.0075) of all contract sales. This is mandated by New York State and cannot be negotiated.
- **CPI Adjustment Window:** Contractors must notify OGS no earlier than 90 calendar days and no later than the first day of the month before the contract year. Missing this window forfeits adjustment for that year—a material risk.
- **Single-Tier Subcontracting Restriction:** All subcontractors contract directly with the prime; no secondary chains. SDVOB utilization goal is 6%.

### Pricing Ranges (Strategic, Not Absolute)

- **Markup Percentages:** Typically 28%–34% for competitiveness and profitability. Below 28% risks negative margin under wage inflation; above 34% risks uncompetitive financial scoring.
- **Payroll Taxes:** 12.0%–15.0% (New York State W-2 contractors); varies by SUTA experience rating.
- **Insurance:** 2.0%–5.0% (workers' comp, GL, professional liability, cybersecurity); higher for specialized roles.
- **Corporate Overhead:** 8.0%–15.0%; decreases as a percentage of revenue at higher volume.
- **Profit Margin:** 8.0%–18.0%; depends on contract size, risk profile, and competitive positioning.

### Labor Market Assumptions

- **Wage Inflation vs. CPI:** IT labor typically inflates 1–3 percentage points faster than CPI-U. Conservative models assume wage inflation = CPI + 1.5%.
- **Regional Variation:** NYC and high-cost metros see faster wage inflation and higher baseline rates; secondary metros lag by 5–10%.
- **Skill-Based Variation:** Commodity roles (e.g., Help Desk) inflate in line with CPI; specialized roles (Security, Cloud Architecture) inflate faster due to scarcity.

## Workflow for Pricing Directors

**Step 1: Cost Model Validation**
Use the decomposition tool to validate your fully burdened cost model. Ensure all cost components are accounted for and that assumptions (overhead, profit target) are realistic for your organization.

**Step 2: Historical Baseline Analysis**
Use the strategic headroom tool to analyze predecessor contract rates. Apply the 4.0% multiplier to establish your NTE ceiling rates. This becomes your master bid submission.

**Step 3: Financial Score Positioning**
Use the financial score calculator to estimate your competitive position. Benchmark against historical averages and market intelligence. Decide whether your rates are defensible in the evaluation or need adjustment.

**Step 4: Multi-Year Profitability Forecast**
Use the CPI escalation and stress-testing tools to forecast margin decay over 7 years. Identify risk years and break-even wage inflation thresholds. Develop mitigation strategies (e.g., Task Order discounting, subcontractor leverage, labor sourcing optimization).

**Step 5: Risk Mitigation Planning**
If profitability risk is high (wage inflation sensitivity), plan hedges: diversified subcontractor network, geographic volume balance to spread overhead, selective discounting strategy at Task Order level to win high-margin segments.

## Output Formats

All calculations are presented in clear, tabular format suitable for executive presentation:

- **Bill Rate Calculations:** Simple formula application with cost decomposition
- **Financial Score Analysis:** Competitive positioning table with score scenarios
- **Multi-Year Forecasts:** Year-by-year profit/loss projection with margin trend
- **Stress Test Results:** Side-by-side scenario comparison with break-even analysis
- **Risk Assessment:** Qualitative summary with mitigation recommendations

## Troubleshooting & Edge Cases

**Q: What if I don't know the exact OGS market basket composition?**  
A: Use industry benchmarks and your best estimate of Job Title + Skill Level mix. The financial score tool will show sensitivity to rate assumptions, helping you understand downside risk.

**Q: Can I submit different markup percentages by region?**  
A: Yes. The instructions explicitly allow "regionally specific, fixed Markup Percentage." Different regions can have different labor costs and overhead structures.

**Q: What if our wage inflation actually exceeds the stress-test scenario?**  
A: That's a profitability risk you must accept in a fixed-rate contract. Mitigation options: (1) negotiate higher rates in Task Order negotiations, (2) focus on high-margin segments, (3) build labor sourcing partnerships to control wage costs, (4) consider exit if margins become unsustainable.

**Q: Do I have to submit CPI adjustments every year?**  
A: No, but missing the notification window forfeits that year's adjustment. The skill will flag the regulatory window and suggest a tracking mechanism. **Strongly recommended:** Set a calendar reminder 100 days before each year-start to avoid forfeiture.

**Q: How do I know if my 32% markup is "safe" for 7 years?**  
A: Use the stress-testing tool with your local wage inflation assumption. Run three scenarios (conservative, moderate, aggressive). If your margin stays above 5% in the moderate scenario, you're defensible.

---

## Reference

For the complete strategic framework, cost model methodology, and historical benchmark data, refer to:
- **Comprehensive Competitive Pricing and Bidding Strategy Report for NYS OGS HBITS Solicitation 23311** (source document)
- **HBITS-PRICING-FORMULA.md** (this repository's pricing formula reference)

For BLS wage and inflation data:
- Bureau of Labor Statistics Occupational Employment and Wage Statistics (OES): https://www.bls.gov/oes/
- Consumer Price Index (CPI-U): https://www.bls.gov/cpi/

---

**Last Updated:** June 6, 2026  
**Expertise Required:** Federal & State Government Procurement, IT Staff Augmentation Pricing, Contract Financial Analysis
