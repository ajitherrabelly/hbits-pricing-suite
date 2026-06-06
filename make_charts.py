# -*- coding: utf-8 -*-
"""Render executive market-analytics charts as PNGs (for the PDF/PPTX deck)."""
import json, os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUTDIR = "charts"
GREEN, BLUE, AMBER, PURPLE, GRAY = "#0d7a4f", "#2a64c4", "#d99a16", "#7048c4", "#9aa6ba"
PALETTE = [GREEN, BLUE, AMBER, PURPLE, "#1f8a8a", "#c4585a", "#5a78c4", GRAY]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.titlesize": 14,
                     "axes.titleweight": "bold", "axes.edgecolor": "#cccccc"})


def load():
    txt = open("analytics_data.js", encoding="utf-8").read()
    txt = re.sub(r"^\s*window\.ANALYTICS\s*=\s*", "", txt).rstrip().rstrip(";")
    return json.loads(txt)


def money(n):
    n = float(n or 0)
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.1f}M"
    if n >= 1e3: return f"${n/1e3:.0f}K"
    return f"${n:.0f}"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, name), dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  wrote", name)


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    A = load()
    years = [str(y) for y in A["years"]]
    py = A["kpi"]["perYear"]

    # 1) Market trend: placements bars + dollars line
    fig, ax1 = plt.subplots(figsize=(9, 5))
    placements = [py[y]["closures"] for y in years]
    dollars = [py[y]["dollars"] for y in years]
    bars = ax1.bar(years, placements, color=GREEN, width=0.55, label="Placements")
    for b, v in zip(bars, placements):
        ax1.text(b.get_x() + b.get_width()/2, v + 8, f"{v:,}", ha="center", fontweight="bold")
    ax1.set_ylabel("Placements won"); ax1.set_ylim(0, max(placements) * 1.18)
    ax2 = ax1.twinx()
    ax2.plot(years, dollars, color=BLUE, marker="o", lw=3, ms=9, label="Award $")
    for x, v in zip(years, dollars):
        ax2.text(x, v, "  " + money(v), color=BLUE, fontweight="bold", va="bottom")
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: money(v)))
    ax2.set_ylabel("Award $"); ax2.set_ylim(0, max(dollars) * 1.2)
    ax1.set_title("HBITS market activity by year")
    save(fig, "trend.png")

    # 2) Top 10 vendors by placements
    topV = A["vendors"][:10][::-1]
    fig, ax = plt.subplots(figsize=(9, 5.4))
    vals = [v["total"] for v in topV]
    bars = ax.barh([v["name"] for v in topV], vals, color=GREEN)
    for b, v, d in zip(bars, vals, [x["dtotal"] for x in topV]):
        ax.text(v + 3, b.get_y() + b.get_height()/2, f"{v}  ({money(d)})", va="center", fontsize=9)
    ax.set_xlim(0, max(vals) * 1.25)
    ax.set_title("Market leaders — placements won (2023–2025)")
    ax.set_xlabel("Placements")
    save(fig, "vendors.png")

    # 3) Market share donut (top 7 + others)
    top7 = A["vendors"][:7]
    others = sum(v["total"] for v in A["vendors"][7:])
    labels = [v["name"] for v in top7] + ["All other vendors"]
    sizes = [v["total"] for v in top7] + [others]
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    wedges, _, autotexts = ax.pie(sizes, colors=PALETTE[:7] + [GRAY], autopct=lambda p: f"{p:.0f}%",
                                  pctdistance=0.8, startangle=90, wedgeprops=dict(width=0.42, edgecolor="white"))
    for t in autotexts: t.set_fontsize(9); t.set_color("white"); t.set_fontweight("bold")
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=9, frameon=False)
    ax.set_title("Market share — placements")
    save(fig, "share.png")

    # 4) Vendor momentum (top 6 x 3 years)
    mV = A["vendors"][:6]
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    import numpy as np
    x = np.arange(len(mV)); w = 0.26
    ax.bar(x - w, [v["c2023"] for v in mV], w, label="2023", color="#9fc4e8")
    ax.bar(x, [v["c2024"] for v in mV], w, label="2024", color="#4a86c8")
    ax.bar(x + w, [v["c2025"] for v in mV], w, label="2025", color="#114e8a")
    ax.set_xticks(x); ax.set_xticklabels([v["name"] for v in mV], rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("Placements"); ax.legend(); ax.set_title("Who is gaining and who is fading")
    save(fig, "momentum.png")

    # 5) Top agencies
    ag = A["agencies"][:10][::-1]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    vals = [a["closures"] for a in ag]
    bars = ax.barh([a["name"][:38] for a in ag], vals, color=AMBER)
    for b, v in zip(bars, vals):
        ax.text(v + 2, b.get_y() + b.get_height()/2, str(v), va="center", fontsize=9)
    ax.set_xlim(0, max(vals) * 1.15)
    ax.set_title("Who is buying — top State agencies"); ax.set_xlabel("Placements")
    save(fig, "agencies.png")

    # 6) Hottest roles (latest year)
    ly = years[-1]
    rows = sorted(A["titles"][ly], key=lambda r: r[1], reverse=True)[:12][::-1]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    vals = [r[1] for r in rows]
    bars = ax.barh([r[0] for r in rows], vals, color=PURPLE)
    for b, v in zip(bars, vals):
        ax.text(v + 0.5, b.get_y() + b.get_height()/2, str(v), va="center", fontsize=9)
    ax.set_xlim(0, max(vals) * 1.15)
    ax.set_title(f"Hottest roles by placements ({ly})"); ax.set_xlabel("Placements")
    save(fig, "roles.png")

    print("charts done ->", OUTDIR)


if __name__ == "__main__":
    main()
