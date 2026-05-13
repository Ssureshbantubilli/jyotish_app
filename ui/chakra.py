"""
ui/chakra.py
──────────────────────────────────────────────────────────────
Jathaka Chakra (South Indian Rasi Chart) renderer.

Public API
──────────────────────────────────────────────────────────────
    chakra_svg(chart, title="", size=480) -> str
        Returns a self-contained <svg> string — embed in HTML or Streamlit.

    chakra_png(chart, title="", figsize=6.0) -> bytes
        Returns PNG bytes rendered via matplotlib — for DOCX embedding.
"""
from __future__ import annotations
import io

# ── South Indian fixed grid: sign_number → (row, col) ────────────────────────
# 4×4 grid; centre 2×2 (rows 1-2, cols 1-2) is a decorative panel.
#
#  [12][ 1][ 2][ 3]
#  [11][  ][  ][ 4]
#  [10][  ][  ][ 5]
#  [ 9][ 8][ 7][ 6]

SIGN_GRID: dict[int, tuple[int, int]] = {
    12: (0, 0),  1: (0, 1),  2: (0, 2),  3: (0, 3),
    11: (1, 0),                            4: (1, 3),
    10: (2, 0),                            5: (2, 3),
     9: (3, 0),  8: (3, 1),  7: (3, 2),  6: (3, 3),
}

SIGN_NAMES: dict[int, str] = {
    1: "Mesha",    2: "Vrishabha", 3: "Mithuna",  4: "Karka",
    5: "Simha",    6: "Kanya",     7: "Tula",      8: "Vrischika",
    9: "Dhanu",   10: "Makara",   11: "Kumbha",   12: "Meena",
}

# Short abbreviations used inside cells
P_SHORT: dict[str, str] = {
    "Surya": "Su", "Chandra": "Mo", "Budha": "Me", "Shukra": "Ve",
    "Mangal": "Ma", "Guru": "Ju", "Shani": "Sa", "Rahu": "Ra", "Ketu": "Ke",
}

# Planet colours (shared between SVG + matplotlib)
P_COLOR: dict[str, str] = {
    "Surya":   "#FFB84D",
    "Chandra": "#B0C8FF",
    "Budha":   "#72E872",
    "Shukra":  "#FFB0D0",
    "Mangal":  "#FF6666",
    "Guru":    "#FFE050",
    "Shani":   "#B8B8CC",
    "Rahu":    "#7AD8C0",
    "Ketu":    "#D8A870",
}

# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _build_sign_info(chart: dict) -> dict[int, dict]:
    """Map sign_number → {house, occupants, is_lagna}."""
    lagna_sign = chart["lagna_sign"]        # 1–12
    houses     = chart["houses"]            # {1..12: {sign, lord, occupants}}
    info: dict[int, dict] = {}
    for h in range(1, 13):
        s = ((lagna_sign - 1 + h - 1) % 12) + 1
        info[s] = {
            "house":     h,
            "occupants": houses[h]["occupants"],
            "is_lagna":  (h == 1),
        }
    return info


# ─────────────────────────────────────────────────────────────────────────────
# SVG renderer  (for Streamlit / HTML infographic)
# ─────────────────────────────────────────────────────────────────────────────

def chakra_svg(chart: dict, title: str = "", size: int = 480) -> str:
    """
    Return a self-contained <svg> string of the South Indian Rasi Chakra.

    Parameters
    ----------
    chart   : dict returned by engine.compute_chart()
    title   : optional person name shown above the grid
    size    : pixel width/height of the grid (must be divisible by 4)
    """
    lagna_sign = chart["lagna_sign"]
    sign_info  = _build_sign_info(chart)

    CW = size // 4            # cell width
    CH = size // 4            # cell height
    TITLE_H = 40              # reserved height for title bar
    W  = size
    H  = size + TITLE_H

    elems: list[str] = []

    # ── outer background ────────────────────────────────────────────────────
    elems.append(
        f'<rect width="{W}" height="{H}" fill="#0D0920" rx="10"/>'
    )

    # ── decorative header ───────────────────────────────────────────────────
    safe_title = (title or "Jathaka Chakra")[:40]
    elems.append(
        f'<text x="{W//2}" y="26" font-size="15" fill="#D8C8F8" '
        f'text-anchor="middle" font-family="Georgia,serif" font-weight="bold">'
        f'Jathaka Chakra'
        f'</text>'
    )
    if title:
        elems.append(
            f'<text x="{W//2}" y="40" font-size="11" fill="#9080C0" '
            f'text-anchor="middle" font-family="Georgia,serif">'
            f'{safe_title}'
            f'</text>'
        )

    # ── cells ────────────────────────────────────────────────────────────────
    for sign_num, (row, col) in SIGN_GRID.items():
        info = sign_info[sign_num]
        x  = col * CW
        y  = TITLE_H + row * CH
        cx = x + CW // 2

        is_lag = info["is_lagna"]
        bg     = "#2A1260" if is_lag else "#16102A"
        ec     = "#FFD700" if is_lag else "#5A4080"
        sw     = "2.5"    if is_lag else "1.2"

        # cell background
        elems.append(
            f'<rect x="{x+1}" y="{y+1}" width="{CW-2}" height="{CH-2}" '
            f'rx="4" fill="{bg}" stroke="{ec}" stroke-width="{sw}"/>'
        )

        # tiny house number (top-left corner)
        hn = info["house"]
        elems.append(
            f'<text x="{x+5}" y="{y+13}" font-size="9" fill="#7060A0" '
            f'font-family="monospace">{hn}</text>'
        )

        # sign name (top-centre)
        sname = SIGN_NAMES[sign_num]
        elems.append(
            f'<text x="{cx}" y="{y+25}" font-size="10" fill="#A898D0" '
            f'text-anchor="middle" font-family="Georgia,serif" '
            f'font-style="italic">{sname}</text>'
        )

        # lagna indicator
        if is_lag:
            elems.append(
                f'<text x="{cx}" y="{y+38}" font-size="9" fill="#FFD700" '
                f'text-anchor="middle" font-family="sans-serif" '
                f'font-weight="bold">↑ Lagna</text>'
            )
            planet_y0 = y + 54
        else:
            planet_y0 = y + 42

        # planets
        occupants = info["occupants"][:6]
        for i, pname in enumerate(occupants):
            pshort = P_SHORT.get(pname, pname[:2])
            pcolor = P_COLOR.get(pname, "#C0C0E0")
            py = planet_y0 + i * 15
            if py + 12 <= y + CH:
                elems.append(
                    f'<text x="{cx}" y="{py}" font-size="13" fill="{pcolor}" '
                    f'text-anchor="middle" font-family="sans-serif" '
                    f'font-weight="bold">{pshort}</text>'
                )

    # ── centre panel (decorative Om + chart details) ─────────────────────────
    cx0 = 1 * CW
    cy0 = TITLE_H + 1 * CH
    cw2 = 2 * CW
    ch2 = 2 * CH
    mc  = cx0 + cw2 // 2
    mr  = cy0 + ch2 // 2

    # subtle gradient-like radial effect via concentric rects
    for s in [80, 60, 40, 20]:
        alpha = int(40 * (s / 80))
        elems.append(
            f'<rect x="{mc - s}" y="{mr - s}" width="{s*2}" height="{s*2}" '
            f'rx="{s//3}" fill="none" stroke="#3A2080" stroke-width="1" opacity="0.6"/>'
        )

    elems.append(
        f'<rect x="{cx0}" y="{cy0}" width="{cw2}" height="{ch2}" '
        f'fill="#0D0920" stroke="#5A4080" stroke-width="1.2"/>'
    )
    # OM symbol
    elems.append(
        f'<text x="{mc}" y="{mr + 10}" font-size="52" fill="#3A2088" '
        f'text-anchor="middle" font-family="serif" opacity="0.85">ॐ</text>'
    )
    # Lagna info in centre
    lagna_sign_name = SIGN_NAMES[lagna_sign]
    elems.append(
        f'<text x="{mc}" y="{cy0 + 20}" font-size="9" fill="#6050A0" '
        f'text-anchor="middle" font-family="sans-serif">Lagna: {lagna_sign_name}</text>'
    )
    # Person name below OM
    if title:
        name_display = title[:22]
        elems.append(
            f'<text x="{mc}" y="{cy0 + ch2 - 12}" font-size="9" fill="#6050A0" '
            f'text-anchor="middle" font-family="sans-serif">{name_display}</text>'
        )

    # ── outer border ─────────────────────────────────────────────────────────
    elems.append(
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" '
        f'fill="none" stroke="#6040C0" stroke-width="2"/>'
    )

    body = "\n  ".join(elems)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n  {body}\n</svg>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# PNG renderer  (for DOCX embedding via matplotlib)
# ─────────────────────────────────────────────────────────────────────────────

def chakra_png(chart: dict, title: str = "", figsize: float = 6.0) -> bytes:
    """
    Return PNG bytes of the Jathaka Chakra drawn with matplotlib.
    Suitable for embedding in Word documents.

    Parameters
    ----------
    chart   : dict returned by engine.compute_chart()
    title   : optional person name
    figsize : size of the square figure in inches
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    lagna_sign = chart["lagna_sign"]
    sign_info  = _build_sign_info(chart)

    FIG_BG = "#0D0920"
    fig, ax = plt.subplots(figsize=(figsize, figsize + 0.4))
    fig.patch.set_facecolor(FIG_BG)
    ax.set_facecolor(FIG_BG)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_aspect("equal")
    ax.axis("off")

    for sign_num, (row, col) in SIGN_GRID.items():
        info     = sign_info[sign_num]
        mpl_row  = 3 - row          # matplotlib y=0 is bottom
        is_lag   = info["is_lagna"]

        bg = "#2A1260" if is_lag else "#16102A"
        ec = "#FFD700" if is_lag else "#5A4080"
        lw = 2.0       if is_lag else 1.0

        cell = mpatches.FancyBboxPatch(
            (col + 0.02, mpl_row + 0.02), 0.96, 0.96,
            boxstyle="round,pad=0.02",
            linewidth=lw, edgecolor=ec, facecolor=bg,
        )
        ax.add_patch(cell)

        cx = col + 0.50
        # house number (top-left)
        ax.text(col + 0.06, mpl_row + 0.90, str(info["house"]),
                fontsize=6.5, color="#7060A0", va="top", ha="left",
                fontfamily="monospace")

        # sign name
        sname = SIGN_NAMES[sign_num]
        ax.text(cx, mpl_row + 0.84, sname,
                fontsize=7, color="#A898D0", ha="center", va="top",
                style="italic")

        # lagna indicator
        if is_lag:
            ax.text(cx, mpl_row + 0.72, "↑ Lagna",
                    fontsize=6.5, color="#FFD700", ha="center", va="top",
                    fontweight="bold")
            py0 = mpl_row + 0.60
        else:
            py0 = mpl_row + 0.68

        # planets
        for i, pname in enumerate(info["occupants"][:5]):
            pshort = P_SHORT.get(pname, pname[:2])
            pcolor = P_COLOR.get(pname, "#C0C0E0")
            py = py0 - i * 0.135
            if py > mpl_row + 0.05:
                ax.text(cx, py, pshort,
                        fontsize=9.5, color=pcolor, ha="center", va="top",
                        fontweight="bold")

    # Centre Om panel
    import numpy as np
    centre = mpatches.Rectangle((1, 1), 2, 2,
                                  linewidth=1.5, edgecolor="#5A4080",
                                  facecolor="#0D0920")
    ax.add_patch(centre)

    # Draw decorative 8-petal lotus using polygons (avoids Devanagari font issue)
    mc_x, mc_y = 2.0, 2.0
    r_outer = 0.55
    r_inner = 0.22
    for petal in range(8):
        angle0 = np.deg2rad(petal * 45 - 22.5)
        angle1 = np.deg2rad(petal * 45 + 22.5)
        angle_mid = np.deg2rad(petal * 45)
        pts = [
            (mc_x + r_inner * np.cos(angle0), mc_y + r_inner * np.sin(angle0)),
            (mc_x + r_outer * np.cos(angle_mid), mc_y + r_outer * np.sin(angle_mid)),
            (mc_x + r_inner * np.cos(angle1), mc_y + r_inner * np.sin(angle1)),
        ]
        petal_patch = mpatches.Polygon(pts, closed=True,
                                        facecolor="#2A1060", edgecolor="#5030A0",
                                        linewidth=0.8, alpha=0.9)
        ax.add_patch(petal_patch)
    # centre circle
    circ = plt.Circle((mc_x, mc_y), r_inner,
                       color="#3A1878", linewidth=1, zorder=5)
    ax.add_patch(circ)
    ax.text(mc_x, mc_y, "OM",
            fontsize=8.5, color="#8060C0", ha="center", va="center",
            fontweight="bold", zorder=6)

    lagna_sign_name = SIGN_NAMES[lagna_sign]
    ax.text(2.0, 3.02, f"Lagna: {lagna_sign_name}",
            fontsize=6.5, color="#6050A0", ha="center", va="top")
    if title:
        ax.text(2.0, 1.06, title[:24],
                fontsize=6.5, color="#6050A0", ha="center", va="bottom")

    # Title
    header = f"Jathaka Chakra — {title}" if title else "Jathaka Chakra"
    fig.text(0.5, 0.98, header,
             ha="center", va="top", fontsize=11, color="#D8C8F8",
             fontweight="bold")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=FIG_BG, pad_inches=0.05)
    plt.close(fig)
    return buf.getvalue()
