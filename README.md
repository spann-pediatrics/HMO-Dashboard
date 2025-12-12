# Overview
This project provides a clean and reproducible workflow for processing Human Milk Oligosaccharide (HMO) data from multiple studies.
It takes raw Excel reports (which vary in structure and naming), detects the correct HMO sheet, cleans datasheets, and produces consistent, analysis-ready files.

The goal is to make HMO data comparable across studies so it can be analyzed in tools like Tableau, Power BI, or Python.

## Project Workflow (Simple Explanation)
1. Raw HMO Excel files are placed in the raw/ folder, grouped by study (e.g., Oxford, Brooklyn, NeoBANK).
2. The data processing pipeline (data_processing.ipynb) scans those files, identifies the correct HMO sheet and standardizes column names.
3. Cleaned versions of each file are saved into the staging/ folder under the matching study name.
4. All cleaned files are combined into one master file inside staging/_merged/. Called 'hmo_merged.csv'
5. The merged file is used for visualization and inital exploratory analysis can be found the notebook analysis/hmo_eda.ipynb.


## Folder Descriptions

#### 1. raw/ — Raw Input Files

- This folder contains the original Excel reports exactly as provided by each study.
- They are not edited.
- Each study (e.g., Brooklyn, NeoBANK, Oxford) has its own subfolder with the respective cmetadata data and HMO area counts.

#### 2. staging/ — Cleaned Outputs

- Where processed data is stored after running the pipeline.
- Each study has its own folder containing cleaned CSV files.
- The staging/_merged/ folder contains: hmo_merged.csv → the final standardized dataset combining all studies.

#### 3. analysis/

- Contains visualization and exploratory analysis.
- hmo_eda.ipynb → plots, summary statistics, and data exploration.


#### 4. data_processing.ipynb — Main Pipeline Notebook

This is the core of the project.

It handles:
- Detecting the correct HMO sheet within each Excel file
- Standardizing column names to renaming HMO columns to a consistent format
- Saving cleaned versions into staging/
- Logging everything in the catalog/ folder
- Creating the final merged dataset
- A non-technical user only needs to run the notebook top-to-bottom to update the data.

#### 5. catalog/ — Automated Logs

These files help track what was processed:
- detection_log.csv → records which sheet was identified as the HMO sheet
- hmo_manifest.csv → inventory of all processed files
- processed_log.csv → prevents re-processing previously cleaned files

This folder is automatically updated by the pipeline.

#### 6. project/helpers/

Contains helper functions used throughout the pipeline:
- hmo_utils.py → sheet detection, renaming rules, cleaning functions, logging, etc.

Non-technical users do not need to modify these files.


## How to Use the Project

### 1. Add new raw files
- Place any new Excel reports into the appropriate folder inside raw/

### 2. Run the data processing notebook
- Open data_processing.ipynb and run all cells.

### 3. View or analyze the results
- Cleaned datasets will appear under staging/

### 4. Explore the data
- Use the notebook: analysis/hmo_eda.ipynb
