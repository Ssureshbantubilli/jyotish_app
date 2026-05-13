#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
#  JYOTISHA APP — ONE-CLICK SETUP & RUN
#  Vedic Astrology System (same logic as conversation reports)
# ═══════════════════════════════════════════════════════════════════════════
set -e

echo ""
echo "ॐ  JYOTISHA VEDIC ASTROLOGY APP  ॐ"
echo "════════════════════════════════════"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 1. Create virtual environment
if [ ! -d ".venv" ]; then
    echo "► Creating virtual environment..."
    python3 -m venv .venv
fi

# 2. Activate
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null

# 3. Install deps
echo "► Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# 4. Create __init__ files
touch engine/__init__.py ui/__init__.py reports/__init__.py

# 5. Run
echo ""
echo "► Launching Jyotisha App..."
echo "   Open your browser at: http://localhost:8501"
echo ""

cd "$SCRIPT_DIR"
python -m streamlit run ui/app.py \
    --server.port 8501 \
    --server.headless false \
    --browser.gatherUsageStats false \
    --theme.base dark \
    --theme.primaryColor "#C89010" \
    --theme.backgroundColor "#0E1117" \
    --theme.secondaryBackgroundColor "#1A1A2A" \
    --theme.textColor "#E8E0D0"