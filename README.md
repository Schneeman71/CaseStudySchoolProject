# CaseStudySchoolProject

# Optimizing University Investments for Student Success

**First Place Winning Solution — BYU Data Case Study Competition**

## Executive Summary

In this project, our team acted as data consultants presenting to a university board of directors. The board was divided on a core strategy: **Would investing heavily in the school's college football program improve the quality of incoming student admissions (measured by SAT scores)?**

Through an analysis of over 50 years of College Scorecard and college football data, we disproved the board's baseline hypothesis and pivoted to a more impactful, data-driven business recommendation focused on student retention and academic infrastructure.

## Key Insights & Recommendations

* **The Football Myth:** We found no statistically significant association between a football program's performance and the quality of student admissions.
* **Redefining Success:** Our EDA revealed that incoming SAT scores are highly correlated with 4-year graduation rates. We pivoted our objective to use the 4-year graduation rate as the ultimate metric for university success. Since SAT scores don't tell you anything about how a student performed after admission.
* **Identifying At-Risk Demographics:** We discovered that minority (non-white) female students were at the highest risk of not graduating in four years. While they make up a growing proportion of the college demographic, historical data showed higher rates of dropping out or transferring for this group.
* **The Strategic Solution:** To actively improve the 4-year graduation rate, we modeled various interventions. We found that increasing the **faculty-to-student ratio** had a highly positive impact on retention, particularly for at-risk demographics, far outpacing the ROI of athletic investments.

*Note: While we communicated to the board that our historical data is observational rather than strictly causal, the trends strongly indicated that academic infrastructure investments yield the highest return for student success.*

## Methodology & Tech Stack

We utilized a bilingual tech stack (Python and R) to process the data, perform exploratory data analysis (EDA), and build our predictive models.

1. **Data Cleaning & Imputation (Python/Pandas):** Handled decades of messy, missing data across multiple merged datasets (Scorecard + Football records).
2. **Exploratory Data Analysis (R/ggplot2):** Analyzed 10-20 year recent trends to explore relationships across admissions (open vs. closed), demographics (race, gender), and institutional spending.
3. **Modeling (R/Quarto):** Developed linear and logistic regression models to predict graduation rates based on university features.
4. **Validation:** Utilized cross-validation to ensure our models were robust and representative.

## Repository Structure

* `/data` - Contains the data dictionaries and raw CSV files.
* `/notebooks` - Jupyter and Quarto notebooks for data cleaning and linear modeling.
* `/scripts` - Standalone Python (`data-cleaning.py`) and R (`EDA.R`) scripts.
* `/graphs` - High-resolution visualizations used in the final presentation.

## The Team

This project was a collaborative effort by our 3-person team. Although every member actively contributed to all phases of the project and joint decision-making, we each took point on specific areas based on our strengths:

James Klein: Data Engineering & Integrity. Leveraged Python and Pandas to lead data cleaning, missing value imputation, and pipeline creation. Partnered on the EDA to ensure our analytical models accurately reflected the underlying imputation methods and maintained data integrity.

Carson Buttars: Exploratory Data Analysis. Partnered closely with James to lead the statistical exploration of the cleaned data in R, uncovering the core trends, and evaluating different analytical approaches.

Jamie Herron: Presentation & Visual Synthesis. Contributed to the EDA and took the lead on translating our statistical findings into a compelling business narrative. Designed the final presentation and polished the R/ggplot2 visualizations to effectively communicate our insights to the judges.
