import pandas as pd

# Read in data
records_df = pd.read_csv("college_football_records.csv")
scorecard_df = pd.read_csv("combined_scorecard_data.csv")



##################################
# Cleaning the Records dataframe #
##################################

# Make all NAs in the tied column 0
records_df.loc[records_df.tied.isna(), "tied"] = 0 

# Remove repeats (Fresno state 2022 is the only one)
records_df.drop(5646, inplace = True)

# The following colleges have no value for "scorecard_name":
# 'Centre', 'Charlotte', 'Sewanee', 'Washington_+_Lee', 'West_Texas_A+M', 'Western_State', 'William_+_Mary'
# The following just doesn't have a match:
# 'The Pennsylvania State University'
# It only exists for 2020 and 2021 in the scorecard dataframe,
# so we'll just remove it from the scorecard dataframe.
# they are rows 4500 and 4681 (in the scoredard dataframe)
# Evidence:
# scorecard_df.loc[scorecard_df.INSTNM.str.contains("Penn"), ["Year", "INSTNM"]]
# all_names = list(record_test_in.scorecard_name.unique())
# [row['scorecard_name'] for index, row in record_test_left.iterrows() if row['scorecard_name'] not in all_names]
# [row['team'] for index, row in record_test_left.iterrows() if row['scorecard_name'] not in all_names]



#####################################
# Cleaning the Scoreboard dataframe #
#####################################

# Remove completely empty columns
scorecard_df.drop(columns = ["LOCALE2","PRGMOFR", "MDCOST_ALL", "MDEARN_ALL"], inplace = True)

# Use correct data types
scorecard_df = scorecard_df.astype({"LOCALE": "int",
                                    "CCSIZSET": "int",
                                    "ADMCON7": "int",
                                    "OPENADMP": "int"})

# Remove Penn State data (see comment from the records section of this script)
scorecard_df.drop([4500, 4681], inplace = True)

# Assume LOCALE based on CITY. 
# All the LOCALE data present is from the 2022 year, so we don't
# have to worry about changes year-to-year
for city in list(scorecard_df.CITY.unique()):
    try:
        locale = int(scorecard_df.loc[(scorecard_df.CITY == city) & (scorecard_df.Year == 2022), "LOCALE"].values[0])
    except:
        locale = 0
    scorecard_df.loc[scorecard_df.CITY == city, "LOCALE"] = locale

# Assume CCSIZSET based on INSTNM.
# All the CCSIZSET data present is from the 2022 year, so we don't
# have to to worry about changes year-to-year
for name in list(scorecard_df.INSTNM.unique()):
    try:
        ccsizset = int(scorecard_df.loc[(scorecard_df.INSTNM == name) & (scorecard_df.Year == 2022), "CCSIZSET"].values[0])
    except:
        ccsizset = 0
    scorecard_df.loc[scorecard_df.INSTNM == name, "CCSIZSET"] = locale

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

# Merge in the first year to simplify naming.
# We'll take it out later.
df = scorecard_df
df = df.merge(records_df,
              how = "inner",
              left_on = ["Year", "INSTNM"],
              right_on = ["year", "scorecard_name"])

# Do the merge
for col in new_columns:
    df = df.merge(records_df,
                  how = "inner",
                  left_on = [col, "INSTNM"],
                  right_on = ["year", "scorecard_name"],
                  suffixes = (None, "_" + col))
    # Remove useless repeat columns
    df.drop(columns = ["team_" + col, "year_" + col, "scorecard_name_" + col], inplace = True)

# Now we can drop the score from the same year
df = df.drop(columns = list(records_df.columns))



####################
# Write final data #
####################

df.to_csv("data.csv", index = False)

