#!/bin/bash

# ─── Colors ───────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GOLD='\033[1;33m'
NC='\033[0m' # No Color

# ─── Banner ───────────────────────────────────
echo ""
echo -e "${GOLD} ============================================${NC}"
echo -e "${GOLD}  ⚔  CyberSentinel - AI IDS/IPS System${NC}"
echo -e "${GOLD}  Automated Linux Installer v2.0${NC}"
echo -e "${GOLD} ============================================${NC}"
echo ""

# ─── Check Root ───────────────────────────────
echo -e "${CYAN}[1/9] Checking permissions...${NC}"
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Not running as root${NC}"
    echo -e "${YELLOW}Some features may need sudo${NC}"
    SUDO="sudo"
else
    echo -e "${GREEN}[OK] Running as root${NC}"
    SUDO=""
fi

# ─── Detect OS ────────────────────────────────
echo ""
echo -e "${CYAN}[2/9] Detecting OS...${NC}"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    echo -e "${GREEN}[OK] Detected: $OS${NC}"
else
    OS="Unknown"
    echo -e "${YELLOW}[WARNING] Could not detect OS${NC}"
fi

# ─── Check Python ─────────────────────────────
echo ""
echo -e "${CYAN}[3/9] Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}[OK] $PYTHON_VERSION${NC}"
    PYTHON="python3"
else
    echo -e "${RED}[ERROR] Python3 not found! Installing...${NC}"
    $SUDO apt-get update -qq
    $SUDO apt-get install -y python3 python3-pip
    PYTHON="python3"
fi

# ─── Check pip ────────────────────────────────
echo ""
echo -e "${CYAN}[4/9] Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}[OK] pip3 found${NC}"
    PIP="pip3"
elif command -v pip &> /dev/null; then
    echo -e "${GREEN}[OK] pip found${NC}"
    PIP="pip"
else
    echo -e "${YELLOW}[INFO] Installing pip...${NC}"
    $SUDO apt-get install -y python3-pip
    PIP="pip3"
fi

# ─── Upgrade pip ──────────────────────────────
echo ""
echo -e "${CYAN}[5/9] Upgrading pip...${NC}"
$PYTHON -m pip install --upgrade pip --quiet 2>/dev/null || \
$PYTHON -m pip install --upgrade pip --break-system-packages --quiet 2>/dev/null
echo -e "${GREEN}[OK] pip upgraded${NC}"

# ─── Install Python Packages ──────────────────
echo ""
echo -e "${CYAN}[6/9] Installing Python packages...${NC}"
echo -e "${YELLOW}This may take 5-10 minutes...${NC}"
echo ""

PACKAGES=(
    "flask"
    "flask-cors"
    "flask-limiter"
    "bcrypt"
    "pandas"
    "numpy"
    "scikit-learn"
    "tensorflow"
    "scapy"
    "joblib"
    "requests"
    "scipy"
    "imbalanced-learn"
    "reportlab"
    "python-whois"
    "tldextract"
    "gdown"
    "beautifulsoup4"
)

# Try normal pip first then --break-system-packages
for package in "${PACKAGES[@]}"; do
    echo -ne "  Installing $package... "
    $PIP install "$package" --quiet 2>/dev/null
    if [ $? -ne 0 ]; then
        # Try with --break-system-packages (Kali/Ubuntu 23+)
        $PIP install "$package" --break-system-packages --quiet 2>/dev/null
    fi
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}WARN - try manually: pip install $package${NC}"
    fi
done

echo ""
echo -e "${GREEN}[OK] Packages installation complete${NC}"

# ─── Fix Scapy Permissions ────────────────────
echo ""
echo -e "${CYAN}[7/9] Setting up Scapy packet capture permissions...${NC}"

# Find Python executable
PYTHON_BIN=$(which python3)

# Method 1 — setcap (recommended)
if command -v setcap &> /dev/null; then
    $SUDO setcap cap_net_raw,cap_net_admin=eip "$PYTHON_BIN" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK] Packet capture permissions set via setcap${NC}"
        echo -e "${GREEN}[OK] Sniffer can now run WITHOUT sudo!${NC}"
    else
        echo -e "${YELLOW}[WARNING] setcap failed - sniffer needs sudo${NC}"
    fi
else
    # Method 2 — install libcap
    echo -e "${YELLOW}[INFO] Installing libcap...${NC}"
    $SUDO apt-get install -y libcap2-bin 2>/dev/null || \
    $SUDO yum install -y libcap 2>/dev/null
    $SUDO setcap cap_net_raw,cap_net_admin=eip "$PYTHON_BIN" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK] Packet capture permissions set${NC}"
    else
        echo -e "${YELLOW}[WARNING] Run sniffer with sudo if needed${NC}"
    fi
fi

# ─── Check Models ─────────────────────────────
echo ""
echo -e "${CYAN}[8/9] Checking ML models...${NC}"
if [ ! -f "models/best_model.pkl" ]; then
    echo -e "${YELLOW}[WARNING] Model files not found${NC}"
    echo -e "${YELLOW}Attempting Git LFS pull...${NC}"

    # Install git-lfs if not present
    if ! command -v git-lfs &> /dev/null; then
        echo -e "${YELLOW}Installing Git LFS...${NC}"
        $SUDO apt-get install -y git-lfs 2>/dev/null || \
        curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | $SUDO bash
        git lfs install
    fi

    git lfs pull 2>/dev/null

    if [ -f "models/best_model.pkl" ]; then
        echo -e "${GREEN}[OK] Models downloaded via Git LFS${NC}"
    else
        echo -e "${YELLOW}[WARNING] Please copy models/ folder manually${NC}"
        echo -e "${YELLOW}Required: models/best_model.pkl${NC}"
    fi
else
    echo -e "${GREEN}[OK] ML models found${NC}"
fi

# ─── Register Systemd Service ─────────────────
echo ""
echo -e "${CYAN}[9/9] Registering CyberSentinel as startup service...${NC}"

APP_DIR=$(pwd)
PYTHON_PATH=$(which python3)
SERVICE_FILE="/etc/systemd/system/cybersentinel.service"
USER=$(whoami)

SERVICE_CONTENT="[Unit]
Description=CyberSentinel AI IDS/IPS
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_PATH $APP_DIR/start_ids.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=$APP_DIR

[Install]
WantedBy=multi-user.target"

# Write service file
echo "$SERVICE_CONTENT" | $SUDO tee "$SERVICE_FILE" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    $SUDO systemctl daemon-reload 2>/dev/null
    $SUDO systemctl enable cybersentinel 2>/dev/null
    echo -e "${GREEN}[OK] Registered as systemd service${NC}"
    echo -e "${GREEN}[OK] CyberSentinel will start on boot!${NC}"
else
    echo -e "${YELLOW}[WARNING] Could not register service${NC}"
    echo -e "${YELLOW}Start manually with: python3 start_ids.py${NC}"
fi

# ─── Create Launcher Script ───────────────────
cat > run_cybersentinel.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "Starting CyberSentinel..."
python3 start_ids.py
EOF
chmod +x run_cybersentinel.sh
echo -e "${GREEN}[OK] Launcher script created: ./run_cybersentinel.sh${NC}"

# ─── Final Summary ────────────────────────────
echo ""
echo -e "${GOLD} ============================================${NC}"
echo -e "${GOLD}  INSTALLATION COMPLETE!${NC}"
echo -e "${GOLD} ============================================${NC}"
echo ""
echo -e "${GREEN}  Start CyberSentinel:${NC}"
echo -e "${CYAN}  python3 start_ids.py${NC}"
echo -e "${CYAN}  OR: ./run_cybersentinel.sh${NC}"
echo ""
echo -e "${GREEN}  Dashboard:     ${CYAN}http://127.0.0.1:5000${NC}"
echo -e "${GREEN}  Live Traffic:  ${CYAN}http://127.0.0.1:5000/live${NC}"
echo ""
echo -e "${YELLOW}  NOTE: If sniffer fails run with sudo:${NC}"
echo -e "${CYAN}  sudo python3 src/sniffer.py auto${NC}"
echo ""
echo -e "${GOLD} ============================================${NC}"
echo ""

# ─── Ask to Start ─────────────────────────────
read -p "Start CyberSentinel now? (y/n): " START
if [[ "$START" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${GREEN}Starting CyberSentinel...${NC}"
    $PYTHON start_ids.py
fi
