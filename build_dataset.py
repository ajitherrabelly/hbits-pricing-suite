"""Build vendors_rates.csv = competitors + BOTH Best Pegasus formula versions.

Adds a Formula_Version column:
  ""    -> competitor rows (Is_Our_Rate=false)
  "v1"  -> Best Pegasus BASELINE (from NYS OGS IT Vendor Rate Estimation.pdf, 30 titles)
  "v1.1"-> Best Pegasus RANK-#19 positioning (derived from competitor field, 31 titles)
"""
import csv
from generate_csv import BASELINE_2026_BILL, SKILLS, ASSUMED_MARKUP
from position_best_pegasus import target_cents, TARGET_RANK

CSV = "vendors_rates.csv"
COMPANY = "Best Pegasus"
REGIONS = ["Region 1", "Region 2", "Region 3"]
FIELDS = ["Contractor_Name", "Federal_ID", "Region", "Job_Title", "Skill_Level",
          "Hourly_Wage_Rate", "Hourly_Bill_Rate", "Markup_Percent", "Is_Our_Rate",
          "Formula_Version"]


def bp_row(region, title, skill, bill, version):
    wage = bill / (1 + ASSUMED_MARKUP / 100)
    return {
        "Contractor_Name": COMPANY, "Federal_ID": "NA", "Region": region,
        "Job_Title": title, "Skill_Level": skill,
        "Hourly_Wage_Rate": f"{wage:.2f}", "Hourly_Bill_Rate": f"{bill:.2f}",
        "Markup_Percent": f"{ASSUMED_MARKUP:.2f}", "Is_Our_Rate": "true",
        "Formula_Version": version,
    }


def main():
    src = list(csv.DictReader(open(CSV, encoding="utf-8")))
    competitors = []
    for r in src:
        if r["Is_Our_Rate"] == "true":
            continue
        competitors.append({
            "Contractor_Name": r["Contractor_Name"], "Federal_ID": r["Federal_ID"],
            "Region": r["Region"], "Job_Title": r["Job_Title"], "Skill_Level": r["Skill_Level"],
            "Hourly_Wage_Rate": r["Hourly_Wage_Rate"], "Hourly_Bill_Rate": r["Hourly_Bill_Rate"],
            "Markup_Percent": r["Markup_Percent"], "Is_Our_Rate": "false", "Formula_Version": "",
        })

    # ---- Version 1: baseline-doc bill rates (Region 1 values applied to all 3 regions) ----
    v1 = []
    for title, vals in BASELINE_2026_BILL.items():
        for skill, bill in zip(SKILLS, vals):
            for region in REGIONS:
                v1.append(bp_row(region, title, skill, bill, "v1"))

    # ---- Version 1.1: rank-#TARGET_RANK positioning derived from competitor field ----
    groups = {}
    for r in competitors:
        key = (r["Job_Title"], r["Region"], r["Skill_Level"])
        groups.setdefault(key, []).append(round(float(r["Hourly_Bill_Rate"]) * 100))
    v11 = []
    off = 0
    for (title, region, skill), cents in groups.items():
        cents.sort()
        t, rank = target_cents(cents)
        if t is None:
            continue
        if rank != TARGET_RANK:
            off += 1
        v11.append(bp_row(region, title, skill, t / 100.0, "v1.1"))

    out = competitors + v1 + v11
    with open(CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)

    print(f"Competitors: {len(competitors)}")
    print(f"v1 (baseline) BP rows: {len(v1)}  ({len(v1)//12} titles x 4 skills x 3 regions)")
    print(f"v1.1 (rank #{TARGET_RANK}) BP rows: {len(v11)}  ({off} off-target due to ties)")
    print(f"Total rows: {len(out)} -> {CSV}")


if __name__ == "__main__":
    main()
