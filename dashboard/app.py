import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../staging/_merged/hmo_merged.csv")
    return df

df = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

secretor_options = ["All"] + sorted(df["Secretor"].dropna().unique())
secretor_filter = st.sidebar.selectbox("Secretor Status", secretor_options)

study_options = ["All"] + sorted(df["Study ID"].dropna().unique())
study_filter = st.sidebar.selectbox("Study", study_options)

# Filter logic
filtered = df.copy()

if secretor_filter != "All":
    filtered = filtered[filtered["Secretor"] == secretor_filter]

if study_filter != "All":
    filtered = filtered[filtered["Study ID"] == study_filter]

# ----------------------------
# KPI Cards
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Unique Studies", df["Study ID"].nunique())
col2.metric("Total Samples", df["Sample Name"].nunique())
col3.metric("Secretors (%)", 
            f"{(df['Secretor'].eq('Secretor').mean() * 100):.1f}%")

st.title("HMO Composition Dashboard")

# ----------------------------
# Stacked Bar Composition Plot
# ----------------------------
# Identify HMO % columns (anything ending in '%')
pct_cols = [c for c in df.columns if c.endswith("%")]

long_df = filtered.melt(
    id_vars=["Sample Name"],
    value_vars=pct_cols,
    var_name="HMO",
    value_name="Relative Abundance"
)

stacked_plot = (
    alt.Chart(long_df)
    .mark_bar()
    .encode(
        x=alt.X("Sample Name:N", sort=None, axis=alt.Axis(labels=False)),
        y=alt.Y("Relative Abundance:Q", stack="normalize"),
        color="HMO:N",
        tooltip=["Sample Name", "HMO", "Relative Abundance"]
    )
    .properties(height=300, width=1000)
)

st.subheader("Relative Abundance Stacked Bar (per Sample)")
st.altair_chart(stacked_plot, use_container_width=True)

st.write(f"Showing **{len(filtered)} samples**")
