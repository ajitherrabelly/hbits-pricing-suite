import pdfplumber, re, os, glob, csv

PRICING_DIR = "Pricing document"
SKILLS = ("Junior", "Mid-Level", "Senior", "Expert")
ROW_RE = re.compile(
    r'([A-Za-z][A-Za-z /]*?)\s+(Junior|Mid-Level|Senior|Expert)\s+\$([\d,]+\.\d{2})\s+\$([\d,]+\.\d{2})'
)
DATE_RE = re.compile(r'Effective\s+(\d+)/(\d+)/(\d{4})')
NAME_RE = re.compile(r'(?:Contractor|Bidder) Name:\s*(.+)')
FID_RE = re.compile(r'Federal ID#:\s*(\S+)')
MARKUP_RE = re.compile(r'(\d+\.\d+)%')


def num(s):
    return float(s.replace(",", ""))


def page_date(txt):
    m = DATE_RE.search(txt)
    if not m:
        return None
    mo, d, y = map(int, m.groups())
    return (y, mo, d)


def extract_pdf(path):
    rows = []
    contractor = None
    fid = None
    markup = None
    page_texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            page_texts.append(txt)
            if contractor is None:
                nm = NAME_RE.search(txt)
                if nm:
                    contractor = nm.group(1).strip()
            if fid is None:
                fm = FID_RE.search(txt)
                if fm:
                    fid = fm.group(1).strip()
            if markup is None:
                mm = MARKUP_RE.search(txt)
                if mm:
                    markup = mm.group(1)

    # find latest effective date
    dates = [page_date(t) for t in page_texts]
    valid = [d for d in dates if d]
    latest = max(valid) if valid else None

    for txt, d in zip(page_texts, dates):
        if latest and d != latest:
            continue
        for line in txt.split("\n"):
            matches = ROW_RE.findall(line)
            if not matches:
                continue
            # up to 3 region segments left-to-right
            for idx, (title, skill, wage, bill) in enumerate(matches[:3]):
                region = f"Region {idx + 1}"
                title = title.strip()
                rows.append({
                    "Contractor_Name": contractor or os.path.basename(path),
                    "Federal_ID": fid or "NA",
                    "Region": region,
                    "Job_Title": title,
                    "Skill_Level": skill,
                    "Hourly_Wage_Rate": f"{num(wage):.2f}",
                    "Hourly_Bill_Rate": f"{num(bill):.2f}",
                    "Markup_Percent": markup or "",
                    "Is_Our_Rate": "false",
                })
    return contractor, fid, markup, latest, rows


if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] or ["7301223158PL_CTS.pdf", "7301223158PL_SLIGO.pdf"]
    for t in targets:
        path = os.path.join(PRICING_DIR, t)
        contractor, fid, markup, latest, rows = extract_pdf(path)
        titles = sorted(set(r["Job_Title"] for r in rows))
        print(f"\n=== {t} ===")
        print(f"Contractor: {contractor} | FID: {fid} | Markup: {markup} | Latest: {latest}")
        print(f"Rows: {len(rows)} | Unique titles: {len(titles)}")
        print("Titles:", titles)
