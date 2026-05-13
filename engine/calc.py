"""
JYOTISHA CALCULATION ENGINE
Exact same logic used throughout this conversation:
- Julian Day computation (standard algorithm)
- Sun: L0 + equation of center (Meeus Ch.25)
- Moon: ELP2000-82 subset (16 periodic terms, same as conversation)
- Planets: Mean longitude + equation of center (Meeus simplified)
- Lagna: GMST → LST → Ascendant formula (same as conversation)
- Lahiri Ayanamsha interpolated per year
- Houses: Equal house from Lagna
- Vimshottari Dasha: From Nakshatra balance
"""

import math
import datetime

# ── SIGN DATA ────────────────────────────────────────────────────────────────
SIGNS_SAN = [
    "Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
    "Tula","Vrischika","Dhanu","Makara","Kumbha","Meena"
]
SIGNS_EN = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]
SIGN_LORDS = ["Mangal","Shukra","Budha","Chandra","Surya","Budha",
              "Shukra","Mangal","Guru","Shani","Shani","Guru"]
SIGN_ELEMENT = ["Fire","Earth","Air","Water","Fire","Earth",
                "Air","Water","Fire","Earth","Air","Water"]
SIGN_QUALITY  = ["Movable","Fixed","Dual","Movable","Fixed","Dual",
                 "Movable","Fixed","Dual","Movable","Fixed","Dual"]

NAKSHATRAS = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
    "Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni",
    "Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
    "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha",
    "Purva Bhadrapada","Uttara Bhadrapada","Revati"
]
NAK_LORDS = [
    "Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru","Shani","Budha",
    "Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru","Shani","Budha",
    "Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru","Shani","Budha"
]
NAK_DEITY = [
    "Ashwini Kumaras","Yama","Agni","Brahma","Soma","Rudra","Aditi","Brihaspati","Naga",
    "Pitrus","Bhaga","Aryaman","Savitar","Tvashtar","Vayu","Indra-Agni","Mitra","Indra",
    "Nirriti","Apas","Vishvedevas","Vishnu","Eight Vasus","Varuna","Aja Ekapada","Ahir Budhnya","Pushan"
]
NAK_SYMBOL = [
    "Horse head","Yoni/Vagina","Razor/Flame","Cart/Ox","Deer head","Teardrop",
    "Bow/Quiver","Flower/Arrow","Coiled snake","Royal throne","Bed/Hammock","Fig tree",
    "Palm/Hand","Pearl/Lamp","Coral/Sword","Potter's wheel","Lotus/Umbrella","Circular amulet",
    "Roots/Elephant goad","Elephant tusk","Elephant tusk","Ear/Three footprints","Drum/Flute","Empty circle",
    "Sword/Front legs of funeral cot","Serpent in water","Fish/Drum"
]

DASHA_ORDER  = ["Ketu","Shukra","Surya","Chandra","Mangal","Rahu","Guru","Shani","Budha"]
DASHA_YEARS  = {"Ketu":7,"Shukra":20,"Surya":6,"Chandra":10,"Mangal":7,
                "Rahu":18,"Guru":16,"Shani":19,"Budha":17}
TOTAL_DASHA  = 120

# Lahiri Ayanamsha table (year → degrees) — same values used in conversation
AYANAMSHA_TABLE = {
    1940: 22.4600, 1945: 22.7100, 1950: 22.9700, 1955: 23.2200,
    1960: 23.3500, 1965: 23.4700, 1970: 23.5500, 1975: 23.6600,
    1980: 23.5400, 1982: 23.5653, 1983: 23.5800, 1984: 23.6167,
    1985: 23.6300, 1990: 23.7000, 1995: 23.8000, 2000: 23.8530,
    2005: 24.0000, 2010: 24.1300, 2015: 24.2000, 2020: 24.3200,
    2025: 24.4000, 2030: 24.5000,
}

def get_ayanamsha(year: float) -> float:
    """Interpolate Lahiri Ayanamsha for given year."""
    years = sorted(AYANAMSHA_TABLE.keys())
    if year <= years[0]:
        return AYANAMSHA_TABLE[years[0]]
    if year >= years[-1]:
        return AYANAMSHA_TABLE[years[-1]]
    for i in range(len(years)-1):
        y1, y2 = years[i], years[i+1]
        if y1 <= year <= y2:
            t = (year - y1) / (y2 - y1)
            return AYANAMSHA_TABLE[y1] + t*(AYANAMSHA_TABLE[y2]-AYANAMSHA_TABLE[y1])
    return 23.85

def julian_day(year: int, month: int, day: int, ut_hours: float) -> float:
    """Standard Julian Day Number calculation."""
    A = int((14 - month) / 12)
    Yp = year + 4800 - A
    Mp = month + 12*A - 3
    JDN = (day + int((153*Mp+2)/5) + 365*Yp +
           int(Yp/4) - int(Yp/100) + int(Yp/400) - 32045)
    return JDN + (ut_hours - 12.0) / 24.0

def T_from_JD(jd: float) -> float:
    """Julian centuries from J2000.0"""
    return (jd - 2451545.0) / 36525.0

def norm360(x: float) -> float:
    """Normalise to [0, 360)"""
    return x % 360.0

def calc_sun(T: float) -> float:
    """Tropical Sun longitude — same Meeus formula used in conversation."""
    L0 = 280.46646 + 36000.76983*T + 0.0003032*T*T
    M  = 357.52911 + 35999.05029*T - 0.0001537*T*T
    Mr = math.radians(norm360(M))
    C  = ((1.914602 - 0.004817*T - 0.000014*T*T)*math.sin(Mr)
          + (0.019993 - 0.000101*T)*math.sin(2*Mr)
          + 0.000289*math.sin(3*Mr))
    return norm360(L0 + C)

def calc_moon(T: float) -> tuple:
    """Moon tropical longitude using ELP2000-82 16-term subset.
    Returns (longitude, Om) — same as conversation."""
    Lm = 218.3165 + 481267.8813*T
    Mm = 134.9634 + 477198.8676*T
    Ms = 357.5291 + 35999.0503*T
    F  = 93.2721  + 483202.0175*T
    Om = 125.0445 - 1934.1362*T

    Lm_r = math.radians(norm360(Lm))
    Mm_r = math.radians(norm360(Mm))
    Ms_r = math.radians(norm360(Ms))
    F_r  = math.radians(norm360(F))
    D    = math.radians(norm360(Lm - Ms))

    dL  =  6.288774*math.sin(Mm_r)
    dL +=  1.274027*math.sin(2*D - Mm_r)
    dL +=  0.658314*math.sin(2*D)
    dL +=  0.213618*math.sin(2*Mm_r)
    dL -= 0.185116*math.sin(Ms_r)
    dL -= 0.114332*math.sin(2*F_r)
    dL +=  0.058793*math.sin(2*D - 2*Mm_r)
    dL +=  0.057066*math.sin(2*D - Ms_r - Mm_r)
    dL +=  0.053322*math.sin(2*D + Mm_r)
    dL +=  0.045758*math.sin(2*D - Ms_r)
    dL -= 0.040923*math.sin(Ms_r - Mm_r)
    dL -= 0.034720*math.sin(D)
    dL -= 0.030383*math.sin(Ms_r + Mm_r)
    dL +=  0.015327*math.sin(2*D - 2*F_r)
    dL -= 0.012528*math.sin(2*F_r + Mm_r)
    dL +=  0.010980*math.sin(2*F_r - Mm_r)

    return norm360(Lm + dL), norm360(Om)

# ── ACCURATE PLANETARY POSITIONS (Meeus Ch.25/31 + VSOP87 low-precision) ────
# Orbital elements at J2000.0 referred to mean ecliptic & equinox of J2000.0
# Format: (L0, L1, a, e0, e1, i0, i1, Om0, Om1, w0, w1)
# L = mean longitude (deg), a = semi-major axis (AU),
# e = eccentricity, i = inclination (deg),
# Om = longitude of ascending node (deg),
# w  = longitude of perihelion (deg)
# Rates are per Julian century T.  Sources: Meeus Table 31.a + USNO

_ORB = {
    # planet:  L0,           L1,              a,           e0,          e1,
    #          i0,         i1,           Om0,        Om1,         w0,          w1
    "Mercury": (252.250906, 149472.6746358, 0.38709831,  0.20563175,  0.000020407,
                7.004986,  -0.0059516,    48.330893,  -0.1254229,  77.456119,   0.1588643),
    "Venus":   (181.979801,  58517.8156760, 0.72332982,  0.00677188, -0.000047766,
                3.394662,  -0.0008568,    76.679920,  -0.2780080, 131.563703,   0.0048746),
    "Earth":   (100.466457,  35999.3728565, 1.000001018, 0.01670862, -0.000042037,
                0.0,        0.0,           0.0,         0.0,        102.937348,  0.3225557),
    "Mars":    (355.433000,  19140.2993313, 1.52366231,  0.09341233, -0.000090484,
                1.849726,  -0.0006011,    49.558093,  -0.2950250, 336.060234,   0.4439016),
    "Jupiter": ( 34.351519,   3034.9056606, 5.20248019,  0.04853590,  0.000016322,
                1.303270,  -0.0054966,   100.292990,   0.1334985,  14.331172,   0.2155209),
    "Saturn":  ( 50.077444,   1222.1138488, 9.54149883,  0.05550825, -0.000346641,
                2.488878,  -0.0037363,   113.665503,  -0.2566722,  93.056787,   0.5665496),
}


def _kepler(M_deg: float, e: float) -> float:
    """Solve Kepler's equation M = E - e*sin(E); return true anomaly (degrees)."""
    M = math.radians(M_deg % 360.0)
    E = M  # initial guess
    for _ in range(50):
        dE = (M - E + e * math.sin(E)) / (1.0 - e * math.cos(E))
        E += dE
        if abs(dE) < 1e-10:
            break
    # True anomaly
    v = 2.0 * math.atan2(
        math.sqrt(1 + e) * math.sin(E / 2),
        math.sqrt(1 - e) * math.cos(E / 2)
    )
    return math.degrees(v)


def _helio_xyz(T: float, planet: str) -> tuple:
    """Return heliocentric ecliptic rectangular coordinates (x, y, z) in AU."""
    L0, L1, a, e0, e1, i0, i1, Om0, Om1, w0, w1 = _ORB[planet]
    L   = norm360(L0 + L1 * T)
    e   = e0 + e1 * T
    i   = math.radians(i0 + i1 * T)
    Om  = math.radians(norm360(Om0 + Om1 * T))
    w   = math.radians(norm360(w0  + w1  * T))
    M   = norm360(L - math.degrees(w))
    v   = math.radians(_kepler(M, e))
    r   = a * (1 - e * e) / (1 + e * math.cos(v))
    u   = v + (w - Om)  # argument of latitude = true_anomaly + argument_of_perihelion

    # Heliocentric ecliptic rectangular
    x = r * (math.cos(Om) * math.cos(u) - math.sin(Om) * math.sin(u) * math.cos(i))
    y = r * (math.sin(Om) * math.cos(u) + math.cos(Om) * math.sin(u) * math.cos(i))
    z = r * math.sin(u) * math.sin(i)
    return x, y, z


def _geo_ecliptic_lon(T: float, planet: str) -> float:
    """Geocentric ecliptic longitude (tropical degrees) via helio→geo conversion."""
    xp, yp, zp = _helio_xyz(T, planet)
    xe, ye, ze = _helio_xyz(T, "Earth")
    dx, dy, dz = xp - xe, yp - ye, zp - ze
    lam = math.degrees(math.atan2(dy, dx))
    return norm360(lam)


def calc_mercury(T: float, sun_trop: float = 0, M_sun: float = 0) -> float:
    return _geo_ecliptic_lon(T, "Mercury")

def calc_venus(T: float, sun_trop: float = 0, M_sun: float = 0) -> float:
    return _geo_ecliptic_lon(T, "Venus")

def calc_mars(T: float) -> float:
    return _geo_ecliptic_lon(T, "Mars")

def calc_jupiter(T: float) -> float:
    return _geo_ecliptic_lon(T, "Jupiter")

def calc_saturn(T: float) -> float:
    return _geo_ecliptic_lon(T, "Saturn")

def calc_lagna(T: float, jd: float, ut_hours: float, lat: float, lon: float) -> float:
    """Tropical Ascendant using GMST → LST → atan2 formula."""
    T0 = (int(jd) + 0.5 - 2451545.0) / 36525.0
    GMST_sec = 24110.54841 + 8640184.812866*T0 + 0.093104*T0*T0
    GMST_h   = (GMST_sec / 3600.0) % 24.0
    LST      = (GMST_h + ut_hours + lon/15.0) % 24.0
    RAMC     = LST * 15.0
    eps      = 23.439291 - 0.013004*T
    RAMC_r   = math.radians(RAMC)
    eps_r    = math.radians(eps)
    lat_r    = math.radians(lat)
    asc = math.degrees(math.atan2(
        math.cos(RAMC_r),
        -(math.sin(RAMC_r)*math.cos(eps_r) + math.tan(lat_r)*math.sin(eps_r))
    )) % 360
    return asc

def tropical_to_sidereal(trop: float, ayan: float) -> float:
    return norm360(trop - ayan)

def sign_from_sid(sid: float) -> int:
    return int(sid / 30)

def deg_in_sign(sid: float) -> float:
    return sid % 30.0

def house_from_lagna(planet_sid: float, lagna_sid: float) -> int:
    lagna_start = sign_from_sid(lagna_sid) * 30.0
    diff = norm360(planet_sid - lagna_start)
    return int(diff / 30) + 1

def get_nakshatra(moon_sid: float) -> tuple:
    nak_span = 360.0 / 27.0
    nak_num  = int(moon_sid / nak_span)
    nak_deg  = moon_sid % nak_span
    pada     = int(nak_deg / (nak_span/4)) + 1
    elapsed  = nak_deg / nak_span
    return nak_num, pada, elapsed

def get_paksha(tithi: int) -> str:
    if 1 <= tithi <= 15:
        return "Shukla Paksha (bright half of the lunar month)"
    return "Krishna Paksha (dark half of the lunar month)"

def get_tithi_name(tithi: int) -> str:
    if tithi == 15:
        return "Purnima (Full Moon)"
    if tithi == 30:
        return "Amavasya (New Moon)"
    if 1 <= tithi <= 15:
        return f"Shukla {tithi} Tithi"
    return f"Krishna {tithi - 15} Tithi"


def dasha_balance_and_sequence(moon_sid: float, birth_date: datetime.date) -> list:
    """
    Returns list of dicts: {lord, start, end, years}
    Same algorithm: balance = (1 - elapsed_fraction) * lord_years
    """
    nak_num, pada, elapsed = get_nakshatra(moon_sid)
    start_lord  = NAK_LORDS[nak_num]
    start_idx   = DASHA_ORDER.index(start_lord)
    balance_yrs = (1.0 - elapsed) * DASHA_YEARS[start_lord]

    result = []
    cur = birth_date
    for i in range(9):
        lord = DASHA_ORDER[(start_idx + i) % 9]
        yrs  = balance_yrs if i == 0 else DASHA_YEARS[lord]
        end  = cur + datetime.timedelta(days=yrs * 365.25)
        result.append({"lord": lord, "start": cur, "end": end, "years": round(yrs, 2)})
        cur = end
    return result

def antardasha_sequence(md: dict) -> list:
    """Compute all 9 Antardashas within a Maha Dasha."""
    md_lord = md["lord"]
    md_yrs  = (md["end"] - md["start"]).days / 365.25
    start_idx = DASHA_ORDER.index(md_lord)
    result = []
    cur = md["start"]
    for i in range(9):
        al = DASHA_ORDER[(start_idx + i) % 9]
        ad_days = int(md_yrs * DASHA_YEARS[al] / TOTAL_DASHA * 365.25)
        end = cur + datetime.timedelta(days=ad_days)
        result.append({"lord": al, "start": cur, "end": end})
        cur = end
    return result

def active_dasha(dasha_seq: list, on_date: datetime.date) -> dict:
    for d in dasha_seq:
        if d["start"] <= on_date <= d["end"]:
            return d
    return dasha_seq[-1]

# ── EXALTATION / DEBILITATION / OWN SIGN ────────────────────────────────────
EXALTATION   = {"Surya":0,"Chandra":1,"Mangal":9,"Budha":5,"Guru":3,
                "Shukra":11,"Shani":6}   # sign index
DEBILITATION = {"Surya":6,"Chandra":7,"Mangal":3,"Budha":11,"Guru":9,
                "Shukra":5,"Shani":0}
OWN_SIGNS    = {"Surya":[4],"Chandra":[3],"Mangal":[0,7],"Budha":[2,5],
                "Guru":[8,11],"Shukra":[1,6],"Shani":[9,10]}

def planet_dignity(planet_name: str, sign_idx: int) -> str:
    ex = EXALTATION.get(planet_name)
    db = DEBILITATION.get(planet_name)
    own = OWN_SIGNS.get(planet_name, [])
    if ex == sign_idx:    return "Exalted (Uccha)"
    if db == sign_idx:    return "Debilitated (Neecha)"
    if sign_idx in own:   return "Own Sign (Swagrahi)"
    return "Neutral"

# ── YOGA DETECTION ───────────────────────────────────────────────────────────
def detect_yogas(planets: dict, lagna_sign: int) -> list:
    """
    Detect classical yogas. planets = {name: {"sign":int, "house":int, "sid":float}}
    Same yogas identified in the conversation reports.
    """
    yogas = []
    p = planets

    def sign(nm): return p[nm]["sign"] if nm in p else -1
    def house(nm): return p[nm]["house"] if nm in p else -1
    def same_house(a,b): return house(a)==house(b) and house(a)>0

    # Budhaditya Yoga
    if same_house("Surya","Budha"):
        yogas.append({
            "name":"Budhaditya Yoga",
            "planets":"Sun + Mercury conjunction",
            "house": house("Surya"),
            "description":"Per Phaladeepika: exceptional intelligence, eloquence, administrative acumen, and recognition in scholarly pursuits.",
            "strength":"Strong"
        })

    # Hamsa Yoga (Jupiter exalted or in own sign in Kendra)
    guru_h = house("Guru"); guru_s = sign("Guru")
    if guru_h in [1,4,7,10] and (guru_s in OWN_SIGNS.get("Guru",[]) or EXALTATION.get("Guru")==guru_s):
        yogas.append({
            "name":"Hamsa Mahapurusha Yoga",
            "planets":"Jupiter in Kendra (own/exalted)",
            "house": guru_h,
            "description":"Per BPHS: wisdom, teaching ability, dharmic prosperity, long life, and spiritual authority.",
            "strength":"Very Strong"
        })

    # Ruchaka Yoga (Mars exalted or own sign in Kendra)
    mars_h = house("Mangal"); mars_s = sign("Mangal")
    if mars_h in [1,4,7,10] and (mars_s in OWN_SIGNS.get("Mangal",[]) or EXALTATION.get("Mangal")==mars_s):
        yogas.append({
            "name":"Ruchaka Mahapurusha Yoga",
            "planets":"Mars in Kendra (own/exalted)",
            "house": mars_h,
            "description":"Per Phaladeepika: great courage, executive ability, victory in all competitive endeavors, high professional position.",
            "strength":"Very Strong"
        })

    # Harsha Yoga (6th lord in 6th)
    sixth_sign = (lagna_sign + 5) % 12
    sixth_lord = SIGN_LORDS[sixth_sign]
    if house(sixth_lord) == 6:
        yogas.append({
            "name":"Harsha Yoga",
            "planets":f"{sixth_lord} (6th lord) in 6th house",
            "house":6,
            "description":"Per Phaladeepika Ch.6: victory over enemies, freedom from serious illness, wealth, and happiness. Invincibility over professional adversaries.",
            "strength":"Strong"
        })

    # Raj Yoga: 9th + 10th lords conjunct or mutual aspect
    ninth_sign  = (lagna_sign + 8) % 12
    tenth_sign  = (lagna_sign + 9) % 12
    ninth_lord  = SIGN_LORDS[ninth_sign]
    tenth_lord  = SIGN_LORDS[tenth_sign]
    if ninth_lord != tenth_lord and same_house(ninth_lord, tenth_lord):
        yogas.append({
            "name":"Dharma-Karma Adhipati Raja Yoga",
            "planets":f"{ninth_lord} (9th) + {tenth_lord} (10th) conjunct",
            "house": house(ninth_lord),
            "description":"Per BPHS Ch.26: conjoining of fortune and career lords creates royal status, authority, and fame.",
            "strength":"Very Strong"
        })

    # 10th lord in 10th (Parakrama Yoga)
    if tenth_lord and house(tenth_lord) == 10:
        yogas.append({
            "name":"Parakrama Yoga (10th lord in 10th)",
            "planets":f"{tenth_lord} in 10th house",
            "house":10,
            "description":"Per BPHS: the native reaches the pinnacle of professional achievement. Career is the native's greatest expression.",
            "strength":"Outstanding"
        })

    # Lagna lord in Kendra / Trikona
    lagna_lord = SIGN_LORDS[lagna_sign]
    ll_house = house(lagna_lord)
    if ll_house in [1,4,7,10,5,9]:
        yogas.append({
            "name":"Lagna Lord in Kendra/Trikona",
            "planets":f"{lagna_lord} in {ll_house}th house",
            "house": ll_house,
            "description":"Per BPHS: Lagna lord in Kendra or Trikona bestows good health, prosperity, and fame throughout life.",
            "strength":"Strong"
        })

    # Vipareet Raja Yoga (6th/8th/12th lord in 6th/8th/12th)
    dusthana_lords = set()
    for idx in [5,7,11]:  # 6th, 8th, 12th houses
        s = (lagna_sign + idx) % 12
        dusthana_lords.add(SIGN_LORDS[s])
    for lord in dusthana_lords:
        if lord in p and house(lord) in [6,8,12]:
            yogas.append({
                "name":"Vipareet Raja Yoga",
                "planets":f"{lord} (dusthana lord) in dusthana house",
                "house": house(lord),
                "description":"Per Saravali: obstacles ultimately transform into extraordinary opportunities. The native rises THROUGH adversity, not despite it.",
                "strength":"Powerful (delayed)"
            })
            break

    # Chandra-Mangal Yoga
    if same_house("Chandra","Mangal"):
        yogas.append({
            "name":"Chandra-Mangal Yoga",
            "planets":"Moon + Mars conjunct",
            "house": house("Chandra"),
            "description":"Per BPHS: wealth through courage and enterprise. Exceptional drive, financial ambition, and emotional strength.",
            "strength":"Strong"
        })

    # Gaja-Kesari Yoga (Jupiter in Kendra from Moon)
    moon_h = house("Chandra"); guru_h = house("Guru")
    if moon_h > 0 and guru_h > 0:
        diff = abs(guru_h - moon_h)
        if diff in [0,3,6,9]:
            yogas.append({
                "name":"Gaja-Kesari Yoga",
                "planets":f"Jupiter in {diff}-house relationship from Moon",
                "house": guru_h,
                "description":"Per BPHS: intelligence, fame, respected by society, rise to prominence like a lion (Kesari) with the strength of an elephant (Gaja).",
                "strength":"Good"
            })

    return yogas

# ── MAIN CHART FUNCTION ──────────────────────────────────────────────────────
def compute_chart(name: str, dob: datetime.date, tob_h: float, lat: float, lon: float) -> dict:
    """
    Full chart computation. Returns a comprehensive dict.
    Mirrors exactly the calc_vedic.py logic used in conversation.
    """
    year = dob.year + (dob.month - 1)/12.0 + (dob.day - 1)/365.25
    ayan = get_ayanamsha(year)

    # IST = UTC + 5:30
    ut_hours = tob_h - 5.5
    if ut_hours < 0:
        ut_hours += 24

    jd = julian_day(dob.year, dob.month, dob.day, ut_hours)
    T  = T_from_JD(jd)

    # Tropical positions
    sun_trop    = calc_sun(T)
    M_sun       = norm360(357.52911 + 35999.05029*T - 0.0001537*T*T)
    moon_trop, Om = calc_moon(T)
    merc_trop   = calc_mercury(T, sun_trop, M_sun)
    ven_trop    = calc_venus(T, sun_trop, M_sun)
    mars_trop   = calc_mars(T)
    jup_trop    = calc_jupiter(T)
    sat_trop    = calc_saturn(T)
    lagna_trop  = calc_lagna(T, jd, ut_hours, lat, lon)

    # Sidereal
    def sid(trop): return tropical_to_sidereal(trop, ayan)
    sun_sid   = sid(sun_trop)
    moon_sid  = sid(moon_trop)
    merc_sid  = sid(merc_trop)
    ven_sid   = sid(ven_trop)
    mars_sid  = sid(mars_trop)
    jup_sid   = sid(jup_trop)
    sat_sid   = sid(sat_trop)
    rahu_sid  = sid(norm360(Om))
    ketu_sid  = norm360(rahu_sid + 180)
    lagna_sid = sid(lagna_trop)

    lagna_sign = sign_from_sid(lagna_sid)

    # Planet dict
    raw = {
        "Surya":  sun_sid,  "Chandra": moon_sid, "Budha":   merc_sid,
        "Shukra": ven_sid,  "Mangal":  mars_sid,  "Guru":    jup_sid,
        "Shani":  sat_sid,  "Rahu":    rahu_sid,  "Ketu":    ketu_sid,
        "Lagna":  lagna_sid,
    }
    planets = {}
    for nm, sid_val in raw.items():
        s = sign_from_sid(sid_val)
        planets[nm] = {
            "sid":     sid_val,
            "sign":    s,
            "sign_san": SIGNS_SAN[s],
            "sign_en":  SIGNS_EN[s],
            "deg":      round(deg_in_sign(sid_val), 2),
            "house":    house_from_lagna(sid_val, lagna_sid),
            "dignity":  planet_dignity(nm, s) if nm not in ["Rahu","Ketu","Lagna"] else "—",
        }

    # Nakshatra
    nak_num, nak_pada, elapsed = get_nakshatra(moon_sid)

    # Dasha
    dasha_seq = dasha_balance_and_sequence(moon_sid, dob)

    # Active dasha today
    today = datetime.date.today()
    md    = active_dasha(dasha_seq, today)
    ads   = antardasha_sequence(md)
    ad    = active_dasha(ads, today)

    # Houses
    houses = {}
    for h in range(1, 13):
        s_idx = (lagna_sign + h - 1) % 12
        occupants = [nm for nm, pd in planets.items()
                     if pd["house"] == h and nm != "Lagna"]
        houses[h] = {
            "sign":    SIGNS_SAN[s_idx],
            "sign_en": SIGNS_EN[s_idx],
            "lord":    SIGN_LORDS[s_idx],
            "occupants": occupants,
        }

    # Yogas
    yogas = detect_yogas(planets, lagna_sign)

    # Tithi (approx) using sidereal Moon and Sun positions for Vedic moon calendar.
    tithi_num = int((norm360(moon_sid - sun_sid)) / 12) + 1
    if tithi_num > 30:
        tithi_num = 30
    paksha = get_paksha(tithi_num)
    tithi_name = get_tithi_name(tithi_num)

    return {
        "name":          name,
        "dob":           dob,
        "tob_h":         tob_h,
        "lat":           lat,
        "lon":           lon,
        "ayanamsha":     round(ayan, 4),
        "jd":            round(jd, 4),
        "lagna_sid":     round(lagna_sid, 2),
        "lagna_sign":    lagna_sign,
        "lagna_san":     SIGNS_SAN[lagna_sign],
        "lagna_en":      SIGNS_EN[lagna_sign],
        "lagna_deg":     round(deg_in_sign(lagna_sid), 2),
        "lagna_lord":    SIGN_LORDS[lagna_sign],
        "moon_sid":      round(moon_sid, 2),
        "moon_sign":     sign_from_sid(moon_sid),
        "moon_san":      SIGNS_SAN[sign_from_sid(moon_sid)],
        "moon_en":       SIGNS_EN[sign_from_sid(moon_sid)],
        "moon_deg":      round(deg_in_sign(moon_sid), 2),
        "nakshatra":     NAKSHATRAS[nak_num],
        "nak_num":       nak_num,
        "nak_pada":      nak_pada,
        "nak_lord":      NAK_LORDS[nak_num],
        "nak_deity":     NAK_DEITY[nak_num],
        "nak_symbol":    NAK_SYMBOL[nak_num],
        "tithi":         tithi_num,
        "paksha":        paksha,
        "tithi_name":    tithi_name,
        "planets":       planets,
        "houses":        houses,
        "dasha_seq":     dasha_seq,
        "active_md":     md,
        "active_ad":     ad,
        "antardasha_seq":ads,
        "yogas":         yogas,
    }
