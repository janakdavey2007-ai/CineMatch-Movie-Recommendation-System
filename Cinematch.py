"""
🎬 CINEMATCH PRO ULTRA
🔥 Final Version: Premium UI + Login + Dark Mode + Chat + Analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import time

st.set_page_config(page_title="CineMatch 🎬", layout="wide")

# =========================
# SESSION INIT
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "ratings" not in st.session_state:
    st.session_state.ratings = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================
# DARK MODE CSS
# =========================
dark_css = """
<style>
body {background-color:#0f172a;color:white;}
.card {background:#1e293b;padding:1rem;border-radius:15px;margin:10px 0;}
.chat-user {background:#6366f1;padding:10px;border-radius:10px;margin:5px;color:white;}
.chat-ai {background:#334155;padding:10px;border-radius:10px;margin:5px;color:white;}
</style>
"""

light_css = """
<style>
body {background-color:white;color:black;}
.card {background:#f1f5f9;padding:1rem;border-radius:15px;margin:10px 0;}
.chat-user {background:#6366f1;padding:10px;border-radius:10px;margin:5px;color:white;}
.chat-ai {background:#e2e8f0;padding:10px;border-radius:10px;margin:5px;color:black;}
</style>
"""

st.markdown(dark_css if st.session_state.dark_mode else light_css, unsafe_allow_html=True)

# =========================
# LOGIN SYSTEM
# =========================
if not st.session_state.logged_in:
    st.title("🔐 Login to CineMatch")
    user = st.text_input("Enter Username")
    
    if st.button("Login"):
        if user.strip():
            st.session_state.logged_in = True
            st.session_state.username = user
            st.rerun()
    st.stop()

# =========================
# HEADER
# =========================
st.title(f"🎬 Welcome {st.session_state.username}!")

# =========================
# DARK MODE TOGGLE
# =========================
if st.button("🌙 Toggle Dark Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# =========================
# DATA
# =========================
movies = {
    "🎭 The Dark Knight":"action",
    "🧠 Inception":"sci-fi",
    "🌌 Interstellar":"sci-fi",
    "🚢 Titanic":"romance",
    "😂 Superbad":"comedy",
    "👊 Fight Club":"dark"
}

# =========================
# ENGINE
# =========================
def generate_recommendations():
    avg = np.mean(list(st.session_state.ratings.values())) if st.session_state.ratings else 3.5
    recs = []
    for m in movies:
        if m not in st.session_state.ratings:
            score = avg + random.uniform(-0.5, 1)
            recs.append((m, round(max(1, min(5, score)),1)))
    return sorted(recs, key=lambda x: x[1], reverse=True)

def explain(movie):
    if not st.session_state.ratings:
        return "Popular movie"
    liked = max(st.session_state.ratings, key=st.session_state.ratings.get)
    return f"Because you liked {liked}"

# =========================
# MOOD FEATURE
# =========================
st.subheader("🎭 Mood-Based Suggestions")
mood = st.selectbox("Choose mood",["Happy","Sad","Excited","Romantic"])

if st.button("Get Mood Movies"):
    st.success(random.sample(list(movies.keys()),2))

# =========================
# MAIN UI
# =========================
col1,col2 = st.columns([1,2])

with col1:
    st.subheader("⭐ Rate Movies")
    movie = st.selectbox("Movie", list(movies.keys()))
    rating = st.slider("Rating",1.0,5.0,4.0,0.5)

    if st.button("Add Rating"):
        st.session_state.ratings[movie] = rating
        st.session_state.history.append((movie,rating))
        st.success("Saved!")
        st.rerun()

    if st.button("🎲 Surprise"):
        m=random.choice(list(movies.keys()))
        st.session_state.ratings[m]=random.choice([3,4,5])
        st.rerun()

    if st.button("🧹 Reset"):
        st.session_state.ratings={}
        st.session_state.history=[]
        st.rerun()

with col2:
    st.subheader("🎯 Recommendations")
    recs=generate_recommendations()
    for m,s in recs[:5]:
        st.markdown(f"<div class='card'>{m} ⭐ {s}<br><small>{explain(m)}</small></div>", unsafe_allow_html=True)

# =========================
# CHAT SYSTEM
# =========================
st.markdown("---")
st.subheader("💬 Chat Recommender")

msg=st.text_input("Ask something like 'action movies'")

if st.button("Send"):
    if msg:
        st.session_state.chat.append(("You",msg))
        if "action" in msg:
            reply="Try Dark Knight or Fight Club"
        elif "romance" in msg:
            reply="Try Titanic"
        else:
            reply="Try Interstellar or Inception"
        st.session_state.chat.append(("AI",reply))

for role,text in st.session_state.chat:
    cls="chat-user" if role=="You" else "chat-ai"
    st.markdown(f"<div class='{cls}'>{role}: {text}</div>", unsafe_allow_html=True)

# =========================
# ANALYTICS
# =========================
if st.session_state.ratings:
    st.subheader("📊 Your Ratings")
    fig=px.histogram(x=list(st.session_state.ratings.values()))
    st.plotly_chart(fig)

# =========================
# USER HISTORY
# =========================
st.subheader("📜 History")
if st.session_state.history:
    df=pd.DataFrame(st.session_state.history, columns=["Movie","Rating"])
    st.dataframe(df)

# =========================
# GAMIFICATION
# =========================
st.subheader("🏆 Achievements")
if len(st.session_state.ratings)>=3:
    st.success("🎖 Beginner Critic")
if len(st.session_state.ratings)>=5:
    st.success("🔥 Movie Expert")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🎬 CineMatch PRO ULTRA | Fully Loaded AI Recommender")
