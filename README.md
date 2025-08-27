# App Store Data Analysis

A Python project that compares apps from the **Google Play Store** and the **Apple App Store**.  
It cleans and explores the data, then generates insights and visualizations about categories, ratings, installs, and more.

---

## 📒 Run the Jupyter Notebook

Instead of running the Python script, you can open the analysis notebook for interactive exploration:

```
# install Jupyter if not already
pip install notebook

# start Jupyter
jupyter notebook
```

Then open analysis.ipynb from the root folder.
This allows you to step through the analysis, rerun cells, and modify plots interactively.

## 📊 Datasets

The analysis is based on three datasets:

- **Google-Playstore.csv** – Apps and metadata from Google Play Store
- **appleAppData.csv** – Apps and metadata from Apple App Store
- **ready_dataset.csv** – Preprocessed and merged dataset used for final analysis

## 📂 Repository Structure

```
app-store-data-analysis/
├─ scripts/
│  └─ download_data.py            # downloads large datasets from Google Drive, prints SHA256, writes samples
├─ data/
│  ├─ ready_dataset.csv           # (optional) merged/cleaned dataset if small enough to commit
├─ analysis.py                    # main analysis
├─ analysis.ipynb                 # Jupyter Notebook
├─ README.md                      # this file
```

> **Why this layout?** Large CSVs don’t belong in Git. We keep raw data out of the repo and fetch it on demand with a script.  
> Small derived files (samples/ready dataset) may be committed for convenience.

---

## 🔧 Setup

**Python 3.9+** recommended. (Works on newer versions too.)

## 🚀 How to Run

1. Clone this repository:

   ```bash
   git clone https://github.com/eliyasamary/app-store-data-analysis.git
   cd app-store-data-analysis
   ```

2. (Optional) Create a virtual environment

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
   ```

3. Install dependencies

   ```bash
   pip install pandas numpy matplotlib seaborn gdown notebook
   ```

4. Download the datasets
   Run the provided script with your Google Drive links:

   ```bash
   python scripts/download_data.py \
   --google-url "https://drive.google.com/file/d/1HWfIK8teob8CHc0jOYExx6MBQ4hAWhbW/view?usp=drive_link" \
   --apple-url  "https://drive.google.com/file/d/1tQxykLL6RoU0x2osOo9MHew0SwfrBb6t/view?usp=drive_link"

   ```

5. Run the analysis script

   ```bash
   python analysis.py
   ```

6. (Optional) Use the Jupyter Notebook

   ```bash
   jupyter notebook
   ```

## 📈 Analysis Overview

- Data cleaning: removing duplicates, handling missing values, merging datasets.
- Exploratory analysis: distributions of categories, ratings, app counts per platform.
- Visualizations: bar plots, histograms, comparative charts of Android vs iOS apps.
- Key insights: most popular categories, rating distributions, market differences.

---

## 📝 Notes

- **Do not commit** large raw CSVs to Git. The included `.gitignore` keeps `data/raw/` out of version control.
- If your **ready dataset** is small (e.g., under ~20 MB), you can commit it to `data/processed/`.
- For very large assets that must be versioned, consider **Git LFS** or **GitHub Releases**.

---

## 📌 Credits

Developed as part of a Python data analysis project using publicly shared datasets.  
The repository includes a downloader script to fetch large source files on demand.

Developed as part of a Python data analysis project. Datasets provided by lecturer and preprocessed for analysis.
