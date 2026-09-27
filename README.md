# YuvaIntern — Data Science with Python (Week 3)

**Intern:** Jermy Biju
**Role:** Virtual Data Science with Python Apprentice Intern
**Organization:** YuvaIntern
**Internship Duration:** August 24, 2026 – September 28, 2026

## Week 3 Task
Statistical Analysis and Hypothesis Testing in Python

## Dataset
Cleaned Titanic dataset from Week 1 (889 rows × 14 columns, zero missing values).

## What was done
Four hypotheses about Titanic survival were formulated and tested using the appropriate statistical methods:

| # | Hypothesis (H₀) | Test | Result |
|---|-----------------|------|--------|
| 1 | Survival and sex are independent | Chi-square | Reject H₀ (χ²=258.43, p≈10⁻⁵⁸) |
| 2 | Mean fare is the same for survivors and non-survivors | Welch's t-test | Reject H₀ (t=6.76, p≈10⁻¹¹) |
| 3 | Mean age is the same across all three classes | One-way ANOVA | Reject H₀ (F=91.40, p≈10⁻³⁷) |
| 4 | Age distribution is the same for survivors and non-survivors | Mann-Whitney U | Fail to reject H₀ (p=0.206) |

A bonus analysis computed Wilson 95% confidence intervals for survival rate across the six sex × class groups.

## Project structure
YuvaIntern-DataScience-Week3/
├── data/
│ └── titanic_cleaned.csv
├── images/
│ ├── week3_chart1_survival_sex_counts.png
│ ├── week3_chart2_fare_ttest.png
│ ├── week3_chart3_age_anova.png
│ ├── week3_chart4_age_mannwhitney.png
│ └── week3_chart5_ci_plot.png
├── report/
│ └── YuvaIntern_Week3_Report.docx
├── analysis.py
├── week3_report.py
├── .gitignore
└── README.md

text

## Tools
Python 3.14, Pandas, NumPy, SciPy, Matplotlib, Seaborn, python-docx

## How to run
python analysis.py # runs all statistical tests and generates charts
python week3_report.py # builds the DOCX report

text

## Key findings
- Sex is strongly associated with survival (Cramér's V = 0.54, large effect).
- Survivors paid on average £26 more than non-survivors (95% CI [£18.51, £33.68]).
- Mean age decreases monotonically from 1st class to 3rd class (η² = 0.17, large effect).
- Age alone does not significantly separate survivors from non-survivors (p = 0.206).

## Note
All findings are reported as statistical associations, not causal claims. The dataset is observational.

## Related repositories
- [Week 1 — Data Acquisition, Cleaning and EDA](https://github.com/jermybiju/YuvaIntern-DataScience-Week1)
- [Week 2 — Advanced Data Visualization and Storytelling](https://github.com/jermybiju/YuvaIntern-DataScience-Week2)