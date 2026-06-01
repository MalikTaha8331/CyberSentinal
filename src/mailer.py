import smtplib
import random
import string
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── Email Configuration ──────────────────────────
SENDER_EMAIL    = 'cybersentinel.ids@gmail.com'
SENDER_PASSWORD = 'afgs iswi ktjk fddo'  # ← paste your 16-char app password here
SENDER_NAME     = 'CyberSentinel Security'

# ─── OTP Storage ──────────────────────────────────
# Format: {email: {'otp': '123456', 'expires': timestamp}}
otp_store = {}
OTP_EXPIRY = 300  # 5 minutes

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def store_otp(email, otp):
    """Store OTP with expiry time"""
    otp_store[email] = {
        'otp':     otp,
        'expires': time.time() + OTP_EXPIRY
    }

def verify_otp(email, otp):
    """Verify OTP is correct and not expired"""
    if email not in otp_store:
        return False, 'OTP not found — please request a new one'
    record = otp_store[email]
    if time.time() > record['expires']:
        del otp_store[email]
        return False, 'OTP expired — please request a new one'
    if record['otp'] != otp:
        return False, 'Invalid OTP — please try again'
    del otp_store[email]
    return True, 'OTP verified successfully'

def send_otp_email(to_email, username, otp):
    """Send OTP email for password reset"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔐 CyberSentinel — Password Reset OTP'
        msg['From']    = f'{SENDER_NAME} <{SENDER_EMAIL}>'
        msg['To']      = to_email

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #05050f;
                    color: #e0e0ff;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 500px;
                    margin: 40px auto;
                    background: #0d0d1f;
                    border: 1px solid #9d4edd;
                    border-radius: 16px;
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #1a0a2e, #0d0d1f);
                    padding: 30px;
                    text-align: center;
                    border-bottom: 1px solid #9d4edd;
                }}
                .header h1 {{
                    color: #ffd700;
                    font-size: 1.8rem;
                    margin: 0;
                    letter-spacing: 3px;
                }}
                .header p {{
                    color: #8888aa;
                    margin: 8px 0 0 0;
                    font-size: 0.85rem;
                    letter-spacing: 1px;
                }}
                .body {{
                    padding: 30px;
                    text-align: center;
                }}
                .body p {{
                    color: #aaaacc;
                    font-size: 0.95rem;
                    line-height: 1.6;
                }}
                .otp-box {{
                    background: rgba(157,78,221,0.15);
                    border: 2px solid #9d4edd;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 24px 0;
                    box-shadow: 0 0 20px rgba(157,78,221,0.3);
                }}
                .otp-code {{
                    font-size: 3rem;
                    font-weight: 900;
                    color: #ffd700;
                    letter-spacing: 8px;
                    font-family: monospace;
                    text-shadow: 0 0 10px rgba(255,215,0,0.5);
                }}
                .expiry {{
                    color: #ff2255;
                    font-size: 0.82rem;
                    margin-top: 8px;
                }}
                .warning {{
                    color: #8888aa;
                    font-size: 0.78rem;
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #2d1b69;
                }}
                .footer {{
                    background: #080818;
                    padding: 16px;
                    text-align: center;
                    color: #555577;
                    font-size: 0.75rem;
                    letter-spacing: 1px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚔️ CyberSentinel</h1>
                    <p>AI-POWERED INTRUSION PREVENTION SYSTEM</p>
                </div>
                <div class="body">
                    <p>Hello <strong style="color:#9d4edd">{username}</strong>,</p>
                    <p>You requested a password reset for your CyberSentinel account.
                       Use the OTP below to reset your password:</p>
                    <div class="otp-box">
                        <div class="otp-code">{otp}</div>
                        <div class="expiry">⏱️ Expires in 5 minutes</div>
                    </div>
                    <p>Enter this code on the verification page to continue.</p>
                    <div class="warning">
                        If you did not request this, please ignore this email.
                        Your account is safe. Never share this OTP with anyone.
                    </div>
                </div>
                <div class="footer">
                    © 2026 CyberSentinel — AI Security System
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"✅ OTP email sent to {to_email}")
        return True, 'OTP sent successfully'

    except Exception as e:
        print(f"❌ Email error: {e}")
        return False, f'Failed to send email: {str(e)}'

def send_welcome_email(to_email, username):
    """Send welcome email after successful setup"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🛡️ Welcome to CyberSentinel!'
        msg['From']    = f'{SENDER_NAME} <{SENDER_EMAIL}>'
        msg['To']      = to_email

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #05050f;
                    color: #e0e0ff;
                    margin: 0; padding: 0;
                }}
                .container {{
                    max-width: 500px;
                    margin: 40px auto;
                    background: #0d0d1f;
                    border: 1px solid #9d4edd;
                    border-radius: 16px;
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #1a0a2e, #0d0d1f);
                    padding: 30px;
                    text-align: center;
                    border-bottom: 1px solid #ffd700;
                }}
                .header h1 {{ color: #ffd700; font-size: 1.8rem;
                              margin: 0; letter-spacing: 3px; }}
                .body {{ padding: 30px; text-align: center; }}
                .body p {{ color: #aaaacc; font-size: 0.95rem; line-height: 1.6; }}
                .info-box {{
                    background: rgba(0,255,136,0.1);
                    border: 1px solid #00ff88;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 20px 0;
                    text-align: left;
                }}
                .info-box p {{ color: #00ff88; margin: 6px 0; font-size: 0.88rem; }}
                .footer {{
                    background: #080818;
                    padding: 16px;
                    text-align: center;
                    color: #555577;
                    font-size: 0.75rem;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚔️ CyberSentinel</h1>
                </div>
                <div class="body">
                    <p>Welcome <strong style="color:#ffd700">{username}</strong>! 🎉</p>
                    <p>Your CyberSentinel account has been created successfully.
                       Your network is now protected by AI!</p>
                    <div class="info-box">
                        <p>✅ Account created successfully</p>
                        <p>✅ ML Model: Random Forest (99.92% accuracy)</p>
                        <p>✅ Real-time threat detection: Active</p>
                        <p>✅ Auto-blocking: Enabled</p>
                        <p>✅ Dashboard: http://127.0.0.1:5000</p>
                    </div>
                    <p>Your network is now being monitored 24/7!</p>
                </div>
                <div class="footer">
                    © 2026 CyberSentinel — AI Security System
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"✅ Welcome email sent to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Welcome email error: {e}")
        return False


def send_attack_alert(to_email, username, attack_data):
    """Send immediate email alert when severe attack detected"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'SEVERE THREAT DETECTED — CyberSentinel Alert'
        msg['From']    = f'{SENDER_NAME} <{SENDER_EMAIL}>'
        msg['To']      = to_email

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background: #05050f; color: #e0e0ff; margin: 0; padding: 0; }}
                .container {{ max-width: 500px; margin: 40px auto; background: #0d0d1f; border: 1px solid #ff2255; border-radius: 16px; overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #2e0a0a, #0d0d1f); padding: 30px; text-align: center; border-bottom: 1px solid #ff2255; }}
                .header h1 {{ color: #ff2255; font-size: 1.6rem; margin: 0; letter-spacing: 3px; }}
                .header p  {{ color: #8888aa; margin: 8px 0 0 0; font-size: 0.85rem; }}
                .body {{ padding: 30px; }}
                .alert-box {{ background: rgba(255,34,85,0.1); border: 2px solid #ff2255; border-radius: 12px; padding: 20px; margin: 20px 0; }}
                .alert-box h2 {{ color: #ff2255; margin: 0 0 16px 0; font-size: 1.2rem; }}
                .info-row {{ display: flex; justify-content: space-between; margin: 8px 0; padding: 6px 0; border-bottom: 1px solid #2d1b69; }}
                .info-label {{ color: #8888aa; font-size: 0.88rem; }}
                .info-value {{ color: #ffffff; font-size: 0.88rem; font-weight: bold; }}
                .action-box {{ background: rgba(157,78,221,0.1); border: 1px solid #9d4edd; border-radius: 8px; padding: 16px; margin-top: 20px; text-align: center; }}
                .footer {{ background: #080818; padding: 16px; text-align: center; color: #555577; font-size: 0.75rem; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>SEVERE THREAT DETECTED</h1>
                    <p>CyberSentinel AI-IDS/IPS — Immediate Action Required</p>
                </div>
                <div class="body">
                    <p style="color:#aaaacc">Hello <strong style="color:#9d4edd">{username}</strong>,</p>
                    <p style="color:#aaaacc">A severe threat has been detected and automatically blocked on your network!</p>
                    <div class="alert-box">
                        <h2>Threat Details</h2>
                        <div class="info-row">
                            <span class="info-label">Category:</span>
                            <span class="info-value" style="color:#ff2255">{attack_data.get('category', 'SEVERE THREAT')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Attack Type:</span>
                            <span class="info-value">{attack_data.get('attack_type', 'Unknown')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Source IP:</span>
                            <span class="info-value" style="color:#ff2255">{attack_data.get('src_ip', 'Unknown')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Confidence:</span>
                            <span class="info-value">{attack_data.get('confidence', 0)}%</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Protocol:</span>
                            <span class="info-value">{attack_data.get('protocol', 'TCP')}</span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Time:</span>
                            <span class="info-value">{attack_data.get('time', 'Unknown')}</span>
                        </div>
                        <div class="info-row" style="border:none">
                            <span class="info-label">Status:</span>
                            <span class="info-value" style="color:#00ff88">AUTO-BLOCKED</span>
                        </div>
                    </div>
                    <div class="action-box">
                        <p style="color:#9d4edd; margin:0; font-weight:bold">
                            The threat has been automatically blocked.
                            Login to your dashboard to review and manage blocked IPs.
                        </p>
                    </div>
                </div>
                <div class="footer">
                    CyberSentinel AI-IDS/IPS — Protecting Your Network 24/7
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"Attack alert email sent to {to_email}")
        return True

    except Exception as e:
        print(f"Attack alert email error: {e}")
        return False