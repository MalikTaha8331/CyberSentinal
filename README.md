# ⚔️ CyberSentinel
### AI-Powered Intrusion Detection & Prevention System

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?style=for-the-badge&logo=flask)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange?style=for-the-badge&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/Accuracy-99.92%25-gold?style=for-the-badge)

> Real-time AI-powered network intrusion detection and prevention system with auto-blocking, live dashboard, email alerts, and GeoIP tracking.

---



## 🎯 Features

| Feature | Description |
|---|---|
| 🤖 **AI Detection** | Random Forest ML model with 99.92% accuracy |
| 🚫 **Auto-Blocking** | Severe threats (>75% confidence) blocked automatically |
| 📊 **Live Dashboard** | Real-time charts, alerts, and threat statistics |
| 📡 **Live Traffic Monitor** | Packet-level monitoring with protocol filters |
| 🔐 **OWASP Security** | bcrypt, rate limiting, brute force protection |
| 📧 **Email Alerts** | Instant email on severe attack detection |
| 🌍 **GeoIP Tracking** | Country and city of attack source |
| 🧙 **Setup Wizard** | First-time personalized account creation |
| 🔑 **OTP Password Reset** | Forgot password via 6-digit email OTP |
| 📋 **Historical Logs** | Persistent JSON logs with search and filters |
| ⚔️ **Attack Types** | Identifies DoS, Port Scan, Brute Force, SYN Flood etc. |
| 📄 **PDF Reports** | One-click security report generation |
| ⚡ **Auto Installer** | One-command setup on Windows and Linux |

---

## 🏗️ System Architecture

```
Network Traffic
      ↓
Scapy Live Sniffer (sniffer.py)
      ↓
Feature Extraction (41 NSL-KDD features)
      ↓
Random Forest ML Model (99.92% accuracy)
      ↓
Threat Classification (Normal / Suspicious / Moderate / Severe)
      ↓
Flask API + Dashboard (app.py)
      ↓
Auto-Block or Alert Admin
```

---

## 🎯 Threat Classification

| Category | Confidence | Action |
|---|---|---|
| ✅ **NORMAL** | Prediction = 0 | No action |
| ⚪ **SUSPICIOUS** | < 55% | Block button shown |
| 🟡 **MODERATE THREAT** | 55% - 75% | Block button shown |
| 🔴 **SEVERE THREAT** | > 75% | **Auto-blocked immediately** |

---

## 📊 ML Model Results

| Model | Accuracy | F1-Score | AUC-ROC |
|---|---|---|---|
| **Random Forest** ⭐ | **99.92%** | **99.92%** | **100.00%** |
| Deep Neural Network | 99.51% | 99.51% | 99.98% |
| SVM | 96.09% | 95.99% | 99.16% |

> Dataset: NSL-KDD (125,973 training + 22,544 test records)

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Git
- pip

### Windows Installation

```bash
# Step 1 — Clone repository
git clone https://github.com/MalikTaha8331/ai-ids-fyp.git
cd ai-ids-fyp

# Step 2 — Run installer
install.bat
```

### Linux / Kali Linux Installation

```bash
# Step 1 — Clone repository
git clone https://github.com/MalikTaha8331/ai-ids-fyp.git
cd ai-ids-fyp

# Step 2 — Make installer executable
chmod +x install.sh

# Step 3 — Run installer
./install.sh
```

### Manual Installation

```bash
# Clone repo
git clone https://github.com/MalikTaha8331/ai-ids-fyp.git
cd ai-ids-fyp

# Install dependencies
pip install -r requirements.txt

# Start CyberSentinel
python start_ids.py
```

---

## 🚀 Running CyberSentinel

```bash
# Start everything (Flask + Sniffer auto-starts from dashboard)
cd src
python app.py
```

Open browser at:
```
http://127.0.0.1:5000
```

First time? The **Setup Wizard** will appear — create your admin account!

### Starting Live Sniffer

> ⚠️ Must run as **Administrator** on Windows for packet capture

```bash
# Option 1 — From dashboard (recommended)
# Click the "Sniffer: OFF" button in the nav bar

# Option 2 — Manual terminal (run as Administrator)
cd src
python sniffer.py auto
```

---

## 📁 Project Structure

```
ai-ids-fyp/
├── src/
│   ├── app.py              # Flask web server + API routes
│   ├── predict.py          # ML model loader + threat classifier
│   ├── sniffer.py          # Live Scapy packet capture
│   ├── simulate.py         # NSL-KDD pipeline simulator
│   ├── features.py         # Feature definitions + encodings
│   ├── auth.py             # OWASP authentication + brute force
│   ├── user_store.py       # User credentials management
│   ├── mailer.py           # Email OTP + alert system
│   ├── pdf_report.py       # PDF report generator
│   └── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html          # Main dashboard
│   ├── live.html           # Live traffic monitor
│   ├── history.html        # Historical logs
│   ├── login.html          # Login page
│   ├── setup.html          # First-time setup wizard
│   ├── forgot.html         # Forgot password
│   ├── otp.html            # OTP verification
│   └── reset.html          # Password reset
├── static/
│   └── style.css           # Purple Gold Cyberpunk theme
├── models/                 # Trained ML models (Git LFS)
│   ├── best_model.pkl      # Deployed Random Forest
│   ├── random_forest.pkl   # Random Forest
│   ├── svm_model.pkl       # SVM model
│   └── dnn_model.keras     # Deep Neural Network
├── data/
│   ├── raw/                # Original NSL-KDD files (gitignored)
│   └── processed/          # Cleaned datasets (Git LFS)
├── notebooks/
│   ├── 01_eda.ipynb        # Exploratory Data Analysis
│   ├── 02_preprocessing.ipynb
│   ├── 03_random_forest.ipynb
│   ├── 04_svm.ipynb
│   ├── 05_dnn.ipynb
│   └── 06_model_comparison.ipynb
├── logs/                   # Security logs (gitignored)
├── docs/                   # Documentation + screenshots
├── setup.py                # Auto installer
├── start_ids.py            # Main launcher
├── install.bat             # Windows installer
├── install.sh              # Linux installer
└── README.md
```

---

## 🔧 Common Errors & Fixes

### ❌ Error: `externally-managed-environment` (Linux/Kali)

```
error: externally-managed-environment
```

**Fix:**
```bash
pip install -r requirements.txt --break-system-packages
```

---

### ❌ Error: `Sniffer error: Interface 'None' not found`

**Fix — Auto detect interface:**
```bash
python sniffer.py auto
```

**Fix — Specify interface manually:**
```bash
# Find your interface name first
python -c "from scapy.all import IFACES; [print(f'{i.name} | {i.ip}') for i in IFACES.values()]"

# Then run with your interface
python sniffer.py WiFi
# or
python sniffer.py Ethernet
```

---

### ❌ Error: `Operation not permitted` / Raw socket error

```
[open_sockraw] socket(): Operation not permitted
```

**Fix — Run as Administrator:**
- **Windows:** Right-click terminal → Run as Administrator
- **Linux:** Use `sudo`

```bash
# Linux
sudo python sniffer.py auto

# Windows — open Admin CMD then
python sniffer.py auto
```

---

### ❌ Error: `UnicodeEncodeError` with emojis

```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Fix — Set UTF-8 encoding:**
```bash
# Windows
set PYTHONIOENCODING=utf-8
python app.py
```

---

### ❌ Error: `flask_limiter` UserWarning

```
UserWarning: Using the in-memory storage for tracking rate limits
```

**This is just a warning, not an error.** App works fine. To suppress:
```python
# In app.py, add storage_uri to limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["5000 per day", "1000 per hour"]
)
```

---

### ❌ Error: `TemplateNotFound: login.html`

```
jinja2.exceptions.TemplateNotFound: login.html
```

**Fix — Make sure you cloned the full repo:**
```bash
git clone https://github.com/MalikTaha8331/ai-ids-fyp.git
```
Not just downloaded as ZIP. The `templates/` folder must exist.

---

### ❌ Error: `Model file not found`

```
FileNotFoundError: models/best_model.pkl not found
```

**Fix — Pull Git LFS files:**
```bash
git lfs install
git lfs pull
```

If Git LFS is not installed:
```bash
# Windows
winget install GitHub.GitLFS

# Linux
sudo apt install git-lfs
git lfs install
git lfs pull
```

---

### ❌ Error: `bcrypt` installation fails on Windows

```
error: Microsoft Visual C++ 14.0 is required
```

**Fix:**
```bash
pip install bcrypt --only-binary=bcrypt
```

---

### ❌ Error: `scapy` not capturing packets on Windows

**Fix — Install Npcap:**
1. Download from: https://npcap.com/#download
2. Install with "WinPcap API-compatible Mode" checked
3. Restart computer
4. Run terminal as Administrator

---

## 📧 Email Configuration

CyberSentinel uses Gmail SMTP for OTP and alert emails.

To configure:

1. Create a Gmail account
2. Enable 2-Factor Authentication
3. Generate App Password: Google Account → Security → App Passwords
4. Update `src/mailer.py`:

```python
SENDER_EMAIL    = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-16-char-app-password'
```

> ⚠️ Never commit real credentials to GitHub!

---

## 🔐 Security Features

- ✅ **bcrypt** password hashing
- ✅ **Brute force protection** — 5 attempt lockout for 5 minutes
- ✅ **Rate limiting** — 10 login attempts per minute
- ✅ **Security headers** — CSP, X-Frame-Options, XSS protection
- ✅ **Session management** — Secure Flask sessions
- ✅ **OWASP Top 10** compliance
- ✅ **Security event logging** — All events logged with IP and timestamp

---

## 🌐 Dashboard Pages

| Page | URL | Description |
|---|---|---|
| Main Dashboard | `/` | Stats, charts, alerts, blocked IPs |
| Live Traffic | `/live` | Real-time packet feed with filters |
| History | `/history` | Paginated security event logs |
| Login | `/login` | OWASP-compliant authentication |
| Setup | `/setup` | First-time account creation |

---

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/predict` | POST | Classify network traffic |
| `/alerts` | GET | Get recent alerts |
| `/stats` | GET | Get traffic statistics |
| `/block` | POST | Manually block an IP |
| `/unblock` | POST | Unblock an IP |
| `/blocked` | GET | List blocked IPs |
| `/traffic` | GET/POST | Live traffic data |
| `/sniffer/start` | POST | Start packet sniffer |
| `/sniffer/stop` | POST | Stop packet sniffer |
| `/report/pdf` | GET | Download PDF report |
| `/logs` | GET | Get historical logs |

---

## 📦 Dependencies

```
flask
flask-cors
flask-limiter
scikit-learn
tensorflow
scapy
pandas
numpy
bcrypt
joblib
reportlab
requests
scipy
imbalanced-learn
```

---

## 🎓 Academic Details

| Field | Details |
|---|---|
| **Project Title** | AI-Powered Intrusion Detection & Prevention System |
| **Dataset** | NSL-KDD (125,973 training + 22,544 test records) |
| **Best Model** | Random Forest (99.92% accuracy) |
| **Other Models** | DNN (99.51%), SVM (96.09%) |
| **University** | Sir Syed CASE Institute of Technology, Islamabad |
| **Program** | BS Cybersecurity |
| **Year** | 2025-2026 |

---

## 🚀 Future Work

- ☁️ Cloud deployment (Railway/AWS)
- 🌍 Full GeoIP world map visualization
- 🔥 Real Windows Firewall / iptables integration
- 📱 Mobile app
- 🧠 Federated learning support
- 📊 SIEM integration
- 🛡️ EDR module

---

## 👨‍💻 Author

**Malik Taha**
- GitHub: [@MalikTaha8331](https://github.com/MalikTaha8331)
- Project: [ai-ids-fyp](https://github.com/MalikTaha8331/ai-ids-fyp)

---

## 📄 License

MIT License — free to use, modify and distribute.

---

<div align="center">
  <strong>⚔️ CyberSentinel — Protecting Networks with Artificial Intelligence</strong>
  <br>
  <sub>Built with Python, Flask, Scikit-learn, TensorFlow, Scapy & Chart.js</sub>
</div>
