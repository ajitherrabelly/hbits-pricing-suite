"""hbits_db.py — thin consumer API over hbits.db.

Build the DB first:  python build_db.py
Then in any script:

    import hbits_db as h
    for row in h.vendor_wins():            # wins + pricing per vendor
        print(row["canonical_name"], row["wins"], row["avg_bill"], row["markup"])

    h.query("SELECT * FROM closures WHERE norm_key=? AND is_hbits=1", ("KNOWLEDGE BUILDERS",))

Run directly for a demo:  python hbits_db.py
"""
import os, sqlite3

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hbits.db")


def connect():
    if not os.path.exists(DB):
        raise FileNotFoundError(f"{DB} not found — run `python build_db.py` first.")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def query(sql, params=()):
    """Run any SQL, return list of dict-like rows."""
    with connect() as con:
        return [dict(r) for r in con.execute(sql, params).fetchall()]


# ---- convenience accessors -------------------------------------------------
def vendor_wins():
    """Per-vendor: total wins, award $, avg competitor bill, markup."""
    return query("SELECT * FROM v_vendor_pricing_vs_wins ORDER BY wins DESC")


def wins_by_year(norm_key=None):
    if norm_key:
        return query("SELECT * FROM v_vendor_year_wins WHERE norm_key=? ORDER BY year", (norm_key,))
    return query("SELECT * FROM v_vendor_year_wins ORDER BY year, wins DESC")


def title_demand(year=None):
    if year:
        return query("SELECT * FROM v_title_demand WHERE year=? ORDER BY wins DESC", (year,))
    return query("SELECT job_title, SUM(wins) wins, SUM(total_amount) total_amount "
                 "FROM v_title_demand GROUP BY job_title ORDER BY wins DESC")


def vendor_key(name_fragment):
    """Resolve a fuzzy name to its norm_key via the alias table."""
    rows = query("SELECT DISTINCT norm_key, canonical_name FROM vendors "
                 "WHERE UPPER(canonical_name) LIKE ?", (f"%{name_fragment.upper()}%",))
    return rows[0]["norm_key"] if rows else None


# ---- demo ------------------------------------------------------------------
if __name__ == "__main__":
    print("=== HBITS DB demo ===\n")

    print("Top 8 vendors - WINS vs PRICING (do the cheapest win?)")
    print(f"{'Vendor':40} {'wins':>5} {'$ won':>14} {'avgBill':>8} {'markup':>7}")
    for r in vendor_wins()[:8]:
        amt = f"${(r['total_amount'] or 0)/1e6:.1f}M"
        print(f"{(r['canonical_name'] or '')[:40]:40} {r['wins']:>5} {amt:>14} "
              f"{(r['avg_bill'] or 0):>8.2f} {(r['markup'] or 0):>6.0f}%")

    k = vendor_key("Knowledge Builders")
    print(f"\nKBI ({k}) wins by year:")
    for r in wins_by_year(k):
        print(f"   {r['year']}: {r['wins']} wins, ${(r['total_amount'] or 0)/1e6:.1f}M")

    print("\nTop 6 roles by demand (HBITS placements, 3 yrs):")
    for r in title_demand()[:6]:
        print(f"   {r['job_title']:24} {int(r['wins']):>4} wins")

    print("\nInsight: KBI is #1 in wins but NOT cheapest on bill - confirms they")
    print("win on sourcing/volume + fat markup, not low price.")
