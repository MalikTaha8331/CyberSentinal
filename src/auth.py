import bcrypt
import logging
import os
import time
from collections import defaultdict
from functools import wraps
from flask import session, jsonify, request

# ─── Logging Setup ────────────────────────────────
os.makedirs('../logs', exist_ok=True)
logging.basicConfig(
    filename='../logs/cybersentinel.log',
    level=logging.WARNING,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# ─── Admin Credentials ────────────────────────────
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'cybersentinel123'  

# ─── Secret Key ───────────────────────────────────
SECRET_KEY = 'cybersentinel-secure-key-2026-xK9mP'

# ─── Brute Force Protection ───────────────────────
failed_attempts = defaultdict(list)
BLOCK_DURATION  = 300  # 5 minutes
MAX_ATTEMPTS    = 5

def is_blocked(ip):
    now      = time.time()
    attempts = [t for t in failed_attempts[ip] if now - t < BLOCK_DURATION]
    failed_attempts[ip] = attempts
    return len(attempts) >= MAX_ATTEMPTS

def record_failed(ip, username):
    failed_attempts[ip].append(time.time())
    attempts = len(failed_attempts[ip])
    logging.warning(
        f"Failed login | IP: {ip} | "
        f"Username: {username} | "
        f"Attempt: {attempts}/{MAX_ATTEMPTS}"
    )
    print(f"⚠️  Failed login from {ip} — attempt {attempts}/{MAX_ATTEMPTS}")

def get_remaining_attempts(ip):
    now      = time.time()
    attempts = [t for t in failed_attempts[ip] if now - t < BLOCK_DURATION]
    return MAX_ATTEMPTS - len(attempts)

def check_credentials(username, password):
    """Verify credentials using bcrypt"""
    try:
        if username != ADMIN_USERNAME:
            return False
        # Hash and compare
        hashed = bcrypt.hashpw(
            ADMIN_PASSWORD.encode('utf-8'),
            bcrypt.gensalt()
        )
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed
        )
    except Exception as e:
        print(f"Auth error: {e}")
        # Fallback to plain comparison
        return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

# ─── Login Required Decorator ─────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated