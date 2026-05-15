import os
import sys
import subprocess
import platform

print("""
╔══════════════════════════════════════════════════╗
║     AI-IDS/IPS — Automated Setup Installer      ║
║     AI-Powered Intrusion Detection System       ║
╚══════════════════════════════════════════════════╝
""")

OS = platform.system()

# ─── Step 1: Install Requirements ─────────────────
print("📦 Step 1: Installing required packages...")
packages = [
    'pandas', 'numpy', 'scikit-learn', 'matplotlib',
    'seaborn', 'flask', 'flask-cors', 'joblib',
    'tensorflow', 'scapy', 'imbalanced-learn',
    'requests', 'scipy'
]

if OS == 'Linux':
    subprocess.run([
        sys.executable, '-m', 'pip', 'install',
        '--break-system-packages'
    ] + packages)
else:
    subprocess.run([
        sys.executable, '-m', 'pip', 'install'
    ] + packages)

print("✅ Packages installed!\n")

# ─── Step 2: Check Model exists ───────────────────
print("🤖 Step 2: Checking ML model...")
if not os.path.exists('models/best_model.pkl'):
    print("⚠️  Model not found in models/ folder!")
    print("   Please copy models/ folder from USB or Google Drive")
    print("   Then run setup.py again")
    sys.exit(1)
else:
    print("✅ Model found!\n")

# ─── Step 3: Check Data exists ────────────────────
print("📊 Step 3: Checking processed data...")
if not os.path.exists('data/processed/X_test.csv'):
    print("⚠️  Processed data not found!")
    print("   Please copy data/processed/ folder")
    print("   Then run setup.py again")
    sys.exit(1)
else:
    print("✅ Data found!\n")

# ─── Step 4: Register as Startup Service ──────────
print("⚙️  Step 4: Registering AI-IDS as startup service...")

if OS == 'Windows':
    # Windows startup via registry
    import winreg
    key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path, 0,
            winreg.KEY_SET_VALUE
        )
        app_path = os.path.abspath('start_ids.py')
        winreg.SetValueEx(
            key, 'AI-IDS', 0,
            winreg.REG_SZ,
            f'pythonw "{app_path}"'
        )
        winreg.CloseKey(key)
        print("✅ Registered in Windows startup!\n")
    except Exception as e:
        print(f"⚠️  Could not register startup: {e}")
        print("   Run setup.py as Administrator!\n")

elif OS == 'Linux':
    # Linux startup via systemd service
    service = f"""[Unit]
Description=AI-IDS Intrusion Detection System
After=network.target

[Service]
Type=simple
User={os.getenv('USER')}
WorkingDirectory={os.path.abspath('.')}
ExecStart={sys.executable} {os.path.abspath('start_ids.py')}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    service_path = '/etc/systemd/system/ai-ids.service'
    try:
        with open('/tmp/ai-ids.service', 'w') as f:
            f.write(service)
        subprocess.run(['sudo', 'cp', '/tmp/ai-ids.service', service_path])
        subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
        subprocess.run(['sudo', 'systemctl', 'enable', 'ai-ids'])
        print("✅ Registered as Linux systemd service!\n")
    except Exception as e:
        print(f"⚠️  Could not register service: {e}")

# ─── Step 5: Done ─────────────────────────────────
print("""
╔══════════════════════════════════════════════════╗
║            ✅ SETUP COMPLETE!                   ║
╠══════════════════════════════════════════════════╣
║  AI-IDS will now start automatically on boot!   ║
║                                                  ║
║  Manual start:  python start_ids.py             ║
║  Dashboard:     http://127.0.0.1:5000           ║
║  Live Traffic:  http://127.0.0.1:5000/live      ║
╚══════════════════════════════════════════════════╝
""")