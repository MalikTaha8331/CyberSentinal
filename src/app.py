from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from predict import predict_traffic
from auth import (check_credentials, SECRET_KEY, is_blocked,
                  record_failed, get_remaining_attempts, login_required)
import time
import os
import logging
import json
import subprocess
import sys
from datetime import datetime

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)
CORS(app)
app.secret_key = SECRET_KEY

# ─── Rate Limiter ─────────────────────────────────
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5000 per day", "1000 per hour"]
)

# ─── Security Headers ─────────────────────────────
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options']    = 'nosniff'
    response.headers['X-Frame-Options']           = 'DENY'
    response.headers['X-XSS-Protection']          = '1; mode=block'
    response.headers['Content-Security-Policy']   = (
        "default-src 'self' 'unsafe-inline' 'unsafe-eval' "
        "cdnjs.cloudflare.com cdn.jsdelivr.net "
        "fonts.googleapis.com fonts.gstatic.com"
    )
    return response

# ─── In-Memory Storage ────────────────────────────
alerts      = []
blocked_ips = {}

# ─── Live Traffic Rolling Buffer ──────────────────
live_traffic    = []
MAX_TRAFFIC     = 400   # Rolling buffer size
traffic_cleared = 0     # Count how many times buffer was cleared

# ─── Historical Logs ──────────────────────────────
LOGS_FILE = '../logs/alerts_history.json'

def load_logs():
    """Load historical logs from file"""
    try:
        if os.path.exists(LOGS_FILE):
            with open(LOGS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_log(alert):
    """Save single alert to history file"""
    try:
        os.makedirs('../logs', exist_ok=True)
        history = load_logs()
        history.append(alert)
        if len(history) > 10000:
            history = history[-10000:]
        with open(LOGS_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Log save error: {e}")

# ─── Auth Routes ──────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    from user_store import is_setup_done, verify_user

    if not is_setup_done():
        return redirect(url_for('setup'))

    if session.get('logged_in'):
        return redirect(url_for('index'))

    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        ip       = request.remote_addr

        if is_blocked(ip):
            error = 'Too many failed attempts! You are blocked for 5 minutes.'
            logging.warning(f"Blocked IP tried to login: {ip}")

        elif verify_user(username, password):
            session['logged_in'] = True
            session['username']  = username
            logging.warning(f"Successful login | IP: {ip} | User: {username}")
            print(f"Admin logged in from {ip}")
            return redirect(url_for('index'))

        else:
            record_failed(ip, username)
            attempts = get_remaining_attempts(ip)
            if attempts <= 0:
                error = 'Too many failed attempts! Blocked for 5 minutes.'
            else:
                error = f'Invalid credentials! {attempts} attempts remaining.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    username = session.get('username', 'unknown')
    ip       = request.remote_addr
    session.clear()
    logging.warning(f"Logout | IP: {ip} | User: {username}")
    print(f"Admin logged out from {ip}")
    return redirect(url_for('login'))

# ─── Main Routes ──────────────────────────────────
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/live')
def live_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('live.html')

# ─── API Routes ───────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data   = request.get_json()
        result = predict_traffic(data)

        src_ip = data.get('src_ip', f"192.168.1.{len(alerts) % 255 + 1}")

        alert = {
            'time':        time.strftime('%H:%M:%S'),
            'label':       result['label'],
            'category':    result['category'],
            'confidence':  result['confidence'],
            'color':       result['color'],
            'auto_block':  result['auto_block'],
            'show_block':  result['show_block'],
            'description': result['description'],
            'src_bytes':   data.get('src_bytes', 0),
            'protocol':    data.get('protocol_type', 'tcp'),
            'src_ip':      src_ip,
            'blocked':     False
        }

        if result['auto_block']:
            blocked_ips[src_ip] = {
                'time':       time.strftime('%H:%M:%S'),
                'reason':     result['category'],
                'confidence': result['confidence']
            }
            alert['blocked'] = True
            print(f"AUTO-BLOCKED: {src_ip} — {result['category']} ({result['confidence']}%)")
            logging.warning(f"AUTO-BLOCKED: {src_ip} | {result['category']} | {result['confidence']}%")

        # Send email alert
        try:
            from mailer import send_attack_alert
            from user_store import load_user
            user = load_user()
            if user:
                attack_data = {
                    'category':    result['category'],
                    'attack_type': result.get('attack_type', 'Unknown'),
                    'src_ip':      src_ip,
                    'confidence':  result['confidence'],
                    'protocol':    data.get('protocol_type', 'TCP'),
                    'time':        time.strftime('%H:%M:%S')
                }
                import threading
                threading.Thread(
                    target=send_attack_alert,
                    args=(user['email'], user['username'], attack_data),
                    daemon=True
                ).start()
        except Exception as email_err:
            print(f"Email alert error: {email_err}")

        alerts.append(alert)
        if len(alerts) > 100:
            alerts.pop(0)

        log_entry = {
            **alert,
            'date':        datetime.now().strftime('%Y-%m-%d'),
            'attack_type': result.get('attack_type', 'Unknown'),
            'attack_icon': result.get('attack_icon', '')
        }
        save_log(log_entry)

        result['src_ip']  = src_ip
        result['blocked'] = alert['blocked']
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts[-50:])

@app.route('/stats', methods=['GET'])
def get_stats():
    total        = len(alerts)
    attacks      = sum(1 for a in alerts if a['label'] == 'ATTACK')
    severe       = sum(1 for a in alerts if a['category'] == 'SEVERE THREAT')
    moderate     = sum(1 for a in alerts if a['category'] == 'MODERATE THREAT')
    suspicious   = sum(1 for a in alerts if a['category'] == 'SUSPICIOUS')
    auto_blocked = sum(1 for a in alerts if a['blocked'])
    return jsonify({
        'total':        total,
        'attacks':      attacks,
        'normal':       total - attacks,
        'severe':       severe,
        'moderate':     moderate,
        'suspicious':   suspicious,
        'auto_blocked': auto_blocked,
        'blocked_ips':  len(blocked_ips)
    })

@app.route('/block', methods=['POST'])
@login_required
def block_ip():
    data = request.get_json()
    ip   = data.get('ip')
    if not ip:
        return jsonify({'error': 'No IP provided'}), 400
    blocked_ips[ip] = {
        'time':       time.strftime('%H:%M:%S'),
        'reason':     'Manual block by admin',
        'confidence': data.get('confidence', 0)
    }
    logging.warning(f"MANUAL BLOCK: {ip} by admin")
    print(f"MANUAL BLOCK: {ip}")
    return jsonify({'success': True, 'message': f'IP {ip} blocked successfully'})

@app.route('/unblock', methods=['POST'])
@login_required
def unblock_ip():
    data = request.get_json()
    ip   = data.get('ip')
    if ip in blocked_ips:
        del blocked_ips[ip]
        logging.warning(f"UNBLOCKED: {ip} by admin")
        print(f"UNBLOCKED: {ip}")
        return jsonify({'success': True, 'message': f'IP {ip} unblocked'})
    return jsonify({'error': 'IP not found'}), 404

@app.route('/blocked', methods=['GET'])
def get_blocked():
    return jsonify(blocked_ips)

# ─── Live Traffic — Rolling Buffer ────────────────
@app.route('/traffic', methods=['POST'])
def add_traffic():
    global live_traffic, traffic_cleared
    try:
        data = request.get_json()
        live_traffic.append(data)

        # Rolling buffer — when full, clear and start fresh
        if len(live_traffic) >= MAX_TRAFFIC:
            traffic_cleared += 1
            live_traffic = []
            print(f"Buffer cleared (cycle {traffic_cleared}) — starting fresh")

        return jsonify({
            'success':  True,
            'count':    len(live_traffic),
            'max':      MAX_TRAFFIC,
            'cleared':  traffic_cleared
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/traffic', methods=['GET'])
@limiter.exempt
def get_traffic():
    protocol = request.args.get('protocol', '')
    service  = request.args.get('service',  '')
    category = request.args.get('category', '')

    filtered = live_traffic

    if protocol:
        filtered = [t for t in filtered if t.get('protocol', '').lower() == protocol.lower()]
    if service:
        filtered = [t for t in filtered if t.get('service',  '').lower() == service.lower()]
    if category:
        filtered = [t for t in filtered if t.get('category', '').lower() == category.lower()]

    return jsonify({
        'data':    filtered,
        'count':   len(live_traffic),
        'max':     MAX_TRAFFIC,
        'cleared': traffic_cleared
    })

# ─── Setup Wizard ─────────────────────────────────
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    from user_store import is_setup_done, save_user
    from mailer import send_welcome_email

    if is_setup_done():
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        name             = request.form.get('name', '').strip()
        email            = request.form.get('email', '').strip()
        username         = request.form.get('username', '').strip()
        password         = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not all([name, email, username, password, confirm_password]):
            error = 'All fields are required!'
        elif password != confirm_password:
            error = 'Passwords do not match!'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters!'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters!'
        else:
            if save_user(username, password, email, name):
                send_welcome_email(email, username)
                session['logged_in'] = True
                session['username']  = username
                print(f"Setup complete! User: {username}")
                return redirect(url_for('index'))
            else:
                error = 'Failed to save user — please try again!'

    return render_template('setup.html', error=error)

# ─── Forgot Password ──────────────────────────────
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    from user_store import get_email, load_user
    from mailer import send_otp_email, generate_otp, store_otp

    error   = None
    success = None

    if request.method == 'POST':
        email        = request.form.get('email', '').strip()
        stored_email = get_email()

        if not email:
            error = 'Please enter your email address!'
        elif email != stored_email:
            error = 'Email not found in our records!'
        else:
            otp      = generate_otp()
            store_otp(email, otp)
            user     = load_user()
            username = user['username'] if user else 'User'
            sent, msg = send_otp_email(email, username, otp)
            if sent:
                return render_template('otp.html', email=email, error=None, success=None)
            else:
                error = f'Failed to send OTP: {msg}'

    return render_template('forgot.html', error=error, success=success)

# ─── OTP Verification ─────────────────────────────
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    from mailer import verify_otp as check_otp

    email = request.form.get('email', '').strip()
    otp   = request.form.get('otp',   '').strip()

    if not email or not otp:
        return render_template('otp.html', email=email, error='Please enter the OTP!', success=None)

    valid, msg = check_otp(email, otp)

    if valid:
        session['otp_verified'] = True
        session['reset_email']  = email
        return render_template('reset.html', email=email, error=None)
    else:
        return render_template('otp.html', email=email, error=msg, success=None)

# ─── Reset Password ───────────────────────────────
@app.route('/reset-password', methods=['POST'])
def reset_password():
    from user_store import update_password

    if not session.get('otp_verified'):
        return redirect(url_for('forgot_password'))

    email            = request.form.get('email',            '').strip()
    password         = request.form.get('password',         '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()

    if not password or not confirm_password:
        return render_template('reset.html', email=email, error='All fields are required!')
    if password != confirm_password:
        return render_template('reset.html', email=email, error='Passwords do not match!')
    if len(password) < 8:
        return render_template('reset.html', email=email, error='Password must be at least 8 characters!')

    success, msg = update_password(email, password)
    if success:
        session.pop('otp_verified', None)
        session.pop('reset_email',  None)
        print(f"Password reset for {email}")
        return redirect(url_for('login'))
    else:
        return render_template('reset.html', email=email, error=msg)

# ─── Sniffer Control ──────────────────────────────
sniffer_process = None

@app.route('/sniffer/start', methods=['POST'])
@login_required
def start_sniffer():
    global sniffer_process
    try:
        if sniffer_process and sniffer_process.poll() is None:
            return jsonify({'success': False, 'message': 'Sniffer already running!'})

        sniffer_path = os.path.join(os.path.dirname(__file__), 'sniffer.py')

        sniffer_process = subprocess.Popen(
            [sys.executable, sniffer_path, "auto"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=os.path.dirname(__file__)
        )

        time.sleep(2)

        if sniffer_process.poll() is not None:
            out, _ = sniffer_process.communicate()
            error_msg = out.decode('utf-8', errors='ignore')
            print(f"Sniffer error: {error_msg}")
            return jsonify({'success': False, 'message': f'Sniffer failed: {error_msg[:150]}'})

        print(f"Sniffer started — PID: {sniffer_process.pid}")
        logging.warning(f"Sniffer started | PID: {sniffer_process.pid}")
        return jsonify({'success': True, 'message': 'Sniffer started! Capturing live traffic...'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/sniffer/stop', methods=['POST'])
@login_required
def stop_sniffer():
    global sniffer_process
    try:
        if not sniffer_process or sniffer_process.poll() is not None:
            return jsonify({'success': False, 'message': 'Sniffer is not running!'})

        sniffer_process.terminate()
        sniffer_process = None
        print("Sniffer stopped by admin")
        logging.warning("Sniffer stopped by admin")
        return jsonify({'success': True, 'message': 'Sniffer stopped!'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/sniffer/status', methods=['GET'])
def sniffer_status():
    global sniffer_process
    running = sniffer_process is not None and sniffer_process.poll() is None
    return jsonify({
        'running': running,
        'pid':     sniffer_process.pid if running else None,
        'count':   len(live_traffic),
        'max':     MAX_TRAFFIC
    })

# ─── Historical Logs Routes ───────────────────────
@app.route('/history')
def history_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('history.html')

@app.route('/logs', methods=['GET'])
def get_logs():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    history  = load_logs()
    page     = int(request.args.get('page',     1))
    per_page = int(request.args.get('per_page', 50))
    category = request.args.get('category', '')
    date     = request.args.get('date',     '')
    search   = request.args.get('search',   '').lower()

    if category:
        history = [h for h in history if h.get('category', '') == category]
    if date:
        history = [h for h in history if h.get('date', '') == date]
    if search:
        history = [h for h in history if search in str(h).lower()]

    total     = len(history)
    start     = (page - 1) * per_page
    end       = start + per_page
    paginated = list(reversed(history))[start:end]

    return jsonify({
        'logs':        paginated,
        'total':       total,
        'page':        page,
        'per_page':    per_page,
        'total_pages': (total + per_page - 1) // per_page
    })

@app.route('/logs/clear', methods=['POST'])
@login_required
def clear_logs():
    try:
        with open(LOGS_FILE, 'w') as f:
            json.dump([], f)
        return jsonify({'success': True, 'message': 'Logs cleared!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# ─── PDF Report ───────────────────────────────────
@app.route('/report/pdf', methods=['GET'])
@login_required
def generate_pdf():
    try:
        from pdf_report import generate_report
        from flask import send_file

        stats = {
            'total':        len(alerts),
            'attacks':      sum(1 for a in alerts if a['label'] == 'ATTACK'),
            'normal':       sum(1 for a in alerts if a['label'] == 'NORMAL'),
            'severe':       sum(1 for a in alerts if a['category'] == 'SEVERE THREAT'),
            'moderate':     sum(1 for a in alerts if a['category'] == 'MODERATE THREAT'),
            'suspicious':   sum(1 for a in alerts if a['category'] == 'SUSPICIOUS'),
            'auto_blocked': sum(1 for a in alerts if a['blocked']),
            'blocked_ips':  len(blocked_ips)
        }

        output_path = os.path.join(
            os.path.dirname(__file__),
            '..', 'logs', 'cybersentinel_report.pdf'
        )

        success, result = generate_report(alerts, blocked_ips, stats, output_path)

        if success:
            return send_file(
                result,
                as_attachment=True,
                download_name=f'CyberSentinel_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )
        else:
            return jsonify({'error': result}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
# ─── Error Handlers ───────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(429)
def rate_limited(e):
    return jsonify({'error': 'Too many requests — slow down!'}), 429

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("CyberSentinel Starting...")
    print("Dashboard: http://127.0.0.1:5000")
    print("OWASP Security: Enabled")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)