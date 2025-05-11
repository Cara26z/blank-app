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

# Define kindness suggestions based on budget and context
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
            "Order a small plant online for a loved one to brighten their space).",
            "Donate a small amount to a local charity online.",
            "Purchase and send a digital book to inspire someone."
        ],
        "Out and About": [
            "Buy a coffee for the person behind you in line.",
            "Leave a generous tip for a server or barista.",
            "Purchase a small treat for a coworker or neighbor.",
            "Buy flowers to give to someone you meet).",
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
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    sorted_dates = df['Date'].sort_values(ascending=False).unique()
    streak = 0
    today = date.today()
    current = today
    for d in sorted_dates:
        if d == current:
            streak += 1
            current = current - pd.Timedelta(days=1)
        else:
            break
    return streak
  

    if submit_daily and completed:
        new_act = pd.DataFrame({"Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Act of Kindness": [st.session_state.daily_suggestion]})
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_act], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Kind act logged successfully!")
        # Reset daily suggestion to encourage a new act tomorrow
        st.session_state.daily_suggestion = random.choice(
            [act for budget in KINDNESS_SUGGESTIONS for context in KINDNESS_SUGGESTIONS[budget] for act in KINDNESS_SUGGESTIONS[budget][context]]
        )

    if new_challenge:
        st.session_state.daily_suggestion = random.choice(
            [act for budget in KINDNESS_SUGGESTIONS for context in KINDNESS_SUGGESTIONS[budget] for act in KINDNESS_SUGGESTIONS[budget][context]]
        )
        st.experimental_rerun()

# Streamlit app title
st.title("Daily Kindness Challenge")
st.write("Get inspired with kindness ideas and track your daily acts to build a streak!")

# Display streak
df = pd.read_csv(DATA_FILE)
streak = calculate_streak(df)
st.subheader(f"Your Kindness Streak: {streak} Day{'s' if streak != 1 else ''}!")

# Celebrate milestones
if streak in [5, 10, 30]:
    st.balloons()
    st.success(f"Wow! You've reached a {streak}-day kindness streak! Keep spreading joy!")



st.markdown(f"**Try this today:** {st.session_state.daily_suggestion}")

# Form to check off or get a new challenge
with st.form("daily_challenge_form"):
    completed = st.checkbox("I completed this act!")
    submit_daily = st.form_submit_button("Submit")
    new_challenge = st.form_submit_button("Get a New Challenge")

# Daily kindness challenge
st.subheader("Today's Kindness Challenge")
daily_suggestion = random.choice(
    [act for budget in KINDNESS_SUGGESTIONS for context in KINDNESS_SUGGESTIONS[budget] for act in KINDNESS_SUGGESTIONS[budget][context]]
)
st.markdown(f"**Try this today:** {daily_suggestion}")

# Get a tailored suggestion
st.subheader("Get a Custom Kindness Idea")
with st.form("suggestion_form"):
    budget = st.selectbox("Select your budget:", ["Free", "Small Budget", "Big Budget"])
    context = st.selectbox("Where are you?", ["From Home", "Out and About"])
    submit_suggestion = st.form_submit_button("Get Idea")

    if submit_suggestion:
        suggestions = KINDNESS_SUGGESTIONS.get(budget, {}).get(context, [])
        if suggestions:
            suggestion = random.choice(suggestions)
            st.success(f"**Kindness Idea:** {suggestion}")
        else:
            st.error("No suggestions available for this combination.")

# Log a kind act
st.subheader("Log Your Own Kind Act")
with st.form("log_form"):
    act = st.text_area("Describe the kind act you performed:", placeholder="e.g., Bought coffee for a stranger")
    submit_log = st.form_submit_button("Log Act")

    if submit_log and act:
        new_act = pd.DataFrame({"Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Act of Kindness": [act]})
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_act], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Kind act logged successfully!")

# Display logged acts
st.subheader("Your Kind Acts")
if not df.empty:
    st.dataframe(df.sort_values(by="Date", ascending=False))
else:
    st.write("No kind acts logged yet. Start today!")

# Add a motivational quote
st.markdown("**Quote of the Day:** *“No act of kindness, no matter how small, is ever wasted.”* — Aesop")

# Add footer with credit
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Made by Cara</p>", unsafe_allow_html=True)
