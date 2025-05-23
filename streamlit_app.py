import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, date

# File to store kind acts
DATA_FILE = "kind_acts.csv"

# Initialize the CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Act of Kindness"])
    df.to_csv(DATA_FILE, index=False)

# Define kindness suggestions based on budget and context, without monetary references
KINDNESS_SUGGESTIONS = {
    "Free": {
        "From Home": [
            "Write a heartfelt thank-you note to someone via email.",
            "Call a friend or family member to check in and brighten their day.",
            "Share a positive post or comment on social media to uplift others.",
            "Offer to help a neighbor with a task via a message or call.",
            "Create and share a playlist of uplifting songs for someone."
        ],
        "Out and About": [
            "Smile and say hello to someone to spread positivity.",
            "Leave a kind note on someone's car or doorstep.",
            "Help someone carry their groceries or heavy bags.",
            "Compliment a service worker for their hard work.",
            "Pick up litter in a park or neighborhood to keep it clean."
        ]
    },
    "Small Budget": {
        "From Home": [
            "Send a small care package with snacks to a friend.",
            "Buy and send an e-gift card for coffee to cheer someone up.",
            "Order a small plant online for a loved one to brighten their space.",
            "Donate a small amount to a local charity online.",
            "Purchase and send a digital book to inspire someone."
        ],
        "Out and About": [
            "Buy a coffee for the person behind you in line.",
            "Leave a generous tip for a server or barista.",
            "Purchase a small treat for a coworker or neighbor.",
            "Buy flowers to give to someone you meet.",
            "Pay for a stranger's parking meter or bus fare."
        ]
    },
    "Big Budget": {
        "From Home": [
            "Sponsor a child's education through a charity.",
            "Order a large meal delivery for a family in need.",
            "Purchase and send a gift basket to a friend or colleague.",
            "Donate to a community project or fundraiser online.",
            "Buy and ship supplies for a local animal shelter."
        ],
        "Out and About": [
            "Pay for a stranger's groceries at the store.",
            "Treat a group of friends to a meal out.",
            "Buy books or supplies for a local school or library.",
            "Cover the cost of someone's pet adoption fee.",
            "Gift a large tip to a street performer or service worker."
        ]
    }
}

# Function to calculate streak
def calculate_streak(df):
    if df.empty:
        return 0
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
        sorted_dates = df['Date'].dropna().sort_values(ascending=False).unique()
        streak = 0
        today = date.today()
        current = today
        for d in sorted_dates:
            if d == current:
                streak += 1
                current -= pd.Timedelta(days=1)
            else:
                break
        return streak
    except Exception:
        return 0

# Custom CSS for colorful styling and prettier title
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
    .main-title {
        font-family: 'Pacifico', cursive;
        font-size: 4em;
        text-align: center;
        background: linear-gradient(45deg, #e91e63, #f06292);
        -webkit-background-clip: text;
        color: transparent;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        margin-bottom: 10px;
    }
    .subheader {
        color: #2196f3;
        font-size: 1.8em;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #4caf50;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .quote {
        color: #f57c00;
        font-style: italic;
        text-align: center;
        font-size: 1.3em;
    }
    .streak {
        color: #d81b60;
        font-size: 1.5em;
        text-align: center;
        font-weight: bold;
    }
    .footer {
        color: #757575;
        text-align: center;
        font-size: 0.9em;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app title and quote
st.markdown('<p class="main-title">Be a Kind Human</p>', unsafe_allow_html=True)
st.markdown('<p class="quote">"No act of kindness, no matter how small, is ever wasted." — Aesop</p>', unsafe_allow_html=True)

# Display streak
df = pd.read_csv(DATA_FILE)
streak = calculate_streak(df)
st.markdown('<p class="subheader">Daily Kindness Streak</p>', unsafe_allow_html=True)
st.markdown(f'<p class="streak">{streak} Day{"s" if streak != 1 else ""}</p>', unsafe_allow_html=True)

# Celebrate milestones
if streak in [5, 10, 30]:
    st.balloons()
    st.success(f"Amazing! You've reached a {streak}-day kindness streak! Keep the kindness flowing!")

# Daily kindness challenge
st.markdown('<p class="subheader">Today\'s Kindness Challenge</p>', unsafe_allow_html=True)
if "daily_suggestion" not in st.session_state:
    st.session_state.daily_suggestion = random.choice(
        [act for budget in KINDNESS_SUGGESTIONS for context in KINDNESS_SUGGESTIONS[budget] for act in KINDNESS_SUGGESTIONS[budget][context]]
    )

st.write(f"**Try this today:** {st.session_state.daily_suggestion}")

# Form to check off or get a new challenge
with st.form("daily_challenge_form", clear_on_submit=True):
    completed = st.checkbox("I completed this act!", key="daily_completed")
    submit_daily = st.form_submit_button("Submit")
    new_challenge = st.form_submit_button("Get a New Challenge")

    if submit_daily and completed:
        new_act = pd.DataFrame({"Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Act of Kindness": [st.session_state.daily_suggestion]})
        try:
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_act], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.session_state.daily_suggestion = random.choice(
                [act for budget in KINDNESS_SUGGESTIONS for context in KINDNESS_SUGGESTIONS[budget] for act in KINDNESS_SUGGESTIONS[budget][context]]
            )
            st.success("Kind act logged successfully!")
        except Exception as e:
            st.error(f"Failed to log act: {str(e)}")

    if new_challenge:
        st.session_state.daily_suggestion = random.choice(
            [act for budget in KINDNESS_SUGGESTIONS for context in KINDNESS_SUGGESTIONS[budget] for act in KINDNESS_SUGGESTIONS[budget][context]]
        )

# Get a custom kindness idea
st.markdown('<p class="subheader">Get a Custom Kindness Idea</p>', unsafe_allow_html=True)
with st.form("suggestion_form", clear_on_submit=True):
    budget = st.selectbox("Select your budget:", ["Free", "Small Budget", "Big Budget"])
    context = st.selectbox("Where are you?", ["From Home", "Out and About"])
    submit_suggestion = st.form_submit_button("Get Idea")

    if submit_suggestion:
        suggestions = KINDNESS_SUGGESTIONS.get(budget, {}).get(context, [])
        if suggestions:
            suggestion = random.choice(suggestions)
            st.session_state.custom_suggestion = suggestion
            st.success(f"**Kindness Idea:** {suggestion}")
        else:
            st.error("No suggestions available for this combination.")

# Form to submit custom kindness idea
if "custom_suggestion" in st.session_state:
    with st.form("custom_challenge_form", clear_on_submit=True):
        st.write(f"**Complete this idea:** {st.session_state.custom_suggestion}")
        custom_completed = st.checkbox("I completed this act!", key="custom_completed")
        submit_custom = st.form_submit_button("Submit")

        if submit_custom and custom_completed:
            new_act = pd.DataFrame({"Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Act of Kindness": [st.session_state.custom_suggestion]})
            try:
                df = pd.read_csv(DATA_FILE)
                df = pd.concat([df, new_act], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                del st.session_state.custom_suggestion
                st.success("Custom kind act logged successfully!")
            except Exception as e:
                st.error(f"Failed to log act: {str(e)}")

# Log a kind act
st.markdown('<p class="subheader">Log Your Kind Act</p>', unsafe_allow_html=True)
with st.form("log_form", clear_on_submit=True):
    act = st.text_area("Describe the kind act you performed:", placeholder="e.g., Complimented a stranger")
    submit_log = st.form_submit_button("Log Act")

    if submit_log and act:
        new_act = pd.DataFrame({"Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Act of Kindness": [act.strip()]})
        try:
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_act], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Kind act logged successfully!")
        except Exception as e:
            st.error(f"Failed to log act: {str(e)}")

# Display logged acts
st.markdown('<p class="subheader">Your Kind Acts</p>', unsafe_allow_html=True)
try:
    df = pd.read_csv(DATA_FILE)
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        st.dataframe(df.sort_values(by="Date", ascending=False)[["Date", "Act of Kindness"]], use_container_width=True)
    else:
        st.write("No kind acts logged yet. Start today!")
except Exception as e:
    st.error(f"Failed to display acts: {str(e)}")

# Add footer with credit
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<p class="footer">Made with love by Cara</p>', unsafe_allow_html=True)
