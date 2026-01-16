# Overview
This project provides a clean and reproducible workflow for processing Human Milk Oligosaccharide (HMO) data from multiple studies.
It takes raw Excel reports (which vary in structure and naming), detects the correct HMO sheet, cleans datasheets, and produces consistent, analysis-ready files. Metadata files are also identified, screened, and cleaned for "core" analysis.

The goal is to make HMO data comparable across studies so it can be analyzed in tools like Streamlit, Tableau, Power BI, or Python.

## Project Workflow 
1. Raw HMO Excel files are placed in the raw/ folder, grouped by study (e.g., Oxford, Brooklyn...). Mannually upload more studies by adding new subfolders within the /raw folder, make sure to upload seperate excel sheets for the HMO area counts and associated metadata.
2. The data processing pipeline (data_processing.ipynb) scans through the raw data, identifies the HMO sheets, standardizes column names, clean file is then saved into the staging/ folder under the matching study name. 
3. All cleaned HMO files are combined into one master file inside staging/_merged/. Called 'hmo_merged.csv'
4. Metadata is identified and standardized. Identifying IDs and Priority columns (study week, maternal age, gestational age (week), lactation week postpartum (week)) are saved into 'metadata__core_cleaned<StudyID>.csv' within the respective study folder in /staging.


## Folder Descriptions

#### 1. raw/ — Raw Input Files

- This folder contains the original Excel reports exactly as provided by each study. They are not edited!
- When uploading studies label the folder the study name (e.g., Brooklyn, NeoBANK, Oxford) with the respective metadata and HMO area count excel sheets seperated within.

#### 2. study extras/
- study_locations: mannually update with the same StudyID in HMO data as new studies are added with the respective information to update the map graphic
- study_descriptions: mannually update with a short description of what the study's focus was on as new studies are added

#### 3. staging/ — Cleaned Outputs
- Where processed data is stored after running the pipeline.
- Each study has its own folder containing cleaned CSV files.
- The staging/_merged/ folder contains: hmo_merged.csv → the final standardized dataset combining all studies.

#### 4. derived/ - Merged HMO + Metadata 
- Where the merged HMO + metadata csv file lives as well as the master metadata csv file.

#### 5. catalog/ — Automated Logs

These files help track what was processed:
- detection_log.csv → records which sheet was identified as the HMO sheet
- processed_log.csv → prevents re-processing previously cleaned files

This folder is automatically updated by the pipeline. Check this as a sanity measure for what files are being read.

#### 5. dashboard/
- For the streamlit visualizations (if wanting to add images add into /assests as a png
- app.py is the python file that is responsible for all information and graphics displayed on the streamlit website


## File Descriptions

#### 1. data_processing.ipynb — Main HMO Pipeline Notebook
- Detecting HMO area count sheets within each /raw study subfolder
- Standardizing column names and renaming HMO columns to a consistent format
- Saving cleaned HMO tables into the staging/ directory
- Logging detection results and processing status into the catalog/ folder
- Merging all cleaned HMO data into a single datasetDetecting HMO area count sheet called hmo_merged.csv 

#### 2.metadataprocessing.ipynb - Metadata Pipeline Notebook
- Scanning each study’s /raw metadata files (Excel or CSV) and identifying metadata sheets
- Loading metadata sheets and normalizing column names (lowercase, stripped, standardized)
- Identifying candidate metadata fields even when naming conventions differ across studies (e.g., mat_age, maternal age, mother_age)
- Mapping study-specific column names to a shared canonical metadata schema
- Prioritizing high-confidence matches and flagging ambiguous or missing fields
- Preserving extra study-specific metadata without discarding information
- Logging all column matches, renames, and unresolved fields for transparency
- Producing: Cleaned, per-study metadata tables in staging/, Resolution logs describing how each metadata field was interpreted, A harmonized metadata dataset ready for merging with HMO data

## How to Use the Project

### 1. Add new raw files
- Place new HMO and Metadata (2 seperate) Excel or CSV files into the appropriate study folder inside /raw/
- Each study should have its own subfolder (e.g., raw/Oxford/, raw/Brooklyn/)
- Do not rename columns to match other studies — column harmonization is handled automatically

### 2. Run the data processing notebook
- Open data_processing.ipynb and run all cells. Mid-point code check should print: 'Merged X file(s) → staging/_merged/hmo_merged.csv (XXXX rows, XX columns)'
- Open metadata_processing.ipynb and run all cells.

### 3. Review Processed Outputs 
- Cleaned per-study data appear in: staging/<study_name>/
- Merged datasets appear in: staging/_merged/ (hmo), derived/ (metadata + hmo, metadata)
- Processing and resolution logs appear in: catalog/

### 4. Update Dashboard Reference Metadata (Manual Step)
- Some dashboard reference files are maintained manually and must be updated when new studies are added: Study descriptions, Geographic location metadata, Display names or study-level annotations
- These files live in the dashboard’s study extras Excel folders and are not auto-generated.

### 5. Launch the Streamlit Dashboard
- From the VS Code terminal:
"""
 cd dashboard
streamlit run app.py
"""
- The dashboard should automatically open in a browser

### 6. Best Practices
- Always rerun both notebooks when adding new studies
- Never manually edit merged CSV files
- If something looks missing in the dashboard: Check /raw/ placement, Rerun the relevant notebook, Review logs in catalog/



