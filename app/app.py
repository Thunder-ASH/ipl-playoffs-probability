import streamlit as st
import pandas as pd
import sys, os

from sim.simulator import run_simulations

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../sim")))
st.set_page_config(layout="wide")

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>

/* Reddit-like font */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
}

/* Reduce page padding */
.block-container {
    padding-top: 0.8rem;
    padding-bottom: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Kill vertical gaps */
div[data-testid="stVerticalBlock"] > div {
    padding-top: 0.05rem !important;
    padding-bottom: 0.05rem !important;
}

/* Remove column padding */
div[data-testid="column"] {
    padding: 0 !important;
}

/* Reduce row spacing */
.element-container {
    margin-bottom: 0.2rem !important;
}

/* Header */
.header {
    font-size: 13px;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 500;
}

/* Data text */
.metric {
    font-size: 20px;
    font-weight: 500;
}

/* Points highlight */
.bold {
    font-weight: 750;
    font-size: 21px;
}

/* Small text */
.small {
    font-size: 17px;
    color: #9ca3af;
}

/* Divider */
.divider {
    border-bottom: 1px solid #1f2937;
    margin-top: 4px;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("PLAYOFF PROBABILITY")
st.markdown(
    "<div class='small' style='margin-bottom:6px;'>As of Apr 27</div>",
    unsafe_allow_html=True
)

# ---------- RUN ----------
teams, top4, top2, points_range = run_simulations()

# ---------- DATA ----------
data = []
for t in teams:
    data.append({
        "Team": t,
        "M": teams[t]["played"],
        "W": teams[t]["won"],
        "L": teams[t]["lost"],
        "Pts": teams[t]["points"],
        "NRR": teams[t]["nrr"],
        "Top4": round(top4[t]*100,1),
        "Top2": round(top2[t]*100,1)
    })

df = pd.DataFrame(data)
df = df.sort_values(by=["Pts","NRR"], ascending=False).reset_index(drop=True)

# ---------- HEADER ----------
cols = st.columns([0.4,1.4,0.5,0.5,0.5,0.8,1.2,3,3])
headers = ["#", "Team", "M", "W", "L", "Pts", "NRR", "Top 4", "Top 2"]

for col, h in zip(cols, headers):
    col.markdown(f"<div class='header'>{h}</div>", unsafe_allow_html=True)

# Thin divider (instead of st.divider)
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ---------- ROWS ----------
for i, row in df.iterrows():
    cols = st.columns([0.4,1.4,0.5,0.5,0.5,0.8,1.2,3,3])

    cols[0].markdown(f"<div class='metric'>{i+1}</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div class='metric'>{row['Team']}</div>", unsafe_allow_html=True)

    cols[2].markdown(f"<div class='metric'>{row['M']}</div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div class='metric'>{row['W']}</div>", unsafe_allow_html=True)
    cols[4].markdown(f"<div class='metric'>{row['L']}</div>", unsafe_allow_html=True)

    # Points bold
    cols[5].markdown(f"<div class='metric bold'>{row['Pts']}</div>", unsafe_allow_html=True)

    # NRR colored
    nrr_color = "#22c55e" if row["NRR"] > 0 else "#ef4444"
    cols[6].markdown(
        f"<div class='metric' style='color:{nrr_color}'>{row['NRR']:.2f}</div>",
        unsafe_allow_html=True
    )

    # Top 4 (bar + % inline)
    with cols[7]:
        bar, pct = st.columns([4,1])
        bar.progress(row["Top4"]/100)
        pct.markdown(f"<div class='small'>{row['Top4']}%</div>", unsafe_allow_html=True)

    # Top 2
    with cols[8]:
        bar, pct = st.columns([4,1])
        bar.progress(row["Top2"]/100)
        pct.markdown(f"<div class='small'>{row['Top2']}%</div>", unsafe_allow_html=True)

    # Thin row divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)