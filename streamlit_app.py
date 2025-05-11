import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File to store kind acts
DATA_FILE = "kind_acts.csv"

# Initialize the CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Act of Kindness"])
    df.to_csv(DATA_FILE, index=False)

# Streamlit app title
st.title("Kindness Tracker")
st.write("Log and celebrate acts of kindness to spread positivity!")

# Form to add a new kind act
with st.form("kindness_form"):
    act = st.text_area("Describe an act of kindness:", placeholder="e.g., Helped a neighbor with groceries")
    submit = st.form_submit_button("Add Kind Act")

    if submit and act:
        # Append the new act to the CSV
        new_act = pd.DataFrame({"Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Act of Kindness": [act]})
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_act], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Kind act added successfully!")

# Display all kind acts
st.subheader("Logged Acts of Kindness")
df = pd.read_csv(DATA_FILE)
if not df.empty:
    st.dataframe(df.sort_values(by="Date", ascending=False))
else:
    st.write("No kind acts logged yet. Start spreading kindness!")

# Add a motivational quote
st.markdown("**Quote of the Day:** *“No act of kindness, no matter how small, is ever wasted.”* — Aesop")

# Add footer with credit
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Made by Cara</p>", unsafe_allow_html=True)
