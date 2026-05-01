"""
PhishVision Authentication Module
Handles user registration, login, password hashing, session management,
and form validation.
"""

import bcrypt
import json
import os
import re
from datetime import datetime, timedelta
import hashlib
import secrets

# ============================================================================
# CONFIGURATION
# ============================================================================

USERS_DB_FILE = "users_db.json"
SESSIONS_DB_FILE = "sessions_db.json"
PASSWORD_MIN_LENGTH = 8
SESSION_EXPIRY_HOURS = 24

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_databases():
    """Initialize user and session databases if they don't exist."""
    if not os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, "w") as f:
            json.dump({}, f)
    
    if not os.path.exists(SESSIONS_DB_FILE):
        with open(SESSIONS_DB_FILE, "w") as f:
            json.dump({}, f)


def load_users():
    """Load users from JSON database."""
    init_databases()
    try:
        with open(USERS_DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(users):
    """Save users to JSON database."""
    with open(USERS_DB_FILE, "w") as f:
        json.dump(users, f, indent=4)


def load_sessions():
    """Load sessions from JSON database."""
    init_databases()
    try:
        with open(SESSIONS_DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_sessions(sessions):
    """Save sessions to JSON database."""
    with open(SESSIONS_DB_FILE, "w") as f:
        json.dump(sessions, f, indent=4)


# ============================================================================
# PASSWORD HASHING & VERIFICATION
# ============================================================================

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except:
        return False


# ============================================================================
# PASSWORD VALIDATION & STRENGTH
# ============================================================================

def validate_email(email: str) -> tuple[bool, str]:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, ""


def validate_username(username: str) -> tuple[bool, str]:
    """Validate username format."""
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(username) > 20:
        return False, "Username must be at most 20 characters"
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password meets security requirements."""
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]', password):
        return False, "Password must contain at least one special character"
    return True, ""


def check_password_strength(password: str) -> dict:
    """Check password strength and return detailed info."""
    strength = {
        "score": 0,
        "level": "Very Weak",
        "feedback": []
    }
    
    # Length check
    if len(password) >= 8:
        strength["score"] += 1
    if len(password) >= 12:
        strength["score"] += 1
    if len(password) >= 16:
        strength["score"] += 1
    
    # Character variety
    if re.search(r'[a-z]', password):
        strength["score"] += 1
    if re.search(r'[A-Z]', password):
        strength["score"] += 1
    if re.search(r'[0-9]', password):
        strength["score"] += 1
    if re.search(r'[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]', password):
        strength["score"] += 1
    
    # Check for patterns
    if re.search(r'(.)\1{2,}', password):  # Repeated characters
        strength["score"] -= 1
        strength["feedback"].append("Avoid repeating characters")
    
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', password):
        strength["score"] -= 1
        strength["feedback"].append("Avoid sequential characters")
    
    # Determine level
    if strength["score"] <= 2:
        strength["level"] = "Very Weak"
    elif strength["score"] <= 4:
        strength["level"] = "Weak"
    elif strength["score"] <= 6:
        strength["level"] = "Good"
    elif strength["score"] <= 8:
        strength["level"] = "Strong"
    else:
        strength["level"] = "Very Strong"
    
    # Add feedback
    if len(password) < 12:
        strength["feedback"].append("Consider using 12+ characters")
    if not re.search(r'[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]', password):
        strength["feedback"].append("Add special characters for better security")
    
    return strength


# ============================================================================
# USER MANAGEMENT
# ============================================================================

def user_exists(username: str) -> bool:
    """Check if user exists by username."""
    users = load_users()
    return username.lower() in [u.lower() for u in users.keys()]


def email_exists(email: str) -> bool:
    """Check if email is already registered."""
    users = load_users()
    return any(user.get("email", "").lower() == email.lower() for user in users.values())


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """Register a new user."""
    # Validation
    username_valid, username_err = validate_username(username)
    if not username_valid:
        return False, username_err
    
    email_valid, email_err = validate_email(email)
    if not email_valid:
        return False, email_err
    
    password_valid, password_err = validate_password(password)
    if not password_valid:
        return False, password_err
    
    # Check if user exists
    if user_exists(username):
        return False, "Username already exists"
    
    if email_exists(email):
        return False, "Email already registered"
    
    # Create user
    users = load_users()
    users[username] = {
        "email": email,
        "password_hash": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "profile": {
            "full_name": "",
            "avatar_color": "#00ff88",
            "bio": ""
        }
    }
    save_users(users)
    
    return True, "User registered successfully"


def authenticate_user(username: str, password: str) -> tuple[bool, str]:
    """Authenticate user with username and password."""
    users = load_users()
    
    # Find user (case-insensitive)
    user = None
    for u, data in users.items():
        if u.lower() == username.lower():
            user = data
            break
    
    if user is None:
        return False, "Invalid username or password"
    
    if not verify_password(password, user["password_hash"]):
        return False, "Invalid username or password"
    
    # Update last login
    users[username]["last_login"] = datetime.now().isoformat()
    save_users(users)
    
    return True, "Authentication successful"


def get_user(username: str) -> dict:
    """Get user data by username."""
    users = load_users()
    for u, data in users.items():
        if u.lower() == username.lower():
            # Return sanitized data (without password hash)
            return {
                "username": u,
                "email": data.get("email", ""),
                "created_at": data.get("created_at", ""),
                "last_login": data.get("last_login", ""),
                "profile": data.get("profile", {})
            }
    return None


def update_user_profile(username: str, full_name: str, bio: str) -> bool:
    """Update user profile information."""
    users = load_users()
    for u in users:
        if u.lower() == username.lower():
            users[u]["profile"]["full_name"] = full_name
            users[u]["profile"]["bio"] = bio
            save_users(users)
            return True
    return False


def change_password(username: str, old_password: str, new_password: str) -> tuple[bool, str]:
    """Change user password."""
    # Authenticate first
    is_valid, msg = authenticate_user(username, old_password)
    if not is_valid:
        return False, "Current password is incorrect"
    
    # Validate new password
    password_valid, password_err = validate_password(new_password)
    if not password_valid:
        return False, password_err
    
    # Update password
    users = load_users()
    for u in users:
        if u.lower() == username.lower():
            users[u]["password_hash"] = hash_password(new_password)
            save_users(users)
            return True, "Password changed successfully"
    
    return False, "User not found"


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def create_session(username: str, remember_me: bool = False) -> str:
    """Create a session token for a user."""
    session_token = secrets.token_urlsafe(32)
    
    # Calculate expiry
    if remember_me:
        expiry = datetime.now() + timedelta(days=30)
    else:
        expiry = datetime.now() + timedelta(hours=SESSION_EXPIRY_HOURS)
    
    sessions = load_sessions()
    sessions[session_token] = {
        "username": username,
        "created_at": datetime.now().isoformat(),
        "expires_at": expiry.isoformat(),
        "remember_me": remember_me
    }
    save_sessions(sessions)
    
    return session_token


def validate_session(session_token: str) -> tuple[bool, str]:
    """Validate a session token."""
    if not session_token:
        print(f"[DEBUG VALIDATE_SESSION] No session token provided")
        return False, ""
    
    try:
        sessions = load_sessions()
        print(f"[DEBUG VALIDATE_SESSION] Loaded sessions, total: {len(sessions)}")
        print(f"[DEBUG VALIDATE_SESSION] Searching for token: {session_token[:20]}...")
        
        session = sessions.get(session_token)
        
        if not session:
            print(f"[DEBUG VALIDATE_SESSION] Session token not found in database")
            return False, ""
        
        print(f"[DEBUG VALIDATE_SESSION] Session found: {session}")
        
        # Check expiry
        expiry = datetime.fromisoformat(session["expires_at"])
        current_time = datetime.now()
        print(f"[DEBUG VALIDATE_SESSION] Current time: {current_time}, Expiry: {expiry}")
        
        if current_time > expiry:
            # Remove expired session
            print(f"[DEBUG VALIDATE_SESSION] Session expired, removing")
            del sessions[session_token]
            save_sessions(sessions)
            return False, ""
        
        print(f"[DEBUG VALIDATE_SESSION] Session valid! Username: {session['username']}")
        return True, session["username"]
    
    except Exception as e:
        print(f"[DEBUG VALIDATE_SESSION] Error validating session: {str(e)}")
        return False, ""


def invalidate_session(session_token: str) -> bool:
    """Invalidate (delete) a session."""
    sessions = load_sessions()
    if session_token in sessions:
        del sessions[session_token]
        save_sessions(sessions)
        return True
    return False


def cleanup_expired_sessions():
    """Remove expired sessions from database."""
    sessions = load_sessions()
    now = datetime.now()
    
    expired = [
        token for token, session in sessions.items()
        if datetime.fromisoformat(session["expires_at"]) < now
    ]
    
    for token in expired:
        del sessions[token]
    
    if expired:
        save_sessions(sessions)
    
    return len(expired)


# ============================================================================
# PASSWORD RESET (PLACEHOLDER)
# ============================================================================

def generate_reset_token(email: str) -> str:
    """Generate a password reset token (placeholder)."""
    reset_token = secrets.token_urlsafe(32)
    return reset_token


def validate_reset_token(reset_token: str) -> tuple[bool, str]:
    """Validate a reset token (placeholder)."""
    # In production: check token against database with expiry
    return True, ""


def reset_password(email: str, reset_token: str, new_password: str) -> tuple[bool, str]:
    """Reset password using reset token (placeholder)."""
    # Validate token
    is_valid, msg = validate_reset_token(reset_token)
    if not is_valid:
        return False, "Invalid or expired reset token"
    
    # Validate new password
    password_valid, password_err = validate_password(new_password)
    if not password_valid:
        return False, password_err
    
    # Find user by email
    users = load_users()
    for username, user in users.items():
        if user.get("email", "").lower() == email.lower():
            users[username]["password_hash"] = hash_password(new_password)
            save_users(users)
            return True, "Password reset successfully"
    
    return False, "User not found"


# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    init_databases()
    print("✓ Authentication databases initialized")
