# App Store Data Analysis

This project analyzes mobile applications from the **Google Play Store** and the **Apple App Store**, 
focusing on app categories, ratings, installs, and other metadata. 
The goal is to compare the two platforms, identify trends, and extract useful insights using Python.

## 📊 Datasets

The analysis is based on three datasets:

- **Google-Playstore.csv** – Apps and metadata from Google Play Store
- **appleAppData.csv** – Apps and metadata from Apple App Store
- **ready_dataset.csv** – Preprocessed and merged dataset used for final analysis

## 🛠 Tools & Libraries

- Python 3.x
- Pandas – data manipulation
- NumPy – numerical computations
- Matplotlib / Seaborn – data visualization
- Jupyter Notebook or IDE (PyCharm/VS Code)

## 📂 Repository Structure

```
app-store-data-analysis/
├─ analysis.py                # Python script for analysis
├─ Google-Playstore.csv       # Google Play dataset
├─ appleAppData.csv           # Apple App Store dataset
├─ ready_dataset.csv          # Final preprocessed dataset
├─ analysis.docx              # Report / documentation
├─ README.md                  # Project documentation (this file)
└─ figures/                   # (Optional) plots, charts, visualizations
```

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/app-store-data-analysis.git
   cd app-store-data-analysis
   ```

2. Install required Python libraries:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```

3. Run the analysis script:
   ```bash
   python analysis.py
   ```

4. (Optional) Open a Jupyter Notebook for interactive exploration.

## 📈 Analysis Overview

- Data cleaning: removing duplicates, handling missing values, merging datasets.
- Exploratory analysis: distributions of categories, ratings, app counts per platform.
- Visualizations: bar plots, histograms, comparative charts of Android vs iOS apps.
- Key insights: most popular categories, rating distributions, market differences.

## 📌 Credits

Developed as part of a Python data analysis project. Datasets provided by lecturer and preprocessed for analysis.
