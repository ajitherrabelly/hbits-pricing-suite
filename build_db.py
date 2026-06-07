"""Build hbits.db (SQLite) from the RFP 23311 source workbooks + the rate-card CSV.

Run:  python build_db.py
Consumes:
  rfp_data/RFP 23311/...                  (extracted zip — closures, contacts, titles, bill matrix)
  vendors_rates.csv                       (rate cards: wage/bill/markup, incl. Best Pegasus)
Produces:
  hbits.db                                (relational DB; see schema below)

Tables
  vendors(vendor_id, canonical_name, norm_key)          -- one row per real company
  vendor_aliases(norm_key, raw_name, source)            -- every spelling seen
  vendor_contacts(norm_key, contact_name, email, phone, designation)
  job_titles(title, category)                           -- 'old' (31) / 'new' (Attachment 7)
  closures(... + job_title, skill_level, county, year)  -- 1 row per task-order WIN
  rate_cards(... wage, bill, markup_percent, is_our_rate, formula_version)
  bill_matrix(norm_key, raw_name, job_title, region, skill_level, bill)
Views
  v_vendor_year_wins, v_title_demand, v_vendor_pricing_vs_wins
"""
import os, re, csv, sqlite3, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
RFP  = os.path.join(ROOT, "rfp_data", "RFP 23311")
DB   = os.path.join(ROOT, "hbits.db")
RATE_CSV = os.path.join(ROOT, "vendors_rates.csv")

import openpyxl

SKILLS = ["Junior", "Mid-Level", "Senior", "Expert"]

# ---- known job titles (the 31 'old' HBITS titles) for description parsing ----
OLD_TITLES = [
    "Business Analyst","Cloud Engineer","Database Administrator","Database Architect",
    "Database Manager","Graphic Designer","Help Desk Manager","IT Manager","IT Specialist",
    "Network Administrator","Network Architect","Operations Manager","Programmer",
    "Project Manager","Security Analyst","Security Manager","Software Analyst",
    "Software Architect","Software Developer","Software Manager","Systems Administrator",
    "Systems Analyst","Systems Architect","Systems Developer","Technical Writer","Tester",
    "Training Developer","Web Administrator","Web Designer","Web Developer","Web Manager",
]


def norm_key(name):
    """Reduce a company name to a stable join key: first 2 significant alnum tokens."""
    if not name:
        return ""
    n = str(name).upper()
    n = n.split(" DBA ")[0].split(" D/B/A ")[0]          # drop 'doing business as' tail
    n = re.sub(r"[^A-Z0-9 ]", " ", n)
    stop = {"INC","LLC","CORP","CO","INCORPORATED","LTD","AND","THE","DBA",
            "CONSULTING","SERVICES","SVCS","SOLUTIONS","GROUP","COMPANY",
            "IN","GLOBAL"}   # 'IN' = truncated INC; 'GLOBAL' = TEKsystems variant
    toks = [t for t in n.split() if t and t not in stop]
    return " ".join(toks[:2])


TITLE_VARIANTS = {
    "system developer": "Systems Developer", "system administrator": "Systems Administrator",
    "system analyst": "Systems Analyst", "system architect": "Systems Architect",
    "programmer analyst": "Programmer", "qa tester": "Tester", "quality assurance": "Tester",
    "dba": "Database Administrator", "web develop": "Web Developer",
}


def is_hbits(desc):
    if not desc:
        return 0
    d = str(desc).upper()
    return 1 if ("HBITS" in d or "73012" in d or "23158" in d) else 0


def parse_description(desc):
    """Best-effort extract (job_title, skill_level, county) from a CONTRACT DESCRIPTION."""
    if not desc:
        return None, None, None
    d = str(desc)
    low = d.lower()
    # skill (check Mid-Level variants before bare 'mid')
    skill = None
    for s, pats in [("Mid-Level", ["mid-level","mid level","midlevel"]),
                    ("Expert", ["expert"]), ("Senior", ["senior"]), ("Junior", ["junior"])]:
        if any(p in low for p in pats):
            skill = s; break
    # title: longest known title that appears
    title = None
    for t in sorted(OLD_TITLES, key=len, reverse=True):
        if t.lower() in low:
            title = t; break
    if title is None:                       # common singular/variant spellings
        for variant, canon in TITLE_VARIANTS.items():
            if variant in low:
                title = canon; break
    # county
    m = re.search(r"([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s+County", d)
    county = (m.group(1) + " County") if m else None
    return title, skill, county


def cell_clean(v):
    if v is None:
        return None
    if isinstance(v, str):
        return v.strip()
    if hasattr(v, "strftime"):          # datetime/date -> MM/DD/YYYY string
        return v.strftime("%m/%d/%Y")
    return v


# ----------------------------------------------------------------------------- closures
PER_YEAR_FILES = {
    2023: "Vendor Closure Data of year 2023/All companies No_s of Closures 2023.xlsx",
    2024: "Vendor Closure Data of year 2024/All companies No_s of Closures 2024.xlsx",
    2025: "Vendor Closure Data of year 2025/All companies Closures 2025.xlsx",
}
CLOSURE_COLS = ["vendor_raw","department","contract_number","amount","spending_to_date",
                "start_date","end_date","description","contract_type","approved_date"]


def read_closures():
    rows = []
    for year, rel in PER_YEAR_FILES.items():
        path = os.path.join(RFP, rel)
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb["Sheet1"] if "Sheet1" in wb.sheetnames else wb.worksheets[-1]
        data = list(ws.iter_rows(values_only=True))
        wb.close()
        # locate header row containing 'VENDOR NAME'
        hidx = next((i for i, r in enumerate(data)
                     if r and any(isinstance(c, str) and "VENDOR NAME" in c.upper() for c in r)), 0)
        for r in data[hidx + 1:]:
            if not r or not cell_clean(r[0]):
                continue
            rec = {c: cell_clean(r[i]) if i < len(r) else None for i, c in enumerate(CLOSURE_COLS)}
            if not rec["contract_number"]:
                continue
            title, skill, county = parse_description(rec["description"])
            rec.update(year=year, job_title=title, skill_level=skill, county=county,
                       is_hbits=is_hbits(rec["description"]),
                       source_file=os.path.basename(path), norm_key=norm_key(rec["vendor_raw"]))
            rows.append(rec)
    return rows


# ----------------------------------------------------------------------------- rate cards
def read_rate_cards():
    rows = []
    if not os.path.exists(RATE_CSV):
        return rows
    for r in csv.DictReader(open(RATE_CSV, encoding="utf-8")):
        rows.append({
            "vendor_raw": r["Contractor_Name"], "norm_key": norm_key(r["Contractor_Name"]),
            "federal_id": r.get("Federal_ID"), "region": r["Region"],
            "job_title": r["Job_Title"], "skill_level": r["Skill_Level"],
            "wage": float(r["Hourly_Wage_Rate"]) if r["Hourly_Wage_Rate"] else None,
            "bill": float(r["Hourly_Bill_Rate"]) if r["Hourly_Bill_Rate"] else None,
            "markup_percent": float(r["Markup_Percent"]) if r.get("Markup_Percent") else None,
            "is_our_rate": 1 if r["Is_Our_Rate"] == "true" else 0,
            "formula_version": r.get("Formula_Version", ""),
        })
    return rows


# ----------------------------------------------------------------------------- bill matrix
def read_bill_matrix():
    path = os.path.join(RFP, "HBITS_31_Sheets_Complete_Data_Final.xlsx")
    if not os.path.exists(path):
        return []
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        title = ws.title.strip()
        data = list(ws.iter_rows(values_only=True))
        if len(data) < 3:
            continue
        region_row, skill_row = data[0], data[1]
        # forward-fill region across columns
        cols = {}
        cur_region = None
        for ci in range(1, len(skill_row)):
            reg = region_row[ci] if ci < len(region_row) else None
            if reg:
                cur_region = str(reg).strip()
            sk = skill_row[ci]
            if cur_region and sk and str(sk).strip() in SKILLS:
                cols[ci] = (cur_region, str(sk).strip())
        for r in data[2:]:
            if not r or not r[0]:
                continue
            comp = str(r[0]).strip()
            for ci, (reg, sk) in cols.items():
                if ci < len(r) and isinstance(r[ci], (int, float)):
                    out.append({"raw_name": comp, "norm_key": norm_key(comp),
                                "job_title": title, "region": reg,
                                "skill_level": sk, "bill": float(r[ci])})
    wb.close()
    return out


# ----------------------------------------------------------------------------- contacts
def read_contacts():
    path = os.path.join(RFP, "HBITS Vendor_s Contact Detail_s.xlsx")
    if not os.path.exists(path):
        return []
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Updated Contact Details"] if "Updated Contact Details" in wb.sheetnames else wb.worksheets[0]
    out, cur = [], None
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        comp = cell_clean(r[0]) if len(r) > 0 else None
        if comp:
            cur = comp
        name = cell_clean(r[1]) if len(r) > 1 else None
        if not (name or (len(r) > 2 and r[2])):
            continue
        out.append({"norm_key": norm_key(cur), "vendor_raw": cur, "contact_name": name,
                    "email": cell_clean(r[2]) if len(r) > 2 else None,
                    "phone": str(cell_clean(r[3])) if len(r) > 3 and r[3] else None,
                    "designation": cell_clean(r[4]) if len(r) > 4 else None})
    wb.close()
    return out


# ----------------------------------------------------------------------------- titles
def read_titles():
    path = os.path.join(RFP, "All Job Title_s List New and Old one.xlsx")
    out = {}
    if os.path.exists(path):
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        def col_a(sheet):
            vals = []
            if sheet in wb.sheetnames:
                for i, r in enumerate(wb[sheet].iter_rows(values_only=True)):
                    if i == 0:        # header label
                        continue
                    if r and r[0] and isinstance(r[0], str):
                        vals.append(r[0].strip())
            return vals
        for t in col_a("Old Titles List"):
            out[t] = "old"
        for t in col_a("New Titles List"):
            out.setdefault(t, "new")
        wb.close()
    for t in OLD_TITLES:
        out.setdefault(t, "old")
    return out


# ----------------------------------------------------------------------------- build
def build():
    closures = read_closures()
    rates    = read_rate_cards()
    billmx   = read_bill_matrix()
    contacts = read_contacts()
    titles   = read_titles()

    # canonical vendor dimension: prefer nicely-cased rate-card names, then closures
    canon = {}     # norm_key -> canonical_name
    for r in rates:
        canon.setdefault(r["norm_key"], r["vendor_raw"])
    for r in closures:
        canon.setdefault(r["norm_key"], (r["vendor_raw"] or "").title())
    for c in contacts:
        canon.setdefault(c["norm_key"], c["vendor_raw"])
    canon.pop("", None)

    aliases = set()
    for r in closures:  aliases.add((r["norm_key"], r["vendor_raw"], "closure"))
    for r in rates:     aliases.add((r["norm_key"], r["vendor_raw"], "rate_card"))
    for r in billmx:    aliases.add((r["norm_key"], r["raw_name"], "bill_matrix"))
    for c in contacts:  aliases.add((c["norm_key"], c["vendor_raw"], "contact"))

    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    c = con.cursor()
    c.executescript("""
    CREATE TABLE vendors(vendor_id INTEGER PRIMARY KEY, canonical_name TEXT, norm_key TEXT UNIQUE);
    CREATE TABLE vendor_aliases(norm_key TEXT, raw_name TEXT, source TEXT);
    CREATE TABLE vendor_contacts(norm_key TEXT, vendor_raw TEXT, contact_name TEXT, email TEXT, phone TEXT, designation TEXT);
    CREATE TABLE job_titles(title TEXT PRIMARY KEY, category TEXT);
    CREATE TABLE closures(
        id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER, norm_key TEXT, vendor_raw TEXT,
        department TEXT, contract_number TEXT, amount REAL, spending_to_date REAL,
        start_date TEXT, end_date TEXT, description TEXT, contract_type TEXT, approved_date TEXT,
        job_title TEXT, skill_level TEXT, county TEXT, is_hbits INTEGER, source_file TEXT);
    CREATE TABLE rate_cards(
        norm_key TEXT, vendor_raw TEXT, federal_id TEXT, region TEXT, job_title TEXT,
        skill_level TEXT, wage REAL, bill REAL, markup_percent REAL,
        is_our_rate INTEGER, formula_version TEXT);
    CREATE TABLE bill_matrix(norm_key TEXT, raw_name TEXT, job_title TEXT, region TEXT, skill_level TEXT, bill REAL);
    """)

    for i, (k, name) in enumerate(sorted(canon.items()), 1):
        c.execute("INSERT INTO vendors VALUES(?,?,?)", (i, name, k))
    c.executemany("INSERT INTO vendor_aliases VALUES(?,?,?)", sorted(aliases))
    c.executemany("INSERT INTO vendor_contacts VALUES(?,?,?,?,?,?)",
                  [(x["norm_key"], x["vendor_raw"], x["contact_name"], x["email"], x["phone"], x["designation"]) for x in contacts])
    c.executemany("INSERT INTO job_titles VALUES(?,?)", sorted(titles.items()))
    c.executemany("""INSERT INTO closures(year,norm_key,vendor_raw,department,contract_number,amount,
        spending_to_date,start_date,end_date,description,contract_type,approved_date,job_title,skill_level,county,is_hbits,source_file)
        VALUES(:year,:norm_key,:vendor_raw,:department,:contract_number,:amount,:spending_to_date,
        :start_date,:end_date,:description,:contract_type,:approved_date,:job_title,:skill_level,:county,:is_hbits,:source_file)""", closures)
    c.executemany("""INSERT INTO rate_cards VALUES(:norm_key,:vendor_raw,:federal_id,:region,:job_title,
        :skill_level,:wage,:bill,:markup_percent,:is_our_rate,:formula_version)""", rates)
    c.executemany("INSERT INTO bill_matrix VALUES(:norm_key,:raw_name,:job_title,:region,:skill_level,:bill)", billmx)

    c.executescript("""
    CREATE INDEX ix_clo_key ON closures(norm_key);
    CREATE INDEX ix_clo_year ON closures(year);
    CREATE INDEX ix_clo_title ON closures(job_title);
    CREATE INDEX ix_rate_key ON rate_cards(norm_key);
    CREATE INDEX ix_rate_combo ON rate_cards(job_title, region, skill_level);

    CREATE VIEW v_vendor_year_wins AS
      SELECT v.canonical_name, c.norm_key, c.year, COUNT(*) wins, ROUND(SUM(c.amount),0) total_amount
      FROM closures c JOIN vendors v ON v.norm_key=c.norm_key
      GROUP BY c.norm_key, c.year;

    CREATE VIEW v_title_demand AS
      SELECT year, job_title, COUNT(*) wins, ROUND(SUM(amount),0) total_amount
      FROM closures WHERE job_title IS NOT NULL GROUP BY year, job_title;

    CREATE VIEW v_vendor_pricing_vs_wins AS
      SELECT v.canonical_name, w.wins, w.total_amount,
             ROUND(AVG(r.bill),2) avg_bill, ROUND(AVG(r.markup_percent),1) markup
      FROM (SELECT norm_key, SUM(wins) wins, SUM(total_amount) total_amount FROM v_vendor_year_wins GROUP BY norm_key) w
      JOIN vendors v ON v.norm_key=w.norm_key
      LEFT JOIN rate_cards r ON r.norm_key=w.norm_key AND r.is_our_rate=0
      GROUP BY w.norm_key;
    """)
    con.commit()

    # ---- validation report ----
    def q(sql):
        return c.execute(sql).fetchall()
    print(f"DB written: {DB}")
    print(f"  vendors          {q('SELECT COUNT(*) FROM vendors')[0][0]}")
    print(f"  closures         {q('SELECT COUNT(*) FROM closures')[0][0]}")
    print(f"  rate_cards       {q('SELECT COUNT(*) FROM rate_cards')[0][0]}")
    print(f"  bill_matrix      {q('SELECT COUNT(*) FROM bill_matrix')[0][0]}")
    print(f"  contacts         {q('SELECT COUNT(*) FROM vendor_contacts')[0][0]}")
    n_titles = c.execute("SELECT COUNT(*) FROM job_titles").fetchone()[0]
    n_old = c.execute("SELECT COUNT(*) FROM job_titles WHERE category=?", ("old",)).fetchone()[0]
    print(f"  job_titles       {n_titles} (old={n_old}, new={n_titles - n_old})")
    print("  closures/year   ", q("SELECT year, COUNT(*) FROM closures GROUP BY year ORDER BY year"))
    hbits = q("SELECT COUNT(*) FROM closures WHERE is_hbits=1")[0][0]
    unparsed_h = q("SELECT COUNT(*) FROM closures WHERE is_hbits=1 AND job_title IS NULL")[0][0]
    print(f"  HBITS closures   {hbits} (non-HBITS {1663 - hbits} flagged out)")
    print(f"  HBITS closures w/o parsed title: {unparsed_h} (amendments / 'additional funds')")
    print("  closures w/o vendor match in rate_cards:",
          q("SELECT COUNT(DISTINCT norm_key) FROM closures WHERE norm_key NOT IN (SELECT norm_key FROM rate_cards)")[0][0], "vendor keys")
    print("  TOP 6 vendors by total wins:")
    for row in q("""SELECT v.canonical_name, SUM(w.wins) tot FROM v_vendor_year_wins w
                    JOIN vendors v ON v.norm_key=w.norm_key GROUP BY w.norm_key ORDER BY tot DESC LIMIT 6"""):
        print("     ", row)
    con.close()


if __name__ == "__main__":
    build()
