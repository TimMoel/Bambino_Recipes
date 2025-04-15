import streamlit as st
import pandas as pd
import os

CSV_FILE = "espresso_recipes.csv"

# Initialize CSV if it doesn't exist
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=[
        "Dose", "Grind Size", "Pre-infusion Time", "Yield", "Shot Time", "Shot Type", "Score"
    ])
    df_init.to_csv(CSV_FILE, index=False)

# Load CSV and ensure columns are clean
df = pd.read_csv(CSV_FILE, usecols=lambda col: col != 'Unnamed: 0')

expected_columns = ["Dose", "Grind Size", "Pre-infusion Time", "Yield", "Shot Time", "Shot Type", "Score"]
rename_map = {
    "Grind": "Grind Size",
    "Tamp": "Pre-infusion Time",
    "Time": "Shot Time"
}
df.rename(columns=rename_map, inplace=True)
for col in expected_columns:
    if col not in df.columns:
        df[col] = "" if col in ["Grind Size", "Shot Type", "Shot Time"] else 0

df = df[expected_columns]

st.set_page_config(page_title="Bambino Espresso Recipes", layout="wide")
st.title("☕ Bambino Espresso Recipes")
st.markdown("Share and vote on your favorite espresso recipes for the Sage Bambino machine!")

# Vote button styling (compact and centered vertically)
st.markdown("""
    <style>
    .vote-button-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
        padding-top: 0.5rem;
    }
    .vote-button-wrapper button {
        padding: 0px !important;
        font-size: 8px !important;
        margin: 1px 0 !important;
        line-height: 1 !important;
        background-color: #ffffff !important;
        color: #ff6600 !important;
        border: none !important;
        min-height: 16px !important;
        width: 16px !important;
        border-radius: 0px !important;
    }
    .vote-button-wrapper button:hover {
        background-color: #ffffff !important;
        color: #ff8533 !important;
    }
    .recipe-container {
        margin-bottom: 0.75rem;
        border-left: 3px solid #ff6600;
        padding-left: 0.5rem;
        font-family: monospace;
        font-size: 13px;
        line-height: 1.4;
    }
    .recipe-header {
        color: #828282;
        margin-bottom: 0.25rem;
    }
    .recipe-details {
        color: #ffffff;
    }
    .recipe-score {
        color: #ff6600;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #ff6600 !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #e65c00 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Filter by shot type
shot_filter = st.radio("☕ Filter by Shot Type", options=["All", "Single", "Double"], horizontal=True)

# Collapsible form
with st.expander("➕ Submit a New Recipe"):
    with st.form("submit_form"):
        dose = st.number_input("Dose (g)", min_value=0.0)
        grind = st.text_input("Grind Size")
        preinfusion = st.number_input("Pre-infusion Time (s)", min_value=0.0)
        yield_ = st.number_input("Yield (g)", min_value=0.0)
        shot_time = st.text_input("Shot Time (e.g. 25-30 sec)")
        shot_type = st.selectbox("Shot Type", options=["Single", "Double"])
        submitted = st.form_submit_button("Submit Recipe")

        if submitted:
            new_recipe = pd.DataFrame([{
                "Dose": dose,
                "Grind Size": grind,
                "Pre-infusion Time": preinfusion,
                "Yield": yield_,
                "Shot Time": shot_time,
                "Shot Type": shot_type,
                "Score": 0
            }])
            df = pd.concat([df, new_recipe], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            st.success("✅ Recipe submitted successfully!")
            st.rerun()

# Apply shot type filter
if shot_filter != "All":
    df = df[df["Shot Type"] == shot_filter]

# Display recipes in table format
st.subheader("🔥 Top Recipes")
if df.empty:
    st.info("No recipes to show yet.")
else:
    for idx, row in df.sort_values("Score", ascending=False).iterrows():
        col1, col2 = st.columns([9, 1])
        with col1:
            st.markdown(f"""
            <div class="recipe-container">
                <div class="recipe-header">
                    <span class="recipe-score">{int(row['Score'])} points</span> | {row['Shot Type']} shot
                </div>
                <div class="recipe-details">
                    {row['Dose']}g dose | {row['Grind Size']} grind | {row['Pre-infusion Time']}s pre-infusion
                </div>
                <div class="recipe-details">
                    {row['Yield']}g yield | {row['Shot Time']} shot time
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown('''
            <style>
            .custom-upvote button {
                background: #fff !important;
                color: #ff6600 !important;
                border: none !important;
                border-radius: 4px !important;
                width: 22px !important;
                height: 22px !important;
                font-size: 16px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                cursor: pointer !important;
                padding: 0 !important;
            }
            .custom-upvote button:hover {
                background: #f6f6ef !important;
                color: #ff8533 !important;
            }
            </style>
            ''', unsafe_allow_html=True)
            if st.button("▲", key=f"up_{idx}", help="Upvote", type="secondary"):
                df.at[idx, 'Score'] += 1
                df.to_csv(CSV_FILE, index=False)
                st.rerun()
            st.markdown('<div class="custom-upvote"></div>', unsafe_allow_html=True)
