# NYS OGS HBITS Pricing Formula & Bidding Strategy

**Solicitation:** NYS OGS Group 73012 (HBITS - Hourly-Based Information Technology Services)  
**Document:** Comprehensive Competitive Pricing and Bidding Strategy Report for NYS OGS HBITS Solicitation 23311  
**Date:** June 6, 2026

---

## Table of Contents

1. [Mathematical Formulation of Rates and Evaluation Mechanics](#mathematical-formulation-of-rates-and-evaluation-mechanics)
2. [Fully Burdened Cost-Load Formula](#fully-burdened-cost-load-formula)
3. [Multi-Year Escalation and CPI Price Update Model](#multi-year-escalation-and-cpi-price-update-model)
4. [Master Contract Financial Scoring Mechanics](#master-contract-financial-scoring-mechanics)
5. [Historical Average Hourly Bill Rates](#historical-average-hourly-bill-rates)
6. [Master Bid Pricing Estimations](#master-bid-pricing-estimations)
7. [Strategic Bidding Summary](#strategic-bidding-summary)

---

## Mathematical Formulation of Rates and Evaluation Mechanics

### Overview

To establish an optimized pricing schedule for the Master Contract, the bidding entity must implement a rigorous cost-load modeling process. This mathematical framework must balance the competitive need to secure a high financial score in the master bid evaluation against the operational necessity of protecting candidate wage margins over a five-to-seven-year contract lifecycle.

### The Core HBITS Bill Rate Equation

The master pricing structure operates on a mathematically bound relationship where the **Not-To-Exceed Hourly Bill Rate** (HBR<sub>NTE</sub>) is calculated by applying a bid regional **Markup Percentage** (M) to a submitted minimum **Hourly Wage Rate** (HWR):

$$HBR_{NTE} = HWR \times (1 + M)$$

#### Key Constraints

- The submitted Hourly Wage Rate represents a **legally binding minimum wage floor** under the HBITS contract terms
- The selected contractor is prohibited from paying a candidate an hourly wage lower than the bid HWR associated with that job title, region, and skill level
- While contractors may pay a candidate a wage higher than the floor rate to attract premium talent, the Hourly Bill Rate paid by the utilizing agency remains fixed at the Task Order bid rate
- **Consequence:** Any premium paid to the candidate directly reduces the contractor's realized markup, transforming rate estimation into a critical exercise in risk management

---

## Fully Burdened Cost-Load Formula

### Framework

To determine a sustainable and profitable **Markup Percentage** (M), the bidding entity must construct a fully burdened cost model that incorporates statutory payroll taxes, insurance, corporate overhead, contract-specific administrative fees, and target profit margins.

$$M = T_{payroll} + I_{insurance} + O_{overhead} + A_{fee} + P_{profit}$$

### Cost Components

#### Statutory Payroll Taxes (T<sub>payroll</sub>)

- **Scope:** For professional W-2 IT contractors in New York State, the employer's portion of payroll taxes includes FICA, FUTA, and SUTA
- **Range:** Typically 12.0% to 15.0% of direct wages, depending on SUTA experience ratings
- **Applicability:** Mandatory under federal and state labor law; non-negotiable in cost models

#### Insurance (I<sub>insurance</sub>)

- **Components:** Reflects the cost of workers' compensation, commercial general liability, professional liability (errors and omissions), and cybersecurity insurance policies
- **Mandate:** Attachment 4 of the solicitation mandates coverage levels for all contractor classes
- **Range:** Typically 2.0% to 5.0% of payroll
- **Strategic Note:** Cybersecurity insurance requirements have expanded; budget accordingly for specialized policies

#### Corporate Sourcing and G&A Overhead (O<sub>overhead</sub>)

- **Scope:** Covers recruiter compensation, applicant tracking system licenses, job board postings, background checks, and administrative overhead
- **Operational Reality:** Includes overhead for client relationship management, contract administration, and financial control
- **Range:** Typically 8.0% to 15.0% of payroll
- **Scaling Consideration:** G&A as a percentage of revenue decreases with contract volume; larger contract awards may sustain lower overhead ratios

#### OGS Administrative Fee (A<sub>fee</sub>)

- **Mandate:** New York State mandates that contractors remit a quarterly administrative fee
- **Calculation:** Three-quarters of one percent (0.75%, or 0.0075) of all contract sales, including both executive and non-executive agency placements
- **Timing:** Quarterly submission to OGS; non-compliance results in contract suspension risk

#### Target Profit Margin (P<sub>profit</sub>)

- **Definition:** Net profit as a percentage of direct wage cost
- **Strategic Range:** Typically 8.0% to 18.0%, depending on contract size, market positioning, and risk profile
- **Consideration:** Profit margins erode over the contract life due to fixed-rate ceilings and escalating labor costs; conservative assumptions are prudent for long-term viability

---

## Multi-Year Escalation and the CPI Price Update Model

### Contract Escalation Mechanism

Because the contract spans up to seven years, the Master Contract contains a **Consumer Price Index adjustment mechanism**. Contractors are permitted to apply for an annual price adjustment based on the percentage change in the CPI for All Urban Consumers (CPI-U), U.S. City Average, as published by the Bureau of Labor Statistics.

The adjusted Hourly Bill Rate for contract year *t* is calculated as:

$$HBR_t = HBR_{t-1} \times (1 + \Delta CPI)$$

### Regulatory Requirements for CPI Adjustments

- **Notification Window:** Contractor must notify the OGS HBITS Team via email no earlier than 90 calendar days and no later than the first day of the month prior to the start date of the contract year
- **Supporting Documentation:** Failure to submit supporting documentation within this regulatory window results in forfeiture of the rate adjustment for that contract year
- **Risk Factor:** Contractors who miss the CPI notification window lose revenue recovery, amplifying margin compression in high-inflation years

### Profitability Decay Analysis

**Critical Risk:** Even with annual CPI adjustments, profitability erodes if:
- Wage inflation exceeds CPI inflation (common in IT labor markets)
- Subcontractor costs escalate faster than the master bill rate
- Candidate retention requires premium wages above the negotiated floor

**Recommendation:** Model scenarios where wage inflation runs 200-300 basis points above CPI-U to stress-test margin sustainability across the seven-year contract cycle.

---

## Master Contract Financial Scoring Mechanics

### Financial Proposal Weight

The master bid evaluation allocates **thirty points** to the Financial Proposal. This score is evaluated based on a pre-determined, undisclosed "market basket" composed of high-utilization combinations of Job Titles, Skill Levels, and Regions.

### Scoring Formula

The bidder with the lowest average Not-To-Exceed Hourly Bill Rate within the market basket receives the maximum financial score of 30 points. All other responsive bidders receive a proportional score calculated as:

$$FS_i = 30 \times \left(\frac{\text{Lowest Average NTE HBR}}{\text{Average NTE HBR}_i}\right)$$

Where FS<sub>i</sub> is the financial score awarded to bidder *i*.

### Strategic Pricing Implications

- **Ceiling Risk:** Because the Master Contract establishes a maximum ceiling rate rather than a fixed placement rate, bidders must strategically evaluate their NTE pricing
- **Low Bid Risk:** Bidding too close to historical averages risks a low financial score during master contract evaluation, while bidding excessively low NTE ceilings may severely restrict the vendor's ability to source qualified talent in high-inflation labor markets over the seven-year lifecycle
- **Qualification Window:** The evaluation team uses each bidder's submitted NTE Hourly Bill Rates for these specific combinations to calculate an average bid rate; undervaluation of high-demand skill categories can yield a low financial score

### Contractor Risk Management

- Avoid submitting floor-level rates for niche or specialized roles where wage inflation is historically volatile
- Consider a tiered pricing strategy: conservative NTE rates for commodity roles (high volume, lower inflation risk) and higher rates for specialized categories (lower volume, wage inflation sensitive)
- Use historical wage trends and BLS occupational projections to stress-test the sustainability of submitted rates across the seven-year term

---

## Historical Average Hourly Bill Rates (Master Baseline)

### Baseline Source and Effective Date

To establish a baseline for competitive pricing analysis, the bidding entity must analyze the historical market-clearing rates from the predecessor **HBITS contract, Award 23158**. The historical average hourly bill rates, effective July 1, 2025, represent the **actual average rates paid by New York State utilizing agencies for staff augmentation** across the three geographic regions.

### Data Reference

Historical baseline rates are derived from contract performance data spanning the previous HBITS contract period. These baseline rates serve as the **Master Baseline** for evaluating bidder pricing competitiveness and compliance with NYS procurement policies.

### Strategic Consideration

Simply quoting the legacy historical averages as NTE ceiling rates presents substantial operational risks:
- Inflationary wage shifts or technical skill shortages over the contract's seven-year lifecycle could render the ceiling rates too low to source qualified candidates
- Bidders who merely match historical averages risk bidding at or below their actual cost of delivery, eroding profitability
- The financial score calculation is relative to the market basket; a bidder matching historical averages may not score competitively if other bidders submit lower NTE rates

---

## Master Bid Pricing Estimations (Recommended NTE Rates)

### Strategic Pricing Adjustment Framework

To formulate a complete, actionable, and competitive pricing proposal for master contract submission under Solicitation 23311, the bidding entity must establish **defensive Not-To-Exceed Hourly Bill Rates**. Simply quoting the legacy historical averages as NTE ceiling rates presents substantial operational risks, as inflationary wage shifts or technical skill shortages over the contract's seven-year lifecycle could render the ceiling rates too low to source qualified candidates.

### Strategic Headroom Multiplier

Therefore, a **strategic pricing adjustment must be applied**. The bidding entity should utilize a **Strategic Headroom Multiplier (H)** of **4.0%** (a 1.04 scaling factor) applied directly to the historical averages. This provides the necessary margin buffer at the contract ceiling level while maintaining a competitive profile during the master financial scoring process.

#### Rationale for 4.0% Headroom

- Provides cushion for wage inflation above baseline historical rates
- Maintains competitive positioning in the financial scoring evaluation
- Allows flexibility to discount ceiling rates at the Task Order level to win placements
- Balances profitability protection against market competitiveness

#### Formula Application

$$NTE\_Rate_{Recommended} = \text{Historical\_Average} \times H \times (1.04)$$

### Implementation Guidance

- Apply the 4.0% strategic multiplier uniformly across all job categories and regions to maintain a defensible, consistent pricing posture
- The multiplier is applied at the Master Contract ceiling level; individual Task Order rates can be discounted below the ceiling to win competitive placements
- Under the NTE rules, the contractor can always discount these ceiling rates at the Task Order level to win placements; the 4.0% headroom protects the contractor's ability to operate profitably over the seven-year contract cycle

---

## Strategic Bidding Summary

### Execution Framework

To execute a successful bid, the contractor should proceed with the following actions:

#### 1. Master Contract Pricing Submission

- Submit the Master Contract pricing utilizing the calculated NTE Rates presented in the Section 4 tables
- Ensure that the master financial proposal remains competitive
- Document assumptions about wage inflation, labor market conditions, and regional skill shortages

#### 2. Markup Percentage Determination

- Submit a **regionally specific, fixed Markup Percentage (M)** between **28% and 34%**
- The markup percentage must reflect the fully burdened cost model of:
  - Statutory payroll taxes (12–15%)
  - Liability and workers' compensation insurance (2–5%)
  - Corporate G&A and sourcing overhead (8–15%)
  - OGS Administrative Fee (0.75%)
  - Target profit margin (8–18%)
- Markup percentages should be calibrated per region to reflect regional labor market dynamics and operational overhead variances

#### 3. Subcontractor Teaming Strategy

- Identify all **certified SDVOB subcontractors** during the master bid phase
- Submit a completed **SDVOB Utilization Plan (Form SDVOB 100)** to meet the mandatory six percent utilization goal under the single-tier subcontractor restriction
- Ensure subcontractor rates align with the overall cost model and do not undermine the primary contractor's profitability
- Maintain single-tier restriction: all subcontractors must contract directly with the prime; no secondary subcontracting chains

#### 4. Vendor Registration & Compliance

- Verify that the bidding entity is **registered in the New York State Vendor File**
- Complete the **OSC Substitute W-9 Form** prior to the **July 1, 2026 bid opening**
- Confirm no debarment or suspension statuses in state or federal databases
- Maintain compliance documentation for post-award audit and verification

### Key Risk Mitigation Points

- **Labor Inflation Risk:** Use the 4.0% Strategic Headroom Multiplier to protect against wage escalation; model scenarios where wage inflation exceeds CPI-U by 200–300 basis points
- **CPI Adjustment Risk:** Establish a calendar reminder system to ensure CPI notifications are submitted within the 90-day to first-of-month regulatory window; failure to meet this deadline forfeits annual rate adjustments
- **Profitability Decay:** Conduct stress tests on the seven-year contract life cycle to ensure that the submitted markup percentage sustains profitability even in high-inflation or high-churn labor market scenarios
- **Financial Score Competitiveness:** Benchmark your NTE rates against historical market baskets and competitor intelligence to ensure your financial score is defensible in the master evaluation process

---

## Appendix: Key Formulas at a Glance

| Formula | Description |
|---------|-------------|
| $HBR_{NTE} = HWR \times (1 + M)$ | Core bill rate equation |
| $M = T_{payroll} + I_{insurance} + O_{overhead} + A_{fee} + P_{profit}$ | Fully burdened markup decomposition |
| $HBR_t = HBR_{t-1} \times (1 + \Delta CPI)$ | Annual CPI escalation adjustment |
| $FS_i = 30 \times \frac{\text{Lowest Avg NTE HBR}}{\text{Avg NTE HBR}_i}$ | Financial score calculation |
| $NTE\_Rate = \text{Historical\_Average} \times 1.04$ | Strategic pricing adjustment (4% headroom) |

---

## Document History

- **Created:** June 6, 2026
- **Source:** Comprehensive Competitive Pricing and Bidding Strategy Report for NYS OGS HBITS Solicitation 23311
- **Classification:** Confidential - Bidding Strategy
