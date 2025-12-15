import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import pydeck as pdk  


# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("../staging/_merged/hmo_merged.csv")
    return df

df = load_data()

@st.cache_data
def load_locations():
    # Adjust the path if needed
    loc = pd.read_excel("../metadata/study_locations.xlsx")
    return loc

locations = load_locations()

# Merge study locations into your HMO dataframe
df = df.merge(locations, on="StudyID", how="left")

@st.cache_data
def load_study_descriptions():
    desc = pd.read_excel("../metadata/study_descriptions.xlsx")
    desc.columns = desc.columns.str.strip()  # clean whitespace
    return desc

study_desc = load_study_descriptions()



# st.write("Location df columns:", locations.columns.tolist())
# st.write("Merged df columns:", df.columns.tolist())


# --- Sidebar Navigation ---
st.sidebar.title("Bode Lab Dashboard")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "HMO Composition", "Statistics"],
)

st.sidebar.markdown("### Lab Website")
st.sidebar.link_button(
    "Visit Bode Lab site",
    "https://www.bodelab.com/"  # TODO: replace with real URL
)





st.markdown(
    """
    <style>
    .card {
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        background-color: #ffffff;
        box-shadow: 0 1px 3px rgba(15, 15, 15, 0.12);
    }
    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6c757d;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #111827;
    }

    /* NEW: scrollable card for links */
    .scroll-card {
        max-height: 220px;      /* adjust height */
        overflow-y: auto;
    }
    .card-link {
        display: block;
        margin-bottom: 0.4rem;
        color: #2563eb;
        text-decoration: none;
        font-size: 0.9rem;
    }
    .card-link:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)




# --------- NAV + STYLES (from steps 1 & 2) go here ---------


# --------- OVERVIEW PAGE ---------
if page == "Overview":
    st.markdown("## Bode Lab: HMO Analysis Overview")

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
                    <div class="metric-label">Number of Studies</div>
                    <div class="metric-value">{n_studies}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kpi2:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">Unique Samples</div>
                    <div class="metric-value">{n_samples}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # bottom row
        kpi3, kpi4 = st.columns(2)
        with kpi3:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">Samples with Location</div>
                    <div class="metric-value">{samples_with_location}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kpi4:
            st.markdown(
                f"""
                <div class="card">
                    <div class="metric-label">Dashboard Last Updated</div>
                    <div class="metric-value">{date_updated}</div>
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
                    Human Milk Oligosaccharides: every baby needs a sugar mama (2012)
                </a>
                <a class="card-link" href="https://pubmed.ncbi.nlm.nih.gov/32160614/" target="_blank">
                    Human Milk Oligosaccharides: Structure and Functions (2020)
                </a>
                <a class="card-link" href="https://doi.org/10.xxxx/your-paper-2" target="_blank">
                    Secretor Status & Milk Glycans (2022)
                </a>
                <a class="card-link" href="https://doi.org/10.xxxx/your-paper-3" target="_blank">
                    HMO–Microbiome Interactions (Review)
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



