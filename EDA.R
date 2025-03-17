library(tidyverse)

records_raw <- read_csv("college_football_records.csv")
scoreboard_raw <- read_csv("combined_scorecard_data.csv") %>%
  mutate(MAIN = factor(MAIN),
         HIGHDEG = factor(HIGHDEG),
         REGION = factor(REGION),
         LOCALE = factor(LOCALE),
         LOCALE2 = factor(LOCALE2),
         CCSIZSET = factor(CCSIZSET),
         OPENADMP = factor(OPENADMP),
         ADMCON7 = factor(ADMCON7))

# Missing data in Scoreboard data
for (col in colnames(scoreboard_raw)) {
  nas <- scoreboard_raw[[col]] %>%
    is.na() %>%
    sum()
  paste(col, ":\t", 100 * nas / nrow(scoreboard_raw), "%\n", sep = "") %>%
    cat()
}

# Remove columns that don't have any data
scoreboard <- scoreboard_raw %>%
  select(!c(
    LOCALE2,
    PRGMOFR,
    MDCOST_ALL,
    MDEARN_ALL
  ))

# Missing data in Record data
for (col in colnames(records_raw)) {
  nas <- records_raw[[col]] %>%
    is.na() %>%
    sum()
  paste(col, ":\t", 100 * nas / nrow(records_raw), "%\n", sep = "") %>%
    cat()
}

records <- records_raw

# Merge data
data <- scoreboard %>%
  left_join(records, by = join_by(Year == year, INSTNM == scorecard_name))

# See data that did not merge correctly
NAs <- data %>%
  select(INSTNM, Year, team, won, lost, tied, notes, UGDS, MAIN) %>%
  filter(is.na(team))
data[data$INSTNM %>% grep("-", .), ] %>% View
NAs[NAs$INSTNM %>% grep("-", .), ] %>% View

# Store variable types
predictors <- data[c(3:5, 7:21, 24:29, 36:41)] %>%
  colnames()

