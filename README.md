# Overview
This project provides a clean and reproducible workflow for processing Human Milk Oligosaccharide (HMO) data from multiple studies.
It takes raw Excel reports (which vary in structure and naming), detects the correct HMO sheet, cleans datasheets, and produces consistent, analysis-ready files.

The goal is to make HMO data comparable across studies so it can be analyzed in tools like Streamlit, Tableau, Power BI, or Python.

## Project Workflow 
1. Raw HMO Excel files are placed in the raw/ folder, grouped by study (e.g., Oxford, Brooklyn, NeoBANK). Mannually upload more studies as more are analyzed, make sure to upload seperate excel sheets for the HMO area counts and associated metadata.
2. The data processing pipeline (data_processing.ipynb) scans those files, identifies the correct HMO sheet and standardizes column names.
3. Cleaned versions of each HMO file are saved into the staging/ folder under the matching study name.
4. All cleaned HMO files are combined into one master file inside staging/_merged/. Called 'hmo_merged.csv'


## Folder Descriptions

#### 1. raw/ — Raw Input Files

- This folder contains the original Excel reports exactly as provided by each study.
- They are not edited.
- When uploading studies label the folder the study name (e.g., Brooklyn, NeoBANK, Oxford) with the respective metadata and HMO area count excel sheets within.

#### 2. staging/ — Cleaned Outputs

- Where processed data is stored after running the pipeline.
- Each study has its own folder containing cleaned CSV files.
- The staging/_merged/ folder contains: hmo_merged.csv → the final standardized dataset combining all studies.

#### 3. data_processing.ipynb — Main Pipeline Notebook

This is the core of the project.

It handles:
- Detecting HMO area count sheets within each /raw subfolder
- Standardizing column names and renaming HMO columns to a consistent format
- Saving cleaned versions into staging/
- Logging everything in the catalog/ folderc
- Creating the final merged dataset
- To update the hmo_merged.csv file with new projects uploaded, run this file (play button, run all) to update.
- Will see a 'HMO Sheet Detection Summary' mid-way through the sheet, with green checkmarks for files that are read and red x for ones not and at the very end should say 'Merged X files(s) -> staging/_merged/hmo_merged.csv (XXXX rows, 70 cols)

#### 5. catalog/ — Automated Logs

These files help track what was processed:
- detection_log.csv → records which sheet was identified as the HMO sheet
- processed_log.csv → prevents re-processing previously cleaned files

This folder is automatically updated by the pipeline. Check this as a sanity measure for what files are being read.

#### 6. project/helpers/

Contains helper functions used throughout the pipeline:
- hmo_utils.py → sheet detection, renaming rules, cleaning functions, logging, etc.

Non-technical users do not need to modify these files.

#### 7. dashboard/
For the streamlit visualizations

#### 8. metadata/
- study_locations: mannually update with the same StudyID in HMO data as new studies are added
- study_descriptions: mannually update with a short description of what the study's focus was on as new studies are added


## How to Use the Project

### 1. Add new raw files
- Place any new Excel reports into the appropriate folder inside raw/

### 2. Run the data processing notebook
- Open data_processing.ipynb and run all cells.

### 3. View or analyze the results
- Cleaned datasets will appear under staging/

### 4. Streamlit Dashboard Visualization
- Mannually update the metadata excel folders for location and study descriptions as new studies are added
- In the terminal on VS Code run 'cd dashboard' (make sure it is reading the correct file) then 'streamlit run app.py'. Should automatically pull up the updated Streamlit website in a browser.
