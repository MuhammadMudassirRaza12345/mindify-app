import streamlit as st
import speech_recognition as sr
from backend import stress_response
import base64
from io import BytesIO

 
st.set_page_config(
    page_title="Mindify",
    page_icon="🧠",
    layout="centered"
)

 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """🌿 **Hello, I’m Mindify — your mental wellbeing companion.**  
I'm here to listen and support you.  
What’s on your mind today?"""
        }
    ]

 
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
    
    
}

/* Background Gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1e1545 0%, #2d1d5e 50%, #492a91 100%);
    color: white;
}

/* Hide Streamlit Header */
[data-testid="stHeader"] {display: none;}

/* Chat Bubbles */
.user-msg {
    background: rgba(94, 234, 212, 0.18);
    border-left: 4px solid #5EEAD4;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 10px;
}

.bot-msg {
    background: rgba(168, 85, 247, 0.20);
    border-left: 4px solid #A855F7;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 10px;
}

/* Title */
.title {
    font-size: 2.6rem;
    font-weight: 700;
    text-align: center;
    padding-top: 1rem;
    margin-bottom: 2rem;
    background: linear-gradient(90deg, #9E60F9, #60FBD3, #9E60F9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glow 4s ease infinite;
}

@keyframes glow {
    0% {opacity: .9}
    50% {opacity: 1}
    100% {opacity: .9}
}

/* Sticky Input */
.sticky-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 16px;
    background: rgba(30, 21, 69, 0.88);
    backdrop-filter: blur(10px);
    box-shadow: 0 -4px 20px rgba(0,0,0,.4);
}

.sticky-input input {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    color: white;
    padding: 14px 20px;
    border-radius: 16px;
}

.sticky-input button {
    background: #A855F7 !important;
    color: #A855F7 !important;
    border-radius: 14px !important;
}

.st-emotion-cache-128upt6 {
    background-color: rgba(168, 85, 247, 0.20) !important;
    color: rgba(168, 85, 247, 0.20) !important;
    
}
.stButton {
    background-color:  rgba(168, 85, 247, 0.20)  !important;
    
}
.st-emotion-cache-5qfegl {
    background-color:  rgba(168, 85, 247, 0.20)  !important;
    
}
.st-emotion-cache-12j140x p {
    background-color:  rgba(168, 85, 247, 0.20)  !important;
    } 
 
.st-emotion-cache-epvm6 {
    colour: #000000 !important;
    
}
.st-emotion-cache-jzs692 {
    colour: #000000 !important;
}
/* Upload Box */
.upload-box {
    text-align: center;
    background: rgba(255,255,255,0.10);
    padding: 12px;
    border-radius: 16px;
    border: 1px dashed rgba(255,255,255,0.3);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)
 
st.markdown('<h1 class="title">🧠 M I N D I F Y</h1>', unsafe_allow_html=True)

 
for msg in st.session_state.messages:
    style = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(f'<div class="{style}">{msg["content"]}</div>', unsafe_allow_html=True)

 
st.markdown('<div class="upload-box">🎤 Upload audio to transcribe (WAV / MP3 / M4A)</div>', unsafe_allow_html=True)

audio_file = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a"], label_visibility="collapsed")

user_text_from_audio = ""
base64_audio = None

 
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    submit = st.button("🎧 Submit Audio")
    if submit:
        if audio_file is None:
            st.warning("Please upload an audio file first.")
        else:
            st.audio(audio_file)

            audio_bytes = audio_file.read()
            base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
            
    
            with st.spinner("💬 Mindify is thinking..."):
                reply = stress_response(user_text_from_audio, base64_audio=base64_audio)

            ai_response = reply["analysis"]
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.rerun()
     
    
     
 
st.markdown('<div class="sticky-input">', unsafe_allow_html=True)
prompt = st.chat_input("Share your thoughts...")
st.markdown('</div>', unsafe_allow_html=True)

final_input = prompt or user_text_from_audio
 
if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})

    with st.spinner("💬 Mindify is thinking..."):
        reply = stress_response(final_input, base64_audio=base64_audio)

    ai_response = reply["analysis"]
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.rerun() 