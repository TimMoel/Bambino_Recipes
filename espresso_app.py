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

# Load external CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Bambino Espresso Recipes")
st.markdown("Share and vote on your favorite espresso recipes for the Sage Bambino machine!")

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
    <div class="full-width-box">
        <h2>🔥 Top Recipes</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Add filter interface
filter_type = st.radio(
    "Filter by Shot Type:",
    ["All", "Single", "Double"],
    horizontal=True,
    key="filter"
)

st.markdown('<hr class="recipe-separator" />', unsafe_allow_html=True)

if df.empty:
    st.info("No recipes to show yet.")
else:
    # Filter the dataframe based on selection
    if filter_type != "All":
        df_display = df[df["Shot Type"] == filter_type]
    else:
        df_display = df.copy()

    for idx, row in df_display.sort_values("Score", ascending=False).iterrows():
        st.markdown(
            f"""
            <div style="position: relative;">
                <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background-color: #ff6600;"></div>
                <div style="margin-left: 12px; margin-top: 0.1rem;">
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
            <div class="recipe-separator">────────────────────────────────────────────────────────────────────────────────────────────────────</div>
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
