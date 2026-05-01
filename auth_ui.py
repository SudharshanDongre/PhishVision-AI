"""
PhishVision Authentication UI Components
Provides all authentication-related UI elements matching the cyberpunk design.
"""

import streamlit as st
import time
from auth import (
    register_user, authenticate_user, check_password_strength,
    create_session, validate_session, invalidate_session,
    get_user, update_user_profile, change_password
)


# ============================================================================
# SHARED STYLING & UTILITIES
# ============================================================================

def auth_css():
    """Apply authentication-specific CSS styling."""
    st.markdown("""
    <style>
    /* ── Password strength indicator ── */
    .strength-very-weak { color: #ff1a1a; }
    .strength-weak { color: #ff6b6b; }
    .strength-good { color: #ffaa00; }
    .strength-strong { color: #66dd00; }
    .strength-very-strong { color: #00ff88; }
    
    /* ── Input field glow on focus ── */
    .stTextInput > div > div > input:focus-visible {
        border: 1px solid #00ff88 !important;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.4) !important;
    }
    
    /* ── Checkbox styling ── */
    .stCheckbox > label {
        color: #00ff88 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    
    /* ── Auth form container ── */
    .auth-form-container {
        background: linear-gradient(135deg, #050a0f 0%, #071020 50%, #050a0f 100%);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 8px;
        padding: 40px;
        margin: 20px 0;
    }
    
    /* ── Tab animation ── */
    .auth-tab {
        transition: all 0.3s ease;
    }
    
    /* ── Links ── */
    a {
        color: #00c8ff;
        text-decoration: none;
    }
    
    a:hover {
        color: #00ff88;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)


def auth_header(title, subtitle=""):
    """Display authentication page header."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 40px;">
        <div style="font-family: 'Orbitron', monospace; color: #00ff88;
                    font-size: 2.2rem; font-weight: 900; letter-spacing: 4px;
                    margin-bottom: 8px;">
            {title}
        </div>
        {f'<div style="font-family: Rajdhani, sans-serif; color: #00c8ff;\n                       font-size: 0.95rem; letter-spacing: 2px;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def password_strength_indicator(password: str):
    """Display visual password strength indicator."""
    if not password:
        return
    
    strength_info = check_password_strength(password)
    level = strength_info["level"]
    
    color_map = {
        "Very Weak": ("#ff1a1a", "████░░░░░░"),
        "Weak": ("#ff6b6b", "█████░░░░░"),
        "Good": ("#ffaa00", "██████░░░░"),
        "Strong": ("#66dd00", "███████░░░"),
        "Very Strong": ("#00ff88", "██████████")
    }
    
    color, bar = color_map.get(level, ("#ffaa00", "░░░░░░░░░░"))
    
    feedback_text = ""
    if strength_info["feedback"]:
        feedback_text = "<br>".join([f"• {f}" for f in strength_info["feedback"]])
        feedback_text = f"<div style='color: #00c8ff88; font-size: 0.8rem; margin-top: 8px;'>{feedback_text}</div>"
    
    st.markdown(f"""
    <div style="margin: 12px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #00c8ff; font-size: 0.85rem;">PASSWORD STRENGTH</span>
            <span style="color: {color}; font-weight: 700; font-size: 0.85rem;">{level.upper()}</span>
        </div>
        <div style="background: #071020; border: 1px solid #00ff8822; border-radius: 2px;
                    padding: 2px; font-size: 0.8rem;">
            <span style="color: {color};">{bar}</span>
        </div>
        {feedback_text}
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# LOGIN PAGE
# ============================================================================

def show_login_page():
    """Display login page."""
    auth_header("LOGIN", "Access your PhishVision account")
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="auth-form-container" style="">
            """, unsafe_allow_html=True)
            
            username = st.text_input(
                "USERNAME",
                placeholder="Enter your username",
                help="3-20 characters, letters, numbers, hyphens, underscores"
            )
            
            password = st.text_input(
                "PASSWORD",
                placeholder="Enter your password",
                type="password",
                help="Case-sensitive"
            )
            
            col_remember, col_forgot = st.columns([1, 1])
            with col_remember:
                remember_me = st.checkbox("REMEMBER ME", value=False)
            with col_forgot:
                if st.button("FORGOT PASSWORD?", use_container_width=True):
                    st.session_state.auth_page = "forgot_password"
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_login, col_signup = st.columns([1, 1])
            
            with col_login:
                if st.button("⚡  LOGIN", use_container_width=True, key="btn_login"):
                    if not username:
                        st.error("⚠ Please enter your username")
                    elif not password:
                        st.error("⚠ Please enter your password")
                    else:
                        # Show loading state
                        with st.spinner("Authenticating..."):
                            is_valid, msg = authenticate_user(username, password)
                            print(f"[DEBUG LOGIN] authenticate_user returned: is_valid={is_valid}, msg={msg}")
                            
                            if is_valid:
                                # Create session
                                session_token = create_session(username, remember_me)
                                print(f"[DEBUG LOGIN] Created session token: {session_token}")
                                
                                # Set session state
                                st.session_state.session_token = session_token
                                st.session_state.username = username
                                st.session_state.is_authenticated = True
                                st.session_state.auth_page = None
                                
                                print(f"[DEBUG LOGIN] Set session state - token: {session_token}, user: {username}")
                                print(f"[DEBUG LOGIN] Session state after setting: token={st.session_state.session_token}, is_auth={st.session_state.is_authenticated}")
                                
                                st.success(f"✓ Welcome back, {username}!")
                                time.sleep(0.5)  # Brief pause for UX
                                st.balloons()
                                
                                print(f"[DEBUG LOGIN] About to rerun")
                                st.rerun()
                            else:
                                st.error(f"✗ {msg}")
            
            with col_signup:
                if st.button("SIGN UP", use_container_width=True, key="btn_to_signup"):
                    st.session_state.auth_page = "signup"
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# SIGNUP PAGE
# ============================================================================

def show_signup_page():
    """Display signup page."""
    auth_header("CREATE ACCOUNT", "Join PhishVision today")
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="auth-form-container">
            """, unsafe_allow_html=True)
            
            username = st.text_input(
                "USERNAME",
                placeholder="Choose a unique username",
                help="3-20 characters, letters, numbers, hyphens, underscores"
            )
            
            email = st.text_input(
                "EMAIL ADDRESS",
                placeholder="your.email@example.com",
                help="We'll never share your email"
            )
            
            password = st.text_input(
                "PASSWORD",
                placeholder="Create a strong password",
                type="password",
                help="Minimum 8 characters with uppercase, lowercase, digit, and special character"
            )
            
            password_strength_indicator(password)
            
            password_confirm = st.text_input(
                "CONFIRM PASSWORD",
                placeholder="Re-enter your password",
                type="password"
            )
            
            terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_signup, col_login = st.columns([1, 1])
            
            with col_signup:
                if st.button("✓  CREATE ACCOUNT", use_container_width=True, key="btn_signup"):
                    # Validation
                    if not username:
                        st.error("⚠ Username is required")
                    elif not email:
                        st.error("⚠ Email is required")
                    elif not password:
                        st.error("⚠ Password is required")
                    elif password != password_confirm:
                        st.error("⚠ Passwords do not match")
                    elif not terms:
                        st.error("⚠ Please agree to the Terms of Service")
                    else:
                        with st.spinner("Creating account..."):
                            success, msg = register_user(username, email, password)
                        
                            if success:
                                st.success("✓ Account created successfully! Logging in...")
                                time.sleep(0.5)
                                
                                # Auto-login after signup
                                session_token = create_session(username, remember_me=False)
                                st.session_state.session_token = session_token
                                st.session_state.username = username
                                st.session_state.is_authenticated = True
                                st.session_state.auth_page = None
                                
                                print(f"[DEBUG SIGNUP] Auto-login successful for user: {username}")
                                st.balloons()
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error(f"✗ {msg}")
            
            with col_login:
                if st.button("← BACK TO LOGIN", use_container_width=True, key="btn_back_login"):
                    st.session_state.auth_page = "login"
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# FORGOT PASSWORD PAGE
# ============================================================================

def show_forgot_password_page():
    """Display forgot password page."""
    auth_header("FORGOT PASSWORD?", "We'll help you reset it")
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="auth-form-container">
            <div style="background: #0a2020; border-left: 3px solid #00c8ff;
                        padding: 16px; border-radius: 4px; margin-bottom: 24px;">
                <div style="color: #00c8ff; font-size: 0.9rem; margin-bottom: 8px;">
                    ℹ PLACEHOLDER FEATURE
                </div>
                <div style="color: #00c8ff88; font-size: 0.85rem;">
                    In a production environment, you would enter your email address and receive
                    a password reset link. For now, this feature is a placeholder.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            email = st.text_input(
                "EMAIL ADDRESS",
                placeholder="Enter your registered email",
                help="We'll send a password reset link"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_reset, col_back = st.columns([1, 1])
            
            with col_reset:
                if st.button("📧  SEND RESET LINK", use_container_width=True):
                    if not email:
                        st.error("⚠ Please enter your email address")
                    else:
                        st.info(f"✓ If {email} is registered, you'll receive a password reset link shortly.")
            
            with col_back:
                if st.button("← BACK TO LOGIN", use_container_width=True):
                    st.session_state.auth_page = "login"
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# USER PROFILE & SETTINGS
# ============================================================================

def show_user_profile(username: str):
    """Display user profile page."""
    user = get_user(username)
    if not user:
        st.error("User not found")
        return
    
    auth_header("USER PROFILE", f"@{username}")
    
    # Profile tabs
    tab1, tab2, tab3 = st.tabs(["👤 PROFILE", "🔐 SECURITY", "⚙️ SETTINGS"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #071020, #0a1628);
                        border: 1px solid #00c8ff22; border-radius: 8px;
                        padding: 24px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 12px;">👤</div>
                <div style="font-family: Orbitron, monospace; color: #00ff88;
                            font-size: 1.1rem; font-weight: 700;">
                    {username}
                </div>
                <div style="color: #00c8ff88; font-size: 0.85rem; margin-top: 4px;">
                    Member since {user['created_at'][:10]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### PROFILE INFORMATION")
            
            full_name = st.text_input(
                "FULL NAME",
                value=user["profile"].get("full_name", ""),
                placeholder="Your full name"
            )
            
            email = st.text_input(
                "EMAIL ADDRESS",
                value=user["email"],
                disabled=True,
                help="Email cannot be changed from here"
            )
            
            bio = st.text_area(
                "BIO",
                value=user["profile"].get("bio", ""),
                placeholder="Tell us about yourself",
                max_chars=500,
                height=100
            )
            
            if st.button("💾  SAVE PROFILE"):
                success = update_user_profile(username, full_name, bio)
                if success:
                    st.success("✓ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error("✗ Failed to update profile")
    
    with tab2:
        st.markdown("#### CHANGE PASSWORD")
        
        old_password = st.text_input(
            "CURRENT PASSWORD",
            type="password",
            placeholder="Enter your current password"
        )
        
        new_password = st.text_input(
            "NEW PASSWORD",
            type="password",
            placeholder="Enter your new password"
        )
        
        password_strength_indicator(new_password)
        
        new_password_confirm = st.text_input(
            "CONFIRM NEW PASSWORD",
            type="password",
            placeholder="Re-enter your new password"
        )
        
        if st.button("🔐  UPDATE PASSWORD"):
            if not old_password:
                st.error("⚠ Please enter your current password")
            elif not new_password:
                st.error("⚠ Please enter a new password")
            elif new_password != new_password_confirm:
                st.error("⚠ New passwords do not match")
            else:
                success, msg = change_password(username, old_password, new_password)
                if success:
                    st.success(msg)
                else:
                    st.error(f"✗ {msg}")
    
    with tab3:
        st.markdown("#### SESSION & PRIVACY")
        
        st.info("🔒 Your data is encrypted and secure")
        
        st.markdown("**Active Sessions**")
        st.info("You have 1 active session (current)")
        
        if st.button("🚪  LOGOUT FROM ALL DEVICES"):
            st.warning("⚠ This will log you out from all devices")
            if st.button("CONFIRM LOGOUT"):
                st.session_state.session_token = None
                st.session_state.username = None
                st.session_state.is_authenticated = False
                st.success("Logged out successfully")
                st.rerun()


# ============================================================================
# NAVBAR & USER DROPDOWN
# ============================================================================

def show_navbar():
    """Display navbar with user dropdown."""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown("""
        <div style="font-family: Orbitron, monospace; color: #00ff88;
                    font-size: 1.2rem; font-weight: 700; letter-spacing: 3px;">
            🛡️ PHISHVISION
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.session_state.get("is_authenticated"):
            username = st.session_state.get("username", "User")
            
            # User dropdown using columns as fallback
            st.markdown(f"""
            <div style="text-align: right;">
                <div style="font-family: Share Tech Mono, monospace;
                            color: #00c8ff; font-size: 0.9rem;">
                    👤 {username}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Dropdown menu
            menu_option = st.selectbox(
                "User Menu",
                ["Profile", "Logout"],
                label_visibility="collapsed",
                key=f"user_menu_{username}"
            )
            
            if menu_option == "Profile":
                st.session_state.page = "profile"
                st.rerun()
            elif menu_option == "Logout":
                if st.session_state.get("session_token"):
                    invalidate_session(st.session_state.session_token)
                st.session_state.session_token = None
                st.session_state.username = None
                st.session_state.is_authenticated = False
                st.success("✓ Logged out successfully")
                st.rerun()
        else:
            if st.button("LOGIN", use_container_width=True):
                st.session_state.auth_page = "login"
                st.rerun()


# ============================================================================
# AUTH FLOW MANAGER
# ============================================================================

def init_auth_state():
    """Initialize authentication session state."""
    print(f"[DEBUG INIT_AUTH_STATE] Initializing auth state")
    
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
        print(f"[DEBUG INIT_AUTH_STATE] Set is_authenticated = False (new)")
    
    if "username" not in st.session_state:
        st.session_state.username = None
        print(f"[DEBUG INIT_AUTH_STATE] Set username = None (new)")
    
    if "session_token" not in st.session_state:
        st.session_state.session_token = None
        print(f"[DEBUG INIT_AUTH_STATE] Set session_token = None (new)")
    
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"
        print(f"[DEBUG INIT_AUTH_STATE] Set auth_page = 'login' (new)")
    
    if "page" not in st.session_state:
        st.session_state.page = "scan"
        print(f"[DEBUG INIT_AUTH_STATE] Set page = 'scan' (new)")
    
    print(f"[DEBUG INIT_AUTH_STATE] Final state - token: {bool(st.session_state.session_token)}, is_auth: {st.session_state.is_authenticated}, user: {st.session_state.username}")


def check_authentication():
    """Check if user has valid session."""
    token = st.session_state.get("session_token")
    print(f"[DEBUG CHECK_AUTH] Checking authentication with token: {token}")
    print(f"[DEBUG CHECK_AUTH] Current session state - is_authenticated: {st.session_state.get('is_authenticated')}, username: {st.session_state.get('username')}")
    
    # First check if already authenticated in this session
    if st.session_state.get("is_authenticated") and st.session_state.get("username"):
        print(f"[DEBUG CHECK_AUTH] User already marked authenticated in session state")
        if token:
            # Validate the token is still valid
            is_valid, username = validate_session(token)
            if is_valid:
                print(f"[DEBUG CHECK_AUTH] Token validation confirmed! Returning True")
                return True
            else:
                print(f"[DEBUG CHECK_AUTH] Token validation failed, clearing session")
                st.session_state.session_token = None
                st.session_state.is_authenticated = False
                st.session_state.username = None
                return False
        else:
            # Authenticated but no token - clear and return false
            st.session_state.is_authenticated = False
            st.session_state.username = None
            return False
    
    # No session state, check if token exists and is valid
    if token:
        is_valid, username = validate_session(token)
        print(f"[DEBUG CHECK_AUTH] validate_session returned: is_valid={is_valid}, username={username}")
        
        if is_valid:
            st.session_state.is_authenticated = True
            st.session_state.username = username
            print(f"[DEBUG CHECK_AUTH] Session valid! Returning True")
            return True
        else:
            # Invalid session
            st.session_state.session_token = None
            st.session_state.is_authenticated = False
            st.session_state.username = None
            print(f"[DEBUG CHECK_AUTH] Session invalid! Returning False")
            return False
    
    print(f"[DEBUG CHECK_AUTH] No token found, returning False")
    return False


def show_auth_page():
    """Show appropriate authentication page."""
    auth_css()
    auth_page = st.session_state.get("auth_page", "login")
    
    if auth_page == "signup":
        show_signup_page()
    elif auth_page == "forgot_password":
        show_forgot_password_page()
    else:  # default to login
        show_login_page()
