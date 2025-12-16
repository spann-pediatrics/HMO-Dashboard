import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import pydeck as pdk  


st.set_page_config(
    page_title="Bode Lab HMO Dashboard",
    layout="wide",                # makes sure to fill the screen width
    initial_sidebar_state="expanded",
)


# ----------------------------
# Load Data
# ----------------------------

#merged HMO data
@st.cache_data
def load_data():
    df = pd.read_csv("../staging/_merged/hmo_merged.csv")
    return df

df = load_data()

# study locations metadata - manually update this excel as new studies are added
@st.cache_data
def load_locations():
    loc = pd.read_excel("../metadata/study_locations.xlsx")
    return loc

locations = load_locations()

# Merge study locations into your HMO dataframe
df = df.merge(locations, on="StudyID", how="left")


# study descriptions metadata - manually update this excel as new studies are added
@st.cache_data
def load_study_descriptions():
    desc = pd.read_excel("../metadata/study_descriptions.xlsx")
    desc.columns = desc.columns.str.strip()  # clean whitespace
    return desc

study_desc = load_study_descriptions()




# ----------------------------
# --- Sidebar Navigation ---
# ----------------------------

# load the UCSD logo from assets folder
st.sidebar.image("assets/UCSD-Logo.png", use_container_width=True)


st.sidebar.title("Bode Lab Dashboard")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "HMO Composition", "Statistics"],  #change page names as needed
)

st.sidebar.markdown("### Lab Website")       # include lab website link (if wanted)
st.sidebar.link_button(
    "Visit Bode Lab site",
    "https://www.bodelab.com/"  # TODO: replace with real URL
)


# ----------------------------
# --- Custom CCS Styles ---
# ----------------------------


st.markdown(
    """
    <style>
    /* ---------- Layout + Background ---------- */
    /* Main content background */
    .main {
        background-color: #f5f7fb;
    }

    /* Center content a bit and give breathing room */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #eef2f7;
    }

    /* ---------- Brand Colors ---------- */
    :root {
        --ucsd-blue: #005b96;
        --ucsd-gold: #ffcd00;
        --text-muted: #6b7280;
        --text-dark: #111827;
        --card-bg: #ffffff;
        --card-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        --radius-xl: 0.9rem;
    }

    /* ---------- KPI & Info Cards ---------- */
    .card {
        padding: 1rem 1.5rem;
        border-radius: var(--radius-xl);
        background-color: var(--card-bg);
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(148, 163, 184, 0.15);
    }

    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--text-muted);
        margin-bottom: 0.25rem;
    }

    .metric-value {
        font-size: 1.9rem;
        font-weight: 600;
        color: var(--text-dark);
    }

    /* ---------- Links (Key Resources, etc.) ---------- */
    .card a.card-link, .card a {
        color: var(--ucsd-blue);
        text-decoration: none;
        font-size: 0.9rem;
    }

    .card a.card-link:hover, .card a:hover {
        text-decoration: underline;
    }

    .card-link {
    display: block;
    margin-bottom: 0.4rem;
    }


    /* ---------- Titles / Section headers ---------- */
    h1, h2, h3, h4 {
        color: var(--text-dark);
    }

    /* tighten space under section headings slightly */
    h3 {
        margin-bottom: 0.4rem;
    }

    /* ---------- Search input styling ---------- */
    input[type="text"] {
        border-radius: 999px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# fonts 

st.markdown("""
<!-- Titles: Merriweather -->
<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap" rel="stylesheet">

<!-- Body: Source Sans Pro -->
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
/* Titles get the serif font */
h1, h2, h3, h4 {
    font-family: 'Merriweather', serif !important;
}

/* Everything else gets Source Sans Pro */
html, body, [class*="css"] {
    font-family: 'Source Sans Pro', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)








# ----------------------------
# --- Overview Page ---
# ----------------------------


if page == "Overview":
    st.markdown("## Overview - Bode Lab Human Milk Oligosaccaride Studies")

    # ---- compute metrics ----
    n_studies = df["StudyID"].nunique()
    n_samples = df["SampleName"].nunique()
    date_updated = datetime.today().strftime("%Y-%m-%d")

    samples_with_location = (
        df[df["Latitude"].notna() & df["Longitude"].notna()]["SampleName"]
        .nunique()
    )

    # ---- layout: left grid of 4 KPIs, right tall resources card ----
    col_main, col_resources = st.columns([2, 1])

    # LEFT: 2x2 grid of KPI cards
    with col_main:
        # top row
        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">Dashboard Last Updated:</div>
                    <div class="metric-value" style="font-size: 1.5rem;">
                        <span style="font-style: italic; color: #6b7280;">
                            {date_updated}
                        </span>
                    </div>
                </div>
                """,
    unsafe_allow_html=True,
)

        with kpi2:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">Number of Studies Included:</div>
                    <div class="metric-value">{n_studies}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # bottom row
        kpi3, kpi4 = st.columns(2)

        #change this metric !!!!!!!!!!!!!!!!!!!!!
        with kpi3:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">Unique Samples:</div>
                    <div class="metric-value">{n_samples}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kpi4:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">Update with New Metrics!</div>
                    <div class="metric-value">{n_samples}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # RIGHT: tall Key Resources card that visually spans both rows
    with col_resources:
        st.markdown(
            """
            <div class="card" style="height: 100%; min-height: 220px;">
                <div class="metric-label">Key Resources</div>
                <a class="card-link" href="https://pubmed.ncbi.nlm.nih.gov/22513036/" target="_blank">
                    1. Human Milk Oligosaccharides: every baby needs a sugar mama (2012)
                </a>
                <a class="card-link" href="https://pubmed.ncbi.nlm.nih.gov/32160614/" target="_blank">
                    2. Human Milk Oligosaccharides: Structure and Functions (2020)
                </a>
                <a class="card-link" href="https://pubmed.ncbi.nlm.nih.gov/33328245/" target="_blank">
                    3. Human Milk Oligosaccharide DSLNT and gut microbiome in preterm infants predicts necrotising entercolitis (2021)
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---- existing section: Study Locations map below ----
    st.markdown("### Study Locations")


    # ---- your existing study_summary + map code ----
    study_summary = (
        df.groupby(["StudyID", "Institution", "City", "Country", "Analyzed"])
          .agg(
              Latitude=("Latitude", "mean"),
              Longitude=("Longitude", "mean"),
              n_samples=("SampleName", "nunique"),
          )
          .reset_index()
    )

    study_summary["Analyzed"] = (
        pd.to_datetime(study_summary["Analyzed"])
          .dt.strftime("%Y-%m-%d")
    )

    mid_lat = study_summary["Latitude"].mean()
    mid_lon = study_summary["Longitude"].mean()

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=study_summary,
        get_position="[Longitude, Latitude]",
        get_radius=200000,
        get_fill_color=[230, 40, 20, 160],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=mid_lat,
        longitude=mid_lon,
        zoom=2,
        pitch=0,
    )

    tooltip = {
        "html": (
            "<b>Study:</b> {StudyID}<br/>"
            "<b>Institution:</b> {Institution}<br/>"
            "<b>Country:</b> {Country}<br/>"
            "<b>Samples:</b> {n_samples}<br/>"
            "<b>Date Analyzed:</b> {Analyzed}"
        ),
        "style": {"backgroundColor": "white", "color": "black"},
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(r, use_container_width=True)




  # ---- new section: Visual for Number of Samples per Study ----

    # --- Samples per Study bar chart ---
    st.markdown("### Number of Samples per Study")

    study_counts = (
        df.groupby("StudyID")["SampleName"]
        .nunique()
        .reset_index(name="n_samples")
    )

    ucsd_blue = "#00356B"  # official UCSD navy shade

    bar = (
        alt.Chart(study_counts)
        .mark_bar(color=ucsd_blue)
        .encode(
            x=alt.X(
                "StudyID:N",
                title="Study",
                sort="-y",
                axis=alt.Axis(labelAngle=-35)  # tilt labels
            ),
            y=alt.Y(
                "n_samples:Q",
                title="Number of Unique Samples"
            ),
            tooltip=["StudyID", "n_samples"]
        )
        .properties(height=450)
    )

    st.altair_chart(bar, use_container_width=True)









    # ---- new section: Study Descriptions ----
    st.markdown("### About the Studies Included")

    # Search box
    query = st.text_input("Search studies", value="", placeholder="Search by StudyID…")

    # Filter by StudyID or Description
    if query:
        filtered_desc = study_desc[
            study_desc["StudyID"].str.contains(query, case=False, na=False) |
            study_desc["Description"].str.contains(query, case=False, na=False)
        ]
    else:
        filtered_desc = study_desc.copy()

    # Handle no matches
    if filtered_desc.empty:
        st.info("No studies match your search.")
    else:
        # Sort alphabetically for consistency
        filtered_desc = filtered_desc.sort_values("StudyID")

        for _, row in filtered_desc.iterrows():
            st.markdown(
                f"""
                <div class="card" style="margin-bottom: 0.75rem; font-size: 0.95rem;">
                    <div class="metric-label">{row['StudyID']}</div>
                    <div>{row['Description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )







#####################################################
# --------- PLACEHOLDERS FOR OTHER "PAGES" ---------
#####################################################


elif page == "HMO Composition":
    st.markdown("## HMO Composition")
    st.info("We’ll put stacked bars, secretor vs non-secretor plots, etc. here.")

elif page == "Statistics":
    st.markdown("## Statistical Analyses")
    st.info("We’ll add PCA, correlations, and models here later.")



