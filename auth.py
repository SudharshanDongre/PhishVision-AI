"""
PhishVision Authentication Module
Talks to the deployed Render API instead of local files.
"""
import requests
import secrets
import re
import os
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURATION — points to your live Render API
# ============================================================================
API_BASE_URL = os.getenv("API_BASE_URL", "https://phishvision-ai.onrender.com")

# In-memory session store (works fine for Streamlit)
_sessions = {}

# ============================================================================
# PASSWORD STRENGTH (keep as-is, no API needed)
# ============================================================================
def check_password_strength(password: str) -> dict:
    strength = {"score": 0, "level": "Very Weak", "feedback": []}
    if len(password) >= 8: strength["score"] += 1
    if len(password) >= 12: strength["score"] += 1
    if len(password) >= 16: strength["score"] += 1
    if re.search(r'[a-z]', password): strength["score"] += 1
    if re.search(r'[A-Z]', password): strength["score"] += 1
    if re.search(r'[0-9]', password): strength["score"] += 1
    if re.search(r'[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]', password): strength["score"] += 1
    if strength["score"] <= 2: strength["level"] = "Very Weak"
    elif strength["score"] <= 4: strength["level"] = "Weak"
    elif strength["score"] <= 6: strength["level"] = "Good"
    elif strength["score"] <= 8: strength["level"] = "Strong"
    else: strength["level"] = "Very Strong"
    if len(password) < 12: strength["feedback"].append("Consider using 12+ characters")
    return strength

# ============================================================================
# USER MANAGEMENT — calls Render API
# ============================================================================
def register_user(username: str, email: str, password: str):
    """Register via Render API. Returns (success, message)."""
    try:
        resp = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"email": email, "full_name": username, "password": password},
            timeout=15
        )
        data = resp.json()
        if resp.status_code == 200 and data.get("success"):
            return True, "Account created successfully"
        return False, data.get("detail", data.get("message", "Registration failed"))
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server. Please try again."
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def authenticate_user(username: str, password: str):
    """Login via Render API. Returns (success, message)."""
    try:
        # Try login with username as email first, then as full_name lookup
        resp = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": username, "password": password},
            timeout=15
        )
        data = resp.json()
        if resp.status_code == 200 and data.get("success"):
            return True, "Authentication successful"
        return False, data.get("detail", "Invalid credentials")
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server. Please try again."
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def get_user(username: str):
    """Get user info from Render API."""
    try:
        resp = requests.get(f"{API_BASE_URL}/auth/user/{username}", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "username": data.get("full_name", username),
                "email": data.get("email", ""),
                "created_at": data.get("created_at", ""),
                "last_login": "",
                "profile": {"full_name": data.get("full_name", ""), "bio": ""}
            }
    except:
        pass
    return None

def update_user_profile(username: str, full_name: str, bio: str) -> bool:
    try:
        resp = requests.post(
            f"{API_BASE_URL}/auth/update",
            params={"email": username},
            json={"full_name": full_name},
            timeout=10
        )
        return resp.status_code == 200
    except:
        return False

def change_password(username: str, old_password: str, new_password: str):
    try:
        resp = requests.post(
            f"{API_BASE_URL}/auth/update",
            params={"email": username},
            json={"password": new_password},
            timeout=10
        )
        if resp.status_code == 200:
            return True, "Password changed successfully"
        return False, "Failed to change password"
    except Exception as e:
        return False, str(e)

# ============================================================================
# SESSION MANAGEMENT — in-memory (no files needed)
# ============================================================================
def create_session(username: str, remember_me: bool = False) -> str:
    token = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(days=30 if remember_me else 1)
    _sessions[token] = {"username": username, "expires_at": expiry}
    return token

def validate_session(token: str):
    if not token or token not in _sessions:
        return False, ""
    session = _sessions[token]
    if datetime.now() > session["expires_at"]:
        del _sessions[token]
        return False, ""
    return True, session["username"]

def invalidate_session(token: str) -> bool:
    if token in _sessions:
        del _sessions[token]
        return True
    return False