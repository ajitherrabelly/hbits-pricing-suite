"""Generate consolidated vendors_rates.csv from all vendor PDFs + Best Pegasus baseline."""
import glob, os, csv
from extract_rates import extract_pdf

PRICING_DIR = "Pricing document"
OUT = "vendors_rates.csv"

# Best Pegasus baseline = Bid Year 2026 BILL rates (Region 1 statewide baseline)
# Source: "NYS OGS IT Vendor Rate Estimation.pdf". Order per title: [Junior, Mid-Level, Senior, Expert]
BASELINE_2026_BILL = {
    "Programmer":              [44.08, 61.29, 74.81, 85.27],
    "Software Developer":      [45.16, 62.28, 78.15, 88.61],
    "Software Analyst":        [44.03, 57.92, 74.03, 85.56],
    "Software Architect":      [55.08, 71.31, 90.59, 102.06],
    "Software Manager":        [51.24, 65.39, 83.33, 97.00],
    "Systems Developer":       [46.68, 61.22, 78.10, 89.57],
    "Cloud Engineer":          [52.67, 69.30, 85.67, 99.89],
    "Database Administrator":  [45.62, 58.80, 76.54, 87.88],
    "Database Architect":      [53.09, 68.44, 86.35, 99.21],
    "Database Manager":        [48.24, 61.14, 80.25, 93.66],
    "Systems Administrator":   [40.86, 52.44, 69.83, 81.05],
    "Systems Analyst":         [44.48, 57.27, 72.26, 83.84],
    "Systems Architect":       [54.46, 69.69, 88.93, 101.35],
    "Network Administrator":   [43.13, 53.99, 69.41, 80.25],
    "Network Architect":       [51.85, 66.11, 82.97, 95.27],
    "Security Analyst":        [48.10, 63.40, 80.74, 93.18],
    "Security Manager":        [52.06, 68.34, 86.46, 101.01],
    "IT Specialist":           [43.44, 58.73, 75.26, 88.88],
    "Help Desk Manager":       [38.71, 46.01, 57.08, 65.82],
    "Project Manager":         [48.47, 61.56, 82.26, 98.35],
    "IT Manager":              [48.27, 60.03, 76.74, 89.38],
    "Operations Manager":      [45.02, 55.47, 71.51, 83.38],
    "Training Developer":      [40.43, 49.43, 61.81, 70.98],
    "Technical Writer":        [34.50, 41.96, 51.28, 60.21],
    "Tester":                  [38.35, 47.51, 59.45, 67.87],
    "Web Developer":           [43.60, 59.11, 72.16, 81.87],
    "Web Administrator":       [40.98, 53.77, 68.36, 77.96],
    "Web Designer":            [39.32, 50.81, 62.36, 70.89],
    "Web Manager":             [45.57, 57.40, 74.84, 86.00],
    "Graphic Designer":        [37.19, 45.74, 56.91, 66.43],
}
SKILLS = ["Junior", "Mid-Level", "Senior", "Expert"]
ASSUMED_MARKUP = 30.0  # used only to display an implied wage for our own row

COMPANY = "Best Pegasus"
FIELDS = ["Contractor_Name", "Federal_ID", "Region", "Job_Title", "Skill_Level",
          "Hourly_Wage_Rate", "Hourly_Bill_Rate", "Markup_Percent", "Is_Our_Rate"]


def baseline_rows():
    rows = []
    for title, vals in BASELINE_2026_BILL.items():
        for skill, bill in zip(SKILLS, vals):
            wage = bill / (1 + ASSUMED_MARKUP / 100)
            for region in ("Region 1", "Region 2", "Region 3"):
                rows.append({
                    "Contractor_Name": COMPANY,
                    "Federal_ID": "NA",
                    "Region": region,
                    "Job_Title": title,
                    "Skill_Level": skill,
                    "Hourly_Wage_Rate": f"{wage:.2f}",
                    "Hourly_Bill_Rate": f"{bill:.2f}",
                    "Markup_Percent": f"{ASSUMED_MARKUP:.2f}",
                    "Is_Our_Rate": "true",
                })
    return rows


def main():
    all_rows = baseline_rows()
    files = sorted(glob.glob(os.path.join(PRICING_DIR, "*.pdf")))
    vendor_count = 0
    for f in files:
        base = os.path.basename(f)
        if "Contractorinfo" in base or base.lower().startswith("main"):
            continue
        contractor, fid, markup, latest, rows = extract_pdf(f)
        if not rows:
            print("WARN no rows:", base); continue
        all_rows.extend(rows)
        vendor_count += 1
        print(f"  + {contractor}: {len(rows)} rows")

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(all_rows)

    print(f"\nVendors: {vendor_count} | Total rows: {len(all_rows)} | -> {OUT}")


if __name__ == "__main__":
    main()
