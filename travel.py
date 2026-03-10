from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Smart AI Travel Assistant", page_icon="✈️")

# ---------- STYLE ----------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(120deg,#eef2ff,#e0c3fc);
}

/* Main Heading */
.header {
    text-align:center;
    color:black;
    background: linear-gradient(90deg,#4facfe,#00f2fe);
    padding:40px;
    border-radius:15px;
    font-size:45px;
    font-weight:900;
    letter-spacing:1px;
    margin-bottom:30px;
}

/* Description box */
.description{
    text-align:center;
    color:#333;
    font-size:18px;
    padding:20px;
    background:pink;
    border-radius:12px;
    width:70%;
    margin:auto;
    margin-bottom:35px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
}
.ai-msg{
background:#ffffff;
padding:12px;
border-radius:10px;
border-left:5px solid #667eea;
color:black
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
"<div class='header'>✈️ Smart AI Travel Assistant</div>",
unsafe_allow_html=True
)

# ---------- CONTENT ----------
st.markdown(
"""
<div class='description'>
<b>Plan your perfect trips with AI</b> 🌍<br><br>
Ask about travel destinations, trip budgets, itineraries,
weather conditions, and the best places to visit around the world.
</div>
""",
unsafe_allow_html=True
)

# ---------- CHAT MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a smart AI travel assistant that helps users plan trips, suggest destinations, and create itineraries."
        }
    ]

# ---------- DISPLAY CHAT ----------
for message in st.session_state.messages:
     if message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(
                    f"<div class='ai-msg'>{message['content']}</div>",
                    unsafe_allow_html=True
                )

        else:
            with st.chat_message("user"):
                st.markdown(
                    f"<div class='user-msg'>{message['content']}</div>",
                    unsafe_allow_html=True
                )


# ---------- CHAT INPUT ----------
if prompt := st.chat_input("Ask about your next trip ✈️"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(
            f"<div class='user-msg'>{prompt}</div>",
            unsafe_allow_html=True
        )

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=200
        )

        response = completion.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(
                f"<div class='ai-msg'>{response}</div>",
                unsafe_allow_html=True
            )


        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    except Exception as e:

        st.error(e)
