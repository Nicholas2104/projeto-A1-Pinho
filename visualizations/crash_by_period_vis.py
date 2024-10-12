import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from data_cleansing.data_pre_processing import CrashByPeriodData

class CrashByPeriodTrends:
    def __init__(self):
        self.accidents_data = CrashByPeriodData().complete_crash_period_data

    def classify_time_of_day(self, row):
        hour = int(str(row['CRASH TIME']).split(':')[0])
        classifying_dict = {'morning':[6,7,8,9,10,11], 
                      'mid_day':[12,13,14,15,16,17], 
                      'night': [18,19,20,21,22,23], 
                      'late_night': [0,1,2,3,4,5]}
        for key, value in classifying_dict.items():
            if hour in value:
                return key 


    def get_contributing_factor_counts(self) -> pd.DataFrame:
        self.accidents_data['TIME OF DAY'] = self.accidents_data.apply(self.classify_time_of_day, axis=1)
        contributing_factor_counts_1 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 1']].value_counts().reset_index(name='Number of occurences')
        contributing_factor_counts_2 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 2']].value_counts().reset_index(name='Number of occurences')
        contributing_factor_counts_3 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 3']].value_counts().reset_index(name='Number of occurences')
        contributing_factor_counts_4 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 4']].value_counts().reset_index(name='Number of occurences')
        contributing_factor_counts_5 = self.accidents_data.groupby(by='TIME OF DAY')[['CONTRIBUTING FACTOR VEHICLE 5']].value_counts().reset_index(name='Number of occurences')

        return contributing_factor_counts_1, contributing_factor_counts_2, contributing_factor_counts_3, contributing_factor_counts_4, contributing_factor_counts_5

    def related_to_factors(self) -> pd.DataFrame:
        cf1_count, cf2_count, cf3_count, cf4_count, cf5_count = self.get_contributing_factor_counts()
        cf1_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 1': 'CONTRIBUTING FACTOR'}, inplace=True)
        cf2_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 2': 'CONTRIBUTING FACTOR'}, inplace=True)
        cf3_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 3': 'CONTRIBUTING FACTOR'}, inplace=True)
        cf4_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 4': 'CONTRIBUTING FACTOR'}, inplace=True)
        cf5_count.rename(columns={'CONTRIBUTING FACTOR VEHICLE 5': 'CONTRIBUTING FACTOR'}, inplace=True)

        concatenated_df = pd.concat([cf1_count, cf2_count, cf3_count, cf4_count, cf5_count], axis=0)
        summed_df = concatenated_df.groupby(by=['CONTRIBUTING FACTOR', 'TIME OF DAY'], as_index=False).sum()
        max_morning = summed_df[summed_df['TIME OF DAY'] == 'morning'].sort_values(by='Number of occurences', ascending=False).head(5)['CONTRIBUTING FACTOR']
        max_mid_day = summed_df[summed_df['TIME OF DAY'] == 'mid_day'].sort_values(by='Number of occurences', ascending=False).head(5)['CONTRIBUTING FACTOR']
        max_night = summed_df[summed_df['TIME OF DAY'] == 'night'].sort_values(by='Number of occurences', ascending=False).head(5)['CONTRIBUTING FACTOR']
        max_late_night = summed_df[summed_df['TIME OF DAY'] == 'late_night'].sort_values(by='Number of occurences', ascending=False).head(5)['CONTRIBUTING FACTOR']
        
        most_common_contributing_factors = list(set(max_morning.to_list() + max_mid_day.to_list() + max_night.to_list() + max_late_night.to_list()))

        return summed_df, most_common_contributing_factors

    def crash_by_period_plot(self):
        plot_df, contributing_factors = self.related_to_factors()
        filtered_df = plot_df[plot_df['CONTRIBUTING FACTOR'].isin(contributing_factors)]
        filtered_df['Number of occurences'] = np.log(filtered_df['Number of occurences'])
        sns.lineplot(data=filtered_df, x='TIME OF DAY', y='Number of occurences', hue='CONTRIBUTING FACTOR', markers='o')
        plt.xlabel('Period of time')
        plt.ylabel('Logaritmic number of accidents')
        plt.legend(title='Contributing factor')
        plt.xticks(rotation=45)
        plt.show()
