# 🛡️ AI-Powered Intrusion Detection & Prevention System

# ⚔️ CyberSentinel  
**AI-Powered Intrusion Detection & Prevention System**  
BS Cybersecurity | 2025–2026  

---

## 📌 Overview  
CyberSentinel is an **AI-driven Intrusion Detection & Prevention System (IDPS)** designed to detect, classify, and block malicious network traffic in real time. Built on the **NSL-KDD dataset**, it leverages **machine learning models** to achieve **99.92% accuracy** in detecting threats, including **zero-day attacks**.  

Key Highlights:  
- ✅ **99.92% Accuracy** (Random Forest model)  
- ⚡ **Real-Time Threat Detection**  
- 🚫 **Auto-Blocking Severe Threats** (>75% confidence)  
- 📊 **Live Dashboard** with traffic monitoring & alerts  
- 🔐 **OWASP-Compliant Security Features**  

---

## 🛠️ System Architecture  
1. **Capture** → Live packet sniffing via **Scapy**  
2. **Extract** → 41 NSL-KDD features per connection  
3. **Classify** → Random Forest ML model  
4. **Categorize** → 4-tier threat levels (Normal → Severe)  
5. **Act** → Alerts, logs, and auto-blocking  

---

## 📂 Technology Stack  
- **Python 3.10+**  
- **Scapy** (packet capture)  
- **Scikit-learn / TensorFlow** (ML models)  
- **Flask** (web dashboard)  
- **Chart.js** (visualizations)  
- **Git LFS** (model hosting)  

---

## 📊 Dataset & Models  
- **Dataset:** NSL-KDD (125,973 training, 22,544 testing records)  
- **Features:** 41 per connection  
- **Balancing:** SMOTE applied  
- **Models Tested:**  
  - Random Forest → **99.92% Accuracy**  
  - Deep Neural Net → 99.51% Accuracy  
  - SVM → 96.09% Accuracy  

---

## 🚨 Threat Classification  
- **Normal (0)** → Safe traffic  
- **Suspicious (<55%)** → Admin decides  
- **Moderate (55–75%)** → Admin recommended to block  
- **Severe (>75%)** → Auto-blocked instantly  

---

## 🔑 Key Features  
- 🛡️ Real-time detection & blocking  
- 📊 Interactive dashboard with charts & logs  
- 🔐 Secure authentication (bcrypt, OTP, lockout policy)  
- 📧 Email OTP system for password recovery  
- ⚔️ Attack identification (DoS, Port Scan, Brute Force, SYN Flood, ICMP Flood, etc.)  
- 🌐 Cross-platform deployment (Windows, Linux, Kali, Ubuntu)  

---

## ⚙️ Installation Guide  

### 1. Clone Repository  
```bash
git clone <repo-link>
cd CyberSentinel
```

### 2. Install Dependencies  
Windows:  
```bash
install.bat
```

Linux / macOS:  
```bash
chmod +x install.sh
./install.sh
```

### 3. Setup Wizard  
On first launch, create your **admin account** with email & password.  

### 4. Auto Start  
CyberSentinel registers as a **startup service** and runs automatically on boot.  

### 5. Access Dashboard  
Open browser:  
```
http://127.0.0.1:5000
```

Login → Monitor live traffic & alerts.  

---

## 🧪 Testing Results  
- **Accuracy:** 99.92%  
- **Precision:** 99.95%  
- **Recall:** 99.89%  
- **False Positive Rate:** <1%  
- **Detection Speed:** <50ms  

Attack Simulation:  
- SYN Flood → Auto-blocked  
- ICMP Flood → Auto-blocked  
- UDP Flood → Alerted  
- Port Scan → Flagged  
- Normal Browsing → Passed  

---

## 🌍 Deployment Targets  
- Banks & Finance  
- Hospitals & IoT Medical Devices  
- Government Portals  
- Universities & Research Labs  
- Telecom Networks  
- SMEs & Enterprises  

---
## 👨‍💻 Authors  
**Malik Taha**  
Cybersecurity Analyst
GitHub: MalikTaha8331 [(github.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fgithub.com%2FMalikTaha8331")  

---

## ⚔️ License  
This project is released under the **MIT License** — free to use, modify, and distribute.  



