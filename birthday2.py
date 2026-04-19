import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("Which Birthday Month Is Most Common?")
st.write("Hypothesis: I think July will be the most common birth month.")
st.write("Help me find out by entering your information below!")

# Month options
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Second question (gender)
gender_options = ["Boy", "Girl", "No comment"]

# User inputs
selected_month = st.selectbox("Select your birth month:", months)
selected_gender = st.selectbox(
    "Are you a boy, girl, or prefer not to comment?",
    gender_options
)

# File to store data
file_name = "birthdays.csv"

# Load existing data or create new
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=["month", "gender"])

# Submit button
if st.button("Submit"):
    new_data = pd.DataFrame({
        "month": [selected_month],
        "gender": [selected_gender]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file_name, index=False)
    st.success("Thanks! Your response was helpful!")

# Show results if data exists
if len(df) > 0:
    st.subheader("Survey Results")

    # Split data
    boy_df = df[df["gender"] == "Boy"]
    girl_df = df[df["gender"] == "Girl"]
    no_comment_df = df[df["gender"] == "No comment"]

    # Count months
    boy_counts = boy_df["month"].value_counts().reindex(months, fill_value=0)
    girl_counts = girl_df["month"].value_counts().reindex(months, fill_value=0)
    no_comment_counts = no_comment_df["month"].value_counts().reindex(months, fill_value=0)

    # Create three columns for graphs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Boy")
        fig1, ax1 = plt.subplots()
        ax1.bar(months, boy_counts)
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Number of People")
        ax1.tick_params(axis="x", rotation=45)
        st.pyplot(fig1)

    with col2:
        st.write("Girl")
        fig2, ax2 = plt.subplots()
        ax2.bar(months, girl_counts)
        ax2.set_xlabel("Month")
        ax2.set_ylabel("Number of People")
        ax2.tick_params(axis="x", rotation=45)
        st.pyplot(fig2)

    with col3:
        st.write("No comment")
        fig3, ax3 = plt.subplots()
        ax3.bar(months, no_comment_counts)
        ax3.set_xlabel("Month")
        ax3.set_ylabel("Number of People")
        ax3.tick_params(axis="x", rotation=45)
        st.pyplot(fig3)

    # Show totals
    st.write("Total responses:", len(df))

    # Most / least common overall
    total_counts = df["month"].value_counts().reindex(months, fill_value=0)

    max_count = total_counts.max()
    min_count = total_counts.min()

    most_common = total_counts[total_counts == max_count].index.tolist()
    least_common = total_counts[total_counts == min_count].index.tolist()

    st.write("Most common month(s):", most_common)
    st.write("Least common month(s):", least_common)
