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

# Apply light theme styling and expand main content
st.markdown("""
    <style>
    /* Expand the main content area */
    [data-testid="stAppViewContainer"] > .main {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    .recipe-details {
        color: #2E2E2E !important;
    }
    .recipe-header {
        color: #2E2E2E !important;
    }
    div[data-testid="stMarkdownContainer"] {
        color: #2E2E2E;
    }
    .stRadio label {
        color: #2E2E2E !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("☕ Bambino Espresso Recipes")
st.markdown("Share and vote on your favorite espresso recipes for the Sage Bambino machine!")

# Add styling for spacing
st.markdown("""
    <style>
    /* Remove all spacing from subheading */
    div[data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }
    
    /* Remove spacing from expander */
    section[data-testid="stExpander"] {
        margin-top: 0.25rem !important;
        padding-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    /* Target the expander content */
    .streamlit-expanderHeader {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove spacing from title and description */
    .stTitle, div[data-testid="stMarkdownContainer"] {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }

    /* Reduce spacing after title */
    h1 {
        margin-bottom: 0.25rem !important;
    }
    
    /* Remove any default paragraph spacing */
    p {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

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
        color: #2E2E2E;
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
        color: #ff6600 !important;
        font-family: monospace !important;
        font-size: 13px !important;
        padding: 0 !important;
        margin: 0 !important;
        background: none !important;
        border: none !important;
        line-height: inherit !important;
        display: inline !important;
        vertical-align: baseline !important;
    }
    .stButton > button:hover {
        opacity: 0.8 !important;
    }
    div[data-testid="stMarkdownContainer"] {
        display: inline-block !important;
        margin-right: 4px !important;
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

# Display recipes in table format
st.markdown(
    """
    <style>
    .full-width-box {
        width: 100%;
        max-width: 100%;
        background-color: #ff6600;
        padding: 8px 16px;
        border-radius: 6px;
        box-sizing: border-box;
        margin-bottom: 1rem;
    }
    .full-width-box h2 {
        color: white !important;
        font-size: 16px !important;
        margin: 0 !important;
        font-weight: normal !important;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* This forces the parent markdown container to behave like a block */
    div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
        display: block !important;
    }
    </style>

    <div class="full-width-box">
        <h2>🔥 Top Recipes</h2>
    </div>
    """,
    unsafe_allow_html=True
)

if df.empty:
    st.info("No recipes to show yet.")
else:
    for idx, row in df.sort_values("Score", ascending=False).iterrows():
        st.markdown(
            f"""
            <div style="position: relative;">
                <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background-color: #ff6600;"></div>
                <div style="margin-left: 12px;">
                    <div style="font-family: monospace; font-size: 13px; margin-bottom: 4px;">
                        <span style="color: #ff6600; font-weight: bold">{int(row["Score"])} points</span>
                        <span style="color: #666666"> | </span>
                        <span style="color: #666666">{row["Shot Type"]} shot</span>
                        <span style="color: #666666"> | </span>
                        <a href="?vote={idx}" target="_self" style="color: #ff6600; text-decoration: none;">upvote</a>
                    </div>
                    <div style="font-family: monospace; font-size: 13px; margin-bottom: 4px;">
                        <span style="color: #ff6600">{row['Dose']}</span><span style="color: #666666">g dose | </span>
                        <span style="color: #ff6600">{row['Grind Size']}</span><span style="color: #666666"> grind | </span>
                        <span style="color: #ff6600">{row['Pre-infusion Time']}</span><span style="color: #666666">s pre-infusion</span>
                    </div>
                    <div style="font-family: monospace; font-size: 13px;">
                        <span style="color: #ff6600">{row['Yield']}</span><span style="color: #666666">g yield | </span>
                        <span style="color: #ff6600">{row['Shot Time']}</span><span style="color: #666666"> shot time</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Handle upvote
    if "vote" in st.query_params:
        vote_idx = st.query_params["vote"]
        if vote_idx.isdigit():
            idx = int(vote_idx)
            if idx < len(df):
                df.at[idx, 'Score'] += 1
                df.to_csv(CSV_FILE, index=False)
                st.query_params.clear()
                st.rerun()

st.markdown("""
    <style>
    div[data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stMarkdownContainer"] > div {
        display: flex !important;
        align-items: center !important;
        gap: 4px !important;
        white-space: nowrap !important;
    }
    .recipe-container {
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
        border-left: 3px solid #ff6600;
        padding-left: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)
