import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Reading csv file
crashes = pd.read_csv("dados/Motor_Vehicle_Collisions_-_Crashes_20241008.csv")

# Converting the column to the type datetime
crashes["CRASH DATE"] = pd.to_datetime(crashes["CRASH DATE"], format="%m/%d/%Y")

# New column with the month name
crashes["MONTH"] = crashes["CRASH DATE"].dt.month_name()

# Filtering the accidents caused by alcohol and drugs
drugs = ["Drugs (Illegal)", "Drugs (illegal)"]
alcohol = ["Alcohol Involvement"]

crashes_by_drugs = crashes[crashes["CONTRIBUTING FACTOR VEHICLE 1"].isin(drugs)]
crashes_by_alcohol = crashes[crashes["CONTRIBUTING FACTOR VEHICLE 1"].isin(alcohol)]

# Grouping data by month and couting the number of accidents for each category
drug_accidents = crashes_by_drugs.groupby("MONTH").size().reset_index(name='Drug Accidents')
alcohol_accidents = crashes_by_alcohol.groupby("MONTH").size().reset_index(name='Alcohol Accidents')

# Merging the dataframes
merged = drug_accidents.merge(alcohol_accidents, on="MONTH", how="outer")
merged = merged.fillna(0)  # Replacing NaN values with 0

# Ordering the months
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
merged["MONTH"] = pd.Categorical(merged["MONTH"], categories=month_order, ordered=True)
merged = merged.sort_values(by="MONTH")

# Reorganizing the data to use in the bar plot
melted = pd.melt(merged, id_vars=["MONTH"], value_vars=["Drug Accidents", "Alcohol Accidents"], var_name="Type", value_name="Count")

# Plotting the data
f, ax = plt.subplots(figsize=(12, 6))

# Plotting the bar plot
sns.barplot(x="MONTH", y="Count", hue="Type", data=melted, palette={"Drug Accidents": "r", "Alcohol Accidents": "g"})

# Adjust the plot
ax.legend(ncol=1, loc="upper right", frameon=True)
sns.despine(left=True, bottom=True)
plt.xticks(rotation=45)
plt.title("Number of Accidents by Month (Drugs and Alcohol)")
plt.xlabel("Month")
plt.ylabel("Number of Accidents")
plt.show()