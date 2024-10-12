# Module reposnsible for produxing temporal analysis on contributing factors to a colision
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from data_cleansing.data_pre_processing import CrashByPeriodData

class CrashByPeriodTrends:
    """Class responsible for producing temporal analysis on CF of collisions 
    """
    def __init__(self):
        self.accidents_data = CrashByPeriodData().complete_crash_period_data

    def classify_time_of_day(self, row:pd.Series) -> str:
        """Classifies datetime values into groups

        Args:
            row pd.Series: accidents data

        Returns:
            str: class of date time
        """
        try:
            # we only care to analyse the hour of the crash time since this allows us to divide the day into seperate blocks of classifications
            hour = int(str(row['CRASH TIME']).split(':')[0])
            #dictionary mapping classifications to time
            classifying_dict = {'morning':[6,7,8,9,10,11], 
                        'mid_day':[12,13,14,15,16,17], 
                        'night': [18,19,20,21,22,23], 
                        'late_night': [0,1,2,3,4,5]} 
            for classification, times in classifying_dict.items(): # iterate over each classification
                # depending on the hour, if it fits into a certain classifications this is what we return
                if hour in times: 
                    return classification 
        except KeyError as error:
            print(f'{error.__class__}: Dataframe passed has inconsistent/unaccounted keys')
        except IndexError as error:
            print(f'{error.__class__}: Index passed is invalid - hour cannot be formatted')


    def get_contributing_factor_counts(self) -> pd.DataFrame:
        """collects dataframes of counts o each contributing factor at a specific time of day

        Returns:
            pd.DataFrame: 5 dataframes correspinding to the contributing factor of the vehicle involved
        """
        try:
            self.accidents_data['TIME OF DAY'] = self.accidents_data.apply(self.classify_time_of_day, axis=1) # classify each time of day
            # group data by Time of day, filtering by respective CF and counting the individual kinds of CF that occurredat that period of the day
            contributing_factor_counts_1 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 1']].value_counts().reset_index(name='Number of occurrences') 
            contributing_factor_counts_2 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 2']].value_counts().reset_index(name='Number of occurrences')
            contributing_factor_counts_3 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 3']].value_counts().reset_index(name='Number of occurrences')
            contributing_factor_counts_4 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 4']].value_counts().reset_index(name='Number of occurrences')
            contributing_factor_counts_5 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 5']].value_counts().reset_index(name='Number of occurrences')

            #return all 5 counts
            return contributing_factor_counts_1, contributing_factor_counts_2, contributing_factor_counts_3, contributing_factor_counts_4, contributing_factor_counts_5
        except KeyError as error:
            print(f'{error.__class__}: Dataframe passed has inconsistent/unaccounted keys')
            
    def related_to_factors(self) -> pd.DataFrame:
        """
        Compile contributing factor counts into a single DataFrame and identify the most common contributing factors at different times of day.

        Returns:
            pd.DataFrame: Compiled DataFrame with contributing factors and their occurrences by time of day.
        """
        try:
            cf1_count, cf2_count, cf3_count, cf4_count, cf5_count = self.get_contributing_factor_counts() # Get counts for contributing factors for each vehicle of all collisions
            # Rename columns for consistency and allow for concatenation
            cf1_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 1': 'CONTRIBUTING FACTOR'}, inplace=True)
            cf2_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 2': 'CONTRIBUTING FACTOR'}, inplace=True)
            cf3_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 3': 'CONTRIBUTING FACTOR'}, inplace=True)
            cf4_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 4': 'CONTRIBUTING FACTOR'}, inplace=True)
            cf5_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 5': 'CONTRIBUTING FACTOR'}, inplace=True)
            # Concatenate all counts into a single DataFrame
            concatenated_df = pd.concat([cf1_count, cf2_count, cf3_count, cf4_count, cf5_count], axis=0)
            summed_df = concatenated_df.groupby(by=['CONTRIBUTING FACTOR', 'TIME OF DAY'], as_index=False).sum() # Sum occurrences by contributing factor and time of day
            # Find the most common contributing factors at different times of day
            max_morning = summed_df[summed_df['TIME OF DAY'] == 'morning'].sort_values(by='Number of occurrences', ascending=False).head(5)['CONTRIBUTING FACTOR']
            max_mid_day = summed_df[summed_df['TIME OF DAY'] == 'mid_day'].sort_values(by='Number of occurrences', ascending=False).head(5)['CONTRIBUTING FACTOR']
            max_night = summed_df[summed_df['TIME OF DAY'] == 'night'].sort_values(by='Number of occurrences', ascending=False).head(5)['CONTRIBUTING FACTOR']
            max_late_night = summed_df[summed_df['TIME OF DAY'] == 'late_night'].sort_values(by='Number of occurrences', ascending=False).head(5)['CONTRIBUTING FACTOR']

            most_common_contributing_factors = list(set(max_morning.to_list() + max_mid_day.to_list() + max_night.to_list() + max_late_night.to_list())) # Compile the most common contributing factors into a list

            return summed_df, most_common_contributing_factors
        except KeyError as error:
            print(f'{error.__class__}: Dataframe passed has inconsistent/unaccounted keys')
    def crash_by_period_plot(self):
        """
        Plot a line graph of crash occurrences by time of day, with contributing factors.
        This method compiles crash data, filters it for significant contributing factors, and plots a line graph 
        showing the logarithmic number of occurrences by time of day, with different lines representing different 
        contributing factors.
        """
        try:
            plot_df, contributing_factors = self.related_to_factors() # Get the DataFrame and the list of contributing factors
            filtered_df = plot_df[plot_df['CONTRIBUTING FACTOR'].isin(contributing_factors)] # Filter the DataFrame for rows where the contributing factor is in the significant factors list
            filtered_df['Number of occurrences'] = np.log(filtered_df['Number of occurrences']) # Apply a log to number of occurrences to make visualizations more readable - not such exagerated gaps
            # Plot the line graph
            sns.lineplot(data=filtered_df, x='TIME OF DAY', y='Number of occurrences', hue='CONTRIBUTING FACTOR', markers='o')
            # Set the x and y labels, alongside eith legend and title
            plt.xlabel('Period of time')
            plt.ylabel('Logarithmic number of accidents')
            plt.legend(title='Contributing factor',loc='upper left')
            plt.xticks(rotation=45)
            plt.show()
        except KeyError as error:
            print(f'{error.__class__}: Dataframe passed has inconsistent/unaccounted keys')

