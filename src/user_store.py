import json
import os
import bcrypt

# ─── User Data File ───────────────────────────────
USER_FILE = '../data/user.json'

def save_user(username, password, email, name):
    """Save user credentials securely"""
    try:
        os.makedirs('../data', exist_ok=True)
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = {
            'username': username,
            'password': hashed,
            'email':    email,
            'name':     name
        }

        with open(USER_FILE, 'w') as f:
            json.dump(user, f, indent=2)

        print(f"✅ User {username} saved!")
        return True

    except Exception as e:
        print(f"❌ Save user error: {e}")
        return False

def load_user():
    """Load user credentials"""
    try:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"❌ Load user error: {e}")
    return None

def is_setup_done():
    """Check if first time setup is complete"""
    return os.path.exists(USER_FILE)

def verify_user(username, password):
    """Verify login credentials"""
    user = load_user()
    if not user:
        return False
    if user['username'] != username:
        return False
    return bcrypt.checkpw(
        password.encode('utf-8'),
        user['password'].encode('utf-8')
    )

def update_password(email, new_password):
    """Update password after OTP verification"""
    try:
        user = load_user()
        if not user or user['email'] != email:
            return False, 'Email not found!'

        hashed = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user['password'] = hashed

        with open(USER_FILE, 'w') as f:
            json.dump(user, f, indent=2)

        return True, 'Password updated successfully!'

    except Exception as e:
        return False, str(e)

def get_email():
    """Get registered email"""
    user = load_user()
    return user['email'] if user else None

def get_username():
    """Get registered username"""
    user = load_user()
    return user['username'] if user else None