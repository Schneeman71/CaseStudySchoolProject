import pandas as pd
import numpy as np

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
# 'Centre', 'Charlotte', 'Sewanee', 'Washington_+_Lee', 'West_Texas_A+M', 'Western_State', 'William_+_Mary'.
# The following just doesn't have a match:
# 'The Pennsylvania State University'
# It only exists for 2020 and 2021 in the scorecard dataframe,
# so we'll just remove it from the scorecard dataframe.
# They are rows 4500 and 4681 (in the scorecard dataframe).
# Evidence:
# scorecard_df.loc[scorecard_df.INSTNM.str.contains("Penn"), ["Year", "INSTNM"]]
# all_names = list(record_test_in.scorecard_name.unique())
# [row['scorecard_name'] for index, row in record_test_left.iterrows() if row['scorecard_name'] not in all_names]
# [row['team'] for index, row in record_test_left.iterrows() if row['scorecard_name'] not in all_names]

# Fill in missing values for wins, losses, and ties
for col in ["won", "lost", "tied"]:
    records_df.loc[records_df[col].isnull(), col] = 0

# Create a total games column
records_df["games"] = records_df["won"] + records_df["lost"] + records_df["tied"]

# Use correct data types
records_df = records_df.astype({"won": "int",
                                "lost": "int",
                                "tied": "int",
                                "games": "int"})



#####################################
# Cleaning the Scoreboard dataframe #
#####################################

# Remove completely or very empty columns
scorecard_df.drop(columns = ["LOCALE2", "PRGMOFR", "MDCOST_ALL", "MDEARN_ALL", "MD_EARN_WNE_P10"], inplace = True)

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
# have to worry about changes year-to-year
for name in list(scorecard_df.INSTNM.unique()):
    try:
        ccsizset = int(scorecard_df.loc[(scorecard_df.INSTNM == name) & (scorecard_df.Year == 2022), "CCSIZSET"].values[0])
    except:
        ccsizset = 0
    finally:
        scorecard_df.loc[scorecard_df.INSTNM == name, "CCSIZSET"] = locale

# Fill in OPENADMP for the first couple of years.
# We'll just assume it is the same as the most
# recent year.
for name in list(scorecard_df.loc[scorecard_df.OPENADMP.isnull(), "INSTNM"].unique()):
    try:
        openadmp = int(scorecard_df.loc[(~scorecard_df.OPENADMP.isnull()) & (scorecard_df.INSTNM == name), "OPENADMP"].iloc[0])
    except:
        continue
    scorecard_df.loc[(scorecard_df.OPENADMP.isnull()) & (scorecard_df.INSTNM == name), "OPENADMP"] = openadmp

# Same thing as OPENADMP but with ADMCON7,
# except if the school has open admissions,
# we know it doesn't have requirements.
for name in list(scorecard_df.loc[scorecard_df.ADMCON7.isnull(), "INSTNM"].unique()):
    try:
        admcon = int(scorecard_df.loc[(~scorecard_df.ADMCON7.isnull()) & (scorecard_df.INSTNM == name), "ADMCON7"].iloc[0])
    except:
        if int(scorecard_df.loc[(~scorecard_df.ADMCON7.isnull()) & (scorecard_df.INSTNM == name), "OPENADMP"].iloc[0]) == 1:
            admcon = 3
        else:
            admcon = 4
    scorecard_df.loc[(scorecard_df.ADMCON7.isnull()) & (scorecard_df.INSTNM == name), "ADMCON7"] = admcon

# Fill in missing numeric values with the school's median
missing_threshold = 0.5
cols_of_interest = ['UGDS', 'NUMBRANCH', 'PCTPELL', 'AVGFACSAL', 'PFTFAC',
                    'BOOKSUPPLY', 'ROOMBOARD_ON', 'ROOMBOARD_OFF',
                    'OTHEREXPENSE_ON', 'OTHEREXPENSE_OFF', 'UGDS_WOMEN',
                    'UGDS_MEN', 'SAT_AVG', 'ACTCMMID', 'RET_FT4', 'C150_4',
                    'TUITIONFEE_IN', 'TUITIONFEE_OUT', 'UGDS_WHITE',
                    'UGDS_BLACK', 'UGDS_HISP', 'UGDS_ASIAN']
for unitid in list(scorecard_df.UNITID.unique()):
    # Replace 0.000 with NaN
    tmp_df = scorecard_df.loc[scorecard_df.UNITID == unitid, ].replace(0.000, np.nan)

    # Check if any numerical column has excessive missing values
    cols_with_excessive_missing = [col for col in cols_of_interest if tmp_df[col].isnull().mean() > missing_threshold]

    if cols_with_excessive_missing:
        # Skip imputation and drop rows with NaN values
        to_drop = [index for index, row in tmp_df.iterrows() if row.isnull().sum() > 0]
        scorecard_df.drop(to_drop, inplace = True)
        continue
    
    # Now we try to impute
    try:
        tmp_df.loc[:, cols_of_interest] = tmp_df.loc[:, cols_of_interest].fillna(tmp_df.loc[:, cols_of_interest].median())
        scorecard_df.loc[scorecard_df.UNITID == unitid, :] = tmp_df
    except:
        # Something went wrong, let's move on and drop NaN values
        to_drop = [index for index, row in tmp_df.iterrows() if row.isnull().sum() > 0]
        scorecard_df = scorecard_df.drop(to_drop, inplace = True)
        continue

# Create delta columns that take the difference between
# the present year and the previous year.
delta_columns = ["INSTNM", "Year", "UGDS", "UGDS_WOMEN", "UGDS_MEN", "ADM_RATE",
                 "SAT_AVG", "ACTCMMID", "RET_FT4", "C150_4", "TUITIONFEE_IN",
                 "TUITIONFEE_OUT", "UGDS_WHITE", "UGDS_BLACK", "UGDS_HISP",
                 "UGDS_ASIAN"]
year_before = scorecard_df.loc[:, delta_columns]
year_before.loc[:, "Year"] = year_before.loc[:, "Year"] + 1
scorecard_df = scorecard_df.merge(year_before,
                                  how = "left",
                                  left_on = ["Year", "INSTNM"],
                                  right_on = ["Year", "INSTNM"],
                                  suffixes = (None, "_delta"))
for col in delta_columns[2:]:
    scorecard_df.loc[:, col + "_delta"] = (scorecard_df[col] / scorecard_df[col + "_delta"]) - 1

# Use correct data types
scorecard_df = scorecard_df.astype({"LOCALE": "int",
                                    "CCSIZSET": "int",
                                    "ADMCON7": "int",
                                    "OPENADMP": "int"})

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
    df.drop(columns = ["team_" + col, "year_" + col, "scorecard_name_" + col, "notes_" + col], inplace = True)

# Now we can drop the score from the same year
df = df.drop(columns = list(records_df.columns))

# And the # of years back columns
df = df.drop(columns = new_columns)

# Again ensure the correct types are used
# integer_cols = [0, 4, 6, 7, 8, 9, 10, 11, 20, 34, 35, 36, 37,
#                 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
#                 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
#                 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
#                 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85,
#                 86, 87, 88, 89, 90, 91, 92, 93, 94]
integer_cols = ['UNITID', 'Year', 'MAIN', 'NUMBRANCH', 'HIGHDEG', 'REGION', 'LOCALE', 'CCSIZSET', 'ADMCON7',
                'OPENADMP', 'won_One_year_ago', 'lost_One_year_ago', 'tied_One_year_ago', 'games_One_year_ago',
                'won_Two_years_ago', 'lost_Two_years_ago', 'tied_Two_years_ago', 'games_Two_years_ago',
                'won_Three_years_ago', 'lost_Three_years_ago' , 'tied_Three_years_ago', 'games_Three_years_ago',
                'won_Four_years_ago', 'lost_Four_years_ago', 'tied_Four_years_ago', 'games_Four_years_ago',
                'won_Five_years_ago', 'lost_Five_years_ago', 'tied_Five_years_ago', 'games_Five_years_ago',
                'won_Six_years_ago', 'lost_Six_years_ago', 'tied_Six_years_ago', 'games_Six_years_ago',
                'won_Seven_years_ago', 'lost_Seven_years_ago', 'tied_Seven_years_ago', 'games_Seven_years_ago',
                'won_Eight_years_ago', 'lost_Eight_years_ago', 'tied_Eight_years_ago', 'games_Eight_years_ago',
                'won_Nine_years_ago', 'lost_Nine_years_ago', 'tied_Nine_years_ago', 'games_Nine_years_ago',
                'won_Ten_years_ago', 'lost_Ten_years_ago', 'tied_Ten_years_ago', 'games_Ten_years_ago',
                'won_Eleven_year_ago', 'lost_Eleven_year_ago', 'tied_Eleven_year_ago', 'games_Eleven_year_ago',
                'won_Twelve_years_ago', 'lost_Twelve_years_ago', 'tied_Twelve_years_ago', 'games_Twelve_years_ago',
                'won_Thirteen_years_ago', 'lost_Thirteen_years_ago', 'tied_Thirteen_years_ago',
                'games_Thirteen_years_ago', 'won_Fourteen_years_ago', 'lost_Fourteen_years_ago',
                'tied_Fourteen_years_ago', 'games_Fourteen_years_ago', 'won_Fifteen_years_ago',
                'lost_Fifteen_years_ago', 'tied_Fifteen_years_ago', 'games_Fifteen_years_ago',
                'won_Sixteen_years_ago', 'lost_Sixteen_years_ago', 'tied_Sixteen_years_ago',
                'games_Sixteen_years_ago', 'won_Seventeen_years_ago', 'lost_Seventeen_years_ago',
                'tied_Seventeen_years_ago', 'games_Seventeen_years_ago', 'won_Eighteen_years_ago',
                'lost_Eighteen_years_ago', 'tied_Eighteen_years_ago', 'games_Eighteen_years_ago',
                'won_Nineteen_years_ago', 'lost_Nineteen_years_ago', 'tied_Nineteen_years_ago',
                'games_Nineteen_years_ago', 'won_Twenty_years_ago', 'lost_Twenty_years_ago',
                'tied_Twenty_years_ago', 'games_Twenty_years_ago']
# df.loc[:, integer_cols] = df.loc[:, integer_cols].astype("Int64")
for col in integer_cols:
    df[col] = df[col].astype("Int64")




####################
# Write final data #
####################

df.to_csv("data.csv", index = False)

