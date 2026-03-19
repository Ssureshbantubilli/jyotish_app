@echo off
echo.
echo Om  JYOTISHA VEDIC ASTROLOGY APP  Om
echo ========================================
echo.

cd /d "%~dp0"

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo.
echo Launching Jyotisha App...
echo Open your browser at: http://localhost:8501
echo.

python -m streamlit run ui\app.py ^
    --server.port 8501 ^
    --theme.base dark ^
    --theme.primaryColor "#C89010" ^
    --theme.backgroundColor "#0E1117" ^
    --theme.secondaryBackgroundColor "#1A1A2A" ^
    --theme.textColor "#E8E0D0"

pause
