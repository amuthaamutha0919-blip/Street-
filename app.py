import streamlit as st
import datetime
import time
from gtts import gTTS
import base64

# --- அடிப்படை அமைப்புகள் ---
st.set_page_config(page_title="GANG BOYS 🥷", page_icon="🥷")

# பாஸ்வேர்டு
ADMIN_PASS = "admintest@123"
MEMBER_PASS = "membertest@123"

# நிதி மற்றும் செய்தி தரவுகள்
if 'income' not in st.session_state: st.session_state.income = 0.0
if 'expense' not in st.session_state: st.session_state.expense = 0.0
if 'news' not in st.session_state: st.session_state.news = "குழுவிற்கு வரவேற்கிறோம்!"

# --- குரல் வாழ்த்து உருவாக்கும் செயல்பாடு ---
def autoplay_audio(name):
    wish_text = f"Happy Birthday {name}. இனிய பிறந்தநாள் வாழ்த்துக்கள் {name}"
    tts = gTTS(text=wish_text, lang='ta') # தமிழ் உச்சரிப்பு
    tts.save("wish.mp3")
    
    with open("wish.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # பட்டனை தட்டியவுடன் ஆடியோ தானாக ஓட இந்த HTML கோட் உதவும்
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# --- லாகின் பக்கம் ---
def login():
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>GANG BOYS 🥷</h1>", unsafe_allow_html=True)
    
    name = st.text_input("உங்கள் பெயர்")
    dob = st.text_input("பிறந்த தேதி (DD-MM)")
    pwd = st.text_input("பாஸ்வேர்டு", type="password")
    
    if st.button("உள்நுழை"):
        if pwd == ADMIN_PASS or pwd == MEMBER_PASS:
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.session_state.is_admin = (pwd == ADMIN_PASS)
            
            today = datetime.datetime.now().strftime("%d-%m")
            if dob == today:
                st.session_state.show_gate = True
            else:
                st.session_state.show_gate = False
            st.rerun()
        else:
            st.error("தவறான பாஸ்வேர்டு!")

# --- பிறந்தநாள் சிறப்பு கேட் ---
def birthday_gate(name):
    st.balloons() # பலூன்கள் பறக்கும்
    
    st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>🎂 ஸ்பெஷல் டே 🎂</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>வாழ்த்துக்களைக் கேட்கவும், உள்ளே செல்லவும் கீழே உள்ள பட்டனைத் தட்டவும்</h3>", unsafe_allow_html=True)
    
    # திரையின் நடுவில் பட்டன்
    st.write("##")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"🎈 {name} - இங்கே தட்டவும் 🎈", use_container_width=True):
            autoplay_audio(name) # பெயரைச் சொல்லி வாழ்த்தும்
            st.toast(f"வாழ்த்துக்கள் {name}!")
            time.sleep(4) # குரல் ஒலித்து முடிக்க சில விநாடிகள் காத்திருத்தல்
            st.session_state.show_gate = False
            st.rerun()

# --- முக்கிய முகப்புப் பக்கம் ---
def main_page():
    st.sidebar.title("🥷 GANG BOYS")
    st.title(f"வணக்கம் {st.session_state.user_name}!")
    
    # வரவு செலவு மெட்ரிக்ஸ்
    bal = st.session_state.income - st.session_state.expense
    st.metric("குழு கையிருப்பு", f"₹{bal}")
    
    st.info(f"📢 அறிவிப்பு: {st.session_state.news}")
    
    # இதர வசதிகள்...
    if st.button("வெளியேறு (Logout)"):
        del st.session_state.logged_in
        st.rerun()

# --- ஆப் இயக்கம் ---
if 'logged_in' not in st.session_state:
    login()
elif st.session_state.get('show_gate', False):
    birthday_gate(st.session_state.user_name)
else:
    main_page()
