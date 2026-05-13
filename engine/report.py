"""
REPORT GENERATOR
Generates full-text reports in the exact same style, depth,
and structure as the reports produced in this conversation.
All shastra references, section headings, and narrative patterns match.
"""

import datetime
from .calc import (
    SIGNS_SAN, SIGNS_EN, SIGN_LORDS,
    DASHA_YEARS, NAKSHATRAS,
)
from .interpret import (
    PLANET_FULL, PLANET_GLYPH, HOUSE_KARAK as HKARAK,
    MD_THEMES, NAK_INTERPRETATION, planet_in_house_text,
    dasha_period_text, spouse_indicators, calc_ashtakoot,
    compute_year_scores, compute_combined_year_scores
)

WEEKDAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def _weekday(d: datetime.date) -> str:
    return WEEKDAYS[d.weekday()]

def _fmt_deg(sid: float) -> str:
    d = int(sid % 30)
    m = int((sid % 30 - d) * 60)
    return f"{d}°{m:02d}'"

# ═══════════════════════════════════════════════════════════════════════════
# INDIVIDUAL REPORT
# ═══════════════════════════════════════════════════════════════════════════
def generate_individual_report(chart: dict, place_name: str = "") -> str:
    c = chart
    lines = []
    add = lines.append

    add("=" * 80)
    add("OM SHRI GANESHAYA NAMAH")
    add("BRIHAT JATAKA KUNDALI VIVECHANA")
    add("A Comprehensive Vedic Astrological Report")
    add("Based on: BPHS • Brihat Jataka (Varahamihira) • Phaladeepika • Saravali")
    add("=" * 80)
    add("")

    # ── BIRTH DATA ──────────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION I — JANMA PARICHAYA (BIRTH PARTICULARS)")
    add("━" * 80)
    add(f"  Native           : {c['name']}")
    add(f"  Date of Birth    : {c['dob'].strftime('%d %B %Y')} ({_weekday(c['dob'])})")
    add(f"  Time of Birth    : {int(c['tob_h']):02d}:{int((c['tob_h']%1)*60):02d} IST")
    add(f"  Place of Birth   : {place_name}")
    add(f"  Latitude / Lon   : {c['lat']:.4f}°N / {c['lon']:.4f}°E")
    add(f"  Ayanamsha        : Lahiri (Chitrapaksha) {c['ayanamsha']:.4f}°")
    add(f"  Julian Day       : {c['jd']:.4f}")
    add(f"  Calculation      : Nirayana (Sidereal) System")
    add("")

    # ── LAGNA & RASHI ───────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION II — JANMA KUNDALI: LAGNA, RASHI & NAKSHATRA")
    add("━" * 80)
    add(f"  LAGNA (Ascendant)   : {c['lagna_san']} ({c['lagna_en']}) — {_fmt_deg(c['lagna_sid'])}")
    add(f"  Lagna Lord          : {c['lagna_lord']}")
    add(f"  JANMA RASHI         : {c['moon_san']} ({c['moon_en']}) — {_fmt_deg(c['moon_sid'])}")
    add(f"  Rashi Lord          : {SIGN_LORDS[c['moon_sign']]}")
    add(f"  JANMA NAKSHATRA     : {c['nakshatra']} (Pada {c['nak_pada']})")
    add(f"  Nakshatra Lord      : {c['nak_lord']}")
    add(f"  Nakshatra Deity     : {c['nak_deity']}")
    add(f"  Tithi               : {c['tithi']} — {c.get('tithi_name','')}" )
    add(f"  Paksha              : {c.get('paksha','')}")
    add("")
    add("  NAKSHATRA VIVEKA (Insight):")
    add(f"  {NAK_INTERPRETATION.get(c['nakshatra'],'A powerful and auspicious nakshatra placement.')}")
    add("")

    # ── PLANETARY TABLE ─────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION III — GRAHA STHANA (PLANETARY POSITIONS)")
    add("━" * 80)
    add(f"  {'GRAHA':<22} {'RASHI':<18} {'DEG':<10} {'HOUSE':<8} {'DIGNITY'}")
    add("  " + "-"*72)
    planet_order = ["Lagna","Surya","Chandra","Budha","Shukra",
                    "Mangal","Guru","Shani","Rahu","Ketu"]
    for nm in planet_order:
        pd = c["planets"].get(nm)
        if not pd: continue
        glyph = PLANET_GLYPH.get(nm,"")
        full  = PLANET_FULL.get(nm, nm)
        add(f"  {glyph} {full:<20} {pd['sign_san']:<18} {_fmt_deg(pd['sid']):<10} "
            f"{pd['house']:<8} {pd['dignity']}")
    add("")

    # ── HOUSE TABLE ─────────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION IV — BHAVA VIVECHANA (HOUSE ANALYSIS)")
    add("━" * 80)
    add(f"  {'HOUSE':<8} {'RASHI':<18} {'LORD':<12} {'OCCUPANTS':<25} {'SIGNIFICATION'}")
    add("  " + "-"*90)
    for h in range(1, 13):
        hd = c["houses"][h]
        occ = ", ".join(hd["occupants"]) if hd["occupants"] else "—"
        sig = HKARAK.get(h,"")[:42]
        add(f"  {h:<8} {hd['sign']:<18} {hd['lord']:<12} {occ:<25} {sig}")
    add("")

    # ── PLANET INTERPRETATIONS ──────────────────────────────────────────────
    add("━" * 80)
    add("SECTION V — GRAHA PHALA (PLANETARY INTERPRETATIONS)")
    add("━" * 80)
    for nm in ["Surya","Chandra","Mangal","Budha","Guru","Shukra","Shani","Rahu","Ketu"]:
        pd = c["planets"].get(nm)
        if not pd: continue
        txt = planet_in_house_text(nm, pd["house"], pd["dignity"], c["lagna_san"])
        add(f"  {PLANET_GLYPH.get(nm,'')} {PLANET_FULL.get(nm,nm)} in {pd['sign_san']} ({pd['sign_en']}) — House {pd['house']}")
        add(f"    Dignity: {pd['dignity']}")
        add(f"    {txt}")
        add("")

    # ── YOGAS ───────────────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION VI — YOGA VIVECHANA (PLANETARY COMBINATIONS)")
    add("━" * 80)
    if c["yogas"]:
        for i, yoga in enumerate(c["yogas"], 1):
            add(f"  {i}. {yoga['name']}")
            add(f"     Combination  : {yoga['planets']}")
            add(f"     House        : {yoga['house']}")
            add(f"     Strength     : {yoga['strength']}")
            add(f"     Phala (Result): {yoga['description']}")
            add("")
    else:
        add("  Standard chart with no exceptional yoga combinations detected.")
        add("  Individual planetary strengths govern the chart.")
        add("")

    # ── DASHA SEQUENCE ──────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION VII — VIMSHOTTARI DASHA SYSTEM")
    add("━" * 80)
    add(f"  Based on Janma Nakshatra: {c['nakshatra']} (Lord: {c['nak_lord']})")
    add("")
    add(f"  {'MAHA DASHA':<15} {'START':<15} {'END':<15} {'YEARS'}")
    add("  " + "-"*55)
    today = datetime.date.today()
    for d in c["dasha_seq"]:
        marker = " ◄ CURRENT" if d["start"] <= today <= d["end"] else ""
        add(f"  {d['lord']:<15} {d['start'].strftime('%b %Y'):<15} "
            f"{d['end'].strftime('%b %Y'):<15} {d['years']:.2f}{marker}")
    add("")

    # Current MD/AD detail
    md = c["active_md"]; ad = c["active_ad"]
    add(f"  CURRENT MAHA DASHA: {md['lord']} ({md['start'].strftime('%b %Y')} — {md['end'].strftime('%b %Y')})")
    add(f"  CURRENT ANTARDASHA: {ad['lord']} ({ad['start'].strftime('%b %Y')} — {ad['end'].strftime('%b %Y')})")
    add("")
    add(f"  MD Theme: {MD_THEMES.get(md['lord'],'varied themes')}")
    add(f"  AD Theme: {MD_THEMES.get(ad['lord'],'varied themes')}")
    add("")
    add("  ANTARDASHA SEQUENCE (within current Maha Dasha):")
    add(f"  {'ANTARDASHA':<15} {'START':<15} {'END'}")
    add("  " + "-"*45)
    for a in c["antardasha_seq"]:
        m2 = " ◄ NOW" if a["start"] <= today <= a["end"] else ""
        add(f"  {a['lord']:<15} {a['start'].strftime('%b %Y'):<15} {a['end'].strftime('%b %Y')}{m2}")
    add("")

    # ── YEAR-WISE SCORES ─────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION VIII — GOCHAR PHALA (YEAR-WISE FORECAST 2025–2035)")
    add("━" * 80)
    yr_scores = compute_year_scores(c, 2025, 2035)
    add(f"  {'YEAR':<8} {'MAHA DASHA':<12} {'ANTARDASHA':<12} {'SCORE':<8} {'CATEGORY'}")
    add("  " + "-"*60)
    for yr in yr_scores:
        add(f"  {yr['year']:<8} {yr['md_lord']:<12} {yr['ad_lord']:<12} "
            f"{yr['score']:<8.1f} {yr['category']}")
    add("")

    # ── REMEDIES ────────────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION IX — UPAYA (VEDIC REMEDIES)")
    add("━" * 80)
    nak_lord = c["nak_lord"]
    lagna_lord = c["lagna_lord"]
    add(f"  Primary Nakshatra Lord : {nak_lord}")
    add(f"  Primary Lagna Lord     : {lagna_lord}")
    add("")
    add(_remedy_text(nak_lord, lagna_lord, c["nakshatra"], c))
    add("")

    add("━" * 80)
    add("OM TAT SAT — Jyotisha is the Eye of the Vedas")
    add("Based on: BPHS • Brihat Jataka (Varahamihira) • Phaladeepika • Saravali • Uttara Kalamrita")
    add("Lahiri Ayanamsha • Nirayana (Sidereal) System • Vimshottari Dasha")
    add("=" * 80)

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# COMPATIBILITY REPORT
# ═══════════════════════════════════════════════════════════════════════════
def generate_compatibility_report(chart1: dict, chart2: dict,
                                   place1: str = "", place2: str = "") -> str:
    lines = []
    add = lines.append

    add("=" * 80)
    add("OM SHRI MAHAALAKSHMYAI NAMAH")
    add("DAMPATI KUNDALI MILAN — VEDIC COMPATIBILITY REPORT")
    add("Based on: BPHS Ch.18 • Jataka Parijata Ch.11 • Phaladeepika")
    add("=" * 80)
    add("")

    add(f"  HUSBAND : {chart1['name']} — {chart1['dob'].strftime('%d %B %Y')}, {place1}")
    add(f"  WIFE     : {chart2['name']} — {chart2['dob'].strftime('%d %B %Y')}, {place2}")
    add("")

    # Basic chart summary for each
    for label, c in [("HUSBAND",chart1),("WIFE",chart2)]:
        add(f"  {label} CHART SUMMARY:")
        add(f"    Lagna : {c['lagna_san']} ({c['lagna_en']}) — Lord: {c['lagna_lord']}")
        add(f"    Rashi : {c['moon_san']} ({c['moon_en']})")
        add(f"    Naksh.: {c['nakshatra']}, Pada {c['nak_pada']} — Lord: {c['nak_lord']}")
        add(f"    Active: {c['active_md']['lord']} MD — {c['active_ad']['lord']} AD")
        add("")

    # ── ASHTAKOOT MILAN ─────────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION I — ASHTAKOOT MILAN (36-POINT COMPATIBILITY ANALYSIS)")
    add("━" * 80)
    milan = calc_ashtakoot(chart1, chart2)
    add(f"  {'KOOTA':<20} {'SCORE':<8} {'MAX':<6} {'DETAIL':<30} {'REMARK'}")
    add("  " + "-"*80)
    for k, v in milan["kootas"].items():
        add(f"  {k:<20} {v['score']:<8} {v['max']:<6} {v['detail']:<30} {v['remark']}")
    add("")
    add(f"  TOTAL SCORE : {milan['total']}/{milan['max']}")
    add(f"  VERDICT     : {milan['verdict']}")
    add("")
    add("  Per classical Jyotisha: 28+ = Excellent • 24-27 = Good • 18-23 = Average • <18 = Below average")
    add("")

    # ── 7TH HOUSE ANALYSIS ──────────────────────────────────────────────────
    add("━" * 80)
    add("SECTION II — KALATRA BHAVA ANALYSIS (7TH HOUSE)")
    add("━" * 80)
    for label, c in [("HUSBAND",chart1),("WIFE",chart2)]:
        si = spouse_indicators(c)
        add(f"  {label}:")
        add(f"    7th House Sign  : {si['seventh_sign']}")
        add(f"    7th Lord        : {si['seventh_lord']} — in {si['seventh_lord_sign']} (House {si['seventh_lord_house']}) [{si['seventh_lord_dignity']}]")
        add(f"    7th Occupants   : {', '.join(si['seventh_occupants']) if si['seventh_occupants'] else 'None'}")
        add(f"    Jupiter         : House {si['jupiter_house']} [{si['jupiter_dignity']}]")
        add(f"    Venus           : House {si['venus_house']}")
        add("")

    # ── DASHA SYNCHRONISATION ───────────────────────────────────────────────
    add("━" * 80)
    add("SECTION III — DAMPATI DASHA SYNCHRONISATION (2025–2035)")
    add("━" * 80)
    cs = compute_combined_year_scores(chart1, chart2, 2025, 2035)
    add(f"  {'YEAR':<8} {chart1['name'][:12]:<14} {chart2['name'][:12]:<14} {'COMBINED':<10} {'CATEGORY'}")
    add("  " + "-"*65)
    for r in cs:
        add(f"  {r['year']:<8} {r['md1']}-{r['ad1']:<12} {r['md2']}-{r['ad2']:<12} "
            f"{r['combined']:<10.1f} {r['category']}")
    add("")

    # ── DAMPATI PROTECTION ANALYSIS ─────────────────────────────────────────
    add("━" * 80)
    add("SECTION IV — DAMPATI YOGA & PROTECTION ANALYSIS")
    add("━" * 80)
    add("  Per BPHS Ch.18 and Jataka Parijata Ch.11:")
    add("  In a dharmic marriage, planets from one partner's chart fill gaps in the other's.")
    add("  When one spouse is in a difficult Dasha, the other's chart provides karmic protection.")
    add("")

    # Cross-chart planet in partner's houses
    add("  GRAHA MELANA (Cross-chart planetary influence):")
    for nm, pd1 in chart1["planets"].items():
        if nm in ["Lagna","Rahu","Ketu"]: continue
        h_in_c2 = ((pd1["sign"] - chart2["lagna_sign"]) % 12) + 1
        if h_in_c2 in [1,4,5,7,9,10]:
            add(f"    {chart1['name']}'s {PLANET_FULL.get(nm,nm)} falls in "
                f"House {h_in_c2} of {chart2['name']}'s chart — positive influence on "
                f"{HKARAK.get(h_in_c2,'that domain')[:50]}")
    add("")

    # Ardhanarishvara analysis
    add("  ARDHANARISHVARA PRINCIPLE (Skanda Purana):")
    add(f"    {chart1['name']} (Purusha): {chart1['active_md']['lord']} MD provides {MD_THEMES.get(chart1['active_md']['lord'],'dharmic direction')}")
    add(f"    {chart2['name']} (Prakriti): {chart2['active_md']['lord']} MD provides {MD_THEMES.get(chart2['active_md']['lord'],'manifesting energy')}")
    add("    Together: Their combined Dasha energies create a third destiny that belongs to neither alone.")
    add("")

    add("━" * 80)
    add("OM TAT SAT — Dampati Sahadharmacharini")
    add("Based on BPHS Ch.18 • Jataka Parijata • Phaladeepika • Rigveda 10.85 (Vivaha Sukta)")
    add("=" * 80)

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# COMBINED REPORT (2026–2050 with graph data)
# ═══════════════════════════════════════════════════════════════════════════
def generate_combined_report(chart1: dict, chart2: dict,
                              place1: str = "", place2: str = "",
                              year_from: int = 2026,
                              year_to:   int = 2050) -> tuple:
    """
    Returns (report_text: str, year_scores: list)
    year_scores contains raw data for graph rendering.
    """
    lines = []
    add = lines.append

    add("=" * 80)
    add("DAMPATI JYOTISHA — ARDHANARISHVARA KUNDALI")
    add("COMBINED LIFE ENERGY REPORT")
    add(f"Year-Wise Analysis: {year_from}–{year_to}")
    add("Based on: BPHS • Jataka Parijata • Phaladeepika • Rigveda 10.85")
    add("=" * 80)
    add("")
    add(f"  HUSBAND : {chart1['name']} | {chart1['lagna_san']} Lagna | {chart1['moon_san']} Rashi | {chart1['nakshatra']} Nak.")
    add(f"  WIFE    : {chart2['name']} | {chart2['lagna_san']} Lagna | {chart2['moon_san']} Rashi | {chart2['nakshatra']} Nak.")
    add(f"  Ayanamsha: Lahiri | System: Nirayana Sidereal")
    add("")

    # Scoring methodology
    add("━" * 80)
    add("SCORING METHODOLOGY")
    add("━" * 80)
    add("  Each year scored 1-10 based on:")
    add("  • Active MD/AD quality (based on planet placement in natal chart): 80%")
    add("  • Jupiter transit modifier (effect on Lagna and Moon): +0.2 to +0.8")
    add("  • Saturn transit / Sade Sati modifier: -0.5 to +0.3")
    add("  • Synergy bonus: +0.5 when both score 8+; -0.3 when either below 6")
    add("")
    add("  SCORE LEGEND:")
    add("  9.0–10.0: OUTSTANDING  | 8.0–8.9: EXCELLENT  | 7.5–7.9: VERY GOOD")
    add("  7.0–7.4:  GOOD         | 6.0–6.9: MODERATE   | <6.0: CHALLENGING")
    add("")

    # Year-wise table
    add("━" * 80)
    add("YEAR-BY-YEAR DAMPATI ENERGY ANALYSIS")
    add("━" * 80)
    cs = compute_combined_year_scores(chart1, chart2, year_from, year_to)
    s1 = compute_year_scores(chart1, year_from, year_to)
    s2 = compute_year_scores(chart2, year_from, year_to)

    add(f"  {'YEAR':<6} {'H-MD-AD':<15} {chart1['name'][:8]:<10} {'W-MD-AD':<15} {chart2['name'][:8]:<10} {'COMBINED':<10} {'CATEGORY'}")
    add("  " + "-"*80)
    for r, a, b in zip(cs, s1, s2):
        add(f"  {r['year']:<6} {a['md_lord']}-{a['ad_lord']:<12} {a['score']:<10.1f} "
            f"{b['md_lord']}-{b['ad_lord']:<12} {b['score']:<10.1f} "
            f"{r['combined']:<10.1f} {r['category']}")
    add("")

    # Phase analysis
    add("━" * 80)
    add("LIFE PHASE ANALYSIS")
    add("━" * 80)
    _write_phase_analysis(cs, chart1, chart2, lines)

    # Dampati protection
    add("")
    add("━" * 80)
    add("DAMPATI PROTECTION PRINCIPLE")
    add("━" * 80)
    add("  Per BPHS and Jataka Parijata:")
    add("  When one spouse is in a challenging period, the other's chart provides karmic protection.")
    add("  This analysis shows the following protection periods:")
    add("")
    for i, r in enumerate(cs):
        if r["combined"] >= 8.5:
            add(f"  {r['year']}: OUTSTANDING ({r['combined']}) — "
                f"{chart1['name']}: {r['md1']}-{r['ad1']} | {chart2['name']}: {r['md2']}-{r['ad2']}")
    add("")

    add("━" * 80)
    add("OM TAT SAT — Dampati Sahadharmacharini")
    add(f"Per Rigveda 10.85.47: 'May you grow old together. May you live a hundred years.'")
    add("=" * 80)

    return "\n".join(lines), cs, s1, s2


def _write_phase_analysis(cs: list, c1: dict, c2: dict, lines: list):
    add = lines.append
    outstanding = [r for r in cs if r["combined"] >= 9.0]
    excellent   = [r for r in cs if 8.0 <= r["combined"] < 9.0]
    moderate    = [r for r in cs if r["combined"] < 6.5]

    if outstanding:
        yrs = [str(r["year"]) for r in outstanding]
        add(f"  OUTSTANDING YEARS ({len(yrs)} years): {', '.join(yrs)}")
        add("  → Peak periods for: major life decisions, property, business launch,")
        add("    significant investments, family celebrations, and career advancements.")
        add("")

    if excellent:
        yrs = [str(r["year"]) for r in excellent]
        add(f"  EXCELLENT YEARS ({len(yrs)} years): {', '.join(yrs)}")
        add("  → Strong periods for: career growth, financial stability, marital harmony.")
        add("")

    if moderate:
        yrs = [str(r["year"]) for r in moderate]
        add(f"  CHALLENGING YEARS ({len(yrs)} years): {', '.join(yrs)}")
        add("  → Periods requiring: patience, spiritual practice, mutual support,")
        add("    reduced major decisions, increased sadhana and pilgrimage.")
        add("")


# ── REMEDY TEXT ──────────────────────────────────────────────────────────────
def _remedy_text(nak_lord: str, lagna_lord: str, nakshatra: str, chart: dict) -> str:
    MANTRA = {
        "Surya":  "Om Hram Hrim Hraum Sah Suryaya Namah",
        "Chandra":"Om Shram Shrim Shraum Sah Chandramase Namah",
        "Mangal": "Om Kram Krim Kraum Sah Bhaumaya Namah",
        "Budha":  "Om Bram Brim Braum Sah Budhaya Namah",
        "Guru":   "Om Gram Grim Graum Sah Gurave Namah",
        "Shukra": "Om Dram Drim Draum Sah Shukraya Namah",
        "Shani":  "Om Pram Prim Praum Sah Shanaischaraya Namah",
        "Rahu":   "Om Bhram Bhrim Bhraum Sah Rahave Namah",
        "Ketu":   "Om Stram Strim Straum Sah Ketave Namah",
    }
    GEMSTONE = {
        "Surya":"Ruby (Manikya) in gold ring, ring finger, Sunday",
        "Chandra":"Pearl (Moti) in silver ring, ring finger, Monday",
        "Mangal":"Red Coral (Moonga) in gold ring, ring finger, Tuesday",
        "Budha":"Emerald (Panna) in gold ring, little finger, Wednesday",
        "Guru":"Yellow Sapphire (Pukhraj) in gold ring, index finger, Thursday",
        "Shukra":"Diamond or White Sapphire in platinum, little finger, Friday",
        "Shani":"Blue Sapphire (Neelam) in silver ring, middle finger, Saturday",
        "Rahu":"Hessonite Garnet (Gomed) in silver ring, middle finger, Saturday",
        "Ketu":"Cat's Eye (Lahsuniya) in silver ring, little finger, Thursday",
    }
    DAY = {
        "Surya":"Sunday","Chandra":"Monday","Mangal":"Tuesday","Budha":"Wednesday",
        "Guru":"Thursday","Shukra":"Friday","Shani":"Saturday",
        "Rahu":"Saturday","Ketu":"Thursday"
    }

    lines = []
    lines.append(f"  1. NAKSHATRA LORD ({nak_lord}) REMEDY:")
    lines.append(f"     Mantra : {MANTRA.get(nak_lord,'Recite Beej Mantra')} — 108x on {DAY.get(nak_lord,'dedicated day')}")
    lines.append(f"     Gemstone: {GEMSTONE.get(nak_lord,'Appropriate gemstone after proper Prana Pratishtha')}")
    lines.append(f"     Deity   : Worship the deity of {nakshatra} Nakshatra for Nakshatra Shanti")
    lines.append("")
    lines.append(f"  2. LAGNA LORD ({lagna_lord}) REMEDY:")
    lines.append(f"     Mantra : {MANTRA.get(lagna_lord,'Recite appropriate Beej Mantra')} — 108x on {DAY.get(lagna_lord,'dedicated day')}")
    lines.append(f"     Gemstone: {GEMSTONE.get(lagna_lord,'Appropriate gemstone')}")
    lines.append("")
    lines.append(f"  3. CURRENT MAHA DASHA LORD ({chart['active_md']['lord']}) REMEDY:")
    md_lord = chart['active_md']['lord']
    lines.append(f"     Mantra : {MANTRA.get(md_lord,'Recite appropriate Beej Mantra')} — 108x on {DAY.get(md_lord,'dedicated day')}")
    lines.append(f"     Charity: Donate items associated with {md_lord} on {DAY.get(md_lord,'dedicated day')}")
    lines.append("")
    lines.append("  4. GENERAL REMEDIES:")
    lines.append("     • Recite Vishnu Sahasranama on Ekadashi (connects all planetary energies)")
    lines.append("     • Perform Navagraha Puja annually for comprehensive planetary harmonization")
    lines.append("     • Visit your Kshetra Devata (presiding deity of birthplace) regularly")
    lines.append("     • Perform Pitru Tarpana on Amavasya to resolve ancestral karmas")

    return "\n".join(lines)
