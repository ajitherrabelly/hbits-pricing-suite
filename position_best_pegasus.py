"""Reprice Best Pegasus to land at a target rank in EVERY role (Title x Region x Skill).

Strategy: for each combo, look at all competitor bill rates sorted ascending and set
Best Pegasus's bill rate to a value that places it at TARGET_RANK among all bidders
(competitors + us). Rank #1 = lowest (most competitive) bill rate.

TARGET_RANK = 19  -> 18 competitors priced below us, the rest above (mid-field).
Works in integer cents to avoid float edge cases; guarantees exactly (TARGET_RANK-1)
competitors strictly below us and no ties, so the rank is exact.
"""
import csv

CSV = "vendors_rates.csv"
TARGET_RANK = 19
ASSUMED_MARKUP = 30.0  # display-only implied wage = bill / (1 + markup/100)
COMPANY = "Best Pegasus"
FIELDS = ["Contractor_Name", "Federal_ID", "Region", "Job_Title", "Skill_Level",
          "Hourly_Wage_Rate", "Hourly_Bill_Rate", "Markup_Percent", "Is_Our_Rate"]


def find_clean(comp_cents, need_below):
    """Find a cent value with exactly `need_below` competitors strictly below it and
    no tie (no competitor equal to it). Returns the value, or None if impossible
    (happens when the boundary competitors are tied)."""
    if need_below < 1 or need_below > len(comp_cents) - 1:
        return None
    lo = comp_cents[need_below - 1]
    hi = comp_cents[need_below]
    mid = (lo + hi) // 2
    for delta in range(0, 5000):
        for t in (mid + delta, mid - delta):
            below = sum(1 for x in comp_cents if x < t)
            equal = sum(1 for x in comp_cents if x == t)
            if below == need_below and equal == 0:
                return t
    return None


def target_cents(comp_cents):
    """Place us at TARGET_RANK if possible. If the boundary competitors are tied,
    fall back to the nearest achievable rank (preferring one notch more competitive).
    Returns (cents, achieved_rank)."""
    ideal = TARGET_RANK - 1  # competitors strictly below for the target rank
    # preference order of "competitors below": ideal first, then +-1, +-2, ...
    order = [ideal]
    for d in range(1, len(comp_cents)):
        if ideal - d >= 1:
            order.append(ideal - d)
        if ideal + d <= len(comp_cents) - 1:
            order.append(ideal + d)
    for nb in order:
        t = find_clean(comp_cents, nb)
        if t is not None:
            return t, nb + 1
    return None, None


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    competitors = [r for r in rows if r["Is_Our_Rate"] != "true"]

    # group competitor bill rates (in cents) by combo
    groups = {}
    for r in competitors:
        key = (r["Job_Title"], r["Region"], r["Skill_Level"])
        cents = round(float(r["Hourly_Bill_Rate"]) * 100)
        groups.setdefault(key, []).append(cents)

    new_bp = []
    off_target = []
    for (title, region, skill), cents in groups.items():
        cents.sort()
        t, achieved = target_cents(cents)
        if t is None:
            off_target.append((title, region, skill, "unrankable"))
            continue
        if achieved != TARGET_RANK:
            off_target.append((title, region, skill, f"rank {achieved} (boundary tie)"))
        bill = t / 100.0
        wage = bill / (1 + ASSUMED_MARKUP / 100)
        new_bp.append({
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

    out = new_bp + competitors
    with open(CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)

    print(f"Best Pegasus rows written: {len(new_bp)} (target rank #{TARGET_RANK})")
    print(f"Competitor rows: {len(competitors)} | Total rows: {len(out)}")
    on_target = len(new_bp) - len([o for o in off_target if o[3] != 'unrankable'])
    print(f"Combos exactly at rank #{TARGET_RANK}: {on_target} / {len(new_bp)}")
    if off_target:
        print(f"Off-target combos ({len(off_target)}) - boundary ties, nearest rank used:")
        for o in off_target:
            print("   ", o)


if __name__ == "__main__":
    main()
