"""
JYOTISHA APP — Main UI
Streamlit-based interface for:
  1. Individual Vedic Astrology Report
  2. Spouse Compatibility Report
  3. Combined 25-Year Dampati Report with Graph
"""

import streamlit as st
import datetime
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.calc import compute_chart
from engine.geocode import geocode
from engine.report import (
    generate_individual_report,
    generate_compatibility_report,
    generate_combined_report,
)
from engine.interpret import (
    NAK_INTERPRETATION,
    compute_year_scores,
    compute_combined_year_scores,
    calc_ashtakoot,
)
from engine import generate_dasha_predictions
from engine.predictions import compute_marriage_timing

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jyotisha Vedic Astrology",
    page_icon="🪔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── STYLING ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,600;1,400&display=swap');

.main-header {
    text-align: center;
    padding: 1.2rem 0 0.5rem;
    border-bottom: 2px solid #C89010;
    margin-bottom: 1.5rem;
}
.main-header h1 { font-family: 'Noto Serif', serif; color: #C89010; font-size: 2rem; margin:0; }
.main-header p  { color: #888; font-size: 0.85rem; margin: 0.3rem 0 0; }

.section-card {
    background: #0E1117;
    border: 1px solid #2A2A3A;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.planet-row { display: flex; align-items: center; gap: 12px; padding: 6px 0;
              border-bottom: 1px solid #1E1E2E; }
.planet-glyph { font-size: 1.2rem; width: 28px; text-align: center; }
.planet-name  { font-weight: 600; width: 160px; color: #E8E0C8; }
.planet-sign  { width: 130px; color: #A0C8F0; }
.planet-house { width: 60px; color: #F0C060; font-weight: 600; }
.planet-dignity { color: #80D080; font-style: italic; font-size: 0.85rem; }
.planet-debil   { color: #E08080; font-style: italic; font-size: 0.85rem; }

.score-badge-outstanding { background:#3A2800; color:#F0C040; border:1px solid #C89010;
    border-radius:6px; padding:4px 10px; font-weight:600; font-size:0.85rem; display:inline-block; }
.score-badge-excellent   { background:#0A2810; color:#40D060; border:1px solid #20A040;
    border-radius:6px; padding:4px 10px; font-weight:600; font-size:0.85rem; display:inline-block; }
.score-badge-good        { background:#0A1428; color:#60A0F0; border:1px solid #2060C8;
    border-radius:6px; padding:4px 10px; font-weight:600; font-size:0.85rem; display:inline-block; }
.score-badge-moderate    { background:#281800; color:#E0A040; border:1px solid #D07800;
    border-radius:6px; padding:4px 10px; font-weight:600; font-size:0.85rem; display:inline-block; }
.score-badge-challenging { background:#280808; color:#F06060; border:1px solid #C02020;
    border-radius:6px; padding:4px 10px; font-weight:600; font-size:0.85rem; display:inline-block; }

.yoga-card { background:#0A0810; border:1px solid #4A2080; border-radius:8px;
             padding:0.9rem; margin-bottom:0.7rem; }
.yoga-name { color:#C090FF; font-weight:600; font-size:1rem; }
.yoga-strength { color:#F0C040; font-size:0.8rem; float:right; }
.yoga-desc { color:#B0A8C0; font-size:0.85rem; margin-top:0.4rem; line-height:1.5; }

.nak-card { background: linear-gradient(135deg,#0A0820,#120A28);
            border:1px solid #6040B0; border-radius:10px; padding:1rem; }
.nak-name { color:#D0A0FF; font-size:1.3rem; font-weight:600; }
.nak-detail { color:#9080B0; font-size:0.85rem; }
.nak-insight { color:#C8C0E0; font-size:0.9rem; margin-top:0.5rem; line-height:1.55; }

.dasha-current { background:#1A0A30; border:1px solid #8040C0; border-radius:6px;
                 padding:0.7rem; margin-bottom:0.5rem; }
.dasha-row { padding:4px 0; border-bottom:1px solid #1A1A2A; display:flex; gap:8px; }
.dasha-lord { font-weight:600; color:#D0B0FF; width:100px; }
.dasha-dates { color:#8080A0; font-size:0.85rem; flex:1; }
.dasha-badge { background:#2A1040; color:#C080FF; border-radius:4px;
               padding:2px 8px; font-size:0.75rem; }

.koota-row { display:flex; align-items:center; gap:8px; padding:5px 0;
             border-bottom:1px solid #1E1E2E; }
.koota-name  { width:140px; color:#E0D8C0; font-size:0.9rem; }
.koota-score { font-weight:700; font-size:1rem; width:40px; }
.koota-bar   { flex:1; height:8px; background:#1A1A2A; border-radius:4px; overflow:hidden; }
.koota-fill  { height:8px; border-radius:4px; }
.koota-rem   { color:#8080A0; font-size:0.8rem; }

.om-header { text-align:center; color:#C89010; font-size:1.6rem;
             font-family:'Noto Serif',serif; padding:0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🪔 Jyotisha — Vedic Astrology System</h1>
  <p>Nirayana (Sidereal) • Lahiri Ayanamsha • Vimshottari Dasha<br>
  Based on BPHS • Brihat Jataka • Phaladeepika • Saravali</p>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="om-header">ॐ</div>', unsafe_allow_html=True)
    st.markdown("### Select Report Type")
    mode = st.radio("Report Type",
        ["🔮 Individual Report", "💑 Spouse Compatibility", "🌟 Combined 25-Year Report"],
        label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Shastra Sources:**")
    st.caption("• Brihat Parashara Hora Shastra")
    st.caption("• Brihat Jataka (Varahamihira)")
    st.caption("• Phaladeepika")
    st.caption("• Saravali • Uttara Kalamrita")
    st.caption("• Jataka Parijata")
    st.markdown("---")
    st.caption("Calculation: Same exact engine used in all previous reports in this session.")

# ── INPUT FORM HELPER ────────────────────────────────────────────────────────
def person_form(key_prefix: str, title: str):
    st.markdown(f"#### {title}")
    cols = st.columns([2,1,1])
    name  = cols[0].text_input("Full Name", key=f"{key_prefix}_name", placeholder="e.g. Suresh Kumar Bantubilli")
    dob   = cols[1].date_input("Date of Birth", key=f"{key_prefix}_dob",
                                min_value=datetime.date(1900,1,1),
                                max_value=datetime.date.today(),
                                value=datetime.date(1985,1,1))
    # Time
    cols2 = st.columns([1,1,2])
    tob_h = cols2[0].number_input("Hour (IST)", 0, 23, 12, key=f"{key_prefix}_h")
    tob_m = cols2[1].number_input("Minute", 0, 59, 0, key=f"{key_prefix}_m")
    place = cols2[2].text_input("Place of Birth", key=f"{key_prefix}_place",
                                 placeholder="e.g. Simhachalam, Visakhapatnam")
    tob_decimal = tob_h + tob_m / 60.0
    return name, dob, tob_decimal, place

# ── RENDER FUNCTIONS ─────────────────────────────────────────────────────────
SIGN_GLYPHS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]

def score_badge(cat: str, score: float) -> str:
    css = {"Outstanding":"outstanding","Excellent":"excellent",
           "Very Good":"good","Good":"good",
           "Moderate":"moderate","Challenging":"challenging","Difficult":"challenging"}
    cls = css.get(cat, "moderate")
    return f'<span class="score-badge-{cls}">{score:.1f} — {cat}</span>'

def render_chart_overview(c: dict, place: str):
    from ui.chakra import chakra_svg

    lagna_s = c["lagna_sign"]
    moon_s  = c["moon_sign"]

    # ── summary pills ────────────────────────────────────────────────────────
    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"**{SIGN_GLYPHS[lagna_s]} Lagna**")
        st.markdown(f"**{c['lagna_san']}** ({c['lagna_en']})")
        st.caption(f"{c['lagna_deg']:.1f}° | Lord: {c['lagna_lord']}")
    with cols[1]:
        st.markdown(f"**{SIGN_GLYPHS[moon_s]} Janma Rashi**")
        st.markdown(f"**{c['moon_san']}** ({c['moon_en']})")
        st.caption(f"{c['moon_deg']:.1f}° | Lord: {SIGN_GLYPHS[moon_s]}")
    with cols[2]:
        st.markdown("**⭐ Janma Nakshatra**")
        st.markdown(f"**{c['nakshatra']}**, Pada {c['nak_pada']}")
        st.caption(f"Lord: {c['nak_lord']} | Deity: {c['nak_deity']}")
    with cols[3]:
        st.markdown("**📅 Active Dasha**")
        st.markdown(f"**{c['active_md']['lord']} MD — {c['active_ad']['lord']} AD**")
        st.caption(f"MD ends: {c['active_md']['end'].strftime('%b %Y')}")

    # ── Jathaka Chakra ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🔯 Jathaka Chakra (South Indian Rasi Chart)")

    _svg = chakra_svg(c, c.get("name", ""), size=480)
    # Centre the SVG with a responsive wrapper
    st.markdown(
        f'<div style="display:flex;justify-content:center;margin:8px 0;">'
        f'{_svg}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Compact planet legend below the chart
    P_SHORT_LEG = {"Surya":"Su","Chandra":"Mo","Budha":"Me","Shukra":"Ve",
                   "Mangal":"Ma","Guru":"Ju","Shani":"Sa","Rahu":"Ra","Ketu":"Ke"}
    P_COLOR_LEG = {"Surya":"#FFB84D","Chandra":"#B0C8FF","Budha":"#72E872",
                   "Shukra":"#FFB0D0","Mangal":"#FF6666","Guru":"#FFE050",
                   "Shani":"#B8B8CC","Rahu":"#7AD8C0","Ketu":"#D8A870"}
    badge_parts = []
    for pname, pshort in P_SHORT_LEG.items():
        col = P_COLOR_LEG[pname]
        badge_parts.append(
            f'<span style="background:#1A1035;border:1px solid {col};border-radius:4px;'
            f'padding:2px 7px;margin:2px;font-size:0.78rem;color:{col};font-weight:600">'
            f'{pshort} = {pname}</span>'
        )
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;gap:2px;justify-content:center;'
        f'margin-top:4px;">{"".join(badge_parts)}</div>',
        unsafe_allow_html=True,
    )

def render_planets(c: dict):
    st.markdown("#### 🪐 Planetary Positions (Nirayana Sidereal)")
    PLANET_ORDER = ["Lagna","Surya","Chandra","Budha","Shukra","Mangal","Guru","Shani","Rahu","Ketu"]
    GLYPHS = {"Surya":"☀","Chandra":"🌙","Budha":"☿","Shukra":"♀","Mangal":"♂",
               "Guru":"♃","Shani":"♄","Rahu":"☊","Ketu":"☋","Lagna":"↑"}

    rows = []
    for nm in PLANET_ORDER:
        pd = c["planets"].get(nm)
        if not pd: continue
        dig = pd["dignity"]
        dig_col = ("🟢" if "Exalted" in dig else "🔴" if "Debil" in dig
                   else "🟡" if "Own" in dig else "⚪")
        rows.append({
            "Graha": f"{GLYPHS.get(nm,'')} {nm}",
            "Rashi": f"{SIGN_GLYPHS[pd['sign']]} {pd['sign_san']}",
            "Degree": f"{pd['deg']:.1f}°",
            "House": pd["house"],
            "Dignity": f"{dig_col} {dig}",
        })

    import pandas as pd_lib
    df = pd_lib.DataFrame(rows)
    st.dataframe(df, hide_index=True, width='stretch',
                 column_config={"House": st.column_config.NumberColumn("House", format="%d")})

def render_nakshatra(c: dict):
    st.markdown("#### 🌙 Nakshatra Viveka")
    st.markdown(f"""
    <div class="nak-card">
      <div class="nak-name">{c['nakshatra']} — Pada {c['nak_pada']}</div>
      <div class="nak-detail">Lord: {c['nak_lord']} | Deity: {c['nak_deity']} | Symbol: {c.get('nak_symbol','—')}</div>
      <div class="nak-insight">{NAK_INTERPRETATION.get(c['nakshatra'],'A powerful nakshatra with deep karmic significance.')}</div>
    </div>
    """, unsafe_allow_html=True)

def render_yogas(c: dict):
    st.markdown("#### ✨ Yoga Vivechana (Planetary Combinations)")
    if not c["yogas"]:
        st.info("Standard chart. Individual planetary strengths govern the chart.")
        return
    for yoga in c["yogas"]:
        st.markdown(f"""
        <div class="yoga-card">
          <span class="yoga-name">{yoga['name']}</span>
          <span class="yoga-strength">⭐ {yoga['strength']}</span>
          <br><small style="color:#8080A0">{yoga['planets']} | House {yoga['house']}</small>
          <div class="yoga-desc">{yoga['description']}</div>
        </div>
        """, unsafe_allow_html=True)

def render_dasha(c: dict):
    st.markdown("#### 🗓️ Vimshottari Dasha")
    today = datetime.date.today()

    # Current dasha highlight
    md = c["active_md"]; ad = c["active_ad"]
    st.markdown(f"""
    <div class="dasha-current">
      <b>Current Maha Dasha:</b> {md['lord']} ({md['start'].strftime('%b %Y')} — {md['end'].strftime('%b %Y')})<br>
      <b>Current Antardasha:</b> {ad['lord']} ({ad['start'].strftime('%b %Y')} — {ad['end'].strftime('%b %Y')})
    </div>
    """, unsafe_allow_html=True)

    # Dasha sequence table
    import pandas as pd_lib
    rows = []
    for d in c["dasha_seq"]:
        cur = "◄ NOW" if d["start"] <= today <= d["end"] else ""
        rows.append({"Maha Dasha": d["lord"],
                     "Start": d["start"].strftime("%b %Y"),
                     "End":   d["end"].strftime("%b %Y"),
                     "Years": f"{d['years']:.1f}",
                     "": cur})
    df = pd_lib.DataFrame(rows)
    st.dataframe(df, hide_index=True, width='stretch')

def render_year_forecast(c: dict, label: str = "", yr_from: int = 2025, yr_to: int = 2040):
    import plotly.graph_objects as go

    st.markdown(f"#### 📈 Year-Wise Forecast {f'— {label}' if label else ''}({yr_from}–{yr_to})")
    scores = compute_year_scores(c, yr_from, yr_to)

    years  = [r["year"]    for r in scores]
    vals   = [r["score"]   for r in scores]
    cats   = [r["category"] for r in scores]
    md_ads = [f"{r['md_lord']}-{r['ad_lord']}" for r in scores]

    COLOR_MAP = {
        "Outstanding":"#F0C040","Excellent":"#40D060","Very Good":"#40C0C0",
        "Good":"#6090F0","Moderate":"#E0A040","Challenging":"#F06060","Difficult":"#C02020"
    }
    bar_colors = [COLOR_MAP.get(cat,"#8080A0") for cat in cats]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=vals,
        marker_color=bar_colors,
        text=[f"{v:.1f}" for v in vals],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}<br>Dasha: %{customdata}<extra></extra>",
        customdata=md_ads,
    ))
    fig.add_hline(y=8.0, line_dash="dot", line_color="#40D060", opacity=0.5,
                  annotation_text="Excellent", annotation_position="right")
    fig.add_hline(y=6.0, line_dash="dot", line_color="#E0A040", opacity=0.5,
                  annotation_text="Moderate", annotation_position="right")

    fig.update_layout(
        plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
        font=dict(color="#C0C0D0"), height=350,
        yaxis=dict(range=[0,10.5], gridcolor="#1A1A2A", title="Shastra Score"),
        xaxis=dict(gridcolor="#1A1A2A", title="Year"),
        margin=dict(t=20,b=40,l=40,r=80),
        showlegend=False,
    )
    st.plotly_chart(fig, width='stretch')

    import pandas as pd_lib
    rows = [{"Year":r["year"],"MD":r["md_lord"],"AD":r["ad_lord"],
             "Score":r["score"],"Category":r["category"]} for r in scores]
    with st.expander("📋 Full Score Table"):
        st.dataframe(pd_lib.DataFrame(rows), hide_index=True, width='stretch')

def render_combined_graph(cs: list, s1: list, s2: list, name1: str, name2: str):
    import plotly.graph_objects as go

    years = [r["year"]     for r in cs]
    comb  = [r["combined"] for r in cs]
    sc1   = [r["score"]    for r in s1]
    sc2   = [r["score"]    for r in s2]
    cats  = [r["category"] for r in cs]

    COLOR_MAP = {"Outstanding":"#F0C040","Excellent":"#40D060","Very Good":"#40C0C0",
                 "Good":"#6090F0","Moderate":"#E0A040","Challenging":"#F06060"}
    bar_colors = [COLOR_MAP.get(c,"#8080A0") for c in cats]

    fig = go.Figure()
    # Combined bars
    fig.add_trace(go.Bar(
        name="Combined Dampati", x=years, y=comb,
        marker_color=bar_colors, opacity=0.85,
        text=[f"{v:.1f}" for v in comb], textposition="outside",
        hovertemplate="<b>%{x}</b><br>Combined: %{y:.1f}<br>Category: %{customdata}<extra></extra>",
        customdata=cats,
    ))
    # Individual lines
    fig.add_trace(go.Scatter(
        name=name1[:15], x=years, y=sc1,
        mode="lines+markers", line=dict(color="#40C0E0",width=2),
        marker=dict(size=6), hovertemplate=f"{name1}: %{{y:.1f}}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        name=name2[:15], x=years, y=sc2,
        mode="lines+markers", line=dict(color="#E060A0",width=2),
        marker=dict(size=6), hovertemplate=f"{name2}: %{{y:.1f}}<extra></extra>",
    ))
    fig.add_hline(y=9.0,line_dash="dot",line_color="#F0C040",opacity=0.4,
                  annotation_text="Outstanding",annotation_position="right")
    fig.add_hline(y=8.0,line_dash="dot",line_color="#40D060",opacity=0.4,
                  annotation_text="Excellent",annotation_position="right")
    fig.add_hline(y=6.0,line_dash="dot",line_color="#E0A040",opacity=0.4,
                  annotation_text="Moderate",annotation_position="right")

    fig.update_layout(
        plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
        font=dict(color="#C0C0D0"), height=480,
        yaxis=dict(range=[0,10.8],gridcolor="#1A1A2A",title="Dampati Shastra Score"),
        xaxis=dict(gridcolor="#1A1A2A",title="Year",
                   tickmode="array",tickvals=years,ticktext=[str(y) for y in years]),
        legend=dict(bgcolor="#0E1117",bordercolor="#2A2A3A"),
        margin=dict(t=20,b=60,l=40,r=100),
    )
    st.plotly_chart(fig, width='stretch')

def render_koota(milan: dict):
    st.markdown("#### 🔢 Ashtakoot Milan (36-Point Analysis)")
    total = milan["total"]; mx = milan["max"]
    pct = total/mx
    col1, col2 = st.columns([1,2])
    with col1:
        st.metric("Total Score", f"{total}/{mx}",
                  delta=f"{total-18} above minimum" if total>=18 else f"{18-total} below minimum")
        st.markdown(f"**Verdict:** {milan['verdict']}")
    with col2:
        st.progress(pct)
        st.caption(f"{'▓'*int(pct*20)}{'░'*(20-int(pct*20))} {total}/{mx}")

    import pandas as pd_lib
    rows = [{"Koota":k, "Score":v["score"], "Max":v["max"],
             "Detail":v["detail"], "Remark":v["remark"]}
            for k,v in milan["kootas"].items()]
    st.dataframe(pd_lib.DataFrame(rows), hide_index=True, width='stretch')

# ═══════════════════════════════════════════════════════════════════════════
# PREDICTION RENDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

COLOR_PRED = {
    "Outstanding":"#F0C040","Excellent":"#40D060","Very Good":"#40C0C0",
    "Good":"#6090F0","Moderate":"#E0A040","Challenging":"#F06060","Difficult":"#C02020",
}
BG_PRED = {
    "Outstanding":"#2A1800","Excellent":"#0A2010","Very Good":"#0A1820",
    "Good":"#0A1028","Moderate":"#201400","Challenging":"#200808","Difficult":"#180404",
}
PLANET_GLYPH_UI = {
    "Surya":"☀","Chandra":"🌙","Budha":"☿","Shukra":"♀","Mangal":"♂",
    "Guru":"♃","Shani":"♄","Rahu":"☊","Ketu":"☋",
}
AREA_ICON = {"career":"💼","health":"🩺","relationships":"💑","finances":"💰","spirituality":"🪔"}
AREA_LABEL = {
    "career":"Career & Status","health":"Health & Vitality",
    "relationships":"Relationships & Family","finances":"Finances & Wealth",
    "spirituality":"Spirituality & Upaya",
}

def render_predictions_tab(chart: dict, name: str, yr_from: int, yr_to: int):
    preds = generate_dasha_predictions(chart, yr_from, yr_to)
    if not preds:
        st.info("No dasha periods found within the selected year range.")
        return

    st.markdown(f"""
    <div style="background:#0A0818;border:1px solid #4A2080;border-radius:10px;padding:0.9rem;margin-bottom:1rem;">
      <b style="color:#D0A0FF;font-size:1rem;">🪔 Dasha-Wise Predictions for {name}</b><br>
      <span style="color:#8080A0;font-size:0.82rem;">
        {yr_from}–{yr_to} | Vimshottari Dasha System | Sources: BPHS • Phaladeepika • Brihat Jataka • Saravali • Uttara Kalamrita
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Current dasha banner
    cur = next((p for p in preds if p["is_current"]), None)
    if cur:
        col_c = COLOR_PRED.get(cur["category"], "#8080A0")
        bg_c  = BG_PRED.get(cur["category"], "#1A1A2A")
        st.markdown(f"""
        <div style="background:{bg_c};border:2px solid {col_c};border-radius:10px;padding:0.9rem;margin-bottom:1rem;">
          <b style="color:{col_c};font-size:1.05rem;">▶ NOW RUNNING: {PLANET_GLYPH_UI.get(cur['lord'],'')} {cur['lord']} Maha Dasha</b>
          <span style="float:right;color:#888;font-size:0.85rem;">{cur['start'].strftime('%b %Y')} — {cur['end'].strftime('%b %Y')}</span><br>
          <span style="color:#C0C0D0;font-size:0.85rem;">
            House {cur['house']} in {cur['sign']} | {cur['dignity']} | Avg Score: {cur['avg_score']}/10 — {cur['category']}
          </span>
        </div>
        """, unsafe_allow_html=True)

    # One expander per Maha Dasha
    for pred in preds:
        glyph = PLANET_GLYPH_UI.get(pred["lord"], "🪐")
        sc    = COLOR_PRED.get(pred["category"], "#8080A0")
        past_tag    = " [Past Period]" if pred["is_past"] else ""
        current_tag = " ◄ ACTIVE NOW" if pred["is_current"] else ""
        header = (f"{glyph} {pred['lord']} Maha Dasha{current_tag}{past_tag}  |  "
                  f"{pred['start'].strftime('%b %Y')} – {pred['end'].strftime('%b %Y')}  "
                  f"({pred['years']:.1f} yrs)  |  Score {pred['avg_score']}/10 — {pred['category']}")

        with st.expander(header, expanded=pred["is_current"]):

            # Shastra source block
            st.markdown(f"""
            <div style="background:#08060E;border-left:3px solid #7040C0;padding:0.7rem 1rem;
                        border-radius:0 6px 6px 0;margin-bottom:0.9rem;">
              <span style="color:#C090FF;font-size:0.83rem;font-style:italic;">{pred['shastra_ref']}</span>
            </div>
            """, unsafe_allow_html=True)

            # Dignity & quality summary
            st.markdown(
                f"**{pred['lord']} is placed in House {pred['house']} ({pred['sign']}) — {pred['dignity']}** — "
                f"delivering a **{pred['quality_word']}** period overall."
            )
            st.caption(pred["quality_note"])
            st.markdown("---")

            # ── Life Areas ──────────────────────────────────────────────
            st.markdown("##### 🌐 Domain-Wise Predictions")
            areas = list(pred["life_areas"].items())
            col_a, col_b = st.columns(2)
            for i, (area, text) in enumerate(areas):
                target = col_a if i % 2 == 0 else col_b
                with target:
                    st.markdown(f"""
                    <div style="background:#0E1117;border:1px solid #2A2A3A;border-radius:8px;
                                padding:0.75rem;margin-bottom:0.6rem;">
                      <b style="color:#E8D8A8;">{AREA_ICON.get(area,'')} {AREA_LABEL.get(area, area.title())}</b>
                      <p style="color:#B0B0C0;font-size:0.84rem;margin:0.4rem 0 0;line-height:1.55;">{text}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Antardasha Detail ────────────────────────────────────────
            if pred["antardashas"]:
                st.markdown("---")
                st.markdown("##### 🗓️ Antardasha Period Predictions")
                st.caption("Each Maha Dasha is subdivided into Antardashas (sub-periods) that modulate its energy. The most auspicious windows for action lie within the strongest Antardashas.")

                for ad in pred["antardashas"]:
                    ag   = PLANET_GLYPH_UI.get(ad["lord"], "🪐")
                    ac   = COLOR_PRED.get(ad["category"], "#8080A0")
                    abg  = BG_PRED.get(ad["category"],  "#0E1117")
                    now  = " ◄ ACTIVE NOW" if ad["is_current"] else ""
                    st.markdown(f"""
                    <div style="background:{abg};border:1px solid {ac}55;border-radius:7px;
                                padding:0.65rem 0.9rem;margin-bottom:0.55rem;">
                      <div style="display:flex;justify-content:space-between;align-items:center;">
                        <b style="color:{ac};">{ag} {pred['lord']} / {ad['lord']} Antardasha{now}</b>
                        <span style="font-size:0.78rem;color:#888;">
                          {ad['start'].strftime('%b %Y')} – {ad['end'].strftime('%b %Y')} | Score {ad['score']}/10 — {ad['category']}
                        </span>
                      </div>
                      <p style="color:#C0C0D0;font-size:0.84rem;margin:0.45rem 0 0;line-height:1.55;">{ad['prediction']}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Upaya & Guidance ────────────────────────────────────────
            st.markdown("---")
            st.markdown("##### 🪔 Upaya (Vedic Remedies) & Guidance for This Period")
            g = pred["guidance"]
            gc1, gc2, gc3 = st.columns(3)
            with gc1:
                st.markdown("**🕉️ Mantra Sadhana**")
                st.caption(g["mantra"])
            with gc2:
                st.markdown("**🌸 Dana (Charity)**")
                st.caption(g["charity"])
            with gc3:
                st.markdown("**🛕 Tirtha Yatra**")
                st.caption(g["pilgrimage"])

            st.markdown(f"""
            <div style="background:#0A1018;border:1px solid #2A3848;border-radius:7px;
                        padding:0.8rem;margin-top:0.6rem;">
              <b style="color:#A0C8E0;">💫 Jyotishi's Counsel for This Period</b>
              <p style="color:#B8C8D8;font-size:0.85rem;margin:0.45rem 0 0;line-height:1.6;">{g['focus']}</p>
            </div>
            """, unsafe_allow_html=True)


def render_combined_predictions_tab(chart1: dict, chart2: dict,
                                     n1: str, n2: str, yr_from: int, yr_to: int):
    # generate_dasha_predictions and compute_combined_year_scores available at module level
    import pandas as pd_lib

    cs_all = compute_combined_year_scores(chart1, chart2, yr_from, yr_to)
    p1     = generate_dasha_predictions(chart1, yr_from, yr_to)
    p2     = generate_dasha_predictions(chart2, yr_from, yr_to)

    outstanding = [r for r in cs_all if r["combined"] >= 9.0]
    excellent   = [r for r in cs_all if 8.0 <= r["combined"] < 9.0]
    challenging = [r for r in cs_all if r["combined"] < 6.5]

    st.markdown("""
    <div style="background:#0A0818;border:1px solid #4A2080;border-radius:10px;padding:0.9rem;margin-bottom:1rem;">
      <b style="color:#D0A0FF;font-size:1rem;">🌟 Dampati Dasha Predictions — Combined Life Journey</b><br>
      <span style="color:#8080A0;font-size:0.82rem;">
        Per BPHS Ch.18 & Jataka Parijata: 'The married couple's charts together form a third destiny —
        the Ardhanarishvara energy that sustains the household dharma (Grihastha Ashrama).'
      </span>
    </div>
    """, unsafe_allow_html=True)

    # Phase summary
    ph1, ph2, ph3 = st.columns(3)
    if outstanding:
        ph1.success(f"⭐ Peak Years ({len(outstanding)}): {', '.join(str(r['year']) for r in outstanding)}")
    if excellent:
        ph2.info(f"✨ Excellent Years ({len(excellent)}): {', '.join(str(r['year']) for r in excellent)}")
    if challenging:
        ph3.warning(f"⚠️ Needs Care ({len(challenging)}): {', '.join(str(r['year']) for r in challenging)}")

    st.markdown("---")

    # Dampati protection table
    st.markdown("#### 🛡️ Dampati Protection Analysis — Year by Year")
    st.caption("Per BPHS Ch.18: 'In a dharmic marriage, when one spouse is in karmic difficulty, the other's Dasha energy provides shelter and strength — this is the sacred geometry of Grihastha Ashrama.'")

    rows = []
    for r in cs_all:
        s1, s2, comb = r["score1"], r["score2"], r["combined"]
        if s1 >= 8.5 and s2 >= 8.5:
            dynamic = "🌟 Both flourish — extraordinary combined year"
        elif s1 >= 8.0 and s2 < 6.5:
            dynamic = f"🛡️ {n1[:10]} strongly protects {n2[:10]}"
        elif s2 >= 8.0 and s1 < 6.5:
            dynamic = f"🛡️ {n2[:10]} strongly protects {n1[:10]}"
        elif s1 < 5.5 and s2 < 5.5:
            dynamic = "🤝 Mutual support & patience required"
        else:
            dynamic = "⚖️ Balanced — steady shared progress"
        rows.append({
            "Year": r["year"],
            f"{n1[:10]} Dasha": f"{r['md1']}-{r['ad1']}",
            f"{n1[:8]} ⭐": s1,
            f"{n2[:10]} Dasha": f"{r['md2']}-{r['ad2']}",
            f"{n2[:8]} ⭐": s2,
            "Combined": comb,
            "Category": r["category"],
            "Dynamic": dynamic,
        })
    st.dataframe(pd_lib.DataFrame(rows), hide_index=True, width='stretch')

    st.markdown("---")

    # Side-by-side individual dasha predictions
    st.markdown("#### 📖 Individual Dasha Predictions")
    col1, col2 = st.columns(2)

    for col, preds, nm in [(col1, p1, n1), (col2, p2, n2)]:
        with col:
            st.markdown(f"**{'👨' if nm == n1 else '👩'} {nm} — Maha Dasha Breakdown**")
            for pred in preds:
                glyph = PLANET_GLYPH_UI.get(pred["lord"], "🪐")
                sc    = COLOR_PRED.get(pred["category"], "#8080A0")
                now   = " ▶ NOW" if pred["is_current"] else ""
                with st.expander(
                    f"{glyph} {pred['lord']} MD{now}  |  "
                    f"{pred['start'].strftime('%b %y')}–{pred['end'].strftime('%b %y')}  |  "
                    f"{pred['avg_score']}/10 — {pred['category']}",
                    expanded=pred["is_current"]
                ):
                    st.markdown(
                        f"<span style='color:{sc};font-weight:600;'>{pred['category']}</span>"
                        f" — House {pred['house']} | {pred['dignity']}",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<small style='color:#8080A0;font-style:italic;'>"
                        f"{pred['shastra_ref'][:160]}…</small>",
                        unsafe_allow_html=True
                    )
                    st.markdown("")
                    for area, text in list(pred["life_areas"].items()):
                        st.markdown(
                            f"**{AREA_ICON.get(area,'')} {AREA_LABEL.get(area,area.title())}:** "
                            f"{text[:180]}…"
                        )
                    if pred["antardashas"]:
                        st.markdown("**Key Sub-Periods:**")
                        for ad in pred["antardashas"]:
                            ac  = COLOR_PRED.get(ad["category"], "#8080A0")
                            now2 = " ◄" if ad["is_current"] else ""
                            st.markdown(
                                f"<span style='color:{ac};font-size:0.82rem;'>"
                                f"**{pred['lord']}/{ad['lord']}**{now2} "
                                f"({ad['start'].strftime('%b %y')}–{ad['end'].strftime('%b %y')}) "
                                f"— {ad['score']}/10 {ad['category']}</span>",
                                unsafe_allow_html=True
                            )
                            st.caption(ad["prediction"][:220] + "…")
                    g = pred["guidance"]
                    st.markdown(f"🕉️ **Upaya:** {g['mantra'][:100]}")
                    st.markdown(f"💫 **Counsel:** {g['focus'][:200]}…")


def render_marriage_predictions(chart: dict, name: str):
    """
    Render marriage timing predictions based on:
    - 7th house lord position and strength
    - Venus placement and dignity
    - Dasha periods favorable for marriage
    """
    marriage_data = compute_marriage_timing(chart)
    
    st.markdown("""
    <div style="background:#1A0A30;border:1px solid #8040C0;border-radius:10px;padding:0.9rem;margin-bottom:1rem;">
      <b style="color:#D0A0FF;font-size:1rem;">💒 Marriage Predictions — Vivaha Yoga Analysis</b><br>
      <span style="color:#8080A0;font-size:0.82rem;">
        Per BPHS Ch.26 (Vivaha) • Brihat Jataka • Phaladeepika • Uttara Kalamrita
      </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Main prediction banner
    status_color = {"Highly Auspicious Window Approaching":"#40D060",
                   "Auspicious Window in Near Term":"#60A0F0",
                   "Distant but Indicated":"#E0A040",
                   "Timing has passed in natal chart timeline":"#F06060"}.get(marriage_data["status"], "#8080A0")
    status_bg = {"Highly Auspicious Window Approaching":"#0A2010",
                "Auspicious Window in Near Term":"#0A1028",
                "Distant but Indicated":"#201400",
                "Timing has passed in natal chart timeline":"#200808"}.get(marriage_data["status"], "#0E1117")
    
    st.markdown(f"""
    <div style="background:{status_bg};border:2px solid {status_color};border-radius:10px;padding:1rem;margin-bottom:1rem;">
      <b style="color:{status_color};font-size:1.1rem;">💒 {marriage_data['status']}</b><br>
      <span style="color:#C0C0D0;font-size:0.9rem;">
        Current Age: {marriage_data['current_age']} | Predicted Marriage Age: {marriage_data['predicted_age']} | 
        Expected Year: {marriage_data['expected_year']} (~{marriage_data['years_away']} years away)
      </span>
    </div>
    """, unsafe_allow_html=True)
    
    # 7th House Analysis
    st.markdown("#### 🏛️ 7th House Analysis (Marriage & Partnerships)")
    col7a, col7b = st.columns(2)
    with col7a:
        st.markdown(f"""
        <div style="background:#0E1117;border:1px solid #2A2A3A;border-radius:8px;padding:0.75rem;margin-bottom:0.6rem;">
          <b style="color:#E8D8A8;">7th Lord: {marriage_data['seventh_lord']}</b><br>
          <span style="color:#B0B0C0;font-size:0.85rem;">
            House: {marriage_data['seventh_lord_house']} | Sign: {marriage_data['seventh_lord_sign']}<br>
            Dignity: <b style="color:#{'40D060' if marriage_data['seventh_lord_strong'] else 'F06060'}">{marriage_data['seventh_lord_dignity']}</b>
          </span>
        </div>
        """, unsafe_allow_html=True)
    
    with col7b:
        st.markdown(f"""
        <div style="background:#0E1117;border:1px solid #2A2A3A;border-radius:8px;padding:0.75rem;margin-bottom:0.6rem;">
          <b style="color:#E8D8A8;">Venus (Marriage Karaka)</b><br>
          <span style="color:#B0B0C0;font-size:0.85rem;">
            House: {marriage_data['venus_house']} | Sign: {marriage_data['venus_sign']}<br>
            Dignity: <b style="color:#{'40D060' if marriage_data['venus_strong'] else 'F06060'}">{marriage_data['venus_dignity']}</b>
          </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Shastra Reference
    st.markdown(f"""
    <div style="background:#08060E;border-left:3px solid #7040C0;padding:0.7rem 1rem;
                border-radius:0 6px 6px 0;margin-bottom:0.9rem;">
      <span style="color:#C090FF;font-size:0.83rem;font-style:italic;">{marriage_data['shastra_ref']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Auspicious Dasha Periods
    if marriage_data['auspicious_periods']:
        st.markdown("#### 🗓️ Auspicious Dasha Periods for Marriage")
        for period in marriage_data['auspicious_periods']:
            period_color = "#D0A0FF" if period['type'].startswith("Venus") else "#A0C8F0"
            period_bg = "#0A0810" if period['type'].startswith("Venus") else "#0A0820"
            st.markdown(f"""
            <div style="background:{period_bg};border:1px solid {period_color}55;border-radius:7px;padding:0.65rem 0.9rem;margin-bottom:0.55rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <b style="color:{period_color};">💫 {period['type']}</b>
                <span style="font-size:0.78rem;color:#888;">{period['strength']}</span>
              </div>
              <span style="color:#C0C0D0;font-size:0.85rem;">
                {period['start'].strftime('%b %Y')} – {period['end'].strftime('%b %Y')} 
                ({(period['end'].year - period['start'].year + (period['end'].month - period['start'].month)/12):.1f} years)
              </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
    
    # Guidance & Remedies
    st.markdown("#### 🪔 Guidance & Remedies for Marriage")
    st.markdown(f"""
    <div style="background:#0A1018;border:1px solid #2A3848;border-radius:7px;padding:0.8rem;margin-bottom:0.8rem;">
      <b style="color:#A0C8E0;">💫 Jyotishi's Counsel</b>
      <p style="color:#B8C8D8;font-size:0.85rem;margin:0.45rem 0 0;line-height:1.6;">{marriage_data['guidance']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Marriage remedies
    st.markdown("#### 🛕 Vedic Remedies (Upaya) for Marriage")
    rem_col1, rem_col2, rem_col3 = st.columns(3)
    
    with rem_col1:
        st.markdown("**🪔 Venus Worship (for Shukra)**")
        st.caption(
            "Observe Shukra Vrata (Fridays)\n\n"
            "Mantra: 'Om Dram Drim Draum Sah Shukraya Namah' 108x\n\n"
            "Donate: White flowers, white rice, milk, silver ornaments to temple"
        )
    
    with rem_col2:
        st.markdown("**👰 Parvati & Shiva Worship**")
        st.caption(
            "Invoke the Divine Pair for harmonious marriage\n\n"
            "Per Rigveda 10.85: Vivaha Sukta chanting\n\n"
            "Perform on Fridays & Full Moon (Purnima) days"
        )
    
    with rem_col3:
        st.markdown("**🙏 7th Lord Strengthening**")
        st.caption(
            f"Worship the lord of the 7th house: {marriage_data['seventh_lord']}\n\n"
            "Strengthen through mantra & charity\n\n"
            "Per BPHS: Appease 7th lord through its deity"
        )


# ═══════════════════════════════════════════════════════════════════════════
# MODE: INDIVIDUAL
# ═══════════════════════════════════════════════════════════════════════════
if mode == "🔮 Individual Report":
    with st.form("individual_form"):
        name, dob, tob_h, place = person_form("p1", "📋 Enter Birth Details")
        submitted = st.form_submit_button("🪔 Generate Vedic Report", width='stretch')

    if submitted:
        if not name.strip():
            st.error("Please enter a name.")
        else:
            with st.spinner(f"Computing chart for {name}..."):
                lat, lon = geocode(place)
                chart = compute_chart(name, dob, tob_h, lat, lon)

            st.success(f"Chart computed for **{name}** | Lat: {lat:.4f}°N Lon: {lon:.4f}°E")
            st.markdown("---")

            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
                ["🗺️ Chart Overview","🪐 Planets","✨ Yogas","🗓️ Dashas","📈 Forecast","🔮 Predictions","💒 Marriage"])

            with tab1:
                render_chart_overview(chart, place)
                st.markdown("---")
                render_nakshatra(chart)

            with tab2:
                render_planets(chart)

            with tab3:
                render_yogas(chart)

            with tab4:
                render_dasha(chart)

            with tab5:
                render_year_forecast(chart)

            with tab6:
                import datetime as _dt
                _yr_from = _dt.date.today().year - 2
                _yr_to   = _dt.date.today().year + 25
                render_predictions_tab(chart, name, _yr_from, _yr_to)

            with tab7:
                render_marriage_predictions(chart, name)

            # Full text report download
            with st.expander("📄 Full Text Report (BPHS Style)"):
                report_text = generate_individual_report(chart, place)
                st.text_area("Full Report", report_text, height=500, label_visibility="collapsed")
                st.download_button("⬇ Download Report (.txt)", report_text,
                                   file_name=f"{name.replace(' ','_')}_Jyotish_Report.txt",
                                   mime="text/plain", width='stretch')

            # ── Enhanced Report Downloads (Infographic + Document) ──────────────
            st.markdown("---")
            with st.expander("📦 Download Enhanced Reports (Infographic & Document)"):
                from ui.report_html import generate_individual_html as _gih
                from ui.report_docx import generate_individual_docx as _gid
                import datetime as _dt_i
                _yf_i = _dt_i.date.today().year - 2
                _yt_i = _dt_i.date.today().year + 25
                _sc_i = compute_year_scores(chart, _yf_i, _yt_i)
                _pr_i = generate_dasha_predictions(chart, _yf_i, _yt_i)
                _html_i = _gih(chart, name, place, dob, tob_h, _sc_i, _pr_i).encode("utf-8")
                _docx_i = _gid(chart, name, place, dob, tob_h, _sc_i, _pr_i)
                _dc1_i, _dc2_i = st.columns(2)
                _dc1_i.download_button("📊 Infographic Report (.html)", _html_i,
                    file_name=f"{name.replace(' ','_')}_Jyotisha_Infographic.html",
                    mime="text/html", width='stretch', type="primary")
                _dc2_i.download_button("📄 Document Report (.docx)", _docx_i,
                    file_name=f"{name.replace(' ','_')}_Jyotisha_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    width='stretch')
                st.caption("📊 Infographic opens in any browser with visual charts and color-coded predictions. 📄 Document opens in Word or Google Docs with full narrative.")

# ═══════════════════════════════════════════════════════════════════════════
# MODE: COMPATIBILITY
# ═══════════════════════════════════════════════════════════════════════════
elif mode == "💑 Spouse Compatibility":
    st.markdown("### 💑 Dampati Kundali Milan")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("compat_h"):
            st.markdown("**👨 Husband**")
            n1,d1,t1,p1 = person_form("h","")
            s1 = st.form_submit_button("Set Husband ✓")
    with col2:
        with st.form("compat_w"):
            st.markdown("**👩 Wife**")
            n2,d2,t2,p2 = person_form("w","")
            s2 = st.form_submit_button("Set Wife ✓")

    if st.button("💑 Generate Compatibility Report", width='stretch', type="primary"):
        if not n1.strip() or not n2.strip():
            st.error("Please enter names for both partners.")
        else:
            with st.spinner("Computing compatibility..."):
                lat1,lon1 = geocode(p1); lat2,lon2 = geocode(p2)
                chart1 = compute_chart(n1, d1, t1, lat1, lon1)
                chart2 = compute_chart(n2, d2, t2, lat2, lon2)
                from engine.interpret import calc_ashtakoot as _cak
                milan  = _cak(chart1, chart2)

            st.success("Compatibility analysis complete!")
            st.markdown("---")

            # compute_combined_year_scores and _cys available at module level
            _cys = compute_year_scores
            import pandas as pd_lib
            cs_data_compat = compute_combined_year_scores(chart1, chart2, 2025, 2035)
            s1_data_compat = _cys(chart1, 2025, 2035)
            s2_data_compat = _cys(chart2, 2025, 2035)

            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "📊 Ashtakoot",
                "🔭 Chart Comparison",
                "🗓️ Dasha Sync",
                f"👨 {n1[:14]} Forecast",
                f"👩 {n2[:14]} Forecast",
                "🔮 Predictions",
                "📄 Full Report"
            ])

            with tab1:
                render_koota(milan)

            with tab2:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**{n1}**")
                    render_chart_overview(chart1, p1)
                with c2:
                    st.markdown(f"**{n2}**")
                    render_chart_overview(chart2, p2)

            with tab3:
                render_combined_graph(cs_data_compat, s1_data_compat, s2_data_compat, n1, n2)
                rows = [{"Year":r["year"],"H-Dasha":f"{r['md1']}-{r['ad1']}",
                         f"{n1[:8]} Score":r["score1"],
                         "W-Dasha":f"{r['md2']}-{r['ad2']}",
                         f"{n2[:8]} Score":r["score2"],
                         "Combined":r["combined"],"Category":r["category"]}
                        for r in cs_data_compat]
                st.dataframe(pd_lib.DataFrame(rows), hide_index=True, width='stretch')

            with tab4:
                render_year_forecast(chart1, label=n1, yr_from=2025, yr_to=2035)
                ind_peak1 = [r for r in s1_data_compat if r["score"] >= 9.0]
                ind_chal1 = [r for r in s1_data_compat if r["score"] < 6.5]
                if ind_peak1:
                    st.success(f"⭐ Outstanding Years: {', '.join(str(r['year']) for r in ind_peak1)}")
                if ind_chal1:
                    st.warning(f"⚠️ Challenging Years: {', '.join(str(r['year']) for r in ind_chal1)}")

            with tab5:
                render_year_forecast(chart2, label=n2, yr_from=2025, yr_to=2035)
                ind_peak2 = [r for r in s2_data_compat if r["score"] >= 9.0]
                ind_chal2 = [r for r in s2_data_compat if r["score"] < 6.5]
                if ind_peak2:
                    st.success(f"⭐ Outstanding Years: {', '.join(str(r['year']) for r in ind_peak2)}")
                if ind_chal2:
                    st.warning(f"⚠️ Challenging Years: {', '.join(str(r['year']) for r in ind_chal2)}")

            with tab6:
                import datetime as _dt
                _yr_from_c = _dt.date.today().year - 2
                _yr_to_c   = _dt.date.today().year + 25
                render_combined_predictions_tab(chart1, chart2, n1, n2, _yr_from_c, _yr_to_c)

            with tab7:
                report_text = generate_compatibility_report(chart1, chart2, p1, p2)
                st.text_area("Compatibility Report", report_text, height=500, label_visibility="collapsed")
                st.download_button("⬇ Download Compatibility Report (.txt)", report_text,
                                   file_name=f"Compatibility_{n1}_{n2}.txt",
                                   mime="text/plain", width='stretch')

            # ── Enhanced Report Downloads (Infographic + Document) ──────────────
            st.markdown("---")
            with st.expander("📦 Download Enhanced Reports (Infographic & Document)"):
                from ui.report_html import generate_combined_html as _gch
                from ui.report_docx import generate_combined_docx as _gcd
                import datetime as _dt_c
                _yf_c = _dt_c.date.today().year - 2
                _yt_c = _dt_c.date.today().year + 25
                _cs_c  = compute_combined_year_scores(chart1, chart2, _yf_c, _yt_c)
                _s1_c  = compute_year_scores(chart1, _yf_c, _yt_c)
                _s2_c  = compute_year_scores(chart2, _yf_c, _yt_c)
                _pr1_c = generate_dasha_predictions(chart1, _yf_c, _yt_c)
                _pr2_c = generate_dasha_predictions(chart2, _yf_c, _yt_c)
                _html_c = _gch(chart1, chart2, n1, n2, p1, p2, d1, d2, t1, t2,
                               _cs_c, _s1_c, _s2_c, _pr1_c, _pr2_c).encode("utf-8")
                _docx_c = _gcd(chart1, chart2, n1, n2, p1, p2, d1, d2, t1, t2,
                               _cs_c, _s1_c, _s2_c, _pr1_c, _pr2_c)
                _dc1_c, _dc2_c = st.columns(2)
                _dc1_c.download_button("📊 Infographic Report (.html)", _html_c,
                    file_name=f"Compatibility_{n1}_{n2}_Infographic.html",
                    mime="text/html", width='stretch', type="primary")
                _dc2_c.download_button("📄 Document Report (.docx)", _docx_c,
                    file_name=f"Compatibility_{n1}_{n2}_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    width='stretch')
                st.caption("📊 Infographic opens in any browser with visual charts and color-coded predictions. 📄 Document opens in Word or Google Docs with full narrative.")

# ═══════════════════════════════════════════════════════════════════════════
# MODE: COMBINED 25-YEAR REPORT
# ═══════════════════════════════════════════════════════════════════════════
elif mode == "🌟 Combined 25-Year Report":
    st.markdown("### 🌟 Dampati Jyotisha — Ardhanarishvara Kundali")
    st.caption("Combined life energy analysis — the same methodology used throughout this conversation")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Husband Details**")
        n1 = st.text_input("Name", key="cn1", value="")
        d1 = st.date_input("DOB", key="cd1", value=datetime.date(1982,11,21))
        t1h = st.number_input("Hour IST", 0,23, 21, key="ct1h")
        t1m = st.number_input("Min", 0,59, 6, key="ct1m")
        p1 = st.text_input("Place", key="cp1", value="Simhachalam, Visakhapatnam")
    with col2:
        st.markdown("**Wife Details**")
        n2 = st.text_input("Name", key="cn2", value="")
        d2 = st.date_input("DOB", key="cd2", value=datetime.date(1984,9,3))
        t2h = st.number_input("Hour IST", 0,23, 16, key="ct2h")
        t2m = st.number_input("Min", 0,59, 20, key="ct2m")
        p2 = st.text_input("Place", key="cp2", value="Jangareddygudem, West Godavari")

    ycols = st.columns(2)
    yr_from = ycols[0].number_input("From Year", 2025, 2060, 2026, key="yfrom")
    yr_to   = ycols[1].number_input("To Year",   2025, 2060, 2050, key="yto")

    if st.button("🌟 Generate Combined Report", width='stretch', type="primary"):
        if not n1.strip() or not n2.strip():
            st.error("Please enter names for both partners.")
        else:
            t1 = t1h + t1m/60; t2 = t2h + t2m/60
            with st.spinner("Computing Dampati Kundali..."):
                lat1,lon1 = geocode(p1); lat2,lon2 = geocode(p2)
                chart1 = compute_chart(n1, d1, t1, lat1, lon1)
                chart2 = compute_chart(n2, d2, t2, lat2, lon2)
                report_text, cs_data, s1_data, s2_data = generate_combined_report(
                    chart1, chart2, p1, p2, int(yr_from), int(yr_to))

            st.success("Combined Dampati report generated!")
            st.markdown("---")

            # Summary metrics
            outstanding = [r for r in cs_data if r["combined"] >= 9.0]
            challenging = [r for r in cs_data if r["combined"] < 6.5]
            avg_score   = sum(r["combined"] for r in cs_data) / len(cs_data)

            m1,m2,m3,m4 = st.columns(4)
            m1.metric("Years Analysed",  len(cs_data))
            m2.metric("Average Score",   f"{avg_score:.1f}/10")
            m3.metric("Outstanding Years", len(outstanding))
            m4.metric("Challenging Years", len(challenging))

            st.markdown("---")

            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📊 Combined Chart",
                f"👨 {n1[:14]} Forecast",
                f"👩 {n2[:14]} Forecast",
                "🔮 Predictions",
                "📋 Year Table",
                "📄 Full Report"
            ])

            with tab1:
                st.markdown("#### Dampati Energy Graph")
                render_combined_graph(cs_data, s1_data, s2_data, n1, n2)

                st.markdown("#### Peak & Caution Years")
                if outstanding:
                    yrs_str = ", ".join(str(r["year"]) for r in outstanding)
                    st.success(f"⭐ **Outstanding Years ({len(outstanding)}):** {yrs_str}")
                if challenging:
                    yrs_str = ", ".join(str(r["year"]) for r in challenging)
                    st.warning(f"⚠️ **Challenging Years ({len(challenging)}):** {yrs_str}")

            with tab2:
                render_year_forecast(chart1, label=n1, yr_from=int(yr_from), yr_to=int(yr_to))
                # Individual peak / caution highlight
                ind_peak1 = [r for r in s1_data if r["score"] >= 9.0]
                ind_chal1 = [r for r in s1_data if r["score"] < 6.5]
                if ind_peak1:
                    st.success(f"⭐ Outstanding Years: {', '.join(str(r['year']) for r in ind_peak1)}")
                if ind_chal1:
                    st.warning(f"⚠️ Challenging Years: {', '.join(str(r['year']) for r in ind_chal1)}")

            with tab3:
                render_year_forecast(chart2, label=n2, yr_from=int(yr_from), yr_to=int(yr_to))
                ind_peak2 = [r for r in s2_data if r["score"] >= 9.0]
                ind_chal2 = [r for r in s2_data if r["score"] < 6.5]
                if ind_peak2:
                    st.success(f"⭐ Outstanding Years: {', '.join(str(r['year']) for r in ind_peak2)}")
                if ind_chal2:
                    st.warning(f"⚠️ Challenging Years: {', '.join(str(r['year']) for r in ind_chal2)}")

            with tab4:
                render_combined_predictions_tab(chart1, chart2, n1, n2, int(yr_from), int(yr_to))

            with tab5:
                import pandas as pd_lib
                rows = [{"Year":r["year"],
                         f"{n1[:10]}-MD":r["md1"],f"{n1[:10]}-AD":r["ad1"],
                         f"{n1[:8]} Score":r["score1"],
                         f"{n2[:10]}-MD":r["md2"],f"{n2[:10]}-AD":r["ad2"],
                         f"{n2[:8]} Score":r["score2"],
                         "Combined":r["combined"],"Category":r["category"]}
                        for r in cs_data]
                st.dataframe(pd_lib.DataFrame(rows), hide_index=True, width='stretch')

            with tab6:
                st.text_area("Combined Report", report_text, height=600, label_visibility="collapsed")
                st.download_button("⬇ Download Combined Report (.txt)", report_text,
                                   file_name=f"Dampati_{n1}_{n2}_Combined_Report.txt",
                                   mime="text/plain", width='stretch')

            # ── Enhanced Report Downloads (Infographic + Document) ──────────────
            st.markdown("---")
            with st.expander("📦 Download Enhanced Reports (Infographic & Document)"):
                from ui.report_html import generate_combined_html as _gch_m
                from ui.report_docx import generate_combined_docx as _gcd_m
                _cs_m  = compute_combined_year_scores(chart1, chart2, yr_from, yr_to)
                _s1_m  = compute_year_scores(chart1, yr_from, yr_to)
                _s2_m  = compute_year_scores(chart2, yr_from, yr_to)
                _pr1_m = generate_dasha_predictions(chart1, yr_from, yr_to)
                _pr2_m = generate_dasha_predictions(chart2, yr_from, yr_to)
                _html_m = _gch_m(chart1, chart2, n1, n2, p1, p2, d1, d2, t1, t2,
                                 _cs_m, _s1_m, _s2_m, _pr1_m, _pr2_m).encode("utf-8")
                _docx_m = _gcd_m(chart1, chart2, n1, n2, p1, p2, d1, d2, t1, t2,
                                 _cs_m, _s1_m, _s2_m, _pr1_m, _pr2_m)
                _dc1_m, _dc2_m = st.columns(2)
                _dc1_m.download_button("📊 Infographic Report (.html)", _html_m,
                    file_name=f"Dampati_{n1}_{n2}_Infographic.html",
                    mime="text/html", width='stretch', type="primary")
                _dc2_m.download_button("📄 Document Report (.docx)", _docx_m,
                    file_name=f"Dampati_{n1}_{n2}_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    width='stretch')
                st.caption("📊 Infographic opens in any browser with visual charts and color-coded predictions. 📄 Document opens in Word or Google Docs with full narrative.")
