import joblib
import numpy as np
import os
from features import FEATURE_NAMES, PROTOCOL_TYPES, SERVICE_TYPES, FLAG_TYPES

# Load model once when server starts
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'best_model.pkl')
model = joblib.load(MODEL_PATH)

def encode_features(data):
    """Encode categorical features to numbers"""
    data['protocol_type'] = PROTOCOL_TYPES.get(data['protocol_type'], 0)
    data['service']       = SERVICE_TYPES.get(data['service'], 42)
    data['flag']          = FLAG_TYPES.get(data['flag'], 9) 
    
import joblib
import numpy as np
import os
from features import FEATURE_NAMES, PROTOCOL_TYPES, SERVICE_TYPES, FLAG_TYPES

# Load model once when server starts
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'best_model.pkl')
model = joblib.load(MODEL_PATH)

def encode_features(data):
    """Encode categorical features to numbers"""
    data['protocol_type'] = PROTOCOL_TYPES.get(data['protocol_type'], 0)
    data['service']       = SERVICE_TYPES.get(data['service'], 42)
    data['flag']          = FLAG_TYPES.get(data['flag'], 9)
    return data

def identify_attack_type(data):
    """Identify specific attack type from traffic features"""
    try:
        flag        = data.get('flag', 'SF')
        protocol    = data.get('protocol_type', 'tcp')
        service     = data.get('service', 'other')
        src_bytes   = float(data.get('src_bytes', 0))
        dst_bytes   = float(data.get('dst_bytes', 0))
        count       = float(data.get('count', 0))
        serror_rate = float(data.get('serror_rate', 0))
        rerror_rate = float(data.get('rerror_rate', 0))
        logged_in   = float(data.get('logged_in', 0))
        hot         = float(data.get('hot', 0))
        num_failed  = float(data.get('num_failed_logins', 0))
        root_shell  = float(data.get('root_shell', 0))
        num_shells  = float(data.get('num_shells', 0))
        dst_host_count = float(data.get('dst_host_count', 0))

        # DoS Attack — high connection count + SYN errors
        if serror_rate > 0.7 and count > 100:
            return 'DoS Attack', '💥'

        # Port Scan — many different services probed
        if dst_host_count > 200 and serror_rate > 0.5 and src_bytes < 100:
            return 'Port Scan', '🔍'

        # Probe Attack — systematic scanning
        if rerror_rate > 0.5 and count > 50:
            return 'Probe Attack', '🕵️'

        # Brute Force — many failed logins
        if num_failed > 3 or (logged_in == 0 and count > 20 and service in ['ssh', 'ftp', 'telnet']):
            return 'Brute Force', '🔨'

        # Privilege Escalation
        if root_shell == 1 or num_shells > 0:
            return 'Privilege Escalation', '⚡'

        # R2L Attack — remote to local
        if logged_in == 0 and hot > 0 and src_bytes > 1000:
            return 'R2L Attack', '🌐'

        # SYN Flood
        if flag == 'S0' and count > 200:
            return 'SYN Flood', '🌊'

        # UDP Flood
        if protocol == 'udp' and count > 100 and src_bytes < 50:
            return 'UDP Flood', '🌊'

        # ICMP Flood
        if protocol == 'icmp' and count > 100:
            return 'ICMP Flood', '📡'

        # FTP Attack
        if service == 'ftp' and logged_in == 0:
            return 'FTP Attack', '📁'

        # SSH Attack
        if service == 'ssh' and logged_in == 0:
            return 'SSH Attack', '🔐'

        # Generic Attack
        return 'Network Attack', '🚨'

    except Exception:
        return 'Unknown Attack', '❓'


def get_threat_category(prediction, confidence, data={}):
    """Classify threat based on prediction and confidence score"""
    try:
        prediction = int(prediction)
        confidence = float(confidence)

        if prediction == 0:
            return {
                'category':     'NORMAL',
                'attack_type':  'Normal Traffic',
                'attack_icon':  '✅',
                'level':        0,
                'color':        'green',
                'auto_block':   False,
                'show_block':   False,
                'description':  'Traffic appears normal'
            }

        # Identify specific attack type
        attack_name, attack_icon = identify_attack_type(data)

        if confidence < 55:
            return {
                'category':     'SUSPICIOUS',
                'attack_type':  attack_name,
                'attack_icon':  attack_icon,
                'level':        1,
                'color':        'gray',
                'auto_block':   False,
                'show_block':   True,
                'description':  f'Suspicious activity detected — possible {attack_name}'
            }
        elif confidence <= 75:
            return {
                'category':     'MODERATE THREAT',
                'attack_type':  attack_name,
                'attack_icon':  attack_icon,
                'level':        2,
                'color':        'yellow',
                'auto_block':   False,
                'show_block':   True,
                'description':  f'{attack_name} detected — admin action recommended'
            }
        else:
            return {
                'category':     'SEVERE THREAT',
                'attack_type':  attack_name,
                'attack_icon':  attack_icon,
                'level':        3,
                'color':        'red',
                'auto_block':   True,
                'show_block':   False,
                'description':  f'{attack_name} detected — auto-blocked immediately!'
            }

    except Exception as e:
        return {
            'category':     'UNKNOWN',
            'attack_type':  'Unknown',
            'attack_icon':  '❓',
            'level':        0,
            'color':        'gray',
            'auto_block':   False,
            'show_block':   False,
            'description':  f'Classification error: {str(e)}'
        }

def predict_traffic(data):
    """Take raw feature dict and return prediction + threat category"""
    try:
        # Make a copy to avoid modifying original
        data_copy = dict(data)

        # Encode categorical values
        data_copy = encode_features(data_copy)

        # Build feature vector in correct order
        features = np.array([[data_copy.get(f, 0) for f in FEATURE_NAMES]])

        # Get prediction and confidence
        prediction  = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        confidence  = round(float(max(probability)) * 100, 2)

        # Get threat category
        threat = get_threat_category(int(prediction), confidence, data)

        return {
            'prediction':  int(prediction),
            'label':       'ATTACK' if prediction == 1 else 'NORMAL',
            'confidence':  confidence,
            'category':    threat['category'],
            'attack_type': threat['attack_type'],
            'attack_icon': threat['attack_icon'],
            'level':       threat['level'],
            'color':       threat['color'],
            'auto_block':  threat['auto_block'],
            'show_block':  threat['show_block'],
            'description': threat['description']
        }
    except Exception as e:
        return {
            'prediction':  0,
            'label':       'ERROR',
            'confidence':  0,
            'category':    'UNKNOWN',
            'level':       0,
            'color':       'gray',
            'auto_block':  False,
            'show_block':  False,
            'description': str(e)
        }