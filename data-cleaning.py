import pandas as pd

# Read in data
records_df = pd.read_csv("college_football_records.csv")
scorecard_df = pd.read_csv("combined_scorecard_data.csv")



##################################
# Cleaning the Records dataframe #
##################################

# Make all NAs in the tied column 0
records_df.loc[records_df.tied.isna(), "tied"] = 0 



#####################################
# Cleaning the Scoreboard dataframe #
#####################################

# Remove completely empty columns
scorecard_df.drop(columns = ["LOCALE2","PRGMOFR", "MDCOST_ALL", "MDEARN_ALL"], inplace = True)

# Add columns of n-years-ago
new_columns = ["One_year_ago", "Two_years_ago", "Three_years_ago", "Four_years_ago",
               "Five_years_ago", "Six_years_ago", "Seven_years_ago", "Eight_years_ago",
               "Nine_years_ago", "Ten_years_ago", "Eleven_year_ago", "Twelve_years_ago",
               "Thirteen_years_ago", "Fourteen_years_ago", "Fifteen_years_ago", "Sixteen_years_ago",
               "Seventeen_years_ago", "Eighteen_years_ago", "Nineteen_years_ago", "Twenty_years_ago"]
# Years correspond to students in the <Year-1>-<Year> school year,
# so we want to link it up to 2 years prior for the first year.
for i in range(20):
    scorecard_df[new_columns[i]] = scorecard_df["Year"] - (i + 2)



####################
# Merge dataframes #
####################
############
############
############
############
############

# Merge in the first year to simplify naming.
# We'll take it out later.
df = scorecard_df
df = df.merge(records_df,
              how = "left",
              left_on = ["Year", "INSTNM"],
              right_on = ["year", "scorecard_name"])

# Do the merge
for col in new_columns:
    df = df.merge(records_df,
                  how = "left",
                  left_on = [col, "INSTNM"],
                  right_on = ["year", "scorecard_name"],
                  suffixes = (None, "_" + col))
    # Remove useless repeat columns
    df.drop(columns = ["year_" + col, "scorecard_name_" + col], inplace = True)

# Now we can drop the score from the same year
df = df.drop(columns = list(records_df.columns))



###################
# Wrie final data #
###################

df.to_csv("data.csv", index = False)

