library(tidyverse)

df <- read_csv("data.csv")

# How much data do we lose by going bask all 20 years?
df$won_Twenty_years_ago %>%
  is.na() %>%
  sum() %>%
  paste("We lose ",
        .,
        " data points by going back 20 years.\n",
        sep = "") %>%
  cat()
df$won_One_year_ago %>%
  is.na() %>%
  sum() %>%
  paste("As opposed to ",
        .,
        " lost by going back 1 year.\n",
        sep = "") %>%
  cat()
# We lose 759 data points by going back 20 years.
# As opposed to 649 lost by going back 1 year.

# How do missing values change for various ways of spliting data?
# Overall (UGDS)
df %>%
  filter(!is.na(UGDS)) %>%
  select("won_Twenty_years_ago") %>%
  is.na() %>%
  mean(.) %>%
  `*`(100) %>%
  round(digits = 2) %>%
  paste("Among non-NA values, we lose ",
        .,
        "% of values from 20 years ago\n",
        sep = "") %>%
  cat()
cat("For other columns, here are the results:\n")
for (col in colnames(df[1:36])) {
  df %>%
    filter(!is.na(UGDS)) %>%
    select(all_of(col)) %>%
    is.na() %>%
    mean(.) %>%
    `*`(100) %>%
    round(digits = 2) %>%
    paste(col, ": ", ., "%\n", sep = "") %>%
    cat()
}
# Among non-NA values, we lose 15.18% of values from 20 years ago
# For other columns, here are the results:
# UNITID: 0%
# OPEID: 0%
# INSTNM: 0%
# CITY: 0%
# Year: 0%
# UGDS: 0%
# MAIN: 0%
# NUMBRANCH: 0%
# HIGHDEG: 0%
# REGION: 0%
# LOCALE: 0%
# CCSIZSET: 96.13%
# PCTPELL: 43.07%
# AVGFACSAL: 0.11%
# PFTFAC: 19.22%
# BOOKSUPPLY: 12.37%
# ROOMBOARD_ON: 12.75%
# ROOMBOARD_OFF: 29.48%
# OTHEREXPENSE_ON: 13.03%
# OTHEREXPENSE_OFF: 29.42%
# ADMCON7: 15.57%
# UGDS_WOMEN: 0%
# UGDS_MEN: 0%
# ADM_RATE: 16.73%
# SAT_AVG: 19.69%
# ACTCMMID: 27.72%
# RET_FT4: 27.36%
# C150_4: 4.57%
# MD_EARN_WNE_P10: 73.52%
# TUITIONFEE_IN: 16.04%
# TUITIONFEE_OUT: 16.04%
# UGDS_WHITE: 42.28%
# UGDS_BLACK: 42.28%
# UGDS_HISP: 42.28%
# UGDS_ASIAN: 42.28%
# OPENADMP: 7.47%

# As far as splitting by demographic goes, we don't lose anything
# from splitting by gender and race seems to all lose the same data

# Open Enrollment (OPENADMP)
df %>%
  filter(OPENADMP == 1) %>%
  select("won_Twenty_years_ago") %>%
  is.na() %>%
  mean(.) %>%
  `*`(100) %>%
  round(digits = 2) %>%
  paste("Among open-enrollment schools, we lose ",
        .,
        "% of values from 20 years ago\n",
        sep = "") %>%
  cat()
df %>%
  filter(OPENADMP == 2) %>%
  select("won_Twenty_years_ago") %>%
  is.na() %>%
  mean(.) %>%
  `*`(100) %>%
  round(digits = 2) %>%
  paste("Among closed-enrollment schools, we lose ",
        .,
        "% of values from 20 years ago\n",
        sep = "") %>%
  cat()
cat("For other columns, here are the results (Open; Closed):\n")
for (col in colnames(df[1:31])) {
  paste(col, ": ", sep = "") %>%
    cat()
  df %>%
    filter(OPENADMP == 1) %>%
    select(all_of(col)) %>%
    is.na() %>%
    mean(.) %>%
    `*`(100) %>%
    round(digits = 2) %>%
    paste(., "%", sep = "") %>%
    cat()
  cat("; ")
  df %>%
    filter(OPENADMP == 2) %>%
    select(all_of(col)) %>%
    is.na() %>%
    mean(.) %>%
    `*`(100) %>%
    round(digits = 2) %>%
    paste(., "%\n", sep = "") %>%
    cat()
}
# Among open-enrollment schools, we lose 42.53% of values from 20 years ago
# Among closed-enrollment schools, we lose 14.59% of values from 20 years ago
# For other columns, here are the results (Open; Closed):
# UNITID: 0%; 0%
# OPEID: 0%; 0%
# INSTNM: 0%; 0%
# CITY: 0%; 0%
# Year: 0%; 0%
# UGDS: 10.34%; 3.86%
# MAIN: 0%; 0%
# NUMBRANCH: 0%; 0%
# HIGHDEG: 0%; 0%
# REGION: 0%; 0%
# LOCALE: 0%; 0%
# CCSIZSET: 98.85%; 95.93%
# PCTPELL: 64.37%; 40.47%
# AVGFACSAL: 10.34%; 3.93%
# PFTFAC: 36.78%; 15.77%
# BOOKSUPPLY: 19.54%; 5.16%
# ROOMBOARD_ON: 45.98%; 5.09%
# ROOMBOARD_OFF: 25.29%; 23.52%
# OTHEREXPENSE_ON: 45.98%; 5.43%
# OTHEREXPENSE_OFF: 28.74%; 23.36%
# ADMCON7: 31.03%; 7.95%
# UGDS_WOMEN: 10.34%; 3.86%
# UGDS_MEN: 10.34%; 3.86%
# ADM_RATE: 100%; 11.88%
# SAT_AVG: 100%; 15.02%
# ACTCMMID: 100%; 23.52%
# RET_FT4: 67.82%; 23.77%
# C150_4: 32.18%; 0.25%
# MD_EARN_WNE_P10: 78.16%; 72.42%
# TUITIONFEE_IN: 22.99%; 8.98%
# TUITIONFEE_OUT: 22.99%; 8.98%

# Student quality data is only present for schools that have closed
# admissions (which is where we need it). There is also lots more
# student success data (RET_FT4 and C150_4) for closed admission
# schools.

