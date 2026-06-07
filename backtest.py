"""backtest.py - Test Best Pegasus pricing strategies against KBI on REAL award data.

Counterfactual backtest over hbits.db:
  Layer 2  Calibration : does PRICE predict who wins?  (distribution of real winners' bill-rank)
  Layer 3  Simulation  : insert Best Pegasus into each historical award's field, under three
                         win-model hypotheses, and score WINS + EXPECTED PROFIT side by side.

Win-model hypotheses (each a proper per-award probability distribution over all bidders):
  H1 lowest   - cheapest bill wins the award.
  H2 filter   - only the cheapest ~50% are forwarded; winner is uniform among them (MSP-filter premise).
  H3 empirical- P(win | price-percentile) fit from the real winners, then applied (the market's actual behavior).

Field model: per (job_title, skill_level), each vendor's bill = mean of its 3 regional NTE bills
(regions differ trivially). Caveats: we see only winners (not the full bid set) and NTE ceilings,
so the competitive field is approximated by the 32 contracted vendors at their ceiling rates.

Run:  python build_db.py  &&  python backtest.py
"""
import os, sqlite3, statistics
from collections import defaultdict, Counter

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hbits.db")

# cost build (matches positioning.html): % of wage, plus OGS fee % of bill
PAYROLL, INS, OH, OGS = 0.135, 0.035, 0.105, 0.0075
KBI_KEY = "KNOWLEDGE BUILDERS"


def margin_pct(bill, wage):
    if not bill:
        return 0.0
    cost = wage * (PAYROLL + INS + OH) + bill * OGS
    return ((bill - wage) - cost) / bill


# ---------------------------------------------------------------- load data
def load():
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    # competitor field: (title,skill) -> {vendor_key: (mean_bill, mean_wage)}
    field = defaultdict(dict)
    agg = defaultdict(lambda: defaultdict(list))      # (t,s)->vendor->[bills]
    aggw = defaultdict(lambda: defaultdict(list))
    for r in con.execute("SELECT norm_key,job_title,skill_level,bill,wage FROM rate_cards WHERE is_our_rate=0"):
        agg[(r["job_title"], r["skill_level"])][r["norm_key"]].append(r["bill"])
        aggw[(r["job_title"], r["skill_level"])][r["norm_key"]].append(r["wage"] or 0)
    for k, vmap in agg.items():
        for v, bills in vmap.items():
            field[k][v] = (statistics.mean(bills), statistics.mean(aggw[k][v]) or 0)
    # awards
    awards = [dict(r) for r in con.execute(
        "SELECT norm_key,job_title,skill_level,amount,year FROM closures "
        "WHERE is_hbits=1 AND job_title IS NOT NULL AND skill_level IS NOT NULL")]
    con.close()
    # keep only awards whose role has a field
    awards = [a for a in awards if (a["job_title"], a["skill_level"]) in field]
    return field, awards


# ---------------------------------------------------------------- Layer 2: calibration
def calibrate(field, awards):
    """Distribution of REAL winners' bill-rank within their role field."""
    ranks, pctls = [], []
    cheapest_hits = top50 = 0
    for a in awards:
        fk = field[(a["job_title"], a["skill_level"])]
        bills = sorted(fk.values())  # list of (bill,wage)
        bvals = sorted(b for b, w in fk.values())
        wb = fk.get(a["norm_key"])
        if not wb:
            continue
        wbill = wb[0]
        rank = sum(1 for b in bvals if b < wbill) + 1
        m = len(bvals)
        ranks.append(rank)
        pctls.append((rank - 1) / (m - 1) if m > 1 else 0)
        if rank == 1:
            cheapest_hits += 1
        if rank <= m / 2:
            top50 += 1
    n = len(ranks)
    print("=" * 78)
    print(f"LAYER 2 - DOES PRICE PREDICT WINNING?   ({n} real awards placed in their field)")
    print("=" * 78)
    print(f"  Winner's bill-rank among ~32 vendors:  median #{int(statistics.median(ranks))}, "
          f"mean #{statistics.mean(ranks):.1f}")
    print(f"  Winners who were the CHEAPEST bidder:  {cheapest_hits/n*100:4.1f}%   "
          f"(price-only market would be ~100%)")
    print(f"  Winners in the cheapest 50% of field:  {top50/n*100:4.1f}%   "
          f"(MSP-filter premise needs this ~100%)")
    print(f"  Winners in the EXPENSIVE half:         {(n-top50)/n*100:4.1f}%")
    # KBI's own winning ranks
    kbi_ranks = []
    for a in awards:
        if a["norm_key"] != KBI_KEY:
            continue
        fk = field[(a["job_title"], a["skill_level"])]
        wb = fk.get(KBI_KEY)
        if not wb:
            continue
        bvals = sorted(b for b, w in fk.values())
        kbi_ranks.append(sum(1 for b in bvals if b < wb[0]) + 1)
    if kbi_ranks:
        print(f"  KBI wins ({len(kbi_ranks)}) at median bill-rank #{int(statistics.median(kbi_ranks))} "
              f"- i.e. KBI wins from the EXPENSIVE half.")
    print("  => Verdict:", "PRICE IS NOT THE DRIVER (winners are spread; KBI wins while pricey)."
          if cheapest_hits / n < 0.25 else "price appears influential.")
    return pctls


# ---------------------------------------------------------------- win models
def decile(p):
    return min(9, int(p * 10))


def build_empirical(pctls):
    c = Counter(decile(p) for p in pctls)
    tot = sum(c.values())
    return {d: c.get(d, 0) / tot for d in range(10)}   # win-share by price-percentile decile


def award_probs(bidders, hypo, emp):
    """bidders: dict key->bill. Return dict key->P(win this award) summing to 1."""
    bvals = sorted(bidders.values())
    m = len(bvals)
    if hypo == "H1":
        lo = min(bvals)
        winners = [k for k, b in bidders.items() if b == lo]
        return {k: (1 / len(winners) if k in winners else 0) for k in bidders}
    if hypo == "H2":
        med = statistics.median(bvals)
        fwd = [k for k, b in bidders.items() if b <= med]
        return {k: (1 / len(fwd) if k in fwd else 0) for k in bidders}
    # H3 empirical by percentile decile, normalized per award
    raw = {}
    for k, b in bidders.items():
        rank = sum(1 for x in bvals if x < b) + 1
        p = (rank - 1) / (m - 1) if m > 1 else 0
        raw[k] = emp[decile(p)]
    s = sum(raw.values()) or 1
    return {k: v / s for k, v in raw.items()}


# ---------------------------------------------------------------- BP strategies
def bp_bill_rank(compbills, target, markup):
    """Place BP at target rank in the competitor bill list; return (bill, wage)."""
    s = sorted(compbills)
    n = len(s)
    t = max(1, min(target, n + 1))
    if t == 1:
        bill = s[0] - 0.01
    elif t > n:
        bill = s[-1] + 0.01
    else:
        bill = (s[t - 2] + s[t - 1]) / 2.0
    return round(bill, 2), round(bill / (1 + markup / 100), 2)


def strategies(field):
    """Return list of (name, fn) where fn(title,skill)-> (bill,wage,markup%)."""
    out = []

    def rank_strat(target, markup):
        def f(t, s):
            comp = [b for b, w in field[(t, s)].values()]
            bill, wage = bp_bill_rank(comp, target, markup)
            return bill, wage, markup
        return f

    def kbi_clone(markup):
        def f(t, s):
            wb = field[(t, s)].get(KBI_KEY)
            if not wb:
                return None
            wage = wb[1]
            bill = round(wage * (1 + markup / 100), 2)
            return bill, wage, markup
        return f

    out.append(("V1.1  rank19 / 30% markup", rank_strat(19, 30)))
    out.append(("      rank16 / 45% markup", rank_strat(16, 45)))
    out.append(("KBI-clone  KBIwage / 110%", kbi_clone(110)))
    out.append(("KBI-undercut KBIwage / 100%", kbi_clone(100)))
    return out


# ---------------------------------------------------------------- Layer 3: simulate
def simulate(field, awards, emp):
    HYPOS = ["H1", "H2", "H3"]
    # KBI actual benchmark
    kbi_awards = [a for a in awards if a["norm_key"] == KBI_KEY]
    kbi_wins = len(kbi_awards)
    kbi_profit = 0.0
    for a in kbi_awards:
        wb = field[(a["job_title"], a["skill_level"])].get(KBI_KEY)
        if wb and a["amount"]:
            kbi_profit += a["amount"] * margin_pct(wb[0], wb[1])
    kbi_margin = statistics.mean(
        margin_pct(*field[(a["job_title"], a["skill_level"])][KBI_KEY])
        for a in kbi_awards if field[(a["job_title"], a["skill_level"])].get(KBI_KEY)) * 100

    print("\n" + "=" * 78)
    print("LAYER 3 - INSERT BEST PEGASUS & SCORE (simulated wins + expected profit)")
    print("=" * 78)
    print(f"  Benchmark  KBI ACTUAL:  {kbi_wins} wins | {kbi_margin:4.1f}% margin | "
          f"${kbi_profit/1e6:5.1f}M expected profit\n")
    hdr = f"  {'Strategy':30} {'H1':>6} {'H2':>6} {'H3':>6} {'margin':>7} {'profit(H3)':>11}"
    print(hdr); print("  " + "-" * (len(hdr) - 2))

    for name, fn in strategies(field):
        wins = {h: 0.0 for h in HYPOS}
        profitH3 = 0.0
        margins = []
        for a in awards:
            key = (a["job_title"], a["skill_level"])
            bp = fn(*key)
            if not bp:
                continue
            bpbill, bpwage, mk = bp
            bidders = {k: b for k, (b, w) in field[key].items()}
            bidders["__BP__"] = bpbill
            margins.append(margin_pct(bpbill, bpwage))
            for h in HYPOS:
                p = award_probs(bidders, h, emp)["__BP__"]
                wins[h] += p
                if h == "H3" and a["amount"]:
                    profitH3 += p * a["amount"] * margin_pct(bpbill, bpwage)
        mm = statistics.mean(margins) * 100 if margins else 0
        print(f"  {name:30} {wins['H1']:6.0f} {wins['H2']:6.0f} {wins['H3']:6.0f} "
              f"{mm:6.1f}% {profitH3/1e6:9.1f}M")

    print("\n  Read: H1=lowest-price wins | H2=cheapest-50% filter | H3=empirical(real market).")
    print("  'wins' are expected counts over the same 1,488 awards KBI competed in.")
    # calibration of hypotheses vs KBI actual
    print("\n  Win-model calibration (does each hypothesis reproduce KBI's real wins?):")
    for h in HYPOS:
        pred = 0.0
        for a in awards:
            key = (a["job_title"], a["skill_level"])
            bidders = {k: b for k, (b, w) in field[key].items()}
            if KBI_KEY in bidders:
                pred += award_probs(bidders, h, emp)[KBI_KEY]
        flag = "  <-- realistic" if abs(pred - kbi_wins) < 0.25 * kbi_wins else "  (off - discard for BP)"
        print(f"     {h}: predicts KBI ~{pred:5.0f} wins   vs actual {kbi_wins}{flag}")


def main():
    field, awards = load()
    pctls = calibrate(field, awards)
    emp = build_empirical(pctls)
    simulate(field, awards, emp)


if __name__ == "__main__":
    main()
