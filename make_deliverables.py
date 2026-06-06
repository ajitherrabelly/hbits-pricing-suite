# -*- coding: utf-8 -*-
"""Generate a shareable PDF handout and PPTX deck of the HBITS pricing strategy briefing."""
import os
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

OUT_PDF = "HBITS_Pricing_Strategy_Briefing.pdf"
OUT_PPTX = "HBITS_Pricing_Strategy_Briefing.pptx"

ARIAL = r"C:\Windows\Fonts\arial.ttf"
ARIAL_B = r"C:\Windows\Fonts\arialbd.ttf"
CONSOLA = r"C:\Windows\Fonts\consola.ttf"

NAVY = (17, 32, 58)
BLUE = (31, 90, 138)
BLUE2 = (42, 100, 196)
GREEN = (22, 112, 69)
RED = (196, 65, 58)
AMBER = (179, 119, 26)
LIGHT = (244, 247, 252)

# ---------------------------------------------------------------- shared content
SUBTITLE = ("Briefing for State IDIQ Pricing Quality Review  -  NYS OGS Group 73012 / "
            "Award 23158 / Solicitation 23311")

# ============================ PDF =============================
class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Arial", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, "HBITS Pricing Strategy Briefing", align="L")
        self.cell(0, 8, "Best Pegasus  -  Confidential", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("Arial", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")


def build_pdf():
    pdf = PDF(format="Letter", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_font("Arial", "", ARIAL)
    pdf.add_font("Arial", "B", ARIAL_B)
    mono = "Arial"
    if os.path.exists(CONSOLA):
        pdf.add_font("Consola", "", CONSOLA); mono = "Consola"
    EPW = pdf.epw

    def h2(t):
        pdf.ln(2)
        pdf.set_fill_color(*NAVY); pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 9, "  " + t, fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2); pdf.set_text_color(30, 30, 30)

    def h3(t):
        pdf.ln(1); pdf.set_text_color(*BLUE); pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 6, t, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)

    def para(t):
        pdf.set_font("Arial", "", 10); pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 5.4, t, new_x="LMARGIN", new_y="NEXT"); pdf.ln(1)

    def bullets(items):
        pdf.set_font("Arial", "", 10); pdf.set_text_color(40, 40, 40)
        for it in items:
            lvl = 0
            if isinstance(it, tuple):
                it, lvl = it
            x = pdf.l_margin + 4 + lvl * 5
            pdf.set_x(x)
            pdf.multi_cell(EPW - 4 - lvl * 5, 5.2, ("-  " if lvl else "•  ") + it,
                           new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def callout(kind, tag, text):
        color = {"info": BLUE2, "warn": RED, "win": GREEN}[kind]
        pdf.ln(1)
        y0 = pdf.get_y()
        pdf.set_fill_color(*color)
        pdf.rect(pdf.l_margin, y0, 1.6, 0)  # placeholder
        pdf.set_x(pdf.l_margin + 4)
        pdf.set_font("Arial", "B", 8.5); pdf.set_text_color(*color)
        pdf.multi_cell(EPW - 4, 5, tag.upper(), new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(pdf.l_margin + 4)
        pdf.set_font("Arial", "", 9.5); pdf.set_text_color(45, 45, 45)
        pdf.multi_cell(EPW - 4, 5, text, new_x="LMARGIN", new_y="NEXT")
        y1 = pdf.get_y()
        pdf.set_fill_color(*color); pdf.rect(pdf.l_margin, y0, 1.6, y1 - y0, "F")
        pdf.ln(2)

    def formula(text):
        pdf.ln(1); pdf.set_fill_color(15, 27, 48); pdf.set_text_color(225, 235, 250)
        pdf.set_font(mono, "", 9.5)
        pdf.multi_cell(0, 5.4, text, fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30); pdf.ln(2)

    def table(headers, rows):
        pdf.ln(1)
        n = len(headers)
        w = EPW / n
        pdf.set_font("Arial", "B", 8.5); pdf.set_fill_color(*NAVY); pdf.set_text_color(255, 255, 255)
        for hh in headers:
            pdf.cell(w, 7, " " + hh, border=0, fill=True)
        pdf.ln()
        pdf.set_font("Arial", "", 8.5); pdf.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            # measure height by wrapping each cell
            heights = []
            for c in row:
                lines = pdf.multi_cell(w, 4.6, str(c), dry_run=True, output="LINES")
                heights.append(len(lines))
            rh = max(heights) * 4.6 + 1.5
            if pdf.get_y() + rh > pdf.h - pdf.b_margin:
                pdf.add_page()
            pdf.set_fill_color(247, 249, 252) if fill else pdf.set_fill_color(255, 255, 255)
            x0 = pdf.get_x(); y0 = pdf.get_y()
            for i, c in enumerate(row):
                x = pdf.l_margin + i * w
                pdf.set_xy(x, y0)
                pdf.multi_cell(w, 4.6, " " + str(c), border="B", fill=True,
                               max_line_height=4.6)
            pdf.set_xy(x0, y0 + rh)
            fill = not fill
        pdf.ln(2)

    # ---- Title page
    pdf.add_page()
    pdf.set_fill_color(*NAVY); pdf.rect(0, 0, pdf.w, 70, "F")
    pdf.set_xy(0, 22); pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", "B", 22)
    pdf.multi_cell(0, 9, "  HBITS Pricing Strategy", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(0); pdf.set_font("Arial", "B", 14)
    pdf.multi_cell(0, 8, "  Briefing for IDIQ Pricing Quality Review", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(78); pdf.set_text_color(60, 60, 60); pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6,
        "A transparent walkthrough of the context, narrative, formulas, data provenance, and known "
        "limitations behind Best Pegasus's Hourly-Based IT Services bid pricing - structured so a "
        "State-level IDIQ pricing strategist can independently quality-test every assumption.",
        new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Arial", "", 9.5); pdf.set_text_color(110, 110, 110)
    pdf.multi_cell(0, 5,
        "NYS OGS Group 73012  -  Award 23158 / Solicitation 23311\n"
        "Bid opening 7/1/2026  -  5-year term + 2-year option\n"
        "Persona: Federal/State Government Pricing & Capture  -  Confidential, for internal review",
        new_x="LMARGIN", new_y="NEXT")

    # ---- 1 Executive Summary
    pdf.add_page()
    h2("1 - Executive Summary")
    para("New York State OGS procures Hourly-Based IT Services (HBITS) through a centralized, "
         "non-negotiated, fixed-bill-rate contract. Bidders submit Not-To-Exceed (NTE) hourly bill "
         "rates for 31 job titles x 4 skill levels x 3 regions; those rates are firm for the life of each placement.")
    para("Best Pegasus pricing is modeled in two versions:")
    bullets([
        "Version 1 (Baseline) - from an internal cost/CPI estimation; lands in the expensive third of the field.",
        "Version 1.1 (Rank Positioning) - the current formula; reverse-engineers the competitor field and prices "
        "each role to a target rank of #19 of 33 bidders (mid-field).",
    ])
    callout("info", "For the reviewer",
            "This briefing exists to be challenged. Section 11 lists the assumptions and design choices that most "
            "warrant scrutiny - starting with whether a flat mid-field rank target is compatible with the MSP's 50% price filter.")

    # ---- 2 Context
    h2("2 - Procurement Context")
    h3("The vehicle")
    para("HBITS (Group 73012, Award 23158, refreshed under Solicitation 23311) serves state agencies, local "
         "governments, school districts, public authorities and eligible non-profits. Term: five years + two-year "
         "option; bid opening 7/1/2026. Prior-award task orders continue on their own terms, so transition rates are decisive.")
    h3("Three regions")
    table(["Region", "Coverage", "Character"],
          [["Region 1", "All NY counties outside R2/R3 (Albany hub)", "Statewide baseline; most placements"],
           ["Region 2", "Dutchess, Orange, Putnam (Mid-Hudson)", "Mid-market labor rates"],
           ["Region 3", "NYC metro (Nassau, Suffolk, Westchester, the 5 boroughs, Rockland)", "Highest labor cost"]])
    h3("The MSP price filter - the critical mechanic")
    para("Before any technical evaluation, a Managed Service Provider applies a price filter to candidate submissions:")
    bullets([
        "10-40 candidates: only the lowest 50% of bill rates are forwarded (plus any within 1% of the cutoff).",
        "6-10 candidates: only the 5 lowest bill rates are forwarded.",
        "5 or fewer: filter bypassed - all candidates forwarded.",
    ])
    callout("warn", "Why this matters",
            "For high-volume roles the pool exceeds 10, so only the lowest half survive. A rate at rank #19 of 33 sits "
            "in the upper half and would be filtered out before technical review. See Section 11, item A.")

    # ---- 3 Story
    h2("3 - The Strategic Story")
    para("HBITS is engineered to be price-driven and transparent, creating a tension every bidder must resolve:")
    bullets([
        "Bid too high (large markup): protect margin per placement, but get filtered out of high-volume task orders.",
        "Bid too low (small markup): pass the filter and win volume, but compress margin and starve overhead.",
    ])
    para("Second-order effect on talent: because the bill rate is fixed, a low-markup vendor can pay the consultant a "
         "higher wage for the same bill rate than a high-markup competitor - recruiting better people and earning higher "
         "agency satisfaction. e.g. at a Business Analyst Junior bill of $40.33, an 11% markup pays ~$36.33 vs a 47% markup paying ~$27.43.")

    # ---- 4 Core formula
    h2("4 - Core Pricing Formula")
    para("Every bill rate is the consultant wage grossed up by the vendor markup:")
    formula("R_bill = R_wage x ( 1 + M / 100 )      // HBR_NTE = HWR x (1 + markup)")
    para("Markup M must cover payroll taxes, insurance, overhead & G&A, the OGS administrative fee, and net profit.")
    h3("Annual CPI escalation (Section 6.5)")
    formula("Price Adjustment (%) = ( CPI_t  -  CPI_t-12 ) / CPI_t-12  x 100")
    para("Escalation is NOT automatic - the contractor must file with BLS index sheets in a 90-day window before each "
         "anniversary, or forfeit that year's adjustment.")
    table(["Anchor", "Index basis", "Multiplier"],
          [["2025 -> 2021 (de-escalation)", "270.970 / 321.943", "0.8417 (-15.83%)"],
           ["2025 -> 2026 (bid year)", "Apr2026 333.020 / Apr2025 320.795", "1.0381 (+3.81%)"],
           ["2026 -> 2029 (CBO/Fed)", "2.4% / 2.3% / 2.3%", "1.0716 (+7.16%)"]])

    # ---- 5 V1
    h2("5 - Version 1: Baseline Formula")
    para("Version 1 uses Best Pegasus's internally estimated Bid Year 2026 bill rates (the 'NYS OGS IT Vendor Rate "
         "Estimation'), built bottom-up from labor benchmarks and the CPI multipliers, presented as Region 1 averages.")
    bullets([
        "Covers 30 of 31 titles - the source document omits Business Analyst.",
        "Region 1 values applied across all three regions.",
        "Competitive position: expensive third (e.g. Programmer / R1 / Senior ranks #26 of 33).",
    ])
    callout("warn", "Limitation",
            "A purely cost-up baseline ignores where competitors actually sit, so it tends to price above the filter "
            "cutoff for commodity roles. This motivated Version 1.1.")

    # ---- 6 V1.1
    h2("6 - Version 1.1: Rank Positioning Formula (current)")
    para("A market-relative rule. For each Title x Region x Skill it inspects the live competitor field and places Best "
         "Pegasus at a chosen target rank (default #19 of 33 - 18 competitors below, 14 above).")
    formula("Sort competitors ascending: c(1) <= c(2) <= ... <= c(32)\n"
            "Choose B* such that  c(18) < B* < c(19)    => rank 19 (18 below, 14 above)\n"
            "B* = midpoint(c(18), c(19)) at whole cents, nudged for exactly 18 below and no tie.")
    bullets([
        "Computed independently per region (regional competitor sets differ).",
        "356 / 372 roles hit exactly #19. 16 / 372 land at #18 because the 18th and 19th cheapest competitors are tied "
        "(an exact #19 is impossible) - the nearest, more-competitive rank is used.",
        "Covers all 31 titles, including Business Analyst.",
        "Target rank is a single tunable parameter - the Bid Builder re-ranks live (e.g. #10, #15).",
    ])
    callout("win", "Strength",
            "Self-calibrating to the actual field, region-specific, fully transparent, and reproducible from public award-notice data.")

    # ---- 7 Data
    h2("7 - Data Foundation & Provenance")
    bullets([
        "Source: public OGS award-notice pricing schedules (Attachment 1) per awarded contractor under Award 23158.",
        "Coverage: 32 competitor rate cards, each parsed to exactly 372 rows (31 titles x 4 skills x 3 regions).",
        "Currency rule: only each vendor's latest effective date is kept - their current contracted NTE rate.",
        "Best Pegasus is added as a 33rd bidder per combo under the selected formula version.",
    ])
    table(["Metric", "Value"],
          [["Competitors", "32"], ["Bidders per role (incl. us)", "33"], ["Role combinations", "372"],
           ["Competitor markups observed", "11% - 110%"], ["Roles at exactly #19 (v1.1)", "356"],
           ["Roles at nearest rank / ties", "16"]])
    callout("warn", "Provenance caveat",
            "Many incumbents' latest effective date is pre-2025 and un-escalated, so the low end of the field reflects "
            "stale rates. Ranking a 2026 rate against a 2019 rate is not strictly like-for-like - Section 11, item B.")

    # ---- 8 Margin
    h2("8 - Margin & Cost-Build Decomposition")
    formula("Net profit  = (R_bill - R_wage) - R_wage x (payroll+insurance+overhead) - R_bill x OGSfee\n"
            "Net margin% = Net profit / R_bill x 100")
    para("Defaults: payroll taxes 13.5%, insurance 3.5%, overhead+G&A 10.5% (of wage); OGS fee 0.75% (of bill); markup sets the wage.")
    table(["Markup", "Implied wage (of bill)", "Net margin (approx)"],
          [["30%", "~77%", "~1-2%"], ["40%", "~71%", "~8%"], ["45%", "~69%", "~11%"]])
    callout("info", "Key property",
            "Because cost loadings are a % of wage, net margin is driven almost entirely by the markup, not the role. "
            "Rank-#19 bill rates require ~40-45% markup to clear a healthy (~10%) margin - which lowers the wage we can "
            "offer (recruiting risk) and, for high-volume roles, pushes us toward the filter cutoff.")

    # ---- 9 Landscape
    h2("9 - Competitive Landscape")
    table(["Archetype", "Markup", "Examples", "Play"],
          [["High-volume / low-margin", "11-33%", "CTS (11%), GCOM (30%), Broad Crossing (33%)", "Win volume; scale-dependent"],
           ["Mid-market", "38-52%", "Mindlance (38%), Sligo (47%), Experis (50%)", "Balanced"],
           ["Aggregator / niche-high", "65-110%", "Spruce (65%), CMA/OST (80%), KBI (110%)", "Margin on scarce, filter-bypassing roles"]])
    para("Doctrine: tier the markup - low (15-25%) for commodity, high-supply roles to pass the 50% filter; higher "
         "(35-45%) for scarce roles (Cloud Engineer, Architects, Security Manager) whose pools fall below 5 and bypass the filter.")

    # ---- 10 Quality test
    h2("10 - Quality-Test Checklist (what to scrutinize)")
    bullets([
        "[CRITICAL] A. Does rank #19 survive the MSP 50% filter? In a 33-bidder high-volume pool only the lowest ~16-17 "
        "are forwarded - #19 is in the upper half and would be filtered out. Should the target be <=16 for commodity roles?",
        "[CRITICAL] B. Are competitor benchmarks current? Many incumbent rates are pre-2025 / un-escalated. Should we "
        "escalate competitor rates to 2026-equivalents (CPI) before ranking?",
        "[MATERIAL] C. Flat rank vs tiered strategy. A single #19 target ignores role scarcity. Should the target vary by title?",
        "[MATERIAL] D. Margin vs recruiting. ~1-2% margin at 30% markup; ~10% needs ~45%, which lowers payable wage. Validate the trade-off.",
        "[MATERIAL] E. Wage & cost-build assumptions. Replace the assumed 30% markup / illustrative loadings with audited rates.",
        "[CHECK] F. 10-year profitability decay - CPI escalation trails IT wage inflation; model margin erosion over 5+2 years.",
        "[CHECK] G. Tie-affected roles - 16 of 372 land at #18; confirm acceptable.",
        "[CHECK] H. Data completeness - are all 32 cards the full awarded pool?",
        "[CHECK] I. Region modeling - confirm regional competitor sets are genuinely distinct.",
        "[CHECK] J. Escalation compliance - workflow to file the CPI adjustment within the window each anniversary.",
    ])

    # ---- 11 Risks
    h2("11 - Risks, Assumptions & Limitations")
    bullets([
        "Assumption: competitors re-bid at/near current Award 23158 rates under 23311 (their 2026 bids are unknown).",
        "Assumption: the MSP filter mechanics carry forward unchanged.",
        "Limitation: displayed Best Pegasus wage and margin are illustrative pending audited cost data.",
        "Limitation: Version 1 omits Business Analyst (source-document gap).",
        "Limitation: ranking treats each vendor's latest effective rate as current regardless of its year.",
    ])
    h2("12 - Glossary")
    para("NTE - Not-To-Exceed bill rate.  HWR - Hourly Wage Rate (consultant; contractual minimum).  HBR - Hourly Bill "
         "Rate (billed to State).  MSP - Managed Service Provider (runs the price filter).  CPI-U - Consumer Price Index, "
         "All Urban Consumers (CUUR0000SA0).  IDIQ - Indefinite-Delivery/Indefinite-Quantity.")

    pdf.output(OUT_PDF)
    print("wrote", OUT_PDF, os.path.getsize(OUT_PDF), "bytes")


# ============================ PPTX =============================
EMU_W, EMU_H = Inches(13.333), Inches(7.5)


def build_pptx():
    prs = Presentation()
    prs.slide_width = EMU_W
    prs.slide_height = EMU_H
    blank = prs.slide_layouts[6]

    def rgb(t): return RGBColor(*t)

    def add_title_slide():
        s = prs.slides.add_slide(blank)
        bg = s.shapes.add_shape(1, 0, 0, EMU_W, EMU_H)
        bg.fill.solid(); bg.fill.fore_color.rgb = rgb(NAVY); bg.line.fill.background()
        bg.shadow.inherit = False
        tb = s.shapes.add_textbox(Inches(0.9), Inches(2.2), Inches(11.5), Inches(3))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = "HBITS Pricing Strategy"
        p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = rgb((255, 255, 255))
        p2 = tf.add_paragraph(); p2.text = "Briefing for IDIQ Pricing Quality Review"
        p2.font.size = Pt(24); p2.font.color.rgb = rgb((159, 199, 232))
        p3 = tf.add_paragraph(); p3.text = SUBTITLE
        p3.font.size = Pt(13); p3.font.color.rgb = rgb((200, 210, 230))
        p4 = tf.add_paragraph(); p4.text = "Bid opening 7/1/2026  -  5-year term + 2-year option  -  Confidential"
        p4.font.size = Pt(11); p4.font.color.rgb = rgb((150, 165, 195))

    def add_slide(title, bullets, accent=BLUE):
        s = prs.slides.add_slide(blank)
        bar = s.shapes.add_shape(1, 0, 0, EMU_W, Inches(0.95))
        bar.fill.solid(); bar.fill.fore_color.rgb = rgb(accent); bar.line.fill.background()
        bar.shadow.inherit = False
        tt = bar.text_frame; tt.word_wrap = True
        tt.margin_left = Inches(0.4); tt.margin_top = Inches(0.12)
        tp = tt.paragraphs[0]; tp.text = title
        tp.font.size = Pt(24); tp.font.bold = True; tp.font.color.rgb = rgb((255, 255, 255))
        body = s.shapes.add_textbox(Inches(0.6), Inches(1.2), Inches(12.1), Inches(6.0))
        bf = body.text_frame; bf.word_wrap = True
        first = True
        for item in bullets:
            text, lvl, color, bold = item if isinstance(item, tuple) else (item, 0, None, False)
            p = bf.paragraphs[0] if first else bf.add_paragraph()
            first = False
            p.text = ("•  " if lvl == 0 else "–  ") + text
            p.level = lvl
            p.font.size = Pt(16 if lvl == 0 else 14)
            p.font.bold = bold
            p.font.color.rgb = rgb(color if color else (40, 45, 55))
            p.space_after = Pt(6)
        return s

    def add_table_slide(title, headers, rows, accent=NAVY):
        s = prs.slides.add_slide(blank)
        bar = s.shapes.add_shape(1, 0, 0, EMU_W, Inches(0.95))
        bar.fill.solid(); bar.fill.fore_color.rgb = rgb(accent); bar.line.fill.background()
        bar.shadow.inherit = False
        tp = bar.text_frame.paragraphs[0]; bar.text_frame.margin_left = Inches(0.4)
        tp.text = title; tp.font.size = Pt(24); tp.font.bold = True; tp.font.color.rgb = rgb((255, 255, 255))
        nr, nc = len(rows) + 1, len(headers)
        gt = s.shapes.add_table(nr, nc, Inches(0.6), Inches(1.3), Inches(12.1), Inches(0.5 + 0.5 * nr)).table
        for j, h in enumerate(headers):
            c = gt.cell(0, j); c.text = h
            c.fill.solid(); c.fill.fore_color.rgb = rgb(NAVY)
            pr = c.text_frame.paragraphs[0]; pr.font.size = Pt(12); pr.font.bold = True; pr.font.color.rgb = rgb((255, 255, 255))
        for i, row in enumerate(rows, start=1):
            for j, val in enumerate(row):
                c = gt.cell(i, j); c.text = str(val)
                pr = c.text_frame.paragraphs[0]; pr.font.size = Pt(11); pr.font.color.rgb = rgb((40, 40, 40))
        return s

    # ----- slides
    add_title_slide()

    add_slide("Executive Summary", [
        ("Centralized, non-negotiated, FIXED bill-rate IT staffing contract (HBITS).", 0, None, False),
        ("NTE bill rates: 31 titles x 4 skills x 3 regions, firm for each placement's life.", 0, None, False),
        ("Version 1 (Baseline): internal cost/CPI estimate - lands in the expensive third.", 0, None, False),
        ("Version 1.1 (Rank Positioning): current formula - prices each role to rank #19 of 33 (mid-field).", 0, None, False),
        ("This deck is built to be challenged - see the Quality-Test Checklist.", 0, BLUE, True),
    ], NAVY)

    add_table_slide("Procurement Context - Three Regions",
        ["Region", "Coverage", "Character"],
        [["R1", "NY counties outside R2/R3 (Albany)", "Statewide baseline; most work"],
         ["R2", "Dutchess, Orange, Putnam", "Mid-Hudson, mid-market"],
         ["R3", "NYC metro + 5 boroughs", "Highest labor cost"]])

    add_slide("The MSP Price Filter - the critical mechanic", [
        ("Applied BEFORE any technical evaluation, on price alone:", 0, None, True),
        ("10-40 candidates: only the lowest 50% of bill rates forwarded (+1% buffer).", 0, None, False),
        ("6-10 candidates: only the 5 lowest forwarded.", 0, None, False),
        ("5 or fewer: filter bypassed - all forwarded.", 0, None, False),
        ("Implication: a rank #19 of 33 rate sits in the UPPER half - filtered out on high-volume roles.", 0, RED, True),
    ], BLUE)

    add_slide("The Strategic Story", [
        ("Bid too high (big markup): protect margin, but get filtered out of high-volume orders.", 0, None, False),
        ("Bid too low (small markup): pass the filter & win volume, but compress margin.", 0, None, False),
        ("Fixed bill rate => low-markup vendors can pay a HIGHER wage for the same bill rate.", 0, None, False),
        ("e.g. BA Junior bill $40.33: 11% markup pays ~$36.33 vs 47% markup pays ~$27.43.", 1, None, False),
        ("Better wages -> better talent -> higher agency satisfaction scores.", 0, GREEN, True),
    ], BLUE)

    add_slide("Core Formula & CPI Escalation", [
        ("HBR_NTE = HWR x (1 + Markup/100)", 0, NAVY, True),
        ("Markup must cover payroll, insurance, overhead & G&A, OGS fee, and net profit.", 0, None, False),
        ("CPI escalation (Sec 6.5): Adj% = (CPI_t - CPI_t-12) / CPI_t-12 x 100", 0, None, False),
        ("Bid-year multiplier (Apr2026/Apr2025): 1.0381 (+3.81%).", 1, None, False),
        ("2026->2029 projection: 1.0716 (+7.16%).", 1, None, False),
        ("NOT automatic - must be filed with BLS sheets in a 90-day window or forfeited.", 0, AMBER, True),
    ], BLUE)

    add_slide("Version 1 - Baseline", [
        ("Internal Bid Year 2026 estimate (labor benchmarks x CPI multipliers).", 0, None, False),
        ("Covers 30 of 31 titles (omits Business Analyst).", 0, None, False),
        ("Region 1 values applied across all regions.", 0, None, False),
        ("Position: expensive third (Programmer/R1/Senior = #26 of 33).", 0, None, False),
        ("Cost-up baseline ignores where competitors sit -> prices above the filter cutoff.", 0, RED, True),
    ], BLUE)

    add_slide("Version 1.1 - Rank Positioning (current)", [
        ("Market-relative: price each role to a target rank (default #19 of 33).", 0, None, False),
        ("Sort competitors asc; set B* between the 18th and 19th cheapest => 18 below, 14 above.", 0, None, False),
        ("356/372 roles hit exactly #19; 16/372 fall to #18 due to competitor ties.", 0, None, False),
        ("Per-region; covers all 31 titles; reproducible from public data.", 0, None, False),
        ("Target rank is one tunable knob - re-rank live in the Bid Builder.", 0, GREEN, True),
    ], BLUE)

    add_table_slide("Data Foundation - Snapshot",
        ["Metric", "Value"],
        [["Competitors", "32"], ["Bidders per role", "33"], ["Role combinations", "372"],
         ["Competitor markups", "11% - 110%"], ["Roles at exactly #19", "356"], ["Roles at nearest (ties)", "16"]])

    add_slide("Margin & Cost Build", [
        ("Net margin% = [(bill-wage) - wage x (payroll+ins+oh) - bill x OGSfee] / bill", 0, None, False),
        ("Defaults: payroll 13.5%, insurance 3.5%, overhead+G&A 10.5% (of wage); OGS fee 0.75%.", 0, None, False),
        ("30% markup -> ~1-2% net margin.", 1, None, False),
        ("45% markup -> ~11% net margin.", 1, None, False),
        ("Margin is driven by MARKUP, not the role. Rank-#19 needs ~40-45% markup for ~10% margin.", 0, AMBER, True),
    ], BLUE)

    add_table_slide("Competitive Landscape - Archetypes",
        ["Archetype", "Markup", "Examples"],
        [["High-volume / low-margin", "11-33%", "CTS, GCOM, Broad Crossing"],
         ["Mid-market", "38-52%", "Mindlance, Sligo, Experis"],
         ["Aggregator / niche-high", "65-110%", "Spruce, CMA/OST, KBI"]])

    add_slide("Quality-Test Checklist - Critical & Material", [
        ("A. Does rank #19 survive the 50% MSP filter? (upper half = filtered)", 0, RED, True),
        ("B. Are competitor benchmarks current, or stale/un-escalated pre-2025 rates?", 0, RED, True),
        ("C. Flat rank vs tiered strategy by role scarcity?", 0, AMBER, True),
        ("D. Margin vs recruiting trade-off (markup sets payable wage)?", 0, AMBER, True),
        ("E. Replace assumed wage / cost loadings with audited rates?", 0, AMBER, True),
    ], NAVY)

    add_slide("Quality-Test Checklist - Verification", [
        ("F. Model 10-year profitability decay (CPI escalation trails IT wage inflation).", 0, None, False),
        ("G. 16/372 roles land at #18 (ties) - acceptable?", 0, None, False),
        ("H. Is the 32-vendor pool complete?", 0, None, False),
        ("I. Confirm regional competitor sets are distinct.", 0, None, False),
        ("J. Workflow to file CPI escalation within the window each anniversary.", 0, None, False),
    ], NAVY)

    add_slide("Risks, Assumptions & Next Steps", [
        ("Assumes competitors re-bid near current rates; MSP mechanics unchanged.", 0, None, False),
        ("Wage/margin figures illustrative pending audited cost data.", 0, None, False),
        ("Recommended next steps:", 0, NAVY, True),
        ("Decide target rank per role tier (commodity <=16 to pass the filter).", 1, None, False),
        ("Escalate stale competitor rates to 2026 before ranking.", 1, None, False),
        ("Plug in audited cost build; model multi-year margin.", 1, None, False),
    ], NAVY)

    prs.save(OUT_PPTX)
    print("wrote", OUT_PPTX, os.path.getsize(OUT_PPTX), "bytes")


if __name__ == "__main__":
    build_pdf()
    build_pptx()
