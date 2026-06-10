@echo off
title CyberSentinel Installer
color 0A

echo.
echo  ============================================
echo   ⚔  CyberSentinel - AI IDS/IPS System
echo   Automated Windows Installer v2.0
echo  ============================================
echo.

:: ─── Check Admin Rights ──────────────────────
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Please run this installer as Administrator!
    echo.
    echo  Right-click install.bat and select
    echo  "Run as Administrator"
    echo.
    pause
    exit /b 1
)
echo  [OK] Running as Administrator

:: ─── Check Python ────────────────────────────
echo.
echo  [1/8] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found!
    echo  Please install Python 3.10+ from https://python.org
    echo  Make sure to check "Add Python to PATH" during install
    pause
    exit /b 1
)
python --version
echo  [OK] Python found

:: ─── Check Git ───────────────────────────────
echo.
echo  [2/8] Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [WARNING] Git not found - installing via winget...
    winget install Git.Git -e --silent
)
echo  [OK] Git found

:: ─── Upgrade pip ─────────────────────────────
echo.
echo  [3/8] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo  [OK] pip upgraded

:: ─── Install All Requirements ─────────────────
echo.
echo  [4/8] Installing Python packages...
echo  This may take 5-10 minutes...
echo.

pip install flask --quiet
pip install flask-cors --quiet
pip install flask-limiter --quiet
pip install bcrypt --quiet
pip install pandas --quiet
pip install numpy --quiet
pip install scikit-learn --quiet
pip install tensorflow --quiet
pip install scapy --quiet
pip install joblib --quiet
pip install requests --quiet
pip install scipy --quiet
pip install imbalanced-learn --quiet
pip install reportlab --quiet
pip install python-whois --quiet
pip install tldextract --quiet
pip install gdown --quiet

echo  [OK] All packages installed

:: ─── Install Npcap for Scapy ─────────────────
echo.
echo  [5/8] Checking Npcap for packet capture...
reg query "HKLM\SOFTWARE\Npcap" >nul 2>&1
if %errorlevel% neq 0 (
    echo  [INFO] Npcap not found - downloading...
    echo  Please install Npcap from: https://npcap.com/#download
    echo  Check "WinPcap API-compatible Mode" during install
    start https://npcap.com/#download
    echo.
    echo  After installing Npcap press any key to continue...
    pause
) else (
    echo  [OK] Npcap already installed
)

:: ─── Check Models ─────────────────────────────
echo.
echo  [6/8] Checking ML models...
if not exist "models\best_model.pkl" (
    echo  [WARNING] Model files not found!
    echo  Please copy models/ folder to: %cd%\models\
    echo  Models should include: best_model.pkl, random_forest.pkl
    echo  You can get them via: git lfs pull
    echo.
    git lfs install >nul 2>&1
    git lfs pull >nul 2>&1
    if exist "models\best_model.pkl" (
        echo  [OK] Models downloaded via Git LFS
    ) else (
        echo  [WARNING] Please manually copy models folder
    )
) else (
    echo  [OK] ML models found
)

:: ─── Check Data ───────────────────────────────
echo.
echo  [7/8] Checking processed data...
if not exist "data\processed\X_test.csv" (
    echo  [WARNING] Processed data not found!
    echo  Attempting Git LFS pull...
    git lfs pull >nul 2>&1
    if exist "data\processed\X_test.csv" (
        echo  [OK] Data downloaded via Git LFS
    ) else (
        echo  [WARNING] Please manually copy data/processed/ folder
    )
) else (
    echo  [OK] Processed data found
)

:: ─── Register Startup Service ─────────────────
echo.
echo  [8/8] Registering CyberSentinel as startup service...
set APP_PATH=%cd%\start_ids.py
set PYTHON_PATH=
for /f "tokens=*" %%i in ('where pythonw') do set PYTHON_PATH=%%i

if not "%PYTHON_PATH%"=="" (
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" ^
        /v "CyberSentinel" ^
        /t REG_SZ ^
        /d "\"%PYTHON_PATH%\" \"%APP_PATH%\"" ^
        /f >nul 2>&1
    echo  [OK] Registered in Windows startup
) else (
    echo  [WARNING] Could not register startup - start manually with:
    echo  python start_ids.py
)

:: ─── Create Desktop Shortcut ──────────────────
echo.
echo  Creating desktop shortcut...
set SHORTCUT=%USERPROFILE%\Desktop\CyberSentinel.bat
echo @echo off > "%SHORTCUT%"
echo title CyberSentinel >> "%SHORTCUT%"
echo cd /d "%cd%" >> "%SHORTCUT%"
echo python start_ids.py >> "%SHORTCUT%"
echo  [OK] Desktop shortcut created

:: ─── Done ─────────────────────────────────────
echo.
echo  ============================================
echo   INSTALLATION COMPLETE!
echo  ============================================
echo.
echo   Start CyberSentinel:
echo   python start_ids.py
echo.
echo   Or double-click CyberSentinel on Desktop
echo.
echo   Dashboard: http://127.0.0.1:5000
echo   Live Traffic: http://127.0.0.1:5000/live
echo.
echo   IMPORTANT: Always run as Administrator
echo   for live packet capture!
echo  ============================================
echo.

set /p START="Start CyberSentinel now? (y/n): "
if /i "%START%"=="y" (
    echo Starting CyberSentinel...
    python start_ids.py
)

pause
