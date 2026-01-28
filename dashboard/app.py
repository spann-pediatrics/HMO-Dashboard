import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import pydeck as pdk  
import plotly as plt
import plotly.express as px


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
    loc = pd.read_excel("../study extras/study_locations.xlsx")
    return loc

locations = load_locations()

# Merge study locations into your HMO dataframe
df = df.merge(locations, on="StudyID", how="left")


# study descriptions metadata - manually update this excel as new studies are added
@st.cache_data
def load_study_descriptions():
    df_desc = pd.read_excel("../study extras/study_descriptions.xlsx")
    df_desc.columns = df_desc.columns.str.strip().str.replace(" ", "_")  # normalize names
    return df_desc

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
        y=alt.Y("StudyID:N", title="Study", sort="-x"),
        x=alt.X("n_samples:Q", title="Number of Unique Samples"),
        tooltip=["StudyID", "n_samples"]
    )
    .properties(height=300)
)

    st.altair_chart(bar, use_container_width=True)










    
    # About the Studies Included
    # -------------------------
    st.markdown("### About the Studies Included")

    # 1) Compute number of samples per study from main df
    sample_counts = (
        df.groupby("StudyID")["SampleName"]
        .nunique()
        .reset_index(name="num_samples")  # <-- we will use THIS name
    )

    # 2) Merge descriptions + sample counts
    # study_desc comes from load_study_descriptions()
    study_info = study_desc.merge(sample_counts, on="StudyID", how="left")

    # 3) Normalize column names from Excel so they are easier to work with in code
    study_info = study_info.rename(columns={
        "collection window": "collection_window",
        "sample type": "sample_type",
    })

    # 4) Search bar
    query = st.text_input(
        "Search studies",
        value="",
        placeholder="Search by StudyID, description, keywords, population, sample type..."
    )

    # 5) Decide which columns we *want* to show
    desired_cols = [
        "StudyID",
        "Description",
        "num_samples",         # <-- uses the computed column name above
        "Keywords",
        "collection_window",
        "population",
        "sample_type",
    ]

    # Only keep the ones that actually exist to avoid KeyErrors
    cols_to_show = [c for c in desired_cols if c in study_info.columns]

    # 6) Filter based on query across several text fields
    if query:
        mask = (
            study_info["StudyID"].astype(str).str.contains(query, case=False, na=False)
            | study_info["Description"].astype(str).str.contains(query, case=False, na=False)
            | study_info["Keywords"].astype(str).str.contains(query, case=False, na=False)
            | study_info.get("population", "").astype(str).str.contains(query, case=False, na=False)
            | study_info.get("sample_type", "").astype(str).str.contains(query, case=False, na=False)
            | study_info.get("collection_window", "").astype(str).str.contains(query, case=False, na=False)
        )
        filtered = study_info[mask]
    else:
        filtered = study_info.copy()

    # 7) Final table for display
    display_df = filtered[cols_to_show].rename(columns={
        "StudyID": "Study ID",
        "num_samples": "# Samples",
        "collection_window": "Collection Window",
        "sample_type": "Sample Type",
        "population": "Population",
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )









#####################################################
# --------- PLACEHOLDERS FOR OTHER "PAGES" ---------
#####################################################


elif page == "HMO Composition":
    st.markdown("## HMO Composition")
    

    # --- Aggregate secretor vs non-secretor per study ---
    comp_df = (
        df
        .dropna(subset=["Secretor", "StudyID"])
        .groupby("StudyID")
        .agg(
            n_total=("Secretor", "count"),
            n_secretor=("Secretor", "sum")  # since 1 = secretor, 0 = non
        )
        .reset_index()
    )

    comp_df["pct_secretor"] = comp_df["n_secretor"] / comp_df["n_total"]
    comp_df["pct_non_secretor"] = 1 - comp_df["pct_secretor"]



    # reshape for staked bar plotting 
    plot_df = comp_df.melt(
        id_vars="StudyID",
        value_vars=["pct_secretor", "pct_non_secretor"],
        var_name="SecretorStatus",
        value_name="Proportion"
    )

    plot_df["SecretorStatus"] = plot_df["SecretorStatus"].map({
        "pct_secretor": "Secretor",
        "pct_non_secretor": "Non-secretor"
    })




    # ----------------------------
    # 1) Identify the 19 HMO columns (use ug/mL columns from your merged file)
    # ----------------------------

    # We want the 19 individual HMOs in ug/mL (NOT the summary columns like SUM)
    HMO_UNIT = "(ug/mL)"
    EXCLUDE_HMO_COLS = {f"SUM {HMO_UNIT}"}  # exclude summary column

    # Auto-detect all ug/mL HMO columns, then remove excluded ones
    HMO_COLS = [
        c for c in df.columns
        if HMO_UNIT in c and c not in EXCLUDE_HMO_COLS
    ]



    
    # --- Layout: Left plot, right text ---

    col1, col2 = st.columns([1.5, 2])


    with col1:
        st.markdown("### Dataset Snapshot")

        # --- KPI values ---
        n_samples = df["SampleName"].nunique()
        n_studies = df["StudyID"].nunique()
        n_hmos = len(HMO_COLS)

        # --- KPI Card 1: Samples ---
        st.markdown(
            f"""
            <div style="padding: 16px; border-radius: 10px; background-color: #F5F7FA; margin-bottom: 12px;">
                <div style="font-size: 14px; color: #6B7280;">Samples Analyzed</div>
                <div style="font-size: 32px; font-weight: 600;">{n_samples:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- KPI Card 2: Studies ---
        st.markdown(
            f"""
            <div style="padding: 16px; border-radius: 10px; background-color: #F5F7FA; margin-bottom: 12px;">
                <div style="font-size: 14px; color: #6B7280;">Studies Represented</div>
                <div style="font-size: 32px; font-weight: 600;">{n_studies}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- KPI Card 3: HMOs ---
        st.markdown(
            f"""
            <div style="padding: 16px; border-radius: 10px; background-color: #F5F7FA;">
                <div style="font-size: 14px; color: #6B7280;">HMOs Quantified</div>
                <div style="font-size: 32px; font-weight: 600;">{n_hmos}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        

    
    with col2:
        fig = px.bar(
        plot_df,
        x="Proportion",
        y="StudyID",
        color="SecretorStatus",
        orientation="h",
        text=plot_df["Proportion"].round(2),
        title="Secretor vs Non-secretor Composition by Study",
        color_discrete_map={
            "Secretor": "#8EC9E6",        # light blue
            "Non-secretor": "#C9C9C9"     # light gray
        }
)

        fig.update_layout(
            barmode="stack",
            xaxis=dict(tickformat=".0%"),
            legend_title=""
        )

        st.plotly_chart(fig, use_container_width=True)







    # Sanity check
    if len(HMO_COLS) == 0:
        st.warning(
            f"No HMO columns found for unit {HMO_UNIT}. "
            "Check your column names (e.g., '2FL (ug/mL)') and update HMO_UNIT / EXCLUDE_HMO_COLS."
        )
        st.stop()

    # ----------------------------
    # 2) Choose ID / metadata columns to carry through the melt
    # ----------------------------
    ID_COLS = [c for c in ["StudyID", "SampleName", "Secretor"]
            if c in df.columns]

    # Optional: ensure the two required IDs exist
    required = {"StudyID", "SampleName"}
    missing = required - set(ID_COLS)
    if missing:
        st.error(f"Missing required columns for plotting: {missing}")
        st.stop()

    # ----------------------------
    # 3) Reshape wide → long (melt)
    # ----------------------------
    plot_df = df[ID_COLS + HMO_COLS].copy()

    long_df = plot_df.melt(
        id_vars=ID_COLS,      # columns to keep (repeated down rows)
        value_vars=HMO_COLS,  # HMO measurement columns to stack
        var_name="HMO",       # new column that stores the HMO name
        value_name="concentration"  # new column that stores the numeric value
)
    
    # ----------------------------
    # 4) Clean concentration + labels
    # ----------------------------
    long_df["concentration"] = pd.to_numeric(long_df["concentration"], errors="coerce")
    long_df = long_df.dropna(subset=["concentration"])

    # Optional: remove units from HMO label for nicer y-axis
    long_df["HMO"] = long_df["HMO"].str.replace(f" {HMO_UNIT}", "", regex=False)

    
    # ----------------------------
    # Add plot-friendly secretor labels
    # ----------------------------
    def secretor_label(x):
        if pd.isna(x):
            return "Unknown"
        s = str(x).strip().lower()
        if s in {"1", "1.0"}:
            return "Secretor"
        if s in {"0", "0.0"}:
            return "Non-secretor"
        return "Unknown"

    long_df["SecretorLabel"] = long_df["Secretor"].apply(secretor_label)

    # Sanity check (temporary, remove later)
    st.caption(long_df["SecretorLabel"].value_counts().to_dict())



    # ----------------------------
    # 6) Sidebar filters (start simple: Study)
    # ----------------------------
    st.sidebar.markdown("## Filters")

    study_options = sorted(long_df["StudyID"].dropna().unique().tolist())
    selected_studies = st.sidebar.multiselect(
        "Study",
        options=study_options,
        default=study_options
    )

    plot_long = long_df[long_df["StudyID"].isin(selected_studies)].copy()


    sel_long = long_df[long_df["StudyID"].isin(selected_studies)].copy()
    plot_long = sel_long.copy()








    st.markdown("### HMO Summary Statistics")

    range_group = st.selectbox(
        "Compute summary statistics for:",
        ["All", "Secretor", "Non-secretor"],
        index=0
    )

    if range_group == "All":
        table_df = sel_long
    else:
        table_df = sel_long[sel_long["SecretorLabel"] == range_group].copy()

    summary = (
        table_df
        .groupby("HMO")["concentration"]
        .agg(
            n="count",
            p05=lambda x: x.quantile(0.05),
            median="median",
            p95=lambda x: x.quantile(0.95),
            mean="mean",
            std="std"
        )
        .reset_index()
    )

    display_summary = summary.copy()
    for c in ["p05", "median", "p95", "mean", "std"]:
        display_summary[c] = display_summary[c].round(2)

    st.dataframe(
        display_summary.sort_values("HMO"),
        use_container_width=True
    )








########## -------- PLOT --------- ##########

    st.markdown('---')
    st.markdown("### HMO Concentration Distributions")



    # Quick sanity
    st.caption(f"Points available to plot: {len(long_df):,}")



    st.caption(f"Showing {plot_long.shape[0]:,} points after Study filter")


    secretor_options = ["Secretor", "Non-secretor", "Unknown"]
    selected_secretors = st.sidebar.multiselect(
        "Secretor status",
        options=secretor_options,
        default=secretor_options
    )

    plot_long = plot_long[plot_long["SecretorLabel"].isin(selected_secretors)].copy()
    st.caption(f"Showing {plot_long.shape[0]:,} points after Secretor filter")



    use_log = st.checkbox("Log scale (x-axis)", value=True)

    fig = px.strip(
    plot_long,
    x="concentration",
    y="HMO",
    color="SecretorLabel",
    stripmode="overlay",
    color_discrete_map={
        "Secretor": "#8EC9E6",
        "Non-secretor": "#F2A3A3",
        "Unknown": "#C9C9C9"
    },
)


    fig.update_traces(marker=dict(opacity=0.6, size=4))

    if use_log:
        fig.update_xaxes(type="log")

    fig.update_layout(
        height=700,
        legend_title="Secretor status",
        xaxis_title="Concentration (ug/mL)",
        yaxis_title="HMO",
    )

    st.plotly_chart(fig, use_container_width=True)



