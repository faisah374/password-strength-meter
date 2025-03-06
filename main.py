import streamlit as st
import random
import string
import re

# --- Streamlit Page Config ---
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="wide")

# --- Custom CSS for Unique & Premium Design ---
st.markdown("""
    <style>
    body {
        background-color: #0D1117;
        color: #EAEAEA;
        font-family: 'Poppins', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #00D4FF;
        text-shadow: 0px 0px 18px #00D4FF;
        animation: glow 2s infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0px 0px 18px #00D4FF; }
        to { text-shadow: 0px 0px 30px #00D4FF; }
    }
    .sub-title {
        text-align: center;
        font-size: 20px;
        color: #A0A0A0;
        margin-bottom: 30px;
            
    .modern-button {
        display: block;
        width: 100%;
        padding: 16px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        color: white;
        background: linear-gradient(135deg, #1A1F71, #007BFF);
        border-radius: 18px;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        border: none;
        box-shadow: 0px 8px 20px rgba(0, 123, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 1.2px;
        animation: fadeIn 0.8s ease-in-out;
        position: relative;
        overflow: hidden;
    }

    .modern-button::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 300%;
        height: 300%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 10%, transparent 50%);
        transition: all 0.6s ease-in-out;
        transform: translate(-50%, -50%) scale(0);
    }

    .modern-button:hover::before {
        transform: translate(-50%, -50%) scale(1);
    }

    .modern-button:hover {
        transform: scale(1.1);
        background: linear-gradient(135deg, #007BFF, #1A1F71);
        box-shadow: 0px 12px 35px rgba(0, 123, 255, 0.8);
    }


    .password-box {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        padding: 18px;
        border-radius: 12px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        color: white;
        border: 2px solid #00D4FF;
        text-shadow: 0px 0px 10px #00D4FF;
        animation: fadeIn 0.8s ease-in-out;
    }
    .progress-bar {
        width: 100%;
        height: 12px;
        border-radius: 5px;
        margin-top: 10px;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Function to Check Password Strength ---
def check_password_strength(password):
    score = 0
    feedback = []
    if len(password) >= 8: score += 1
    else: feedback.append("🔹 Password should be **at least 8 characters long**.")
    if re.search(r'[A-Z]', password): score += 1
    else: feedback.append("🔹 Add **at least one uppercase letter (A-Z)**.")
    if re.search(r'[a-z]', password): score += 1
    else: feedback.append("🔹 Include **at least one lowercase letter (a-z)**.")
    if re.search(r'\d', password): score += 1
    else: feedback.append("🔹 Use **at least one digit (0-9)**.")
    if re.search(r'[!@#$%^&*]', password): score += 1
    else: feedback.append("🔹 Add **at least one special character (!@#$%^&*)**.")
    return score, feedback

# --- Function to Generate Strong Password ---
def generate_password(length):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# --- UI Title ---
st.markdown("<h1 class='main-title'>🔐 Password Strength Meter</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Generate a strong password or check your password strength.</p>", unsafe_allow_html=True)

# --- Default State (Initially Show "Generate Password") ---
if "selected_option" not in st.session_state:
    st.session_state.selected_option = "Generate Password"

# --- Unique Option Selection ---
col1, col2 = st.columns(2)
if col1.button("⚡ Generate Password", key="gen", help="Click to generate a strong password"):
    st.session_state.selected_option = "Generate Password"
if col2.button("🛡️ Check Password Strength", key="check", help="Click to check password strength"):
    st.session_state.selected_option = "Check Password Strength"

st.write("<hr style='border-color: #00D4FF;'>", unsafe_allow_html=True)

# --- Show Generate Password Section ---
if st.session_state.selected_option == "Generate Password":
    st.subheader("✨ Generate a Strong Password")
    length = st.slider("Select Password Length", min_value=8, max_value=32, value=12)
    if st.button("🔑 Generate Password", key="generate", help="Click to generate a strong password"):
        strong_password = generate_password(length)
        st.markdown(f"<div class='password-box'>{strong_password}</div>", unsafe_allow_html=True)

# --- Show Check Password Strength Section (Only when clicked) ---
if st.session_state.selected_option == "Check Password Strength":
    st.subheader("🛡️ Check Password Strength")
    password = st.text_input("Enter Password", type="password", help="Your password will be analyzed.")
    if st.button("📊 Check Strength", key="check_strength", help="Click to analyze password strength"):
        if password:
            strength, feedback = check_password_strength(password)
            progress_color = "red" if strength < 3 else "yellow" if strength < 5 else "green"
            st.markdown(f"<div class='password-box'>{'✅ Strong' if strength == 5 else '⚠️ Moderate' if strength >= 3 else '❌ Weak'}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='progress-bar' style='background: {progress_color}; width: {strength * 20}%;'></div>", unsafe_allow_html=True)
            if feedback:
                st.subheader("💡 Suggestions to Improve Your Password:")
                for tip in feedback:
                    st.markdown(f"<p class='password-feedback'>{tip}</p>", unsafe_allow_html=True)

st.write("<hr style='border-color: #00D4FF;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00D4FF;'>🔑 Secure your online accounts with a strong password!</p>", unsafe_allow_html=True)
