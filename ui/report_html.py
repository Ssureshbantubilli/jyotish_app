"""
HTML Infographic Report Generator for Jyotisha App
Generates beautiful, self-contained HTML files with Chart.js visualizations.
"""

import json
import datetime

SIGN_GLYPHS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]
PLANET_GLYPH = {
    "Surya":"☀","Chandra":"🌙","Budha":"☿","Shukra":"♀","Mangal":"♂",
    "Guru":"♃","Shani":"♄","Rahu":"☊","Ketu":"☋","Lagna":"↑"
}
AREA_ICON  = {"career":"💼","health":"🩺","relationships":"💑","finances":"💰","spirituality":"🪔"}
AREA_LABEL = {
    "career":"Career & Status","health":"Health & Vitality",
    "relationships":"Relationships & Family","finances":"Finances & Wealth",
    "spirituality":"Spirituality & Upaya",
}
COLOR_MAP = {
    "Outstanding":"#F0C040","Excellent":"#40D060","Very Good":"#40C0C0",
    "Good":"#6090F0","Moderate":"#E0A040","Challenging":"#F06060","Difficult":"#C02020",
}
BG_MAP = {
    "Outstanding":"#2A1800","Excellent":"#0A2010","Very Good":"#0A1820",
    "Good":"#0A1028","Moderate":"#201400","Challenging":"#200808","Difficult":"#180404",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
body{background:#060810;color:#D0C8E0;font-family:'Inter',sans-serif;font-size:14px;line-height:1.6}
.page-wrap{max-width:1100px;margin:0 auto;padding:24px 20px}
.report-header{text-align:center;padding:40px 20px 32px;border-bottom:2px solid #C89010;margin-bottom:32px;background:linear-gradient(135deg,#0A0612 0%,#120818 100%);border-radius:16px}
.om{font-size:2.5rem;color:#C89010;margin-bottom:8px}
.report-title{font-family:'Noto Serif',serif;font-size:2rem;color:#C89010;margin-bottom:6px}
.report-subtitle{color:#8080A0;font-size:0.9rem;letter-spacing:0.05em}
.report-name{font-family:'Noto Serif',serif;font-size:1.5rem;color:#E8D8A8;margin:16px 0 4px}
.report-meta{color:#7070A0;font-size:0.83rem}
.report-date{color:#6060A0;font-size:0.78rem;margin-top:8px}
.section{margin-bottom:32px}
.section-title{font-family:'Noto Serif',serif;font-size:1.2rem;color:#C89010;border-bottom:1px solid #2A2030;padding-bottom:8px;margin-bottom:16px;display:flex;align-items:center;gap:8px}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-bottom:16px}
.metric-card{background:#0E1020;border:1px solid #2A2A3A;border-radius:12px;padding:16px;text-align:center}
.metric-card .label{color:#7080A0;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px}
.metric-card .value{color:#E8D8A8;font-weight:700;font-size:1.1rem;margin-bottom:2px}
.metric-card .sub{color:#6070A0;font-size:0.8rem}
.metric-card .glyph{font-size:1.6rem;margin-bottom:6px}
.badge{display:inline-block;padding:3px 10px;border-radius:6px;font-weight:600;font-size:0.8rem}
.badge-Outstanding{background:#2A1800;color:#F0C040;border:1px solid #C89010}
.badge-Excellent{background:#0A2010;color:#40D060;border:1px solid #20A040}
.badge-Very-Good{background:#0A1820;color:#40C0C0;border:1px solid #20A0A0}
.badge-Good{background:#0A1028;color:#6090F0;border:1px solid #2060C8}
.badge-Moderate{background:#201400;color:#E0A040;border:1px solid #D07800}
.badge-Challenging{background:#200808;color:#F06060;border:1px solid #C02020}
.badge-Difficult{background:#180404;color:#E04040;border:1px solid #A01818}
.planet-table{width:100%;border-collapse:collapse;background:#0A0C18;border-radius:10px;overflow:hidden}
.planet-table th{background:#160E28;color:#C89010;padding:10px 14px;text-align:left;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.06em;border-bottom:1px solid #2A2030}
.planet-table td{padding:10px 14px;border-bottom:1px solid #141420;color:#C0B8D8}
.planet-table tr:last-child td{border-bottom:none}
.planet-table tr:hover td{background:#12101E}
.dig-exalted{color:#F0C040;font-weight:600}
.dig-own{color:#40D060;font-weight:600}
.dig-debil{color:#F06060}
.dig-friend{color:#60A0F0}
.dig-enemy{color:#E08050}
.dig-neutral{color:#8090A0}
.yoga-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.yoga-card{background:#0A0810;border:1px solid #4A2080;border-radius:10px;padding:14px}
.yoga-name{color:#C090FF;font-weight:700;font-size:0.95rem;margin-bottom:4px}
.yoga-meta{color:#6050A0;font-size:0.78rem;margin-bottom:8px}
.yoga-desc{color:#A0A0C0;font-size:0.84rem;line-height:1.55}
.yoga-strength{float:right;color:#F0C040;font-size:0.78rem}
.dasha-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.dasha-card{border:1px solid #2A2040;border-radius:9px;padding:12px;background:#0C0A18}
.dasha-card.active{border-color:#8040C0;background:#140828}
.dasha-lord{font-weight:700;color:#D0B0FF;font-size:1rem;margin-bottom:2px}
.dasha-dates{color:#7060A0;font-size:0.82rem}
.dasha-active-tag{display:inline-block;background:#8040C0;color:#fff;border-radius:4px;padding:1px 8px;font-size:0.72rem;margin-left:6px}
.pred-block{margin-bottom:18px;border:1px solid #2A2040;border-radius:12px;overflow:hidden}
.pred-header{padding:13px 16px;display:flex;justify-content:space-between;align-items:center}
.pred-lord{font-weight:700;font-size:1rem}
.pred-period{color:#8080A0;font-size:0.82rem}
.pred-body{padding:14px 16px;background:#08060E}
.pred-shastra{border-left:3px solid #6040A0;padding:6px 12px;margin-bottom:12px;color:#A090C0;font-style:italic;font-size:0.82rem;background:#0A0818}
.pred-areas{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.pred-area{background:#0E1020;border:1px solid #1E1E30;border-radius:8px;padding:10px}
.pred-area-title{color:#E8D0A0;font-weight:600;font-size:0.82rem;margin-bottom:5px}
.pred-area-text{color:#A0A0C0;font-size:0.82rem;line-height:1.5}
.pred-guidance{background:#0A1018;border:1px solid #1A2830;border-radius:8px;padding:12px;margin-top:10px}
.pred-guidance-title{color:#A0C8E0;font-weight:600;margin-bottom:6px;font-size:0.85rem}
.pred-guidance-text{color:#B0B8C8;font-size:0.83rem;line-height:1.55}
.chart-wrap{background:#0A0C18;border:1px solid #1A1A2A;border-radius:12px;padding:16px;margin-bottom:16px}
.partner-section{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.partner-card{background:#0E1020;border:1px solid #2A2A3A;border-radius:12px;padding:16px}
.partner-title{font-family:'Noto Serif',serif;color:#C89010;font-size:1rem;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #2A2030}
.protection-table{width:100%;border-collapse:collapse}
.protection-table th{background:#160E28;color:#C89010;padding:8px 10px;text-align:left;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.04em}
.protection-table td{padding:8px 10px;border-bottom:1px solid #141420;font-size:0.82rem}
.protection-table tr:last-child td{border-bottom:none}
.report-footer{text-align:center;margin-top:40px;padding:20px;border-top:1px solid #1A1A2A;color:#4A4A6A;font-size:0.78rem}
@media print{
  body{background:#fff;color:#222}
  .report-header{background:#f8f4ec;border-color:#C89010}
  .report-title,.om,.section-title{color:#8B6000}
  .planet-table th{background:#f0e8d0}
  .metric-card,.yoga-card,.dasha-card,.pred-area,.pred-guidance,.chart-wrap{background:#fafafa;border-color:#ddd}
}
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def _badge(cat):
    return f'<span class="badge badge-{cat.replace(" ","-")}">{cat}</span>'

def _dignity_class(dig):
    if "Exalted" in dig: return "dig-exalted"
    if "Own"     in dig: return "dig-own"
    if "Debil"   in dig: return "dig-debil"
    if "Friend"  in dig: return "dig-friend"
    if "Enemy"   in dig: return "dig-enemy"
    return "dig-neutral"

def _planet_rows_html(chart):
    ORDER = ["Lagna","Surya","Chandra","Budha","Shukra","Mangal","Guru","Shani","Rahu","Ketu"]
    rows = ""
    for nm in ORDER:
        pd = chart["planets"].get(nm)
        if not pd: continue
        dig = pd["dignity"]
        rows += (f'<tr><td>{PLANET_GLYPH.get(nm,"")} {nm}</td>'
                 f'<td>{SIGN_GLYPHS[pd["sign"]]} {pd["sign_san"]}</td>'
                 f'<td>{pd["deg"]:.1f}°</td>'
                 f'<td style="text-align:center">{pd["house"]}</td>'
                 f'<td class="{_dignity_class(dig)}">{dig}</td></tr>')
    return rows

def _yoga_cards_html(chart):
    if not chart["yogas"]:
        return "<p style='color:#6060A0;font-style:italic'>Standard chart — individual planetary strengths govern.</p>"
    cards = "".join(
        f'<div class="yoga-card"><span class="yoga-strength">⭐ {y["strength"]}</span>'
        f'<div class="yoga-name">{y["name"]}</div>'
        f'<div class="yoga-meta">{y["planets"]} | House {y["house"]}</div>'
        f'<div class="yoga-desc">{y["description"]}</div></div>'
        for y in chart["yogas"]
    )
    return f'<div class="yoga-grid">{cards}</div>'

def _dasha_cards_html(chart):
    today = datetime.date.today()
    cards = ""
    for d in chart["dasha_seq"]:
        active = d["start"] <= today <= d["end"]
        cls  = "dasha-card active" if active else "dasha-card"
        tag  = '<span class="dasha-active-tag">▶ NOW</span>' if active else ""
        cards += (f'<div class="{cls}">'
                  f'<div class="dasha-lord">{PLANET_GLYPH.get(d["lord"],"")} {d["lord"]} MD{tag}</div>'
                  f'<div class="dasha-dates">{d["start"].strftime("%b %Y")} — {d["end"].strftime("%b %Y")} · {d["years"]:.0f} yrs</div>'
                  f'</div>')
    return f'<div class="dasha-grid">{cards}</div>'

def _overview_cards_html(chart, place):
    return f"""
    <div class="card-row">
      <div class="metric-card">
        <div class="glyph">{SIGN_GLYPHS[chart["lagna_sign"]]}</div>
        <div class="label">Lagna (Ascendant)</div>
        <div class="value">{chart["lagna_san"]} ({chart["lagna_en"]})</div>
        <div class="sub">{chart["lagna_deg"]:.1f}° | Lord: {chart["lagna_lord"]}</div>
      </div>
      <div class="metric-card">
        <div class="glyph">{SIGN_GLYPHS[chart["moon_sign"]]}</div>
        <div class="label">Janma Rashi</div>
        <div class="value">{chart["moon_san"]} ({chart["moon_en"]})</div>
        <div class="sub">{chart["moon_deg"]:.1f}°</div>
      </div>
      <div class="metric-card">
        <div class="glyph">⭐</div>
        <div class="label">Janma Nakshatra</div>
        <div class="value">{chart["nakshatra"]}, Pada {chart["nak_pada"]}</div>
        <div class="sub">Lord: {chart["nak_lord"]} | Deity: {chart["nak_deity"]}</div>
      </div>
      <div class="metric-card">
        <div class="glyph">📅</div>
        <div class="label">Active Dasha</div>
        <div class="value">{chart["active_md"]["lord"]} MD – {chart["active_ad"]["lord"]} AD</div>
        <div class="sub">MD ends: {chart["active_md"]["end"].strftime("%b %Y")}</div>
      </div>
    </div>"""

def _year_chart_js(year_scores, chart_id, score_key="score"):
    years  = [r["year"] for r in year_scores]
    vals   = [round(r.get(score_key, r.get("combined", r.get("score", 0))), 2) for r in year_scores]
    colors = [COLOR_MAP.get(r["category"], "#8080A0") for r in year_scores]
    cats   = [r["category"] for r in year_scores]
    md_ads = [f"{r.get('md_lord', r.get('md1','?'))}-{r.get('ad_lord', r.get('ad1','?'))}" for r in year_scores]
    return f"""
    <div class="chart-wrap">
      <canvas id="{chart_id}" height="260"></canvas>
    </div>
    <script>
    (function(){{
      var ctx = document.getElementById('{chart_id}').getContext('2d');
      new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: {json.dumps(years)},
          datasets: [{{
            label: 'Shastra Score',
            data: {json.dumps(vals)},
            backgroundColor: {json.dumps(colors)},
            borderColor: {json.dumps(colors)},
            borderWidth: 1,
            borderRadius: 4,
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                afterLabel: function(ctx) {{
                  var cats = {json.dumps(cats)};
                  var mds  = {json.dumps(md_ads)};
                  return [cats[ctx.dataIndex], 'Dasha: '+mds[ctx.dataIndex]];
                }}
              }},
              backgroundColor: '#1A1A2A', titleColor: '#E8D8A8', bodyColor: '#B0B0C0'
            }}
          }},
          scales: {{
            x: {{ grid: {{ color: '#1A1A2A' }}, ticks: {{ color: '#8080A0', font: {{size:11}} }} }},
            y: {{
              min: 0, max: 10.5,
              grid: {{ color: '#1A1A2A' }}, ticks: {{ color: '#8080A0', font: {{size:11}} }},
              title: {{ display: true, text: 'Shastra Score (0–10)', color: '#7070A0', font: {{size:11}} }}
            }}
          }}
        }}
      }});
    }})();
    </script>"""

def _predictions_html(preds):
    if not preds:
        return "<p style='color:#6060A0'>No predictions for selected range.</p>"
    html = ""
    for p in preds:
        col  = COLOR_MAP.get(p["category"], "#8080A0")
        bg   = BG_MAP.get(p["category"], "#0A0818")
        g    = PLANET_GLYPH.get(p["lord"], "🪐")
        tag  = " &nbsp;▶ ACTIVE NOW" if p["is_current"] else (" &nbsp;[Past]" if p["is_past"] else "")
        areas_html = "".join(
            f'<div class="pred-area">'
            f'<div class="pred-area-title">{AREA_ICON.get(area,"")} {AREA_LABEL.get(area,area.title())}</div>'
            f'<div class="pred-area-text">{text}</div>'
            f'</div>'
            for area, text in list(p["life_areas"].items())[:5]
        )
        g_data  = p.get("guidance", {})
        html += f"""
        <div class="pred-block">
          <div class="pred-header" style="background:{bg};border-bottom:1px solid {col}44">
            <span class="pred-lord" style="color:{col}">{g} {p["lord"]} Maha Dasha{tag}</span>
            <span class="pred-period">{p["start"].strftime("%b %Y")} – {p["end"].strftime("%b %Y")} &nbsp;·&nbsp; {p["years"]:.1f} yrs &nbsp;·&nbsp; {_badge(p["category"])}</span>
          </div>
          <div class="pred-body">
            <div class="pred-shastra">{p.get("shastra_ref","")}</div>
            <p style="color:#B0A8C0;font-size:0.85rem;margin-bottom:12px">
              <b>House {p["house"]} in {p["sign"]}</b> — {p["dignity"]} &nbsp;|&nbsp; {p.get("quality_note","")}
            </p>
            <div class="pred-areas">{areas_html}</div>
            <div class="pred-guidance">
              <div class="pred-guidance-title">🪔 Upaya & Jyotishi's Counsel</div>
              <p style="color:#A0B8C0;font-size:0.82rem;margin-bottom:6px">🕉️ <b>Mantra:</b> {g_data.get("mantra","")}</p>
              <p style="color:#A0A8C0;font-size:0.82rem;margin-bottom:6px">🌸 <b>Dana:</b> {g_data.get("charity","")}</p>
              <div class="pred-guidance-text">💫 {g_data.get("focus","")}</div>
            </div>
          </div>
        </div>"""
    return html

def _combined_protection_table(cs_all, n1, n2):
    rows = ""
    for r in cs_all:
        s1, s2, comb = r["score1"], r["score2"], r["combined"]
        cat = r["category"]
        col = COLOR_MAP.get(cat, "#8080A0")
        if s1 >= 8.5 and s2 >= 8.5:    dynamic = "🌟 Both flourish"
        elif s1 >= 8.0 and s2 < 6.5:   dynamic = f"🛡️ {n1[:10]} protects"
        elif s2 >= 8.0 and s1 < 6.5:   dynamic = f"🛡️ {n2[:10]} protects"
        elif s1 < 5.5 and s2 < 5.5:    dynamic = "🤝 Mutual support"
        else:                            dynamic = "⚖️ Steady progress"
        _cat_key = r.get("category", "Moderate")
        _cat_col = COLOR_MAP.get(_cat_key, "#8080A0")
        rows += (f'<tr>'
                 f'<td style="font-weight:600;color:#D0C0F0">{r["year"]}</td>'
                 f'<td>{r["md1"]}-{r["ad1"]}</td>'
                 f'<td style="text-align:center;color:{_cat_col}">{s1:.1f}</td>'
                 f'<td>{r["md2"]}-{r["ad2"]}</td>'
                 f'<td style="text-align:center;color:{_cat_col}">{s2:.1f}</td>'
                 f'<td style="text-align:center;font-weight:700;color:{col}">{comb:.1f}</td>'
                 f'<td style="font-size:0.8rem">{dynamic}</td>'
                 f'</tr>')
    return (f'<table class="protection-table"><thead><tr>'
            f'<th>Year</th><th>{n1[:10]} Dasha</th><th>{n1[:8]} ⭐</th>'
            f'<th>{n2[:10]} Dasha</th><th>{n2[:8]} ⭐</th>'
            f'<th>Combined</th><th>Dynamic</th>'
            f'</tr></thead><tbody>{rows}</tbody></table>')

def _wrap_html(title, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>{CSS}</style>
</head>
<body>
<div class="page-wrap">
{body}
<div class="report-footer">
  ॐ तत्सत् · Jyotisha Report · Nirayana Sidereal System · Lahiri Ayanamsha<br>
  Sources: Brihat Parashara Hora Shastra · Brihat Jataka · Phaladeepika · Saravali · Uttara Kalamrita<br>
  This report is for spiritual guidance and self-reflection. Consult a qualified Jyotishi for life decisions.
</div>
</div>
</body>
</html>"""

# ── Public API ────────────────────────────────────────────────────────────────

def generate_individual_html(chart, name, place, dob, tob_h, year_scores, predictions):
    today_str = datetime.date.today().strftime("%d %B %Y")
    dob_str   = dob.strftime("%d %B %Y") if hasattr(dob, "strftime") else str(dob)
    tob_str   = f"{int(tob_h):02d}:{int((tob_h % 1)*60):02d} IST"

    # Pre-build category badge strip (avoids backslash-in-f-string on Python < 3.12)
    _all_cats = ["Outstanding","Excellent","Very Good","Good","Moderate","Challenging","Difficult"]
    _badge_parts = []
    for _cat in _all_cats:
        _yrs = [str(r["year"]) for r in year_scores if r["category"] == _cat]
        if _yrs:
            _css = _cat.replace(" ", "-")
            _badge_parts.append(f'<span class="badge badge-{_css}">{_cat}: {", ".join(_yrs)}</span>')
    category_badges = " ".join(_badge_parts)
    pred_yr_range = (f"{year_scores[0]['year']}–{year_scores[-1]['year']}" if year_scores else "")

    body = f"""
    <div class="report-header">
      <div class="om">ॐ</div>
      <div class="report-title">Jyotisha Vedic Astrology Report</div>
      <div class="report-subtitle">Nirayana Sidereal · Lahiri Ayanamsha · Vimshottari Dasha<br>
        BPHS · Brihat Jataka · Phaladeepika · Saravali · Uttara Kalamrita</div>
      <div class="report-name">{name}</div>
      <div class="report-meta">Date of Birth: {dob_str} &nbsp;·&nbsp; Time: {tob_str} &nbsp;·&nbsp; Place: {place}</div>
      <div class="report-date">Report generated: {today_str}</div>
    </div>

    <div class="section">
      <div class="section-title">🗺️ Chart Overview</div>
      {_overview_cards_html(chart, place)}
    </div>

    <div class="section">
      <div class="section-title">🪐 Planetary Positions (Nirayana Sidereal)</div>
      <table class="planet-table">
        <thead><tr><th>Graha</th><th>Rashi</th><th>Degree</th><th>House</th><th>Dignity</th></tr></thead>
        <tbody>{_planet_rows_html(chart)}</tbody>
      </table>
    </div>

    <div class="section">
      <div class="section-title">✨ Yoga Vivechana (Planetary Combinations)</div>
      {_yoga_cards_html(chart)}
    </div>

    <div class="section">
      <div class="section-title">🗓️ Vimshottari Dasha Sequence</div>
      {_dasha_cards_html(chart)}
    </div>

    <div class="section">
      <div class="section-title">📈 Year-Wise Forecast</div>
      {_year_chart_js(year_scores, "yearChart1")}
      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:10px">{category_badges}</div>
    </div>

    <div class="section">
      <div class="section-title">🔮 Dasha-Wise Predictions ({pred_yr_range})</div>
      <p style="color:#7070A0;font-size:0.82rem;margin-bottom:14px">
        Per Vimshottari Dasha system (BPHS Ch.46). Each Maha Dasha period shapes the karmic trajectory
        across its duration — Antardasha sub-periods modulate the energy within.
      </p>
      {_predictions_html(predictions)}
    </div>
    """
    return _wrap_html(f"Jyotisha Report — {name}", body)


def generate_combined_html(chart1, chart2, n1, n2, place1, place2,
                            dob1, dob2, tob1, tob2,
                            combined_scores, s1_data, s2_data, preds1, preds2):
    today_str = datetime.date.today().strftime("%d %B %Y")
    dob1_str  = dob1.strftime("%d %B %Y") if hasattr(dob1, "strftime") else str(dob1)
    dob2_str  = dob2.strftime("%d %B %Y") if hasattr(dob2, "strftime") else str(dob2)
    t1_str    = f"{int(tob1):02d}:{int((tob1%1)*60):02d} IST"
    t2_str    = f"{int(tob2):02d}:{int((tob2%1)*60):02d} IST"

    outstanding = [r for r in combined_scores if r["combined"] >= 9.0]
    excellent   = [r for r in combined_scores if 8.0 <= r["combined"] < 9.0]
    challenging = [r for r in combined_scores if r["combined"] < 6.5]
    avg_score   = sum(r["combined"] for r in combined_scores) / max(len(combined_scores), 1)
    yr_start    = combined_scores[0]["year"]  if combined_scores else ""
    yr_end      = combined_scores[-1]["year"] if combined_scores else ""

    peak_tag  = (f'<span class="badge badge-Outstanding">⭐ Peak: {", ".join(str(r["year"]) for r in outstanding)}</span>'
                 if outstanding else "")
    excel_tag = (f'<span class="badge badge-Excellent">✨ Excellent: {", ".join(str(r["year"]) for r in excellent)}</span>'
                 if excellent else "")
    chal_tag  = (f'<span class="badge badge-Challenging">⚠️ Needs Care: {", ".join(str(r["year"]) for r in challenging)}</span>'
                 if challenging else "")

    avg_cat = ("Excellent" if avg_score >= 8 else "Very Good" if avg_score >= 7
               else "Good" if avg_score >= 6 else "Moderate")

    body = f"""
    <div class="report-header">
      <div class="om">ॐ</div>
      <div class="report-title">Dampati Jyotisha — Combined Report</div>
      <div class="report-subtitle">Ardhanarishvara Kundali · Vimshottari Dasha System<br>
        BPHS Ch.18 · Jataka Parijata · Phaladeepika · Saravali</div>
      <div class="report-name">{n1} &nbsp;&amp;&nbsp; {n2}</div>
      <div class="report-meta">
        {n1}: {dob1_str} · {t1_str} · {place1}<br>
        {n2}: {dob2_str} · {t2_str} · {place2}
      </div>
      <div class="report-date">Report generated: {today_str}</div>
    </div>

    <div class="section">
      <div class="section-title">📊 Combined Summary</div>
      <div class="card-row">
        <div class="metric-card"><div class="glyph">📅</div>
          <div class="label">Years Analysed</div>
          <div class="value">{len(combined_scores)}</div>
          <div class="sub">{yr_start} – {yr_end}</div></div>
        <div class="metric-card"><div class="glyph">⚡</div>
          <div class="label">Average Combined Score</div>
          <div class="value">{avg_score:.1f}/10</div>
          <div class="sub">{_badge(avg_cat)}</div></div>
        <div class="metric-card"><div class="glyph">⭐</div>
          <div class="label">Outstanding Years</div>
          <div class="value">{len(outstanding)}</div>
          <div class="sub">{", ".join(str(r["year"]) for r in outstanding) or "—"}</div></div>
        <div class="metric-card"><div class="glyph">⚠️</div>
          <div class="label">Challenging Years</div>
          <div class="value">{len(challenging)}</div>
          <div class="sub">{", ".join(str(r["year"]) for r in challenging) or "—"}</div></div>
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:4px">{peak_tag} {excel_tag} {chal_tag}</div>
    </div>

    <div class="section">
      <div class="section-title">👥 Individual Chart Overviews</div>
      <div class="partner-section">
        <div class="partner-card"><div class="partner-title">👨 {n1}</div>{_overview_cards_html(chart1, place1)}</div>
        <div class="partner-card"><div class="partner-title">👩 {n2}</div>{_overview_cards_html(chart2, place2)}</div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">🪐 Planetary Positions</div>
      <div class="partner-section">
        <div class="partner-card">
          <div class="partner-title">👨 {n1}</div>
          <table class="planet-table">
            <thead><tr><th>Graha</th><th>Rashi</th><th>°</th><th>H</th><th>Dignity</th></tr></thead>
            <tbody>{_planet_rows_html(chart1)}</tbody>
          </table>
        </div>
        <div class="partner-card">
          <div class="partner-title">👩 {n2}</div>
          <table class="planet-table">
            <thead><tr><th>Graha</th><th>Rashi</th><th>°</th><th>H</th><th>Dignity</th></tr></thead>
            <tbody>{_planet_rows_html(chart2)}</tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">📈 Year-Wise Forecasts</div>
      <p style="color:#8080A0;font-size:0.83rem;margin-bottom:8px">Combined Dampati Energy</p>
      {_year_chart_js(combined_scores, "combChart", score_key="combined")}
      <div class="partner-section" style="margin-top:20px">
        <div>
          <p style="color:#40C0E0;font-weight:600;margin-bottom:8px">👨 {n1} Individual Forecast</p>
          {_year_chart_js(s1_data, "s1Chart", score_key="score")}
        </div>
        <div>
          <p style="color:#E060A0;font-weight:600;margin-bottom:8px">👩 {n2} Individual Forecast</p>
          {_year_chart_js(s2_data, "s2Chart", score_key="score")}
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">🛡️ Dampati Protection Analysis — Year by Year</div>
      <p style="color:#7070A0;font-size:0.82rem;margin-bottom:12px">
        Per BPHS Ch.18: In a dharmic marriage, when one spouse is in karmic difficulty,
        the other's Dasha energy provides shelter — the sacred geometry of Grihastha Ashrama.
      </p>
      {_combined_protection_table(combined_scores, n1, n2)}
    </div>

    <div class="section">
      <div class="section-title">🔮 Dasha Predictions — {n1}</div>
      {_predictions_html(preds1)}
    </div>

    <div class="section">
      <div class="section-title">🔮 Dasha Predictions — {n2}</div>
      {_predictions_html(preds2)}
    </div>
    """
    return _wrap_html(f"Dampati Jyotisha — {n1} & {n2}", body)
