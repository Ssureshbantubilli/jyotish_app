<<<<<<< HEAD
# 🪔 Jyotisha — Vedic Astrology App

**The same calculation engine and report style used throughout this conversation, packaged as a full application.**


## What This Is

This application programmatically replicates the **exact same** Vedic astrology calculations, interpretations, and report structure used to generate all charts and reports in this conversation — including the charts for Suresh Kumar Bantubilli and Nagasireesha Rayudu.


## Project Structure

```
jyotish_app/
│
├── engine/
│   ├── __init__.py       — Public API
│   ├── calc.py           — Core astronomical calculations (same as conversation)
│   │                       • Julian Day computation
│   │                       • Sun: Meeus Ch.25 L0 + equation of center
│   │                       • Moon: ELP2000-82 16-term subset
│   │                       • Planets: Mean longitude + equation of center
│   │                       • Lagna: GMST → LST → atan2 formula
│   │                       • Ayanamsha: Lahiri interpolated table
│   │                       • Vimshottari Dasha from Nakshatra balance
│   │                       • Yoga detection (11 yogas from classical texts)
│   │
│   ├── interpret.py      — Interpretation engine (same style/depth as reports)
│   │                       • Planet-in-house text (BPHS/Phaladeepika references)
│   │                       • Dasha phala narration
│   │                       • Ashtakoot Milan (8 kootas)
│   │                       • Year-wise scoring (MD/AD + Jupiter + Saturn transits)
│   │                       • Dampati combined scoring + synergy
│   │
│   ├── report.py         — Report generator (same structure as conversation)
│   │                       • Individual report (9 sections)
│   │                       • Compatibility report (4 sections)
│   │                       • Combined 25-year report with year table
│   │
│   └── geocode.py        — Place → lat/lon (does NOT affect calc engine)
│                           • 100+ Indian city lookup table
│                           • Online Nominatim fallback
│
├── ui/
│   └── app.py            — Streamlit UI (3 modes: Individual/Compat/Combined)
│
├── requirements.txt      — Python dependencies
├── run.sh                — Linux/Mac one-click setup & run
├── run.bat               — Windows one-click setup & run
└── README.md             — This file
```


## Setup & Run

### Linux / Mac
```bash
chmod +x run.sh
./run.sh
```

### Windows
```
Double-click run.bat
```

### Manual Setup
```bash
cd jyotish_app

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate.bat     # Windows

# Install dependencies
pip install -r requirements.txt

# Run
python -m streamlit run ui/app.py \
    --theme.base dark \
    --theme.primaryColor "#C89010"
```

Open browser at: **http://localhost:8501**


## Calculation Engine Details

### Same Logic as Conversation Reports

| Component | Method | Source |
|---|---|---|
| Julian Day | Standard Gregorian → JD formula | Meeus, "Astronomical Algorithms" |
| Sun longitude | L0 + equation of center (3 terms) | Meeus Ch.25 |
| Moon longitude | ELP2000-82 subset (16 periodic terms) | Same as calc_vedic.py |
| Mercury | Mean lon + equation of center | Meeus |
| Venus | Mean lon + equation of center | Meeus |
| Mars | Mean lon + equation of center | Meeus |
| Jupiter | Mean lon + equation of center | Meeus |
| Saturn | Mean lon + equation of center | Meeus |
| Rahu/Ketu | From Moon's ascending node (Om) | Same formula |
| Lagna | GMST → LST → atan2 ascendant | Same as conversation |
| Ayanamsha | Lahiri interpolated table | Same values (1982: 23.5653°, 1984: 23.6167°) |
| Houses | Equal house from Lagna | BPHS standard |
| Dasha | Vimshottari from Nakshatra balance | BPHS Ch.46 |

### Verification

The engine produces identical results to the manually computed charts:


## Report Sections

### Individual Report (9 Sections)
1. Janma Parichaya (Birth Particulars)
2. Janma Kundali: Lagna, Rashi & Nakshatra
3. Graha Sthana (Planetary Positions)
4. Bhava Vivechana (House Analysis)
5. Graha Phala (Planetary Interpretations)
6. Yoga Vivechana (Planetary Combinations)
7. Vimshottari Dasha System
8. Gochar Phala (Year-wise Forecast 2025–2035)
9. Upaya (Vedic Remedies)

### Compatibility Report (4 Sections)
1. Ashtakoot Milan (36-Point System)
2. Kalatra Bhava Analysis (7th House)
3. Dampati Dasha Synchronisation
4. Dampati Yoga & Protection Analysis

### Combined Report


## Classical Shastra Basis



## Key Design Decisions

1. **No external ephemeris library** — All calculations use the same mathematical formulas from the conversation (Meeus algorithms)
2. **Lahiri Ayanamsha table** — Same interpolated values used throughout
3. **Geocoding is separate** — Location lookup does not affect any calculation
4. **Deterministic** — Same input always produces same output
5. **Modular** — Each module can be used independently


*ॐ तत् सत् — Jyotisha is the Eye of the Vedas*
=======
# jyotish_app
>>>>>>> dd24463ec4a3b1e04c085db104ab5209f54c9e1e
