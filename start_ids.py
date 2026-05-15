import subprocess
import sys
import os
import time
import threading
import platform

print("""
╔══════════════════════════════════════════════════╗
║        🛡️  AI-IDS/IPS System Starting...        ║
║     AI-Powered Intrusion Detection System       ║
╚══════════════════════════════════════════════════╝
""")

OS = platform.system()

def start_flask():
    """Start Flask web server"""
    print("🌐 Starting Flask dashboard server...")
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=src_path
    )
    print("✅ Dashboard running at http://127.0.0.1:5000")

def start_sniffer():
    """Start live packet sniffer"""
    print("🔍 Starting live packet sniffer...")
    time.sleep(3)  # Wait for Flask to start first
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    subprocess.Popen(
        [sys.executable, 'sniffer.py'],
        cwd=src_path
    )
    print("✅ Live sniffer running!")

def open_browser():
    """Open dashboard in browser after 5 seconds"""
    time.sleep(5)
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')

# Start everything in threads
t1 = threading.Thread(target=start_flask)
t2 = threading.Thread(target=start_sniffer)
t3 = threading.Thread(target=open_browser)

t1.start()
time.sleep(2)
t2.start()
t3.start()

print("""
╔══════════════════════════════════════════════════╗
║           ✅ AI-IDS IS RUNNING!                 ║
╠══════════════════════════════════════════════════╣
║  Dashboard:    http://127.0.0.1:5000            ║
║  Live Traffic: http://127.0.0.1:5000/live       ║
║                                                  ║
║  The system is now monitoring your network!     ║
║  Browser will open automatically...             ║
╚══════════════════════════════════════════════════╝
""")

# Keep running
try:
    while True:
        time.sleep(60)
        print("🛡️  AI-IDS running... Press Ctrl+C to stop")
except KeyboardInterrupt:
    print("\n⏹ AI-IDS stopped!")