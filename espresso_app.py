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
    .recipe-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        width: 100%;
    }
    .recipe-content {
        flex-grow: 1;
    }
    .vote-button-wrapper {
        margin-left: 20px;
    }
    .vote-button-wrapper button {
        background: rgba(255,255,255,0.1) !important;
        color: #ff6600 !important;
        border: none !important;
        padding: 6px 12px !important;
        font-size: 13px !important;
        font-family: monospace !important;
        cursor: pointer !important;
        border-radius: 4px !important;
    }
    .vote-button-wrapper button:hover {
        background: rgba(255,255,255,0.15) !important;
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
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .recipe-details {
        color: #ffffff;
    }
    .recipe-score {
        color: #ff6600;
        font-weight: bold;
    }
    .upvote-text {
        color: #ff6600;
    }
    .stButton {
        display: inline-block !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .stButton > button {
        all: unset;
        color: #ff6600 !important;
        font-family: monospace !important;
        font-size: 13px !important;
        cursor: pointer !important;
        padding: 0 !important;
        margin: 0 !important;
        display: inline !important;
        background: none !important;
        border: none !important;
        line-height: inherit !important;
        white-space: nowrap !important;
    }
    .stButton > button:hover {
        text-decoration: underline !important;
    }
    [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
        min-width: auto !important;
        width: auto !important;
        flex-shrink: 0 !important;
        white-space: nowrap !important;
    }
    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 0 !important;
        min-width: 300px !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    @media (max-width: 640px) {
        [data-testid="stHorizontalBlock"] {
            min-width: 250px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

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

# Filter by shot type (moved here)
shot_filter = st.radio("☕ Filter by Shot Type", options=["All", "Single", "Double"], horizontal=True)

# Apply shot type filter
if shot_filter != "All":
    df = df[df["Shot Type"] == shot_filter]

# Display recipes in table format
st.subheader("🔥 Top Recipes")
if df.empty:
    st.info("No recipes to show yet.")
else:
    for idx, row in df.sort_values("Score", ascending=False).iterrows():
        header_cols = st.columns([0.15, 0.15])
        with header_cols[0]:
            st.write(f'<span class="recipe-score">{int(row["Score"])} points</span> | {row["Shot Type"]} shot', unsafe_allow_html=True)
        with header_cols[1]:
            if st.button("| upvote", key=f"up_{idx}"):
                df.at[idx, 'Score'] += 1
                df.to_csv(CSV_FILE, index=False)
                st.rerun()
        
        st.markdown(f"""
        <div class="recipe-container">
            <div class="recipe-details">
                {row['Dose']}g dose | {row['Grind Size']} grind | {row['Pre-infusion Time']}s pre-infusion
            </div>
            <div class="recipe-details">
                {row['Yield']}g yield | {row['Shot Time']} shot time
            </div>
        </div>
        """, unsafe_allow_html=True)
