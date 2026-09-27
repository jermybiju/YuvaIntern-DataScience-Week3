import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

# Load the cleaned dataset from Week 1
df = pd.read_csv("data/titanic_cleaned.csv")

# Create images folder if it does not exist
os.makedirs("images", exist_ok=True)

# Style
sns.set_style("whitegrid")

print("=" * 60)
print("WEEK 3 — STATISTICAL ANALYSIS AND HYPOTHESIS TESTING")
print("=" * 60)

# ==================================================================
# HYPOTHESIS 1 — Chi-Square Test of Independence
# H0: Survival and Sex are independent
# H1: Survival and Sex are associated
# ==================================================================

print("\n" + "=" * 60)
print("HYPOTHESIS 1: Survival and Sex")
print("=" * 60)

# Create a contingency table
contingency_table = pd.crosstab(df['sex'], df['survived'])
print("\nContingency Table (observed counts):")
print(contingency_table)

# Perform Chi-square test
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

print(f"\nChi-square statistic: {chi2:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"p-value: {p_value:.6e}")

# Interpret the result
alpha = 0.05
if p_value < alpha:
    print(f"\nResult: p ({p_value:.2e}) < alpha ({alpha})")
    print("Decision: REJECT the null hypothesis.")
    print("Conclusion: There is a statistically significant association")
    print("            between sex and survival.")
else:
    print(f"\nResult: p ({p_value:.2e}) >= alpha ({alpha})")
    print("Decision: FAIL TO REJECT the null hypothesis.")
    print("Conclusion: No statistically significant association detected.")

# Effect size: Cramer's V
n = contingency_table.sum().sum()
cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
print(f"\nCramer's V (effect size): {cramers_v:.4f}")
if cramers_v < 0.1:
    print("Interpretation: Negligible association.")
elif cramers_v < 0.3:
    print("Interpretation: Weak association.")
elif cramers_v < 0.5:
    print("Interpretation: Moderate association.")
else:
    print("Interpretation: Strong association.")

# Visualization: Stacked bar chart of counts
fig, ax = plt.subplots(figsize=(8, 5))
contingency_table.plot(kind='bar', stacked=True, ax=ax,
                        color=['#C44E52', '#55A868'])
ax.set_title("Survival Counts by Sex (Observed)", fontsize=13, fontweight='bold')
ax.set_xlabel("Sex", fontsize=11)
ax.set_ylabel("Count", fontsize=11)
ax.legend(title='Survived', labels=['Did Not Survive', 'Survived'], loc='upper right')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("images/week3_chart1_survival_sex_counts.png", dpi=150)
plt.close()

print("\nChart saved: images/week3_chart1_survival_sex_counts.png")

# ==================================================================
# HYPOTHESIS 2 — Independent Samples t-test (Welch's)
# H0: Mean fare is the same for survivors and non-survivors
# H1: Mean fare differs between the two groups
# ==================================================================

print("\n" + "=" * 60)
print("HYPOTHESIS 2: Mean Fare by Survival")
print("=" * 60)

# Split fare by survival status
fare_survived = df[df['survived'] == 1]['fare']
fare_not_survived = df[df['survived'] == 0]['fare']

# Descriptive statistics
print("\nDescriptive Statistics:")
print(f"Survived (n = {len(fare_survived)}):")
print(f"  Mean:   £{fare_survived.mean():.2f}")
print(f"  Median: £{fare_survived.median():.2f}")
print(f"  Std:    £{fare_survived.std():.2f}")
print(f"\nDid Not Survive (n = {len(fare_not_survived)}):")
print(f"  Mean:   £{fare_not_survived.mean():.2f}")
print(f"  Median: £{fare_not_survived.median():.2f}")
print(f"  Std:    £{fare_not_survived.std():.2f}")

# Welch's t-test (equal_var=False for unequal variances)
t_stat, p_value = stats.ttest_ind(fare_survived, fare_not_survived, equal_var=False)

print(f"\nWelch's t-test:")
print(f"  t-statistic: {t_stat:.4f}")
print(f"  p-value: {p_value:.6e}")

# Interpret
alpha = 0.05
if p_value < alpha:
    print(f"\nResult: p ({p_value:.2e}) < alpha ({alpha})")
    print("Decision: REJECT the null hypothesis.")
    print("Conclusion: Mean fare differs significantly between survivors")
    print("            and non-survivors.")
else:
    print(f"\nResult: p ({p_value:.2e}) >= alpha ({alpha})")
    print("Decision: FAIL TO REJECT the null hypothesis.")

# 95% Confidence Interval for the difference in means
mean_diff = fare_survived.mean() - fare_not_survived.mean()
se_diff = np.sqrt(fare_survived.var(ddof=1)/len(fare_survived) +
                  fare_not_survived.var(ddof=1)/len(fare_not_survived))
# Welch-Satterthwaite degrees of freedom
df_welch = (fare_survived.var(ddof=1)/len(fare_survived) +
            fare_not_survived.var(ddof=1)/len(fare_not_survived))**2 / (
            (fare_survived.var(ddof=1)/len(fare_survived))**2/(len(fare_survived)-1) +
            (fare_not_survived.var(ddof=1)/len(fare_not_survived))**2/(len(fare_not_survived)-1))
t_critical = stats.t.ppf(0.975, df_welch)
ci_lower = mean_diff - t_critical * se_diff
ci_upper = mean_diff + t_critical * se_diff

print(f"\n95% Confidence Interval for (Mean_Survived - Mean_Not_Survived):")
print(f"  Difference in means: £{mean_diff:.2f}")
print(f"  95% CI: [£{ci_lower:.2f}, £{ci_upper:.2f}]")
print("  Interpretation: With 95% confidence, survivors paid on average")
print(f"                  between £{ci_lower:.2f} and £{ci_upper:.2f} more than")
print("                  non-survivors.")

# Visualization: Boxplot of fare by survival
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x='survived', y='fare', data=df, ax=ax,
            hue='survived', palette={0: '#C44E52', 1: '#55A868'},
            legend=False)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Did Not Survive', 'Survived'])
ax.set_title("Fare Distribution by Survival Status", fontsize=13, fontweight='bold')
ax.set_xlabel("Survival Status", fontsize=11)
ax.set_ylabel("Fare (pounds)", fontsize=11)

# Annotate means
means = [fare_not_survived.mean(), fare_survived.mean()]
for i, m in enumerate(means):
    ax.text(i, m + 15, f"Mean: £{m:.2f}", ha='center', fontsize=9,
            style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                     edgecolor='gray', alpha=0.8))

plt.tight_layout()
plt.savefig("images/week3_chart2_fare_ttest.png", dpi=150)
plt.close()

print("\nChart saved: images/week3_chart2_fare_ttest.png")


# ==================================================================
# HYPOTHESIS 3 — One-Way ANOVA
# H0: Mean age is the same across all three passenger classes
# H1: At least one class has a different mean age
# ==================================================================

print("\n" + "=" * 60)
print("HYPOTHESIS 3: Mean Age Across Passenger Classes")
print("=" * 60)

# Split age by passenger class
age_1st = df[df['pclass'] == 1]['age']
age_2nd = df[df['pclass'] == 2]['age']
age_3rd = df[df['pclass'] == 3]['age']

# Descriptive statistics
print("\nDescriptive Statistics:")
for cls, ages in [('1st Class', age_1st), ('2nd Class', age_2nd), ('3rd Class', age_3rd)]:
    print(f"{cls} (n = {len(ages)}):")
    print(f"  Mean:   {ages.mean():.2f} years")
    print(f"  Median: {ages.median():.2f} years")
    print(f"  Std:    {ages.std():.2f}")

# One-way ANOVA
f_stat, p_value = stats.f_oneway(age_1st, age_2nd, age_3rd)

print(f"\nOne-Way ANOVA:")
print(f"  F-statistic: {f_stat:.4f}")
print(f"  p-value: {p_value:.6e}")

# Interpret
alpha = 0.05
if p_value < alpha:
    print(f"\nResult: p ({p_value:.2e}) < alpha ({alpha})")
    print("Decision: REJECT the null hypothesis.")
    print("Conclusion: At least one passenger class has a significantly")
    print("            different mean age.")
else:
    print(f"\nResult: p ({p_value:.2e}) >= alpha ({alpha})")
    print("Decision: FAIL TO REJECT the null hypothesis.")

# Effect size: Eta-squared
grand_mean = df['age'].mean()
ss_between = (len(age_1st) * (age_1st.mean() - grand_mean)**2 +
              len(age_2nd) * (age_2nd.mean() - grand_mean)**2 +
              len(age_3rd) * (age_3rd.mean() - grand_mean)**2)
ss_total = ((df['age'] - grand_mean)**2).sum()
eta_squared = ss_between / ss_total

print(f"\nEta-squared (effect size): {eta_squared:.4f}")
if eta_squared < 0.01:
    print("Interpretation: Small effect.")
elif eta_squared < 0.06:
    print("Interpretation: Medium effect.")
else:
    print("Interpretation: Large effect.")

# Visualization: Boxplot of age by class
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x='pclass', y='age', data=df, ax=ax,
            hue='pclass', palette='Set2', legend=False)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['1st Class', '2nd Class', '3rd Class'])
ax.set_title("Age Distribution by Passenger Class", fontsize=13, fontweight='bold')
ax.set_xlabel("Passenger Class", fontsize=11)
ax.set_ylabel("Age (years)", fontsize=11)

# Annotate means
means = [age_1st.mean(), age_2nd.mean(), age_3rd.mean()]
for i, m in enumerate(means):
    ax.text(i, m + 3, f"Mean: {m:.1f}", ha='center', fontsize=9,
            style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                     edgecolor='gray', alpha=0.8))

plt.tight_layout()
plt.savefig("images/week3_chart3_age_anova.png", dpi=150)
plt.close()

print("\nChart saved: images/week3_chart3_age_anova.png")

# ==================================================================
# HYPOTHESIS 4 — Mann-Whitney U Test (Non-parametric)
# H0: Age distribution is the same for survivors and non-survivors
# H1: Age distributions differ between the two groups
# ==================================================================

print("\n" + "=" * 60)
print("HYPOTHESIS 4: Age Distribution by Survival (Mann-Whitney U)")
print("=" * 60)

# Split age by survival status
age_survived = df[df['survived'] == 1]['age']
age_not_survived = df[df['survived'] == 0]['age']

# Descriptive statistics
print("\nDescriptive Statistics:")
print(f"Survived (n = {len(age_survived)}):")
print(f"  Mean:   {age_survived.mean():.2f} years")
print(f"  Median: {age_survived.median():.2f} years")
print(f"  Std:    {age_survived.std():.2f}")
print(f"\nDid Not Survive (n = {len(age_not_survived)}):")
print(f"  Mean:   {age_not_survived.mean():.2f} years")
print(f"  Median: {age_not_survived.median():.2f} years")
print(f"  Std:    {age_not_survived.std():.2f}")

# Mann-Whitney U test
u_stat, p_value = stats.mannwhitneyu(age_survived, age_not_survived,
                                      alternative='two-sided')

print(f"\nMann-Whitney U Test:")
print(f"  U-statistic: {u_stat:.2f}")
print(f"  p-value: {p_value:.6e}")

# Interpret
alpha = 0.05
if p_value < alpha:
    print(f"\nResult: p ({p_value:.2e}) < alpha ({alpha})")
    print("Decision: REJECT the null hypothesis.")
    print("Conclusion: Age distributions differ significantly between")
    print("            survivors and non-survivors.")
else:
    print(f"\nResult: p ({p_value:.2e}) >= alpha ({alpha})")
    print("Decision: FAIL TO REJECT the null hypothesis.")
    print("Conclusion: No statistically significant difference in age")
    print("            distributions detected.")

# Effect size: rank-biserial correlation
n1 = len(age_survived)
n2 = len(age_not_survived)
rank_biserial = 1 - (2 * u_stat) / (n1 * n2)
print(f"\nRank-biserial correlation (effect size): {rank_biserial:.4f}")
print(f"  |r| = {abs(rank_biserial):.4f}")
if abs(rank_biserial) < 0.1:
    print("  Interpretation: Negligible effect.")
elif abs(rank_biserial) < 0.3:
    print("  Interpretation: Small effect.")
elif abs(rank_biserial) < 0.5:
    print("  Interpretation: Moderate effect.")
else:
    print("  Interpretation: Large effect.")

# Visualization: Overlaid histograms of age by survival
fig, ax = plt.subplots(figsize=(10, 5))
bins = np.arange(0, 85, 5)
ax.hist(age_not_survived, bins=bins, alpha=0.6, label='Did Not Survive',
        color='#C44E52', edgecolor='black')
ax.hist(age_survived, bins=bins, alpha=0.6, label='Survived',
        color='#55A868', edgecolor='black')
ax.set_title("Age Distribution by Survival Status", fontsize=13, fontweight='bold')
ax.set_xlabel("Age (years)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.legend(loc='upper right', title='Survived')
ax.axvline(age_survived.median(), color='green', linestyle='--',
           linewidth=2, alpha=0.8, label=f'Survived median: {age_survived.median():.0f}')
ax.axvline(age_not_survived.median(), color='red', linestyle='--',
           linewidth=2, alpha=0.8, label=f'Non-survivor median: {age_not_survived.median():.0f}')
ax.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig("images/week3_chart4_age_mannwhitney.png", dpi=150)
plt.close()

print("\nChart saved: images/week3_chart4_age_mannwhitney.png")

# ==================================================================
# BONUS — 95% Confidence Intervals for Survival Rate by Sex × Class
# Shows the uncertainty around each group's survival estimate
# ==================================================================

print("\n" + "=" * 60)
print("BONUS: 95% Confidence Intervals for Survival Rate by Sex × Class")
print("=" * 60)

def wilson_ci(successes, total, confidence=0.95):
    """Wilson score interval for a proportion (better than normal approx)."""
    if total == 0:
        return (0.0, 0.0)
    p = successes / total
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    denom = 1 + z**2 / total
    centre = (p + z**2 / (2 * total)) / denom
    margin = z * np.sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / denom
    return (max(0, centre - margin), min(1, centre + margin))

# Compute survival rate and 95% CI for each sex × class group
groups = []
for sex in ['female', 'male']:
    for pclass in [1, 2, 3]:
        subset = df[(df['sex'] == sex) & (df['pclass'] == pclass)]
        n = len(subset)
        k = int(subset['survived'].sum())
        rate = k / n if n > 0 else 0
        lo, hi = wilson_ci(k, n)
        groups.append({
            'label': f"{sex.capitalize()} {pclass}",
            'rate': rate,
            'lo': lo,
            'hi': hi,
            'n': n
        })

# Print the table
print("\nGroup            |   N  | Survival |  95% CI")
print("-" * 55)
for g in groups:
    print(f"{g['label']:<15} | {g['n']:>4} |  {g['rate']:.3f}   | [{g['lo']:.3f}, {g['hi']:.3f}]")

# Visualization — horizontal errorbar plot
fig, ax = plt.subplots(figsize=(9, 5))
labels = [g['label'] for g in groups]
rates = [g['rate'] for g in groups]
errors = [[g['rate'] - g['lo'] for g in groups],
          [g['hi'] - g['rate'] for g in groups]]

colors = ['#DD8452' if 'Female' in g['label'] else '#4C72B0' for g in groups]
y_pos = np.arange(len(labels))

ax.errorbar(rates, y_pos, xerr=errors, fmt='o', capsize=5,
            color='black', ecolor='gray', elinewidth=2, markersize=10,
            markerfacecolor='white', markeredgewidth=2)

# Color the marker dots individually
for i, (rate, color) in enumerate(zip(rates, colors)):
    ax.plot(rate, i, 'o', markersize=12, color=color, zorder=3)
    ax.text(rate + 0.02, i, f"{rate:.2f}", va='center', fontsize=9)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlim(0, 1.1)
ax.set_xlabel("Survival Rate", fontsize=11)
ax.set_title("Survival Rate with 95% Confidence Intervals\nby Sex and Passenger Class",
             fontsize=12, fontweight='bold')
ax.axvline(0.5, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig("images/week3_chart5_ci_plot.png", dpi=150)
plt.close()

print("\nChart saved: images/week3_chart5_ci_plot.png")