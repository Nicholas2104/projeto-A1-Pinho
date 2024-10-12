# Module that cleans and plot seasonal data related to drunk/drugged driving 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

crashes = pd.read_csv("dados/Motor_Vehicle_Collisions_-_Crashes.csv")

class SeasonalAlcoholColissions:
    """
    Used to filter and plot data related to drug usage or alcohol drinking along the months of the year
    """
    def __init__(self):
        self.df = crashes.copy(deep=True)

    def data_processing(self) -> pd.DataFrame:
        """Cleans and categorize accidents

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame with all the needed data to plot the figures
        """
        self.df['CRASH DATE'] = pd.to_datetime(self.df['CRASH DATE'], format="%m/%d/%Y")
        self.df['MONTH'] = self.df['CRASH DATE'].dt.month_name()
        
        drugs = ["Drugs (Illegal)", "Drugs (illegal)"]
        alcohol = ["Alcohol Involvement"]
        # Filtering the DataFrame with the useful information (whether the accident was caused by drug usage or alcohol usage)
        crashes_by_drugs = self.df[self.df["CONTRIBUTING FACTOR VEHICLE 1"].isin(drugs)] 
        crashes_by_alcohol = self.df[self.df["CONTRIBUTING FACTOR VEHICLE 1"].isin(alcohol)]
        # Grouping each DataFrame by month to analyse seasonal data
        crashes_by_drugs = crashes_by_drugs.groupby('MONTH').size().reset_index(name='Drug Accidents')
        crashes_by_alcohol = crashes_by_alcohol.groupby('MONTH').size().reset_index(name='Alcohol Accidents')
        # Merging both dataframes after counting accidents by month
        processed_df = crashes_by_drugs.merge(crashes_by_alcohol, on='MONTH', how="outer")
        processed_df = processed_df.dropna()  # Dropping rows without information
        
        month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        # Sort_values uses alphabetical order, pd.Categorical crates the correct month order
        processed_df['MONTH'] = pd.Categorical(processed_df['MONTH'], categories=month_order, ordered=True)
        processed_df = processed_df.sort_values(by='MONTH')
        return processed_df
    
    def graph_plotting(self):
        """Creates the visualization of accidents involving drugs/alcohol seasonally
        """
        df = self.data_processing()
        # Changes the structure of the Dataframe for Seaborn be able to plot it
        df = df.melt(id_vars=["MONTH"], 
                     value_vars=["Drug Accidents", "Alcohol Accidents"], 
                     var_name="Type", 
                     value_name="Count")
        
        f, ax = plt.subplots(figsize=(12, 6)) # Subplots returns a tuple, but we only need the axes values
        # Plotting the data
        sns.barplot(data=df, 
                    x="MONTH", 
                    y="Count", 
                    hue="Type", 
                    palette={"Drug Accidents": "r", "Alcohol Accidents": "g"})
        # Major style changes 
        ax.legend(ncol=1, loc="upper right", frameon=True)
        sns.despine(left=True, bottom=True)
        plt.xticks(rotation=45)
        plt.title("Number of Accidents by Month (Drugs and Alcohol)")
        plt.xlabel("Month")
        plt.ylabel("Number of Accidents")
        plt.show()