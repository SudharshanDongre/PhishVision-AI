# 🚀 PhishVision Authentication - Quick Start Guide

## ⚡ Get Started in 2 Minutes

### Step 1: Install Dependencies
```bash
cd c:\PhishVision
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🎯 Test Account

You can immediately:

1. **Create a Test Account**
   - Click "SIGN UP"
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `SecurePass123!` (satisfies all requirements)
   - Agree to terms & Create

2. **Login**
   - Username: `testuser`
   - Password: `SecurePass123!`
   - Check "REMEMBER ME" (optional)
   - Click "LOGIN"

3. **Access Main App**
   - Enter any URL and click "INITIATE SCAN"
   - View profile by clicking your username in navbar
   - Logout from profile dropdown

---

## 📋 What's New

### Authentication Pages
- **Login Page**: Username/password + Remember Me + Forgot Password link
- **Sign Up Page**: Real-time password strength meter + validation
- **Profile Page**: Edit profile, change password, view account info
- **Navbar**: User dropdown with Profile and Logout

### Features
✅ Secure password hashing (bcrypt)  
✅ Session management with 24-hour expiry  
✅ Remember Me (30-day sessions)  
✅ Password strength meter  
✅ Form validation  
✅ Protected routes  
✅ User profile management  

---

## 🔐 Password Requirements

Your password must have:
- ✅ Minimum 8 characters
- ✅ At least 1 UPPERCASE letter
- ✅ At least 1 lowercase letter
- ✅ At least 1 digit (0-9)
- ✅ At least 1 special character (!@#$%^&*)

**Example valid password:** `MySecure@Pass123`

---

## 📁 Project Structure

```
PhishVision/
├── app.py                    # Main app (AUTH ENABLED)
├── auth.py                   # Authentication module
├── auth_ui.py               # UI components
├── app_main.py              # Original app logic (backup)
├── requirements.txt         # Dependencies (UPDATED)
├── users_db.json            # User database (auto-created)
├── sessions_db.json         # Session database (auto-created)
├── AUTHENTICATION.md        # Full documentation
└── AUTH_GUIDE.md           # Architecture guide
```

---

## ✨ Features Breakdown

### 1. Registration
- Username: 3-20 chars (alphanumeric, -, _)
- Email: Valid format required
- Password: Must pass all 5 requirements
- Real-time validation feedback
- Duplicate user detection

### 2. Login
- Supports username or email
- Case-insensitive matching
- Remember Me: Keeps you logged in 30 days
- Secure token-based sessions

### 3. Password Strength
- Shows meter while typing
- Real-time feedback (Very Weak → Very Strong)
- Suggests improvements
- Warns about patterns (repeated chars, sequences)

### 4. User Profile
- Edit full name
- Edit bio (up to 500 chars)
- View account creation date
- View last login time
- Change password (with current password verification)

### 5. Security
- Passwords hashed with bcrypt
- Cryptographic session tokens
- Automatic session expiry
- Input validation on all forms
- Protection against common attacks

---

## 🧪 Quick Test Scenarios

### Scenario 1: Weak Password
1. Click SIGN UP
2. Username: `demo1`
3. Password: `weak` → See "Very Weak" indicator
4. Password: `Weak123` → See strength improve
5. Add `!` → "Very Strong" ✓

### Scenario 2: Duplicate Username
1. Click SIGN UP
2. Username: `testuser` (already exists)
3. Error: "Username already exists"
4. Try different username

### Scenario 3: Invalid Email
1. Click SIGN UP
2. Email: `invalidemail` (no @)
3. Error: "Invalid email format"
4. Enter: `user@example.com`

### Scenario 4: Session Persistence
1. Login with username/password
2. Check "REMEMBER ME"
3. Close and reopen browser
4. Still logged in! (30 days)

### Scenario 5: Profile Editing
1. Login
2. Click username → "Profile"
3. Edit full name to "John Doe"
4. Add bio "Security Researcher"
5. Click "SAVE PROFILE"
6. Changes persist after refresh

---

## 🎨 Design Features

- **Color Scheme**: Neon green (#00ff88) on dark (#050a0f)
- **Fonts**: Orbitron (title), Share Tech Mono (code), Rajdhani (labels)
- **Animations**: Smooth 0.25s transitions, button ripple effects
- **Responsive**: Works on mobile, tablet, desktop
- **Accessibility**: High contrast, large buttons, clear labels

---

## 🔄 Data Flow

```
User enters credentials
        ↓
Form validation (email, username, password)
        ↓
Check if user exists (for signup) OR authenticate (for login)
        ↓
Hash password (bcrypt) OR verify against hash
        ↓
Create session token
        ↓
Store in sessions_db.json with expiry
        ↓
Redirect to main app
        ↓
User accesses protected routes (URL scanning)
```

---

## 📊 File Storage

### users_db.json
Stores all user accounts with:
- Username (case-sensitive storage, case-insensitive login)
- Email (lowercase)
- Bcrypt password hash (never stores plain passwords)
- Creation timestamp
- Last login timestamp
- Profile info (name, bio, color)

### sessions_db.json
Stores active sessions with:
- Unique token (256-bit)
- Username
- Creation timestamp
- Expiry timestamp
- Remember Me flag

**Note:** Both files auto-created on first run

---

## 🚨 Important Notes

1. **First Time Only**: Databases are created automatically
2. **Backup**: Periodically backup JSON files (SQL database recommended for production)
3. **Security**: Never commit users_db.json to version control
4. **Performance**: JSON storage OK for < 1000 users; use database for scale
5. **Reset**: Delete JSON files to reset all users/sessions

---

## 🎓 Learning Resources

- See `auth.py` for authentication logic
- See `auth_ui.py` for UI components
- See `app.py` for integration example
- Check `AUTHENTICATION.md` for detailed docs

---

## 🆘 Common Issues

**Q: "Module not found: bcrypt"**
A: Run `pip install -r requirements.txt` again

**Q: "Model file not found"**
A: Run `python train.py` to generate models

**Q: "Can't login with correct password"**
A: Passwords are case-sensitive; check CAPS LOCK

**Q: "Session expires too quickly"**
A: Check "REMEMBER ME" for 30-day sessions

**Q: "Password too weak"**
A: Add uppercase, digit, and special character

---

## 📈 Next Steps

1. ✅ Create test account
2. ✅ Test login/logout
3. ✅ Scan a URL (core functionality)
4. ✅ Edit profile
5. ✅ Test Remember Me
6. ✅ Review password strength
7. ✅ Explore all features

**Done!** Your PhishVision app is now secure and ready to use! 🎉

---

## 🤝 Support

For detailed docs: See [AUTHENTICATION.md](AUTHENTICATION.md)  
For architecture: See [AUTH_GUIDE.md](AUTH_GUIDE.md)  
For code: See `auth.py` and `auth_ui.py`

**Happy scanning!** 🛡️
