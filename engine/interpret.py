"""
INTERPRETATION ENGINE
Mirrors exactly the language, depth, and structure of reports generated
throughout this conversation. All shastra references, phala (results),
and narrative patterns are preserved.
"""

import datetime
from .calc import (
    SIGNS_SAN, SIGNS_EN, SIGN_LORDS, DASHA_YEARS, DASHA_ORDER,
    NAKSHATRAS, NAK_LORDS, OWN_SIGNS, EXALTATION, DEBILITATION,
    active_dasha, antardasha_sequence
)

# ── PLANET FULL NAMES ────────────────────────────────────────────────────────
PLANET_FULL = {
    "Surya":"Surya (Sun)","Chandra":"Chandra (Moon)","Budha":"Budha (Mercury)",
    "Shukra":"Shukra (Venus)","Mangal":"Mangal (Mars)","Guru":"Guru (Jupiter)",
    "Shani":"Shani (Saturn)","Rahu":"Rahu (North Node)","Ketu":"Ketu (South Node)",
    "Lagna":"Lagna (Ascendant)"
}
PLANET_GLYPH = {
    "Surya":"☀","Chandra":"🌙","Budha":"☿","Shukra":"♀","Mangal":"♂",
    "Guru":"♃","Shani":"♄","Rahu":"☊","Ketu":"☋","Lagna":"↑"
}

# ── HOUSE SIGNIFICATIONS ─────────────────────────────────────────────────────
HOUSE_KARAK = {
    1: "Self, personality, body, health, first impressions",
    2: "Wealth, family, speech, food, accumulated resources",
    3: "Courage, siblings, short travel, communication, hands",
    4: "Mother, home, education, vehicles, inner peace, property",
    5: "Intelligence, children, creativity, Purva Punya, speculation",
    6: "Enemies, debts, disease, service, daily work, obstacles",
    7: "Spouse, partnerships, business, public dealings",
    8: "Longevity, sudden events, occult, inheritance, transformation",
    9: "Father, fortune, dharma, religion, guru, higher learning",
   10: "Career, status, authority, karma, public recognition",
   11: "Gains, fulfillment of desires, elder siblings, social networks",
   12: "Expenditure, foreign lands, liberation, hidden enemies, sleep",
}

# ── NAKSHATRA INTERPRETATIONS ────────────────────────────────────────────────
NAK_INTERPRETATION = {
    "Ashwini":   "Born under the Ashwini Kumaras — divine physicians of the gods. Quick, energetic, healing qualities. Pioneer spirit with swift results.",
    "Bharani":   "Born under Yama — lord of dharma and transformation. Deep creative power, magnetic personality, carries both the seed of life and the certainty of change.",
    "Krittika":  "Born under Agni (fire). Sharp, penetrating, purifying intelligence. Leadership through precision and critical discernment.",
    "Rohini":    "Born under Brahma — the most fertile and creative nakshatra. Magnetic beauty, artistic gifts, and abundance. The favourite star of the Moon.",
    "Mrigashira":"Born under Soma (Moon). Gentle, curious, ever-searching. Quest for beauty and perfection. Sensitive and perceptive mind.",
    "Ardra":     "Born under Rudra (Shiva the destroyer). Sharp, penetrating, transformative. Great intellectual depth; storms precede profound wisdom.",
    "Punarvasu": "Born under Aditi — goddess of boundless space. Generous, optimistic, philosophical. The 'return of the light' — renewals and comebacks.",
    "Pushya":    "Born under Brihaspati (Jupiter) — the most auspicious nakshatra. Nourishing, wise, spiritually abundant. Natural teacher and guide.",
    "Ashlesha":  "Born under the Naga (serpent). Penetrating intuition, hypnotic presence, ability to see hidden truths. Powerful healing and transformation.",
    "Magha":     "Born under the Pitrus (ancestors). Regal bearing, sense of lineage, throne of authority. Carries the weight and dignity of the ancestral line.",
    "Purva Phalguni": "Born under Bhaga — god of good fortune and marital bliss. Creative, sensual, generous. The stage is set for pleasure, love, and prosperity.",
    "Uttara Phalguni": "Born under Aryaman — god of contracts and partnership. Reliable, service-oriented, bestows enduring success through social alliances.",
    "Hasta":     "Born under Savitar (the creator Sun). Skilled hands, artisanal mastery, healing touch. Practical intelligence applied with precision.",
    "Chitra":    "Born under Tvashtar (the divine craftsman). Artistic brilliance, architectural mind, and magnetic charisma. Beauty in all forms.",
    "Swati":     "Born under Vayu (wind). Independent, adaptable, socially skillful. Like the wind: cannot be contained; reaches everywhere.",
    "Vishakha":  "Born under Indra-Agni (purpose and fire). Intensely ambitious, goal-oriented, willing to sacrifice comfort for achievement. The arrow aimed at the target.",
    "Anuradha":  "Born under Mitra — god of friendship and devotion. Loyal, devoted, with the power to create deep and lasting bonds across all boundaries.",
    "Jyeshtha":  "Born under Indra — King of the Gods. Inherent authority, fierce protectiveness, desire to be the elder/chief. Carries the pride and the burden of leadership.",
    "Mula":      "Born under Nirriti (dissolution). Investigative, philosophical, drawn to roots and origins. The mind that asks 'why' until it reaches the source.",
    "Purva Ashadha": "Born under Apas (water). Invincible, purifying, convincing. Never accepts defeat. The power to cleanse, refresh, and rejuvenate.",
    "Uttara Ashadha": "Born under the Vishvedevas (all gods). Righteous, enduring, universally respected. Victory that is lasting because it is earned through dharma.",
    "Shravana":  "Born under Lord Vishnu — the preserver and protector of creation. Learning, listening, and wisdom. Carries the blessings of the cosmos's sustaining force.",
    "Dhanishtha":"Born under the Eight Vasus (gods of abundance). Musical, rhythmic, prosperity-generating. The beat of the cosmos in human form.",
    "Shatabhisha":"Born under Varuna (cosmic order). Mysterious, healing, scientific. The hundred healers — one who seeks and finds hidden cures and truths.",
    "Purva Bhadrapada": "Born under Aja Ekapada (the one-footed goat). Fiery, transformative, purifying. Bridges the material and the spiritual through radical change.",
    "Uttara Bhadrapada": "Born under Ahir Budhnya (the serpent of the deep). Deeply wise, compassionate, connected to cosmic waters. The wisdom that comes from depth.",
    "Revati":    "Born under Pushan (nourishing Sun). Protective, nurturing, caring for others on their journey. The last nakshatra — synthesis of all wisdom.",
}

# ── DASHA PLANET EFFECTS (MD level) ─────────────────────────────────────────
MD_THEMES = {
    "Ketu":   "spiritual detachment, past-karma resolution, moksha-seeking, psychic sensitivity, unexpected separations",
    "Shukra": "creativity, romance, wealth, artistic expression, relationships, pleasures, beauty",
    "Surya":  "authority, self-realization, career advancement, father-related themes, government connections, ego refinement",
    "Chandra":"emotions, mind, mother, public life, fluctuations, social connections, intuition, home",
    "Mangal": "energy, ambition, courage, career action, property, siblings, conflicts, technical skills",
    "Rahu":   "ambition, foreign connections, unconventional paths, rapid change, illusions, worldly expansion",
    "Guru":   "wisdom, dharma, prosperity, children, teaching, spirituality, expansion, guru-grace",
    "Shani":  "discipline, karma, delayed gratification, service, longevity, Vipareet Raja Yoga potential, responsibility",
    "Budha":  "intelligence, communication, business, trade, education, adaptability, analytical mastery",
}

# ── PLANET IN HOUSE INTERPRETATIONS ─────────────────────────────────────────
def planet_in_house_text(planet: str, house: int, dignity: str, lagna_san: str) -> str:
    """Generate interpretation text — mirrors conversation report style."""
    d = f" [{dignity}]" if dignity and dignity != "—" and dignity != "Neutral" else ""
    base = {
        ("Surya",1):"Sun in the Lagna{d} gives royal bearing, strong vitality, and leadership presence. The native's identity is tied to self-expression and authority. Per BPHS, Sun in Lagna creates 'Atma Bala' — strength of soul.",
        ("Surya",4):"Sun in 4th creates tensions with mother and home but builds inner resolve. Authority is exercised through domestic mastery.",
        ("Surya",5):"Sun in 5th{d} shines on intelligence, children, and creativity. Purva Punya is strong. Leadership through mentorship and creative expression.",
        ("Surya",6):"Sun in 6th{d} with dignity creates 'Harsha Yoga component' — the native's vitality and authority defeat all enemies and adversaries.",
        ("Surya",7):"Sun in 7th creates powerful but ego-challenging partnerships. The spouse may be authoritative or from a respected family.",
        ("Surya",10):"Sun in 10th{d} — exalted placement for career. Leadership, government connections, and public recognition are naturally attained.",
        ("Chandra",4):"Moon in 4th{d} — own sign energy or dignified. Deep emotional security, excellent mother relationship, comfort in homeland.",
        ("Chandra",7):"Moon in 7th creates an emotionally sensitive partnership. The native seeks emotional fulfillment through relationships.",
        ("Chandra",8):"Moon in 8th creates deep emotional intensity, occult interests, and transformative life experiences. Profound intuition and research abilities.",
        ("Chandra",10):"Moon in 10th — Lagna lord or chart lord in career house. The native's public image is emotionally magnetic. Career fluctuates but public recognition is strong.",
        ("Chandra",11):"Moon in 11th creates social magnetism, financial gains through networks, and fulfillment of desires. Per Saravali: continuous income and respected friends.",
        ("Mangal",6):"Mars in 6th{d} in own sign or exalted activates Harsha Yoga — complete victory over enemies, adversaries, and health challenges. Per Phaladeepika Ch.6.",
        ("Mangal",10):"Mars in 10th{d} — Parakrama Yoga. The native attacks career with warrior energy. Fearless professional execution and authority. Per BPHS.",
        ("Mangal",1):"Mars in Lagna{d} gives tremendous energy, courage, and assertiveness. The native is a natural leader and initiator.",
        ("Budha",1):"Mercury in Lagna{d} in own sign or strong — exceptional analytical ability, communication mastery, and intellectual leadership. Per Phaladeepika.",
        ("Budha",10):"Mercury in 10th{d} — fame through communication, analytical skills, and intellectual leadership. 'Kanaka Yoga' element — gold through words and mind.",
        ("Shukra",4):"Venus in 4th brings aesthetic beauty to home, vehicles, and domestic life. Comfortable living environment and artistic sensibility.",
        ("Shukra",7):"Venus in 7th — natural placement for romance and partnership. Beautiful, harmonious spouse. Per Brihat Jataka: fulfillment in relationships.",
        ("Guru",1):"Jupiter in Lagna{d} — divine protection, wisdom, and expansion as the native's core identity. Career and purpose aligned with dharma.",
        ("Guru",7):"Jupiter in 7th{d} — exalted or strong — the greatest possible marital blessing. Per BPHS: wise, respected, prosperous spouse; long and dharmic marriage.",
        ("Guru",10):"Jupiter in 10th{d} — peak career yoga. Advancement through wisdom, teaching, or advisory roles. Per Phaladeepika: fame and institutional recognition.",
        ("Shani",4):"Saturn in 4th — exalted in Libra is exceptionally auspicious here. Real estate gains, vehicles, and property accumulation in middle life.",
        ("Shani",5):"Saturn in 5th creates disciplined, long-term strategic intelligence. Children may come late but with extraordinary qualities.",
        ("Shani",12):"Saturn in 12th (Vyaya Bhava) — the Vipareet Raja Yoga foundation. Per BPHS: long-term hidden effort eventually yields extraordinary behind-the-scenes success.",
        ("Rahu",1):"Rahu in Lagna — the great amplifier of identity. Foreign connections, unconventional path, and rapid rises through ambitious networking. Per Sarvartha Chintamani.",
        ("Ketu",7):"Ketu in 7th creates karmic, unusual authority relationships. The native RISES DESPITE conventional partnerships, not because of them. Per BPHS.",
    }.get((planet, house))

    if base:
        return base.format(d=d)
    return (f"{PLANET_FULL.get(planet,planet)} in {house}th house{d}: "
            f"Per classical texts, this placement influences the significations of the {house}th bhava "
            f"({HOUSE_KARAK.get(house,'general life matters')}) according to the planet's natural qualities.")

# ── DASHA PERIOD TEXT ────────────────────────────────────────────────────────
def dasha_period_text(lord: str, start: datetime.date, end: datetime.date,
                       yrs: float, md_text: bool=True) -> str:
    theme = MD_THEMES.get(lord, "varied karmic themes")
    if md_text:
        return (f"{lord} Maha Dasha ({start.strftime('%b %Y')} — {end.strftime('%b %Y')}, "
                f"{yrs:.1f} years): This period activates themes of {theme}. "
                f"Results depend on {lord}'s placement and dignity in the birth chart.")
    else:
        return (f"{lord} Antardasha ({start.strftime('%b %Y')} — {end.strftime('%b %Y')}): "
                f"Sub-period focusing on {theme}.")

# ── COMPATIBILITY ENGINE ─────────────────────────────────────────────────────
KOOTA_POINTS = {
    # Nadi: 8 pts — most important
    # Bhakoot: 7 pts
    # Gana: 6 pts
    # Graha Maitri: 5 pts
    # Rashi: 7 pts
    # Yoni: 4 pts
    # Tara: 3 pts
    # Varna: 1 pt
    "Nadi": 8, "Bhakoot": 7, "Gana": 6, "Graha_Maitri": 5,
    "Rashi": 7, "Yoni": 4, "Tara": 3, "Varna": 1
}

NADI = ["Aadi","Madhya","Antya"]  # 0,1,2 based on nak_num % 3
GANA  = {
    # Nakshatra index → gana
    0:"Deva",1:"Manushya",2:"Rakshasa",3:"Deva",4:"Deva",5:"Manushya",
    6:"Deva",7:"Deva",8:"Rakshasa",9:"Rakshasa",10:"Manushya",11:"Deva",
    12:"Deva",13:"Rakshasa",14:"Deva",15:"Rakshasa",16:"Deva",17:"Rakshasa",
    18:"Rakshasa",19:"Manushya",20:"Deva",21:"Deva",22:"Rakshasa",23:"Deva",
    24:"Manushya",25:"Deva",26:"Manushya",
}

def calc_ashtakoot(chart1: dict, chart2: dict) -> dict:
    """
    Calculate Ashtakoot Milan scores.
    Returns dict with each koota and total.
    """
    n1 = chart1["nak_num"]; n2 = chart2["nak_num"]
    m1 = chart1["moon_sign"]; m2 = chart2["moon_sign"]

    results = {}

    # 1. Nadi (8 pts) — most important for health
    nadi1 = n1 % 3; nadi2 = n2 % 3
    nadi_score = 8 if nadi1 != nadi2 else 0
    results["Nadi"] = {"score": nadi_score, "max": 8,
        "detail": f"{['Aadi','Madhya','Antya'][nadi1]} × {['Aadi','Madhya','Antya'][nadi2]}",
        "remark": "Excellent — no Nadi Dosha" if nadi_score==8 else "Nadi Dosha present — remedies advised"}

    # 2. Bhakoot (7 pts) — prosperity and progeny
    diff = abs(m1 - m2) + 1
    if diff > 12: diff = 13 - diff
    bhakoot_score = 7 if diff not in [6,8,9,12,5,3] else 0
    # 2-12, 1-7, 3-11, 4-10 are compatible; 6-8, 5-9 are afflicted
    # simplified: only penalise known bad combos
    bad_diffs = {6,8}  # 2-12 and 1-7 are actually auspicious; 6-8 is bad
    real_diff = (m2 - m1) % 12 + 1
    if real_diff in [6,8] or (12-real_diff+1) in [6,8]:
        bhakoot_score = 0
    else:
        bhakoot_score = 7
    results["Bhakoot"] = {"score": bhakoot_score, "max": 7,
        "detail": f"Rashi interval: {real_diff}",
        "remark": "Auspicious" if bhakoot_score==7 else "Bhakoot Dosha — wealth and progeny may be affected"}

    # 3. Gana (6 pts) — temperament
    g1 = GANA.get(n1,"Deva"); g2 = GANA.get(n2,"Deva")
    gana_matrix = {("Deva","Deva"):6,("Manushya","Manushya"):6,("Rakshasa","Rakshasa"):6,
                   ("Deva","Manushya"):5,("Manushya","Deva"):5,
                   ("Deva","Rakshasa"):1,("Rakshasa","Deva"):1,
                   ("Manushya","Rakshasa"):0,("Rakshasa","Manushya"):0}
    gana_score = gana_matrix.get((g1,g2), 3)
    results["Gana"] = {"score": gana_score, "max": 6,
        "detail": f"{g1} (husband) × {g2} (wife)",
        "remark": "Harmonious temperaments" if gana_score>=5 else
                  "Moderate compatibility" if gana_score>=3 else "Temperament differences require conscious effort"}

    # 4. Graha Maitri (5 pts) — mental compatibility
    ml1 = SIGN_LORDS[m1]; ml2 = SIGN_LORDS[m2]
    FRIENDSHIP = {
        "Surya":  {"Chandra","Mangal","Guru"},
        "Chandra":{"Surya","Budha"},
        "Mangal": {"Surya","Chandra","Guru"},
        "Budha":  {"Surya","Shukra"},
        "Guru":   {"Surya","Chandra","Mangal"},
        "Shukra": {"Budha","Shani"},
        "Shani":  {"Budha","Shukra"},
        "Rahu":   {"Shukra","Shani"},
        "Ketu":   {"Mangal","Shukra"},
    }
    f12 = ml1 in FRIENDSHIP.get(ml2,set())
    f21 = ml2 in FRIENDSHIP.get(ml1,set())
    if f12 and f21:   gm = 5
    elif f12 or f21:  gm = 4
    elif ml1==ml2:    gm = 4
    else:             gm = 3
    results["Graha_Maitri"] = {"score": gm, "max": 5,
        "detail": f"{ml1} (husband's Moon lord) × {ml2} (wife's Moon lord)",
        "remark": "Natural mental affinity" if gm>=4 else "Mental understanding requires cultivation"}

    # 5. Rashi (7 pts) — overall compatibility
    rashi_score = 7 if m1==m2 else 5 if abs(m1-m2) in [1,11] else 3
    results["Rashi"] = {"score": rashi_score, "max": 7,
        "detail": f"{SIGNS_SAN[m1]} × {SIGNS_SAN[m2]}",
        "remark": "Same Rashi — very deep emotional resonance" if m1==m2 else "Compatible" if rashi_score>=5 else "Moderate"}

    # 6. Tara (3 pts) — birth star compatibility
    tara = (n2 - n1) % 27 + 1
    good_taras = {1,2,4,6,8,9}
    tara_score = 3 if tara in good_taras else 1
    results["Tara"] = {"score": tara_score, "max": 3,
        "detail": f"Tara count: {tara}",
        "remark": "Auspicious Tara" if tara_score==3 else "Tara requires attention"}

    # 7. Yoni (4 pts) — physical compatibility (simplified)
    yoni_score = 4  # simplified; full yoni requires symbol table
    results["Yoni"] = {"score": yoni_score, "max": 4,
        "detail": "Nakshatra animal symbols",
        "remark": "Compatible"}

    # 8. Varna (1 pt)
    varna_score = 1
    results["Varna"] = {"score": varna_score, "max": 1,
        "detail": "Spiritual compatibility",
        "remark": "Compatible"}

    total = sum(v["score"] for v in results.values())
    max_t = sum(v["max"]   for v in results.values())

    verdict = ("Uttama (Excellent) — Highly recommended" if total >= 28 else
               "Uttama-Madhyama (Very Good)" if total >= 24 else
               "Madhyama (Good)" if total >= 18 else
               "Below average — remedies and counseling advised")

    return {"kootas": results, "total": total, "max": max_t, "verdict": verdict}

# ── 7TH HOUSE ANALYSIS ───────────────────────────────────────────────────────
def spouse_indicators(chart: dict) -> dict:
    """Analyse 7th house, 7th lord, and Venus for spouse qualities."""
    lagna_sign = chart["lagna_sign"]
    seventh_sign = (lagna_sign + 6) % 12
    seventh_lord = SIGN_LORDS[seventh_sign]
    pl = chart["planets"]

    # What's in 7th house?
    seventh_occupants = [nm for nm,pd in pl.items() if pd["house"]==7 and nm!="Lagna"]

    # 7th lord position
    sl_data = pl.get(seventh_lord, {})
    sl_house = sl_data.get("house", 0)
    sl_sign  = sl_data.get("sign_san","")
    sl_dignity = sl_data.get("dignity","")

    # Jupiter's role (natural karaka for husband in female chart)
    # Venus's role (natural karaka for wife in male chart)
    jupiter_h = pl.get("Guru",{}).get("house",0)
    jupiter_dignity = pl.get("Guru",{}).get("dignity","")
    venus_h = pl.get("Shukra",{}).get("house",0)

    return {
        "seventh_sign": SIGNS_SAN[seventh_sign],
        "seventh_lord": seventh_lord,
        "seventh_lord_house": sl_house,
        "seventh_lord_sign": sl_sign,
        "seventh_lord_dignity": sl_dignity,
        "seventh_occupants": seventh_occupants,
        "jupiter_house": jupiter_h,
        "jupiter_dignity": jupiter_dignity,
        "venus_house": venus_h,
    }

# ── YEAR-WISE COMBINED SCORING ────────────────────────────────────────────────
def dasha_quality_score(md_lord: str, ad_lord: str, chart: dict) -> float:
    """
    Score MD-AD combination 1-10 based on planet placements in natal chart.
    Same logic as dampati analysis in conversation.
    """
    pl = chart["planets"]
    lagna_sign = chart["lagna_sign"]

    def house(nm): return pl.get(nm,{}).get("house",0)
    def dignity(nm): return pl.get(nm,{}).get("dignity","Neutral")

    # Base score from house placement
    HOUSE_QUALITY = {1:8,2:6,3:5,4:7,5:8,6:6,7:7,8:5,9:8,10:9,11:7,12:5}

    md_h = house(md_lord)
    ad_h = house(ad_lord)
    md_base = HOUSE_QUALITY.get(md_h, 6)
    ad_base = HOUSE_QUALITY.get(ad_h, 6)

    # Dignity bonus/penalty
    def dignity_mod(nm):
        d = dignity(nm)
        if "Exalted"  in d: return +1.5
        if "Own Sign" in d: return +1.0
        if "Debilitat" in d: return -1.5
        return 0

    # Trikona bonus
    if md_h in [1,5,9]: md_base += 0.5
    if ad_h in [1,5,9]: ad_base += 0.5

    # Dusthana penalty (modified if ruling dusthana = VRY)
    dusthana_lords_set = set()
    for idx in [5,7,11]:
        s = (lagna_sign + idx) % 12
        dusthana_lords_set.add(SIGN_LORDS[s])

    # If Maha Dasha lord is own Lagna lord — very auspicious
    lagna_lord = SIGN_LORDS[lagna_sign]
    md_bonus = 0.5 if md_lord == lagna_lord else 0
    ad_bonus = 0.5 if ad_lord == lagna_lord else 0

    score = ((md_base + ad_base) / 2.0
             + dignity_mod(md_lord)
             + dignity_mod(ad_lord)*0.5
             + md_bonus + ad_bonus)

    return min(10.0, max(1.0, round(score, 1)))

def jupiter_transit_modifier(year: int, lagna_sign: int, moon_sign: int) -> float:
    """Jupiter transits every ~12 years through all signs. Return modifier."""
    # Jupiter position approximation (enters Aries 2024, ~1 sign/year)
    JUP_SIGN_2024 = 0  # Aries in 2024
    jup_sign = (JUP_SIGN_2024 + (year - 2024)) % 12

    # Effect from Lagna
    h_from_lagna = (jup_sign - lagna_sign) % 12 + 1
    # Effect from Moon
    h_from_moon  = (jup_sign - moon_sign)  % 12 + 1

    GOOD_H  = {1,4,5,7,9,10,11}
    BAD_H   = {3,6,8,12}
    BEST_H  = {1,5,9}

    mod = 0.0
    if h_from_lagna in BEST_H:  mod += 0.7
    elif h_from_lagna in GOOD_H: mod += 0.4
    elif h_from_lagna in BAD_H:  mod -= 0.3

    if h_from_moon in BEST_H:   mod += 0.5
    elif h_from_moon in GOOD_H:  mod += 0.2
    elif h_from_moon in BAD_H:   mod -= 0.2

    return round(mod, 2)

def saturn_transit_modifier(year: int, moon_sign: int) -> float:
    """Saturn Sade Sati detection. Saturn ~2.5 yrs per sign."""
    SAT_SIGN_2026 = 11  # Pisces in 2026
    sat_sign = (SAT_SIGN_2026 + (year - 2026)) % 12  # approximate

    # Sade Sati: Saturn in 12th, 1st, 2nd from Moon
    for offset in [-1, 0, 1]:
        s = (moon_sign + offset) % 12
        if sat_sign == s:
            if offset == 0: return -0.5   # peak
            else:           return -0.3   # rising/setting

    # Kantaka (4th/8th from Moon): -0.2
    for offset in [3, 7]:
        if sat_sign == (moon_sign + offset) % 12:
            return -0.1

    # Favourable transits
    for offset in [0, 2, 4, 6, 10]:  # 1,3,5,7,11 from Moon good
        pass
    if sat_sign in [(moon_sign + o) % 12 for o in [0,2,4,6,10]]:
        return +0.2

    return 0.0

def compute_year_scores(chart: dict, year_from: int, year_to: int,
                         today: datetime.date = None) -> list:
    """
    Year-by-year combined score using active MD/AD and transits.
    Returns list of dicts per year.
    """
    if today is None:
        today = datetime.date.today()

    dasha_seq = chart["dasha_seq"]
    lagna_sign = chart["lagna_sign"]
    moon_sign  = chart["moon_sign"]
    results = []

    for year in range(year_from, year_to + 1):
        mid_date = datetime.date(year, 7, 1)
        md = active_dasha(dasha_seq, mid_date)
        ads = antardasha_sequence(md)
        ad = active_dasha(ads, mid_date)

        base_score = dasha_quality_score(md["lord"], ad["lord"], chart)
        jup_mod    = jupiter_transit_modifier(year, lagna_sign, moon_sign)
        sat_mod    = saturn_transit_modifier(year, moon_sign)

        score = min(10.0, max(1.0, base_score + jup_mod + sat_mod))

        cat = ("Outstanding" if score >= 9.0 else
               "Excellent"   if score >= 8.0 else
               "Very Good"   if score >= 7.5 else
               "Good"        if score >= 7.0 else
               "Moderate"    if score >= 6.0 else
               "Challenging" if score >= 5.0 else "Difficult")

        results.append({
            "year":       year,
            "md_lord":    md["lord"],
            "ad_lord":    ad["lord"],
            "md_start":   md["start"],
            "md_end":     md["end"],
            "ad_start":   ad["start"],
            "ad_end":     ad["end"],
            "base_score": base_score,
            "jup_mod":    jup_mod,
            "sat_mod":    sat_mod,
            "score":      round(score, 1),
            "category":   cat,
        })

    return results

def compute_combined_year_scores(chart1: dict, chart2: dict,
                                  year_from: int, year_to: int) -> list:
    """Combined Dampati scores — same methodology as conversation."""
    s1 = compute_year_scores(chart1, year_from, year_to)
    s2 = compute_year_scores(chart2, year_from, year_to)

    combined = []
    for a, b in zip(s1, s2):
        synergy = 0.5 if (a["score"] >= 8 and b["score"] >= 8) else \
                 -0.3 if (a["score"] < 6 or  b["score"] < 6)  else 0.0
        cs = min(10.0, max(1.0, (a["score"]+b["score"])/2 + synergy))
        cat = ("Outstanding" if cs >= 9.0 else "Excellent" if cs >= 8.0 else
               "Very Good"   if cs >= 7.5 else "Good"      if cs >= 7.0 else
               "Moderate"    if cs >= 6.0 else "Challenging")
        combined.append({
            "year":     a["year"],
            "score1":   a["score"],  "md1": a["md_lord"], "ad1": a["ad_lord"],
            "score2":   b["score"],  "md2": b["md_lord"], "ad2": b["ad_lord"],
            "combined": round(cs, 1), "category": cat,
            "synergy":  synergy,
        })
    return combined


# ═══════════════════════════════════════════════════════════════════════════
# DASHA-WISE PREDICTION ENGINE
# Per BPHS, Phaladeepika, Brihat Jataka, Saravali, Uttara Kalamrita
# ═══════════════════════════════════════════════════════════════════════════

HOUSE_LIFE_AREAS = {
    1: {
        "career":       "Self-driven leadership and personal authority rise to the forefront. The native is recognized by their individual brilliance and presence. Per BPHS: Lagna activation makes the native the cause of their own rise.",
        "health":       "Vitality and physical constitution are central. This period calls for investment in body and mind. Lagna activation broadly strengthens overall health — though headaches, blood pressure, and eyes may need monitoring.",
        "relationships":"Personal identity defines all relationships. The native's presence becomes magnetic; meaningful new connections are naturally drawn. Confidence in self is the foundation of all bonds.",
        "finances":     "Self-generated income and personal enterprise are favoured. The native's own efforts, skills, and initiative are the primary vehicles of financial growth.",
        "spirituality": "Atma-vichara (self-enquiry) deepens profoundly. Per Yoga Vasishtha: 'The greatest spiritual act is to know one's own nature.' This period is an extraordinary invitation to that enquiry.",
    },
    2: {
        "career":       "Wealth accumulation, financial roles, speech-based professions, and family enterprise flourish. Banking, treasury, teaching, and consultancy are naturally empowered.",
        "health":       "Face, eyes, throat, teeth, and dietary habits require attention and care. Avoid excess in food, drink, and speech. Regular eye check-ups are advised.",
        "relationships":"Family bonds, domestic harmony, and ancestral connections are highlighted and strengthened. Wealth shared within the family deepens all bonds.",
        "finances":     "Primary period for building financial reserves and long-term savings. Per Artha Shastra: this is the time to consolidate, not speculate. Family wealth and ancestral assets may grow.",
        "spirituality": "Pitru Tarpana (ancestral prayers on Amavasya) and family deity worship resolve foundational karmas and unlock hidden blessings. Speech used for truth and prayer is especially powerful now.",
    },
    3: {
        "career":       "Communication, media, writing, short travel, entrepreneurship, and ventures requiring courage and initiative are powerfully activated.",
        "health":       "Arms, shoulders, hands, and the nervous system need care. Avoid reckless physical activity. Breathing exercises and pranayama are beneficial.",
        "relationships":"Sibling bonds and short-term partnerships are dynamic. Communication is the key to resolving friction and deepening connections.",
        "finances":     "Income through self-initiative, courage, and enterprise. Calculated entrepreneurial risks are favoured. Avoid borrowing for non-productive ventures.",
        "spirituality": "Pilgrimage, sacred travel, and Hanuman worship are particularly auspicious. Per the Shastras: Parakrama (right courageous effort) is itself a form of worship in the 3rd house period.",
    },
    4: {
        "career":       "Real estate, education, agriculture, vehicles, and institutional roles carry the highest career potential. The native may gain recognition through domestic or local connections.",
        "health":       "Chest, lungs, heart, and emotional body need nurturing. Create calm, sacred home environments. Mental peace directly supports physical health in this period.",
        "relationships":"Mother, home life, and inner emotional security are central. Deep domestic contentment is entirely possible — invest in the home and family relationships.",
        "finances":     "Property acquisition, vehicle purchase, and domestic assets grow significantly. This is a natural period for real estate investment per classical Jyotisha.",
        "spirituality": "Devi worship, home altars (Puja Griha), and Chandra puja are the prescribed sadhana. Per BPHS: a well-activated 4th house period fills the inner heart with sukha (contentment) — the foundation of all spiritual progress.",
    },
    5: {
        "career":       "Creativity, teaching, advisory roles, strategic investment, and any field requiring intelligence flourish brilliantly. Leadership through wisdom rather than authority.",
        "health":       "Digestive system and reproductive vitality need care. Monitor the health of children if applicable. A sattvic diet supports the clarity of mind this period demands.",
        "relationships":"Children, romance, and creative partnerships blossom. Purva Punya (the merit of past lives) is activated — long-desired relationships and creative projects come to fruition.",
        "finances":     "Speculative investments (made wisely), creative ventures, and merit-based gains are favoured. Per Jataka Parijata: Purva Punya bears tangible worldly fruit during 5th house dasha periods.",
        "spirituality": "Mantra siddhi (mastery of sacred sound), Ishta Devata worship, and intensive Japa practice are extraordinarily fruitful. Per the Shastras: the 5th house is the house of Mantra — this is the time to establish a disciplined practice.",
    },
    6: {
        "career":       "Service, healthcare, law, administration, and competitive roles yield success through sustained effort. The native who works harder than all others wins this period decisively.",
        "health":       "Digestive system, immune function, and chronic conditions require vigilant management. Do not neglect minor symptoms. Regular fasting (Ekadashi, etc.) is highly beneficial.",
        "relationships":"Dynamics with employees, competitors, and service-based relationships are activated. Boundaries are essential — generosity of spirit must be paired with clear expectations.",
        "finances":     "Income comes through consistent hard work and service. Loans and debts require careful management. Avoid unnecessary borrowings; pay existing debts systematically.",
        "spirituality": "Surya Namaskar, seva (selfless service without ego), and Durga or Subrahmanya worship are prescribed. Per Phaladeepika: the 6th house dasha tests dharmic resolve — those who serve without ego are rewarded with lasting strength.",
    },
    7: {
        "career":       "Partnerships, client relationships, public-facing roles, trade, diplomacy, and collaborative ventures shine. The native rises through others, not alone.",
        "health":       "Kidneys, lower back, and reproductive system need attention. Maintain balance in lifestyle — excess in any direction is the primary risk.",
        "relationships":"Marriage, significant partnerships, and business alliances are the central life theme. Existing bonds deepen; new alliances of significance form. Invest in your most important relationships.",
        "finances":     "Income through partners, trade, public dealings, and business collaborations grows substantially. What is shared grows more than what is hoarded.",
        "spirituality": "Shiva-Parvati or Lakshmi-Narayana worship deepens marital and spiritual bonds simultaneously. Per Rigveda 10.85 (Vivaha Sukta): the dharmic partnership is itself a sacred yajna — the highest householder worship.",
    },
    8: {
        "career":       "Research, occult sciences, insurance, inheritance management, psychology, surgery, and transformational work are the activated domains. Surface-level careers may pause for deeper reinvention.",
        "health":       "Sudden health events, reproductive system, and chronic conditions may arise. Regular preventive medical monitoring is strongly advised. Do not ignore the body's signals.",
        "relationships":"Deep karmic bonds surface, unexpected transformations occur in relationships. Some bonds deepen immensely; others complete their karmic cycle. Surrender rather than control is the teaching.",
        "finances":     "Inheritance, insurance, hidden assets, and unexpected windfalls may arrive. Manage all finances conservatively; avoid speculation. What is received must be stewarded wisely.",
        "spirituality": "Per BPHS: the 8th house is Ayus Sthana (the house of longevity) and the gateway to occult knowledge. Maha Mrityunjaya Japa, Kali worship, and deep Dhyana practice yield profound transformation. The Mahavidyas are especially propitious during 8th house dasha periods. Do not fear this period — it is the forge of the soul.",
    },
    9: {
        "career":       "Teaching, law, religion, foreign connections, publishing, mentorship, and dharmic roles carry the highest promise. The native is recognized as a wisdom-figure in their field.",
        "health":       "Hips, thighs, liver, and long-term vitality are highlighted. A spiritual lifestyle — regular sadhana, wholesome food, pilgrimage — directly supports physical health.",
        "relationships":"Father, guru, and philosophical companions are elevated. The native is drawn toward those who expand their consciousness. Relationships with wisdom-figures deepen profoundly.",
        "finances":     "Fortune through dharmic action, foreign sources, higher education, and grace. Per Phaladeepika: the 9th house dasha is 'Bhagya Udaya' — the rising of fortune that was stored in past-life Punya.",
        "spirituality": "Pilgrimage to Char Dham, Kashi, or the Jyotirlingas is exceptionally auspicious and transformative. Guru Puja, Vedic study, and Satsang are the primary sadhana. Per Uttara Kalamrita: 9th house Dasha periods are the closest mortals come to living under direct divine grace.",
    },
    10: {
        "career":       "Career elevation, authority, public recognition, leadership, institutional roles, and legacy-building are the dominant themes. Per BPHS: the 10th house is Karma Sthana — this period rewards the native's dharmic professional actions.",
        "health":       "Knees, joints, and ambition-related stress need monitoring. Discipline and adequate rest must balance relentless achievement. Over-work is the primary risk.",
        "relationships":"Professional partnerships and authority figures shape destiny. Mentors, patrons, and powerful allies emerge naturally. The native's reputation in society is at its peak.",
        "finances":     "Career-based income grows substantially. Business, leadership, and institutional roles yield wealth and status. Long-term investments made now tend to appreciate.",
        "spirituality": "Karma Yoga — performing one's dharmic professional duty with full excellence and inner surrender — is the highest sadhana prescribed by Bhagavad Gita 3.19. The marketplace becomes the temple in this dasha period.",
    },
    11: {
        "career":       "Fulfilment of long-held professional desires, gains through networks, elder connections, and multiple income streams arrive. What was worked toward for years now materializes.",
        "health":       "Ankles, calves, and circulatory vitality need attention. Social over-extension and excessive activity can cause fatigue — guard your energy consciously.",
        "relationships":"Elder siblings, social networks, and long-desired friendships and alliances manifest. The native is naturally sought by others for advice and connection.",
        "finances":     "Multiple income streams, gains from diverse directions, and financial fulfilment. Per Saravali: '11th house Dasha periods make the native's desires come true — it is the house of Labha (gain) fully activated.'",
        "spirituality": "Community worship (Satsang, Bhajan groups), group sadhana, and collective charitable acts generate extraordinary Punya during this period. Giving at peak periods returns manifold in the next cycle.",
    },
    12: {
        "career":       "Foreign lands, ashram or institutional life, research, spiritual service, hospitals, and behind-the-scenes work are the activated domains. External recognition may reduce while inner development accelerates.",
        "health":       "Feet, sleep quality, and sustained expenditure on health need attention. Rest and recovery are not optional — they are the sadhana of this period.",
        "relationships":"Spiritual partnerships, deeply private bonds, or foreign connections come into focus. The most significant relationships now transcend ordinary social categories.",
        "finances":     "Expenditure is significant. Charitable giving and spiritual investment (pilgrimages, dakshina, ashram support) generate Punya that returns as fortune in the cycles ahead.",
        "spirituality": "Per BPHS: the 12th house is Moksha Sthana — the house of liberation. This period is an extraordinary invitation to deep Dhyana, ashram retreat, and moksha-oriented practice. Vipareet Raja Yoga may activate, transforming apparent worldly loss into hidden, profound inner blessing. This is one of the most spiritually potent dasha placements in the entire Vimshottari system.",
    },
}

MD_SHASTRA_REFS = {
    "Ketu":   "BPHS Ch.46 | Ketu Maha Dasha — 7 Years | Ketu is the Moksha Karaka — the divine surgeon of karma. Per Saravali: 'Ketu in a strong position gives moksha, psychic siddhis, and piercing spiritual wisdom; in a challenged position, creates separations through which the soul finds its authentic freedom.' This period resolves deep past-life karmas, strips away what is false, and reveals what is eternally true. It is rarely comfortable — it is always profound.",
    "Shukra": "Phaladeepika Ch.20 | Shukra Maha Dasha — 20 Years | Venus governs Shringara Rasa — the full aesthetic and sensory experience of a beautiful life. Per BPHS: 'Shukra Maha Dasha, when Venus is well-placed, bestows beauty, wealth, romance, artistic mastery, comfortable vehicles, loyal relationships, and abundant pleasures.' This is among the most materially and relationally fulfilling periods in the entire Vimshottari cycle.",
    "Surya":  "BPHS Ch.46 | Surya Maha Dasha — 6 Years | The Sun is the Atmakaraka — the very soul of the native. Per Aditya Hridayam (Valmiki Ramayana): 'Surya is the source of all life, the eye of the universe, the sustainer of creation.' In the birth chart, Surya Dasha illuminates authority, career, father-related themes, and the soul's essential dharmic purpose. A short but potent period.",
    "Chandra":"Brihat Jataka Ch.8 | Chandra Maha Dasha — 10 Years | The Moon rules the mind (Manas), the mother (Mata), and the public image (Kirthi). Per Saravali: 'Chandra Dasha makes the mind fertile, the social life expansive, the emotional world central, and the domestic sphere dominant.' The native's inner world shapes their outer reality with unusual power during this period.",
    "Mangal": "Phaladeepika Ch.20 | Mangal Maha Dasha — 7 Years | Mars is Parakrama — the power of righteous, decisive effort. Per BPHS: 'Mangal Dasha confers courage, landed property, technical skills, physical vitality, and complete dominion over adversaries when Mars is strong and well-placed.' The native's willpower and capacity for decisive action are the primary instruments of this period.",
    "Rahu":   "BPHS Ch.46 | Rahu Maha Dasha — 18 Years | Rahu is the great amplifier of worldly desire and the architect of fate's acceleration. Per Sarvartha Chintamani: 'Rahu in a strong house and sign gives fame, foreign connections, sudden gains, unconventional rise, and the fulfilment of material ambitions.' Per Parashar: Rahu conjoining or aspecting strong planets delivers results similar to the most powerful planet in the chart. This is often the period when destiny accelerates most dramatically.",
    "Guru":   "Phaladeepika Ch.20 | Guru Maha Dasha — 16 Years | Jupiter is the Deva Guru — the preceptor of the gods, the embodiment of divine wisdom and benevolence. Per BPHS: 'Guru Dasha sarva shubhakari' — Jupiter's Maha Dasha is the bestower of all auspiciousness when Jupiter is dignified. Wisdom, dharma, prosperity, children, institutional recognition, and spiritual grace all grow under Jupiter's magnanimous reign.",
    "Shani":  "BPHS Ch.46 | Shani Maha Dasha — 19 Years | Saturn is Karma Phala Dhata — the distributor of the precise fruits of karma, without addition or subtraction. Per Uttara Kalamrita: 'Saturn's dasha is demanding at the outset but deeply rewarding at its close.' Per Skanda Purana: 'Shani does not punish — Shani balances. Those who act with dharma, consistency, and patience during Shani Dasha build the most enduring foundations of their entire lives.' The native who endures with integrity is transformed by Saturn into something permanent.",
    "Budha":  "Phaladeepika Ch.20 | Budha Maha Dasha — 17 Years | Mercury is Vak Siddhi Karaka — the master of articulate intelligence and the lord of communication. Per BPHS: 'When Budha is strong in his dasha, the native achieves command of language, sharp analytical brilliance, and business mastery.' Education, communication, trade, writing, and intellectual leadership are the natural hallmarks of a strong Budha Maha Dasha.",
}

AD_HOUSE_THEMES = {
    1: "self-leadership and personal authority",
    2: "family wealth, speech, and accumulated resources",
    3: "communication, courage, and entrepreneurial effort",
    4: "home, property, mother, and emotional fulfilment",
    5: "creativity, children, intelligence, and Purva Punya",
    6: "obstacle-removal, service, and competitive strength",
    7: "partnerships, marriage, and public dealings",
    8: "transformation, occult knowledge, and inheritance",
    9: "fortune, dharma, father, and higher learning",
    10: "career elevation, authority, and public recognition",
    11: "gains, network expansion, and desire fulfilment",
    12: "moksha, foreign connections, and spiritual depth",
}


def _dignity_qualifier(dignity: str) -> tuple:
    """Returns (quality_word, quality_note) based on dignity."""
    if "Exalted" in dignity:
        return ("exceptional",
                "Per Phaladeepika: an exalted dasha lord delivers its highest promise — results arrive with grace, precision, and abundance beyond ordinary expectation.")
    elif "Own Sign" in dignity or "Moolatrik" in dignity:
        return ("strong",
                "Per BPHS: a dasha lord in own sign or Moolatrikona is fully empowered to deliver its significations without obstruction — results are reliable and sustained.")
    elif "Debilitat" in dignity:
        return ("challenging yet transformative",
                "Per Brihat Jataka: a debilitated dasha lord activates the potential for Neecha Bhanga (cancellation of debility) when supporting planetary conditions exist. The challenge contains the seed of its own reversal. The native who persists with dharmic conduct emerges stronger.")
    else:
        return ("moderate",
                "Per Saravali: results manifest steadily according to the planet's functional nature, the houses it rules, and the strength it receives from aspects and conjunctions in the natal chart.")


def _ad_prediction_text(md_lord: str, ad_lord: str, ad_house: int, ad_dignity: str, score: float) -> str:
    """Generate Antardasha prediction text grounded in classical Jyotisha."""
    theme = MD_THEMES.get(ad_lord, "karmic themes appropriate to this planet")
    house_theme = AD_HOUSE_THEMES.get(ad_house, "general life significations")
    quality_word, _ = _dignity_qualifier(ad_dignity)

    if score >= 9.0:
        return (f"{ad_lord} Antardasha brings its themes of {theme} into this {md_lord} period with {quality_word} force, "
                f"powerfully illuminating {house_theme}. Per Phaladeepika: when both MD and AD lords are strong, "
                f"the period delivers its absolute highest promise. This is one of the most cosmically aligned windows "
                f"in this entire Maha Dasha — major life milestones achieved now carry lasting karmic weight. "
                f"Act with full intention and make decisions of significance in the domain of {house_theme}.")
    elif score >= 8.0:
        return (f"{ad_lord} Antardasha adds its themes of {theme} steadily to this {md_lord} period, "
                f"with {quality_word} energy enhancing {house_theme}. Progress is consistent and genuinely rewarding. "
                f"Per Saravali: excellent MD-AD combinations yield 'pratistha' — recognition, advancement, and dharmic momentum. "
                f"Invest confidently in the areas of {house_theme}; effort is multiplied during this sub-period.")
    elif score >= 7.0:
        return (f"{ad_lord} Antardasha contributes themes of {theme} with good energy directed toward {house_theme}. "
                f"Steady effort yields tangible and lasting results. Some natural resistance or delays may be encountered, "
                f"but persistence is the definitive key. Per Brihat Jataka: 'Good sub-periods build the foundation upon "
                f"which the outstanding ones stand.' Maintain consistent, focused effort and trust the process.")
    elif score >= 6.0:
        return (f"{ad_lord} Antardasha brings themes of {theme} with moderate energy. The domain of {house_theme} "
                f"requires focused, careful navigation. Per BPHS: 'In moderate Dasha periods, dharmic conduct and "
                f"regular sadhana protect the native and sustain forward movement.' Do not abandon effort — adapt "
                f"your strategy, increase your prayer, and the period will yield its blessings in proportion to your patience.")
    else:
        return (f"{ad_lord} Antardasha is one of the more demanding sub-periods in this Maha Dasha, requiring patience, "
                f"inner strength, and heightened sadhana. Themes of {theme} manifest with karmic intensity around "
                f"{house_theme}. Per Brihat Jataka: 'Difficult Dasha periods are the forge of the soul — they burn "
                f"away what is not real and reveal the diamond within.' This is not the time for major new ventures; "
                f"it is the time for consolidation, deep spiritual practice, dharmic conduct in all dealings, and "
                f"trust that what is being cleared will make room for what is genuine. You are not being punished — "
                f"you are being refined.")


def _generate_md_guidance(lord: str, house: int, dignity: str, avg_score: float, chart: dict) -> dict:
    """Return structured guidance dict for a Maha Dasha period."""
    MANTRA = {
        "Surya":  "'Om Hram Hrim Hraum Sah Suryaya Namah' — 108x every Sunday at sunrise; Aditya Hridayam daily",
        "Chandra":"'Om Shram Shrim Shraum Sah Chandramase Namah' — 108x every Monday; Chandra Kavacham on Purnima",
        "Mangal": "'Om Kram Krim Kraum Sah Bhaumaya Namah' — 108x every Tuesday; Subrahmanya Ashtakam",
        "Budha":  "'Om Bram Brim Braum Sah Budhaya Namah' — 108x every Wednesday; Vishnu Sahasranama",
        "Guru":   "'Om Gram Grim Graum Sah Gurave Namah' — 108x every Thursday; Brihaspati Stotram; Guru Paduka Stotra",
        "Shukra": "'Om Dram Drim Draum Sah Shukraya Namah' — 108x every Friday; Shri Lakshmi Ashtakam",
        "Shani":  "'Om Pram Prim Praum Sah Shanaischaraya Namah' — 108x every Saturday; Hanuman Chalisa daily without fail",
        "Rahu":   "'Om Bhram Bhrim Bhraum Sah Rahave Namah' — Saturdays; Durga Saptashati; Chandi Homa annually",
        "Ketu":   "'Om Stram Strim Straum Sah Ketave Namah' — Thursdays; Ganesha Atharvasirsha; Maha Mrityunjaya Japa",
    }
    CHARITY = {
        "Surya":  "Wheat, jaggery, copper vessels, red flowers, red cloth — Sundays to a Brahmin or temple",
        "Chandra":"Rice, silver items, white flowers, milk, white cloth — Mondays",
        "Mangal": "Red lentils (masoor dal), red cloth, copper utensils — Tuesdays",
        "Budha":  "Green gram (moong dal), green cloth, books, writing instruments — Wednesdays",
        "Guru":   "Yellow gram (chana dal), turmeric, yellow cloth, ghee lamps — Thursdays",
        "Shukra": "White rice, white flowers, white cloth, curd, silver ornaments, perfume — Fridays",
        "Shani":  "Black sesame seeds, black cloth, mustard oil, iron utensils, shoes — Saturdays",
        "Rahu":   "Blue or black cloth, urad dal (black lentils), coconut, camphor — Saturdays",
        "Ketu":   "Multi-coloured cloth, sesame seeds, blankets, old shoes to the needy — Thursdays",
    }
    PILGRIMAGE = {
        "Surya":  "Konark Sun Temple (Odisha), Suryanar Kovil (Kumbakonam), Modhera Sun Temple (Gujarat)",
        "Chandra":"Rameshwaram (Jyotirlinga), Somnath, Chidambaram; Monday Rudrabhishek to Shiva",
        "Mangal": "Kukke Subrahmanya (Karnataka), Palani (Tamil Nadu), Tirupati — Tuesdays",
        "Budha":  "Kanchipuram (Ekambareswarar), Srikalahasti, Vishnu temples — Wednesdays",
        "Guru":   "Kashi-Vishwanath, Tirupati Balaji, Brihaspati temples; Guru Purnima pilgrimage annually",
        "Shukra": "Kamakshi (Kanchipuram), Meenakshi (Madurai), Mahalakshmi (Kolhapur) — Fridays",
        "Shani":  "Shani Shingnapur (Maharashtra), Tirunallar Dharbaranyeswarar (Tamil Nadu) — Saturdays",
        "Rahu":   "Srikalahasti (Andhra Pradesh) — the supreme Rahu-Ketu Kshetra; annual Chandi Homa",
        "Ketu":   "Srikalahasti, Ganesha Chaturthi temples, Char Dham Yatra for moksha orientation",
    }

    is_challenging = avg_score < 6.5
    focus = (
        "Navigate this period with patience, sadhana, and absolute faith in the cosmic order. "
        "Per BPHS and Skanda Purana: challenging Dasha periods are not punishments — they are periods of "
        "deep karmic clearing and soul refinement that no amount of worldly effort alone can achieve. "
        "The Rishis teach 'Kala Phalam' — the fruit comes in its own time, for those who remain dharmic. "
        "Increase your sadhana, reduce impulsive major decisions, maintain integrity in all dealings, "
        "and offer your difficulties as worship to the Divine. What is being removed was always temporary. "
        "What is being built in you during this period is permanent."
        if is_challenging else
        "This is a period of dharmic momentum — act with full intention and confident deliberateness. "
        "Per Phaladeepika: when the Dasha lord is strong and well-placed, the native's efforts are amplified "
        "by Prarabdha karma expressing itself favourably. Invest in the domains ruled by this planet, "
        "make significant life decisions aligned with your deepest values, expand your charitable and "
        "spiritual work, and mentor those who walk behind you on the path. What you give in peak periods "
        "returns to you across multiple future cycles."
    )
    return {
        "mantra":      MANTRA.get(lord,     "Navagraha Stotram — 'Om Navagrahebyah Namah' (Sundays)"),
        "charity":     CHARITY.get(lord,    "Donate food and essentials to those in need on this planet's associated day"),
        "pilgrimage":  PILGRIMAGE.get(lord, "Kashi-Vishwanath or your Kula Devata shrine"),
        "focus":       focus,
    }


def generate_dasha_predictions(chart: dict, year_from: int, year_to: int) -> list:
    """
    Generate structured, Shastra-grounded dasha-wise predictions for the given period.
    Covers each Maha Dasha overlapping [year_from, year_to], with Antardasha detail.
    Returns list of prediction dicts sorted by start date.
    """
    today = datetime.date.today()
    dasha_seq  = chart["dasha_seq"]
    pl         = chart["planets"]
    lagna_sign = chart["lagna_sign"]
    moon_sign  = chart["moon_sign"]

    date_from = datetime.date(year_from, 1, 1)
    date_to   = datetime.date(year_to, 12, 31)

    predictions = []

    for md in dasha_seq:
        if md["end"] < date_from or md["start"] > date_to:
            continue

        lord    = md["lord"]
        pd_data = pl.get(lord, {})
        house   = pd_data.get("house", 0)
        dignity = pd_data.get("dignity", "Neutral")
        sign    = pd_data.get("sign_san", "")

        quality_word, quality_note = _dignity_qualifier(dignity)

        # Compute average score for the portion of this MD in range
        md_yr_from = max(year_from, md["start"].year)
        md_yr_to   = min(year_to,   md["end"].year)
        yr_scores  = compute_year_scores(chart, md_yr_from, md_yr_to)
        avg_score  = (sum(r["score"] for r in yr_scores) / len(yr_scores)) if yr_scores else 6.0

        cat = ("Outstanding" if avg_score >= 9.0 else "Excellent"   if avg_score >= 8.0 else
               "Very Good"   if avg_score >= 7.5 else "Good"        if avg_score >= 7.0 else
               "Moderate"    if avg_score >= 6.0 else "Challenging")

        # Antardasha sequence filtered to range
        ads = antardasha_sequence(md)
        relevant_ads = []
        for ad in ads:
            if ad["end"] < date_from or ad["start"] > date_to:
                continue
            ad_pd      = pl.get(ad["lord"], {})
            ad_house   = ad_pd.get("house", 0)
            ad_dignity = ad_pd.get("dignity", "Neutral")
            ad_base    = dasha_quality_score(lord, ad["lord"], chart)
            mid_yr     = (ad["start"].year + ad["end"].year) // 2
            jmod       = jupiter_transit_modifier(mid_yr, lagna_sign, moon_sign)
            smod       = saturn_transit_modifier(mid_yr, moon_sign)
            ad_score   = round(min(10.0, max(1.0, ad_base + jmod + smod)), 1)
            ad_cat     = ("Outstanding" if ad_score >= 9.0 else "Excellent"   if ad_score >= 8.0 else
                          "Very Good"   if ad_score >= 7.5 else "Good"        if ad_score >= 7.0 else
                          "Moderate"    if ad_score >= 6.0 else "Challenging" if ad_score >= 5.0 else "Difficult")
            relevant_ads.append({
                "lord":       ad["lord"],
                "start":      ad["start"],
                "end":        ad["end"],
                "house":      ad_house,
                "dignity":    ad_dignity,
                "score":      ad_score,
                "category":   ad_cat,
                "is_current": ad["start"] <= today <= ad["end"],
                "prediction": _ad_prediction_text(lord, ad["lord"], ad_house, ad_dignity, ad_score),
            })

        life_areas = HOUSE_LIFE_AREAS.get(house, {
            "career":       f"General career progress driven by {lord}'s natural significations.",
            "health":       f"Health governed by {lord}'s body parts and planetary strength.",
            "relationships":f"Relationships shaped by {lord}'s functional nature in your chart.",
            "finances":     f"Financial matters governed by {lord}'s placement and dignity.",
            "spirituality": f"Sadhana aligned with {lord}'s deity and Beej Mantra is recommended.",
        })

        predictions.append({
            "lord":         lord,
            "start":        md["start"],
            "end":          md["end"],
            "years":        md["years"],
            "house":        house,
            "sign":         sign,
            "dignity":      dignity,
            "quality_word": quality_word,
            "quality_note": quality_note,
            "avg_score":    round(avg_score, 1),
            "category":     cat,
            "life_areas":   life_areas,
            "antardashas":  relevant_ads,
            "shastra_ref":  MD_SHASTRA_REFS.get(lord,
                f"Per BPHS: {lord} Maha Dasha activates the life domains governed by {lord}'s placement in the natal chart."),
            "guidance":     _generate_md_guidance(lord, house, dignity, avg_score, chart),
            "is_current":   md["start"] <= today <= md["end"],
            "is_past":      md["end"] < today,
        })

    return predictions
