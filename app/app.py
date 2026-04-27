import streamlit as st
import pandas as pd
import sys, os

# FIX IMPORT PATH (must be BEFORE import)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sim.simulator import run_simulations


# ---------------- UI SETTINGS ----------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
/* Reduce top/bottom padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Smaller row spacing */
.row {
    margin-bottom: 6px;
}

/* Header style */
.header {
    font-size: 13px;
    color: #8b949e;
    font-weight: 500;
}

/* Team name */
.team {
    font-size: 15px;
    font-weight: 600;
}

/* Points bold */
.points {
    font-weight: 700;
    font-size: 16px;
}

/* Bar background */
.bar-bg {
    background: #1f2937;
    height: 8px;
    border-radius: 6px;
    width: 100%;
}

/* Bar fill */
.bar-fill {
    height: 8px;
    border-radius: 6px;
    background: linear-gradient(90deg, #3b82f6, #22c55e);
}

/* Thin separator */
.sep {
    border-bottom: 1px solid #1f2937;
    margin: 4px 0;
}
</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.title("IPL Playoff Probability")
st.caption("Monte Carlo Simulation")

# ---------------- DATA ----------------
teams, top4, top2, pts_range = run_simulations()

# Convert to dataframe
data = []
for t in teams:
    data.append({
        "Team": t,
        "M": teams[t]["played"],
        "Pts": teams[t]["points"],
        "NRR": teams[t]["nrr"],
        "Top4": round(top4[t] * 100, 1),
        "Top2": round(top2[t] * 100, 1),
        "Range": pts_range[t]
    })

df = pd.DataFrame(data)
df = df.sort_values(by=["Pts", "NRR"], ascending=False).reset_index(drop=True)


# ---------------- HEADER ----------------
cols = st.columns([0.5, 2.5, 0.7, 0.8, 1.0, 3, 3])

headers = ["#", "TEAM", "M", "PTS", "NRR", "TOP 4", "TOP 2"]

for col, h in zip(cols, headers):
    col.markdown(f"<div class='header'>{h}</div>", unsafe_allow_html=True)

st.markdown("<div class='sep'></div>", unsafe_allow_html=True)


# ---------------- ROWS ----------------
for i, row in df.iterrows():
    cols = st.columns([0.5, 2.5, 0.7, 0.8, 1.0, 3, 3])

    # Rank
    cols[0].write(i + 1)

    # Team
    cols[1].markdown(f"<div class='team'>{row['Team']}</div>", unsafe_allow_html=True)

    # Matches
    cols[2].write(int(row["M"]))

    # Points (bold)
    cols[3].markdown(f"<div class='points'>{int(row['Pts'])}</div>", unsafe_allow_html=True)

    # NRR
    nrr_color = "#22c55e" if row["NRR"] >= 0 else "#ef4444"
    cols[4].markdown(
        f"<span style='color:{nrr_color}'>{row['NRR']:.2f}</span>",
        unsafe_allow_html=True
    )

    # -------- TOP 4 BAR --------
    cols[5].markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;">
        <div class="bar-bg">
            <div class="bar-fill" style="width:{row['Top4']}%"></div>
        </div>
        <div style="font-size:12px;">{row['Top4']}%</div>
    </div>
    """, unsafe_allow_html=True)

    # -------- TOP 2 BAR --------
    cols[6].markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;">
        <div class="bar-bg">
            <div class="bar-fill" style="width:{row['Top2']}%"></div>
        </div>
        <div style="font-size:12px;">{row['Top2']}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Separator
    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)