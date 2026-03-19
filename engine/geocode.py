"""
GEOCODING MODULE
Fetches latitude/longitude for a place name.
Falls back to a curated India/world city table if network unavailable.
This module is COMPLETELY SEPARATE from the calculation engine.
"""

import urllib.request
import urllib.parse
import json
import time

# ── FALLBACK TABLE (key Indian cities + common world cities) ─────────────────
CITY_TABLE = {
    # Andhra Pradesh
    "simhachalam":          (17.7667, 83.3333),
    "visakhapatnam":        (17.6868, 83.2185),
    "vizag":                (17.6868, 83.2185),
    "jangareddygudem":      (17.1667, 81.3000),
    "rajamahendravaram":    (17.0066, 81.7799),
    "rajahmundry":          (17.0066, 81.7799),
    "tirupati":             (13.6288, 79.4192),
    "vijayawada":           (16.5062, 80.6480),
    "guntur":               (16.3067, 80.4365),
    "nellore":              (14.4426, 79.9865),
    "kurnool":              (15.8281, 78.0373),
    "kakinada":             (16.9891, 82.2475),
    "eluru":                (16.7107, 81.0952),
    "srikalahasti":         (13.7499, 79.6983),
    "ahobilam":             (15.1419, 78.5414),
    # Telangana
    "hyderabad":            (17.3850, 78.4867),
    "secunderabad":         (17.4399, 78.4983),
    "warangal":             (17.9784, 79.5941),
    # Tamil Nadu
    "chennai":              (13.0827, 80.2707),
    "madurai":              (9.9252,  78.1198),
    "coimbatore":           (11.0168, 76.9558),
    "trichy":               (10.7905, 78.7047),
    "tiruchirappalli":      (10.7905, 78.7047),
    "tirunelveli":          (8.7139,  77.7567),
    "kanchipuram":          (12.8342, 79.7036),
    # Karnataka
    "bengaluru":            (12.9716, 77.5946),
    "bangalore":            (12.9716, 77.5946),
    "mysuru":               (12.2958, 76.6394),
    "mysore":               (12.2958, 76.6394),
    "hubli":                (15.3647, 75.1240),
    "mangaluru":            (12.9141, 74.8560),
    # Kerala
    "thiruvananthapuram":   (8.5241,  76.9366),
    "trivandrum":           (8.5241,  76.9366),
    "kochi":                (9.9312,  76.2673),
    "kozhikode":            (11.2588, 75.7804),
    "thrissur":             (10.5276, 76.2144),
    # Maharashtra
    "mumbai":               (19.0760, 72.8777),
    "pune":                 (18.5204, 73.8567),
    "nagpur":               (21.1458, 79.0882),
    "nashik":               (19.9975, 73.7898),
    "aurangabad":           (19.8762, 75.3433),
    # North India
    "delhi":                (28.6139, 77.2090),
    "new delhi":            (28.6139, 77.2090),
    "noida":                (28.5355, 77.3910),
    "gurgaon":              (28.4595, 77.0266),
    "lucknow":              (26.8467, 80.9462),
    "kanpur":               (26.4499, 80.3319),
    "varanasi":             (25.3176, 82.9739),
    "prayagraj":            (25.4358, 81.8463),
    "allahabad":            (25.4358, 81.8463),
    "agra":                 (27.1767, 78.0081),
    "jaipur":               (26.9124, 75.7873),
    "jodhpur":              (26.2389, 73.0243),
    "udaipur":              (24.5854, 73.7125),
    "ahmedabad":            (23.0225, 72.5714),
    "surat":                (21.1702, 72.8311),
    "vadodara":             (22.3072, 73.1812),
    "bhopal":               (23.2599, 77.4126),
    "indore":               (22.7196, 75.8577),
    "kolkata":              (22.5726, 88.3639),
    "patna":                (25.5941, 85.1376),
    "ranchi":               (23.3441, 85.3096),
    "bhubaneswar":          (20.2961, 85.8245),
    "chandigarh":           (30.7333, 76.7794),
    "amritsar":             (31.6340, 74.8723),
    "guwahati":             (26.1445, 91.7362),
    # Sacred sites
    "rishikesh":            (30.0869, 78.2676),
    "haridwar":             (29.9457, 78.1642),
    "vrindavan":            (27.5800, 77.7000),
    "mathura":              (27.4924, 77.6737),
    "ayodhya":              (26.7922, 82.1998),
    "dwarka":               (22.2390, 68.9678),
    "puri":                 (19.8135, 85.8312),
    "kashi":                (25.3176, 82.9739),
    "nasik":                (19.9975, 73.7898),
    "ujjain":               (23.1765, 75.7885),
    "shirdi":               (19.7667, 74.4779),
    "madurai meenakshi":    (9.9195,  78.1193),
    "rameswaram":           (9.2881,  79.3174),
    # World cities
    "london":               (51.5074, -0.1278),
    "new york":             (40.7128, -74.0060),
    "dubai":                (25.2048, 55.2708),
    "singapore":            (1.3521,  103.8198),
    "sydney":               (-33.8688, 151.2093),
    "toronto":              (43.6532, -79.3832),
    "kuala lumpur":         (3.1390,  101.6869),
}

def geocode_online(place_name: str) -> tuple | None:
    """Try Nominatim (OpenStreetMap) — no API key required."""
    try:
        query = urllib.parse.urlencode({
            "q": place_name + ", India",
            "format": "json",
            "limit": 1,
        })
        url = f"https://nominatim.openstreetmap.org/search?{query}"
        req = urllib.request.Request(url,
              headers={"User-Agent": "JyotishaApp/1.0 (Vedic Astrology Calculator)"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read())
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None

def geocode(place_name: str) -> tuple:
    """
    Returns (lat, lon) for place_name.
    1. Try online (Nominatim)
    2. Fallback to curated table
    3. Default to Delhi if unknown
    """
    if not place_name or not place_name.strip():
        return (28.6139, 77.2090)  # Delhi default

    key = place_name.strip().lower()

    # Exact match in table
    if key in CITY_TABLE:
        return CITY_TABLE[key]

    # Partial match
    for city, coords in CITY_TABLE.items():
        if city in key or key in city:
            return coords

    # Online geocode
    result = geocode_online(place_name)
    if result:
        return result

    # Last resort — return Delhi with warning
    return (28.6139, 77.2090)
