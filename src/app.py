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
    default_limits=["500 per day", "100 per hour"]
)

# ─── Security Headers ─────────────────────────────
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options']    = 'nosniff'
    response.headers['X-Frame-Options']           = 'DENY'
    response.headers['X-XSS-Protection']          = '1; mode=block'
    response.headers['Content-Security-Policy']   = (
        "default-src 'self' 'unsafe-inline' 'unsafe-eval' "
        "cdnjs.cloudflare.com cdn.jsdelivr.net"
    )
    return response

# ─── In-Memory Storage ────────────────────────────
alerts      = []
blocked_ips = {}
live_traffic = []
MAX_TRAFFIC  = 100000

# ─── Auth Routes ──────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))

    error    = None
    attempts = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        ip       = request.remote_addr

        # Check if IP is blocked
        if is_blocked(ip):
            error = 'Too many failed attempts! You are blocked for 5 minutes.'
            logging.warning(f"Blocked IP tried to login: {ip}")

        elif check_credentials(username, password):
            session['logged_in'] = True
            session['username']  = username
            logging.warning(f"Successful login | IP: {ip} | User: {username}")
            print(f"✅ Admin logged in from {ip}")
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
    print(f"🚪 Admin logged out from {ip}")
    return redirect(url_for('login'))

# ─── Main Routes ──────────────────────────────────
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html',
                           username=session.get('username'))

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
            print(f"🚫 AUTO-BLOCKED: {src_ip} — {result['category']} "
                  f"({result['confidence']}%)")
            logging.warning(f"AUTO-BLOCKED: {src_ip} | "
                          f"{result['category']} | "
                          f"{result['confidence']}%")

        alerts.append(alert)
        if len(alerts) > 100:
            alerts.pop(0)

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
    print(f"🚫 MANUAL BLOCK: {ip}")
    return jsonify({'success': True,
                    'message': f'IP {ip} blocked successfully'})

@app.route('/unblock', methods=['POST'])
@login_required
def unblock_ip():
    data = request.get_json()
    ip   = data.get('ip')
    if ip in blocked_ips:
        del blocked_ips[ip]
        logging.warning(f"UNBLOCKED: {ip} by admin")
        print(f"✅ UNBLOCKED: {ip}")
        return jsonify({'success': True,
                        'message': f'IP {ip} unblocked'})
    return jsonify({'error': 'IP not found'}), 404

@app.route('/blocked', methods=['GET'])
def get_blocked():
    return jsonify(blocked_ips)

@app.route('/traffic', methods=['POST'])
def add_traffic():
    try:
        data = request.get_json()
        live_traffic.append(data)
        if len(live_traffic) > MAX_TRAFFIC:
            live_traffic.pop(0)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/traffic', methods=['GET'])
def get_traffic():
    protocol = request.args.get('protocol', '')
    service  = request.args.get('service',  '')
    category = request.args.get('category', '')

    filtered = live_traffic

    if protocol:
        filtered = [t for t in filtered
                    if t.get('protocol', '').lower() == protocol.lower()]
    if service:
        filtered = [t for t in filtered
                    if t.get('service', '').lower() == service.lower()]
    if category:
        filtered = [t for t in filtered
                    if t.get('category', '').lower() == category.lower()]

    return jsonify(filtered[-500:])

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
    print("⚔️  CyberSentinel Starting...")
    print("📊 Dashboard: http://127.0.0.1:5000")
    print("🔒 OWASP Security: Enabled")
    app.run(debug=True, host='0.0.0.0', port=5000)