# 🌍 Global Military Expenditure Analysis

**Python for Business — CIA Project**

An exploratory data analysis (EDA) and visualization project analysing global military spending data sourced from [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures).

---

## 📂 Project Structure

```
Python CIA II/
├── data/                                    # Datasets (CSV)
│   ├── military_spending_sipri_2024.csv     # Top 40 spenders — SIPRI 2024
│   ├── military_spending_iiss_2025.csv      # Top 15 spenders — IISS 2025
│   ├── gdp_pct_sipri_2024.csv              # Spending as % of GDP (SIPRI)
│   └── gdp_pct_iiss_2020.csv              # Spending as % of GDP (IISS)
├── notebooks/
│   └── analysis.ipynb                       # Main Jupyter Notebook (EDA + Viz)
├── docs/
│   ├── analysis.html                        # HTML export of notebook
│   └── additional_codes.docx               # Word doc — custom markers & colors
├── app/
│   └── app.py                               # Streamlit interactive dashboard
├── scripts/
│   ├── scrape_data.py                       # Wikipedia data scraper
│   ├── generate_notebook.py                 # Notebook generator script
│   ├── generate_docx.py                     # Word document generator
│   └── export_pdf.bat                       # PDF/HTML export script
├── .gitignore
├── requirements.txt
└── README.md                                # This file
```

---

## 📊 Datasets

Data was scraped from the Wikipedia article: [List of countries with highest military expenditures](https://en.wikipedia.org/wiki/List_of_countries_with_highest_military_expenditures)

| Dataset | Source | Rows | Key Columns |
|---------|--------|------|-------------|
| SIPRI 2024 | Stockholm International Peace Research Institute | 40 | Rank, Country, Spending ($bn), % GDP, % Global |
| IISS 2025 | International Institute for Strategic Studies | 15 | Rank, Country, Spending ($bn) |
| GDP % (SIPRI) | SIPRI 2024 | 25 | Rank, Country, % of GDP |
| GDP % (IISS) | IISS 2020 | 15 | Rank, Country, % of GDP |

---

## 🛠️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Jupyter Notebook
```bash
jupyter notebook notebooks/analysis.ipynb
```

### 3. Generate Documentation
```bash
# Generate the Word document
python scripts/generate_docx.py

# Export notebook to HTML/PDF
scripts\export_pdf.bat
```

### 4. Launch the Interactive Dashboard
```bash
streamlit run app/app.py
```
The dashboard will open at [http://localhost:8501](http://localhost:8501)

---

## 📓 Notebook Contents

The Jupyter notebook covers **18 sections**:

| # | Section | Description |
|---|---------|-------------|
| 1 | Imports | pandas, numpy, matplotlib, seaborn, squarify |
| 2 | Read Data | Load all 4 CSV datasets |
| 3 | View DataFrames | head, tail, shape, columns, dtypes, info, describe |
| 4 | Data Cleaning | Null checks, duplicate checks, type conversions |
| 5 | Indexing & Slicing | iloc, loc, boolean filtering |
| 6 | Sorting | sort_values (single & multi-column) |
| 7 | GroupBy & Aggregation | Regional grouping, sum, mean, agg |
| 8 | Merge & Concat | merge SIPRI+IISS, concat GDP tables |
| 9 | Bar Chart | Vertical & horizontal bar charts |
| 10 | Pie Chart | Global spending share |
| 11 | Line Chart | SIPRI vs IISS comparison |
| 12 | Scatter Plot | Spending vs % GDP (bubble chart) |
| 13 | Heatmap | Correlation matrix |
| 14 | Box Plot | Distribution analysis + by-region |
| 15 | Custom Markers & Colors | Marker types, palettes, hatch patterns |
| 16 | 🎯 Bonus: Treemap | Proportional area chart |
| 17 | 🎯 Bonus: Grouped Bar | Side-by-side SIPRI vs IISS |
| 18 | 🎯 Bonus: Radar Chart | Multi-metric spider comparison |

---

## 🖥️ Dashboard Features

The Streamlit dashboard provides:
- **Sidebar controls** — dataset selector, country count slider, chart type, color scheme
- **Tab 1: Charts** — Bar, Horizontal Bar, Pie, Scatter, Treemap (all interactive)
- **Tab 2: Data Table** — Full dataset with search/filter and summary statistics
- **Tab 3: % GDP Analysis** — Side-by-side SIPRI vs IISS GDP percentage charts
- **Tab 4: Source Comparison** — Grouped bar chart comparing SIPRI and IISS estimates

---

## 🔑 Key Findings

1. **The United States dominates** global military spending at **$997 billion** (35.5% of the world total)
2. The **top 5 countries** account for over **58%** of all military spending worldwide
3. **Ukraine** has the highest spending as a % of GDP (**34%**) due to the ongoing conflict
4. **SIPRI and IISS** estimates differ — SIPRI generally reports higher figures
5. **Regional patterns**: North America and Asia lead in total spending

---

## 📦 Technologies Used

- **Python 3.12+**
- **pandas** — Data manipulation
- **numpy** — Numerical operations
- **matplotlib** — Static visualizations
- **seaborn** — Statistical plots
- **squarify** — Treemap charts
- **plotly** — Interactive charts (dashboard)
- **streamlit** — Web dashboard framework
- **python-docx** — Word document generation

---

## 📄 License

This project is provided for educational purposes as part of the Python for Business CIA assessment.
