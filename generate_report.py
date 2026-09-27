"""
YuvaIntern Week 3 Report Generator
Statistical Analysis and Hypothesis Testing on the Titanic dataset.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def add_code_block(doc, code_text):
    para = doc.add_paragraph()
    para.paragraph_format.left_indent = Inches(0.25)
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(4)
    run = para.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(8)
    pPr = para._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F2F2F2')
    pPr.append(shd)


def add_table(doc, headers, rows):
    """Insert a table that does not split rows across pages."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Prevent each row from splitting across pages
    for row in table.rows:
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        cantSplit = OxmlElement('w:cantSplit')
        trPr.append(cantSplit)

    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = str(h)
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(10)

    for row_data in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row_data):
            cells[i].text = str(val)
            for p in cells[i].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)

    # Keep all rows together with the next paragraph
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.keep_with_next = True

    doc.add_paragraph()


def add_bullet(doc, text):
    doc.add_paragraph(text, style='List Bullet')


def add_image_with_caption(doc, img_path, caption, width=5.5):
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(width))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cap.add_run(caption)
        run.font.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


# ------------------------------------------------------------------
# Build document
# ------------------------------------------------------------------

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# ---------- Title page ----------
doc.add_paragraph('\n\n')
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('YuvaIntern')
r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

s = doc.add_paragraph()
s.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = s.add_run('Virtual Data Science with Python Apprentice Internship')
r.font.size = Pt(14); r.font.italic = True

doc.add_paragraph()

h = doc.add_paragraph()
h.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = h.add_run('WEEK 3 REPORT')
r.font.size = Pt(16); r.font.bold = True

h = doc.add_paragraph()
h.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = h.add_run('Statistical Analysis and Hypothesis Testing in Python')
r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

h = doc.add_paragraph()
h.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = h.add_run('Four Hypotheses About Titanic Survival — Tested with Rigor')
r.font.size = Pt(12); r.font.italic = True

doc.add_paragraph('\n\n')

info = doc.add_table(rows=0, cols=2)
info.alignment = WD_TABLE_ALIGNMENT.CENTER
rows = [
    ('Submitted by', 'Jermy Biju'),
    ('Role', 'Virtual Data Science with Python Apprentice Intern'),
    ('Organization', 'YuvaIntern'),
    ('Internship Duration', 'August 24, 2026 – September 28, 2026'),
    ('Week 3 Duration', '30 – 35 hours'),
    ('Dataset', 'Titanic (cleaned in Week 1, 889 rows × 14 columns)'),
    ('Tools', 'Python 3.14, Pandas, NumPy, SciPy, Matplotlib, Seaborn'),
]
for k, v in rows:
    cells = info.add_row().cells
    cells[0].text = k; cells[1].text = v
    for p in cells[0].paragraphs:
        for r in p.runs:
            r.font.bold = True; r.font.size = Pt(11)
    for p in cells[1].paragraphs:
        for r in p.runs:
            r.font.size = Pt(11)

doc.add_page_break()


# ---------- 1. Executive Summary ----------
doc.add_heading('1. Executive Summary', level=1)
doc.add_paragraph(
    'This report presents Week 3 of the YuvaIntern Virtual Data Science with Python '
    'Apprenticeship. The task was to perform rigorous statistical analysis and hypothesis '
    'testing in Python. Four hypotheses about survival on the Titanic were formulated and '
    'tested using the appropriate statistical methods — chi-square, Welch\'s t-test, '
    'one-way ANOVA, and the Mann-Whitney U test.'
)
doc.add_paragraph('Summary of findings:')
add_bullet(doc, 'Sex and survival: strongly associated (chi-square = 258.43, p = 3.78e-58, Cramer\'s V = 0.54). Reject H0.')
add_bullet(doc, 'Fare and survival: significant difference in mean fare (t = 6.76, p = 4.48e-11). Reject H0.')
add_bullet(doc, 'Age across classes: significant difference in mean age (F = 91.40, p = 8.19e-37, eta-squared = 0.17). Reject H0.')
add_bullet(doc, 'Age and survival: no significant difference in age distribution (U = 88,631, p = 0.21). Fail to reject H0.')
doc.add_paragraph(
    'Three of the four hypotheses were supported by the data; one was not. The strongest '
    'association is between sex and survival, followed by fare and survival, and age across '
    'passenger classes. The weakest is age itself, which does not differ significantly '
    'between survivors and non-survivors. All findings are reported as statistical '
    'associations, not causal claims.'
)


# ---------- 2. Introduction ----------
doc.add_heading('2. Introduction — Why Hypothesis Testing?', level=1)
doc.add_paragraph(
    'Exploratory data analysis can reveal patterns, but it cannot tell us whether a '
    'pattern is real or simply the result of random variation in the sample. Hypothesis '
    'testing provides a formal, quantitative framework for that decision. It forces the '
    'analyst to state a claim in advance (the null hypothesis), choose a test statistic '
    'appropriate to the data, and decide whether the observed data are compatible with '
    'that null hypothesis.'
)
doc.add_paragraph(
    'For Week 3, four hypotheses were formulated about the Titanic dataset and tested '
    'using standard statistical methods. Each test is accompanied by a p-value, an effect '
    'size measure, and — where appropriate — a confidence interval. The result is a '
    'rigorous and reproducible assessment of which factors were and were not associated '
    'with survival.'
)

doc.add_page_break()

# ---------- 3. Dataset ----------
doc.add_heading('3. Dataset', level=1)
doc.add_paragraph(
    'The dataset is the cleaned Titanic dataset from Week 1: 889 passengers, 14 columns, '
    'with zero missing values. Cleaning steps included dropping the deck column (approx 77% '
    'missing), imputing age using the median within (pclass, sex) subgroups, and removing '
    'two rows with missing embarkation information.'
)
doc.add_paragraph('Variables used in this report:')
add_table(doc,
          ['Variable', 'Type', 'Role in tests'],
          [
              ('survived', 'Binary (0/1)', 'Outcome variable in all hypotheses'),
              ('sex', 'Categorical', 'Grouping variable (Hypothesis 1)'),
              ('fare', 'Continuous', 'Numerical outcome (Hypothesis 2)'),
              ('pclass', 'Categorical (1/2/3)', 'Grouping variable (Hypothesis 3)'),
              ('age', 'Continuous', 'Numerical variable (Hypotheses 3 and 4)'),
          ])


# ---------- 4. Methodology ----------
doc.add_heading('4. Methodology', level=1)
doc.add_paragraph(
    'Each hypothesis was paired with the statistical test most appropriate to the types '
    'of variables involved. Effect sizes were calculated alongside p-values, because a '
    'statistically significant result can still have a negligible practical impact.'
)
add_table(doc,
          ['#', 'Hypothesis (H0)', 'Test', 'Why this test'],
          [
              ('1', 'Survival and sex are independent',
               'Chi-square test of independence',
               'Both variables are categorical'),
              ('2', 'Mean fare is the same for survivors and non-survivors',
               'Welch\'s independent t-test',
               'Continuous outcome across two groups with unequal variances'),
              ('3', 'Mean age is the same across all three classes',
               'One-way ANOVA',
               'Continuous outcome across three groups'),
              ('4', 'Age distribution is the same for survivors and non-survivors',
               'Mann-Whitney U test',
               'Non-parametric alternative to t-test (age is not normally distributed)'),
          ])
doc.add_paragraph('Significance level: alpha = 0.05 (two-sided tests).')
doc.add_paragraph('Effect sizes reported: Cramer\'s V (chi-square), mean difference with 95% CI (t-test), Eta-squared (ANOVA), rank-biserial correlation (Mann-Whitney).')

doc.add_page_break()

# ---------- 5. Results ----------
doc.add_heading('5. Results', level=1)


# --- H1 ---
doc.add_heading('5.1 Hypothesis 1 — Survival and Sex (Chi-Square)', level=2)
doc.add_paragraph('H0: Survival and sex are independent.')
doc.add_paragraph('H1: Survival and sex are associated.')
add_image_with_caption(doc,
    'images/week3_chart1_survival_sex_counts.png',
    'Figure 1: Observed survival counts by sex. Female passengers mostly survived; male passengers mostly did not.')

doc.add_paragraph('Contingency table (observed counts):')
add_table(doc,
          ['Sex', 'Did Not Survive', 'Survived', 'Total'],
          [
              ('Female', '81', '231', '312'),
              ('Male', '468', '109', '577'),
          ])

doc.add_paragraph('Test results:')
add_table(doc,
          ['Statistic', 'Value'],
          [
              ('Chi-square', '258.43'),
              ('Degrees of freedom', '1'),
              ('p-value', '3.78 x 10^-58'),
              ('Cramer\'s V', '0.5392 (strong)'),
          ])
doc.add_paragraph(
    'Decision: Reject H0 at alpha = 0.05. There is an extremely strong statistical '
    'association between sex and survival. The effect size (Cramer\'s V = 0.54) is large, '
    'meaning this is not only statistically significant but also practically important.'
)


# --- H2 ---
doc.add_heading('5.2 Hypothesis 2 — Mean Fare by Survival (Welch\'s t-test)', level=2)
doc.add_paragraph('H0: Mean fare is the same for survivors and non-survivors.')
doc.add_paragraph('H1: Mean fare differs between the two groups.')
add_image_with_caption(doc,
    'images/week3_chart2_fare_ttest.png',
    'Figure 2: Fare distributions for survivors (green) and non-survivors (red). Survivors paid higher fares on average.')

doc.add_paragraph('Descriptive statistics:')
add_table(doc,
          ['Group', 'n', 'Mean', 'Median', 'Std Dev'],
          [
              ('Survived', '340', '48.21', '26.00', '66.75'),
              ('Did Not Survive', '549', '22.12', '10.50', '31.39'),
          ])

doc.add_paragraph('Test results:')
add_table(doc,
          ['Statistic', 'Value'],
          [
              ('t-statistic', '6.7597'),
              ('p-value', '4.48 x 10^-11'),
              ('Difference in means', '26.09'),
              ('95% CI for difference', '[18.51, 33.68]'),
          ])
doc.add_paragraph(
    'Decision: Reject H0 at alpha = 0.05. Survivors paid on average 26 more than '
    'non-survivors, and the 95% confidence interval excludes zero by a wide margin. '
    'However, note that fare is strongly correlated with class, so this effect likely '
    'reflects the class difference documented in Hypothesis 3.'
)


# --- H3 ---
doc.add_heading('5.3 Hypothesis 3 — Mean Age Across Passenger Classes (ANOVA)', level=2)
doc.add_paragraph('H0: Mean age is the same across all three passenger classes.')
doc.add_paragraph('H1: At least one class has a different mean age.')
add_image_with_caption(doc,
    'images/week3_chart3_age_anova.png',
    'Figure 3: Age distributions by passenger class. Median age decreases from 1st to 3rd class.')

doc.add_paragraph('Descriptive statistics:')
add_table(doc,
          ['Class', 'n', 'Mean Age', 'Median Age', 'Std Dev'],
          [
              ('1st Class', '214', '38.16', '38.00', '13.73'),
              ('2nd Class', '184', '29.86', '30.00', '13.58'),
              ('3rd Class', '491', '24.80', '25.00', '10.67'),
          ])

doc.add_paragraph('Test results:')
add_table(doc,
          ['Statistic', 'Value'],
          [
              ('F-statistic', '91.3962'),
              ('p-value', '8.19 x 10^-37'),
              ('Eta-squared', '0.1710 (large)'),
          ])
doc.add_paragraph(
    'Decision: Reject H0 at alpha = 0.05. Mean age differs significantly across classes, '
    'and the effect size (eta-squared = 0.17) is large. The pattern is monotonic: mean age '
    'decreases from 1st to 3rd class. This means that class is a proxy for age, which may '
    'partially explain why higher-class passengers survived at higher rates.'
)


# --- H4 ---
doc.add_heading('5.4 Hypothesis 4 — Age Distribution by Survival (Mann-Whitney U)', level=2)
doc.add_paragraph('H0: Age distribution is the same for survivors and non-survivors.')
doc.add_paragraph('H1: Age distributions differ between the two groups.')
add_image_with_caption(doc,
    'images/week3_chart4_age_mannwhitney.png',
    'Figure 4: Overlaid age histograms for survivors and non-survivors. The distributions overlap heavily.')

doc.add_paragraph('Descriptive statistics:')
add_table(doc,
          ['Group', 'n', 'Mean Age', 'Median Age', 'Std Dev'],
          [
              ('Survived', '340', '27.98', '27.00', '13.92'),
              ('Did Not Survive', '549', '29.74', '25.00', '12.82'),
          ])

doc.add_paragraph('Test results:')
add_table(doc,
          ['Statistic', 'Value'],
          [
              ('U-statistic', '88,631.50'),
              ('p-value', '0.206'),
              ('Rank-biserial correlation', '0.0503 (negligible)'),
          ])
doc.add_paragraph(
    'Decision: Fail to reject H0 at alpha = 0.05. There is no statistically significant '
    'difference in age distributions between survivors and non-survivors, and the effect '
    'size is negligible. Age, on its own, does not meaningfully separate survivors from '
    'non-survivors — a result that contrasts sharply with the associations found for sex, '
    'fare, and class.'
)


# --- Bonus ---
doc.add_page_break()
doc.add_heading('5.5 Bonus — 95% Confidence Intervals for Survival Rate', level=2)
doc.add_paragraph(
    'To illustrate uncertainty around each group\'s survival estimate, Wilson 95% '
    'confidence intervals were computed for the six sex-by-class groups.'
)
add_image_with_caption(doc,
    'images/week3_chart5_ci_plot.png',
    'Figure 5: Survival rate with 95% confidence intervals by sex and passenger class. Female 1st class is the highest; male 3rd class is the lowest.')

doc.add_paragraph('Survival rate and 95% CI:')
add_table(doc,
          ['Group', 'n', 'Survival Rate', '95% CI'],
          [
              ('Female 1st', '92', '0.967', '[0.908, 0.989]'),
              ('Female 2nd', '76', '0.921', '[0.838, 0.963]'),
              ('Female 3rd', '144', '0.500', '[0.419, 0.581]'),
              ('Male 1st', '122', '0.369', '[0.288, 0.457]'),
              ('Male 2nd', '108', '0.157', '[0.101, 0.238]'),
              ('Male 3rd', '347', '0.135', '[0.103, 0.175]'),
          ])
doc.add_paragraph(
    'Female 1st class survival is near-certain (96.7%, CI [90.8%, 98.9%]). Male 3rd '
    'class survival is near-certain in the opposite direction (13.5%, CI [10.3%, 17.5%]). '
    'Female 3rd class is the only group whose confidence interval crosses 50%, reflecting '
    'genuine uncertainty about whether more than half of that group survived.'
)

doc.add_page_break()
 

# ---------- 6. Discussion ----------
doc.add_heading('6. Discussion', level=1)

doc.add_heading('6.1 Statistical significance vs practical significance', level=2)
doc.add_paragraph(
    'A small p-value tells us that an effect is unlikely to have arisen by chance. It '
    'does not tell us how large the effect is. This distinction matters. For example:'
)
add_bullet(doc, 'Sex and survival: p = 3.78e-58 AND Cramer\'s V = 0.54 -> both significant and large. A clear, practical effect.')
add_bullet(doc, 'Fare and survival: p = 4.48e-11 AND mean difference = 26 -> significant with a sizable effect, though partly driven by class.')
add_bullet(doc, 'Age across classes: p = 8.19e-37 AND eta-squared = 0.17 -> significant and large. Class is genuinely age-stratified.')
add_bullet(doc, 'Age and survival: p = 0.206 -> not significant. Fails the primary test.')

doc.add_heading('6.2 Correct test choice matters', level=2)
doc.add_paragraph(
    'Each hypothesis was matched to the appropriate test. Chi-square was used for two '
    'categorical variables, Welch\'s t-test for a continuous variable across two groups '
    'with unequal variances, ANOVA for a continuous variable across three groups, and the '
    'Mann-Whitney U test as a non-parametric alternative when normality could not be '
    'assumed. Choosing the wrong test — for example, using a t-test on heavily skewed '
    'fare data — could produce misleading results.'
)

doc.add_heading('6.3 What this analysis does not claim', level=2)
doc.add_paragraph(
    'All findings are statistical associations in an observational dataset. No causal '
    'claims are made. For example, the fact that survivors paid higher fares on average '
    'does not mean paying a higher fare caused survival. Class, sex, age, and fare are '
    'interrelated, and this analysis documents the patterns rather than explaining the '
    'underlying mechanisms.'
)


# ---------- 7. Conclusion ----------
doc.add_heading('7. Conclusion', level=1)
doc.add_paragraph(
    'Week 3 demonstrated how formal hypothesis testing can confirm, qualify, or reject '
    'patterns observed during exploratory analysis. Three of the four hypotheses were '
    'supported by the data: survival was associated with sex (extremely strong), mean '
    'fare differed between survivors and non-survivors (strong, but entangled with '
    'class), and mean age differed across passenger classes (large effect). The fourth '
    'hypothesis — that age distribution differs by survival — was not supported.'
)
doc.add_paragraph(
    'The statistical workflow followed here is directly relevant to real-world analytics: '
    'state a hypothesis, choose a test that matches the data, report both p-values and '
    'effect sizes, interpret confidence intervals, and acknowledge the limits of what the '
    'data can and cannot establish. The result is an analysis that is honest about what it '
    'found and honest about what it did not.'
)


# ---------- 8. Appendix ----------
doc.add_heading('8. Appendix — Key Code Snippets', level=1)

doc.add_heading('8.1 Chi-square test (Hypothesis 1)', level=2)
add_code_block(doc, '''from scipy import stats
contingency = pd.crosstab(df['sex'], df['survived'])
chi2, p, dof, expected = stats.chi2_contingency(contingency)''')

doc.add_heading('8.2 Welch\'s t-test with 95% CI (Hypothesis 2)', level=2)
add_code_block(doc, '''t, p = stats.ttest_ind(fare_survived, fare_not_survived,
                      equal_var=False)
mean_diff = fare_survived.mean() - fare_not_survived.mean()
# 95% CI computed using Welch-Satterthwaite degrees of freedom''')

doc.add_heading('8.3 One-way ANOVA (Hypothesis 3)', level=2)
add_code_block(doc, '''f, p = stats.f_oneway(age_1st, age_2nd, age_3rd)
# Effect size: eta-squared
eta_sq = ss_between / ss_total''')

doc.add_heading('8.4 Mann-Whitney U test (Hypothesis 4)', level=2)
add_code_block(doc, '''u, p = stats.mannwhitneyu(age_survived, age_not_survived,
                            alternative='two-sided')
rank_biserial = 1 - (2 * u) / (n1 * n2)''')

doc.add_heading('8.5 Wilson 95% CI for a proportion (Bonus)', level=2)
add_code_block(doc, '''def wilson_ci(k, n, confidence=0.95):
    p = k / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2*n)) / denom
    margin = z * ((p*(1-p)/n + z**2/(4*n**2))**0.5) / denom
    return (centre - margin, centre + margin)''')


# ---------- Save ----------
os.makedirs('report', exist_ok=True)
out = 'report/YuvaIntern_Week3_Report.docx'
doc.save(out)
print(f"Report saved to: {out}")