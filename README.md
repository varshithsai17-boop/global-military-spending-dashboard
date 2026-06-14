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
│   ├── Extra Analysis.ipynb                 # Full 18-section EDA + visualization notebook
│   ├── Required Analysis.ipynb              # Core required EDA sections
│   └── military_spending_analysis.ipynb     # Working analysis notebook
├── docs/
│   ├── analysis.html                        # HTML export of notebook
│   └── additional_codes.docx               # Word doc — custom markers & colors
├── app/
│   └── app.py                               # Streamlit interactive dashboard
├── .streamlit/
│   └── config.toml                          # Dark theme configuration
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
jupyter notebook "notebooks/Extra Analysis.ipynb"
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

The main notebook (`Extra Analysis.ipynb`) covers **18 sections**:

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

A polished, dark-themed Streamlit dashboard with a cohesive design system
(custom fonts, gradient KPI cards, and a unified Plotly style across every chart):

- **Hero header + KPI cards** — total tracked spending, top spender, top-5 concentration, and highest defense burden at a glance
- **Sidebar controls** — dataset selector, country-count slider, and rankings chart type
- **🌍 Overview** — interactive **world choropleth map** of spending, plus top-10 and by-region breakdowns
- **🏆 Rankings** — configurable Bar / Horizontal Bar / Treemap / Pie / Scatter (spending vs % GDP)
- **💰 % of GDP** — side-by-side SIPRI vs IISS defense-burden charts with a key-insight callout
- **🔄 Source Comparison** — grouped SIPRI vs IISS bars, a difference table, and regional totals
- **📋 Data** — searchable, sortable full dataset with one-click **CSV export**

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
