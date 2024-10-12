import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from data_cleansing.data_pre_processing import LiscenseStatusCollisionData

class LiscenseStatusTrends:
    def __init__(self):
        self.collision_data = LiscenseStatusCollisionData().complete_liscense_status_df 

    def classify_contributing_factor(self, row):
        """Classify contributing factors as inattention/inexperience related, unspecified, or other.
        
        Args:
            row (pd.Series): A row from the DataFrame containing contributing factor data.
        
        Returns:
            str: Classification of the contributing factor.
        """
        contributing_factor_1 = row['CONTRIBUTING_FACTOR_1']  
        contributing_factor_2 = row['CONTRIBUTING_FACTOR_2']  
        important_factors = ['Driver Inattention/Distraction', 'Driver Inexperience']  # Important factors list
        if contributing_factor_1 in important_factors or contributing_factor_2 in important_factors:
            return 'Inattention/Inexperience Related'  # Classify as inattention/inexperience related
        elif contributing_factor_1 == 'Unspecified' and contributing_factor_2 == 'Unspecified':
            return 'Unspecified'  # Classify as unspecified
        else:
            return 'Other'  # Classify as other

    def get_borough_collision_composition(self) -> pd.DataFrame:
        """Compute the composition of collisions by contributing factor class for each borough.
        
        Returns:
            pd.DataFrame: DataFrame with the percentage of collisions by contributing factor class for each borough.
        """
        # classify CF
        self.collision_data['CONTRIBUTING FACTOR CLASS'] = self.collision_data.apply(self.classify_contributing_factor, axis=1)  
        # calculate percentage of collisions caused by specific CF class
        borough_group_collisions = self.collision_data.groupby(by='BOROUGH')[['CONTRIBUTING FACTOR CLASS']].value_counts(normalize=True).reset_index(name='Percentage of Collisions')  
        return borough_group_collisions 

    def get_population_collision_composition(self) -> pd.DataFrame:
        """Compute the overall composition of collisions by contributing factor class for all of NYC.
        Returns:
            pd.DataFrame: DataFrame with the percentage of collisions by contributing factor class for all of NYC.
        """
        # classify each CF class
        self.collision_data['CONTRIBUTING FACTOR CLASS'] = self.collision_data.apply(self.classify_contributing_factor, axis=1)  
        # calculate percentage of collisions caused by specific CF class
        population_collision_composition = self.collision_data[['CONTRIBUTING FACTOR CLASS']].value_counts(normalize=True).reset_index(name='Percentage of Collisions')  
        population_collision_composition['BOROUGH'] = 'All NYC'  
        return population_collision_composition  

    def get_borough_liscense_composition(self) -> pd.DataFrame:
        """Compute the composition of collisions by driver license status for each borough.
        Returns:
            pd.DataFrame: DataFrame with the percentage of collisions by driver license status for each borough.
        """
        # return dataframe which breaksdown the composition of collisons in each borugh cause dby a specifica driver licesnse status
        borough_license_composition = self.collision_data.groupby(by='BOROUGH')['DRIVER_LICENSE_STATUS'].value_counts(normalize=True).reset_index(name='Percentage of Collisions')  
        return borough_license_composition  

    def get_population_liscense_composition(self) -> pd.DataFrame:
        """Compute the overall composition of collisions by driver license status for all of NYC.
        Returns:
            pd.DataFrame: DataFrame with the percentage of collisions by driver license status for all of NYC.
        """
        # produce percentage of all ollisions with a specific kind of driver license status
        population_license_composition = self.collision_data['DRIVER_LICENSE_STATUS'].value_counts(normalize=True).reset_index(name='Percentage of Collisions') 
        population_license_composition['BOROUGH'] = 'All NYC'  
        return population_license_composition  
    
    def pie_chart_borough_license_composition(self):
        """Produces a collection of piecharts, one representative of the total population and other individualizaed
        by Borough demonstrating the proportion of collisions involving liscensed, unliscensed, and permit drivers
        """
        borough_lisc_comp = self.get_borough_liscense_composition()
        population_lisc_comp = self.get_population_liscense_composition()

        complete_lisc_comp = pd.concat([population_lisc_comp,borough_lisc_comp]) # create dataframe of the license compposition of borough and population

        all_area_names = complete_lisc_comp['BOROUGH'].unique().tolist() # collection of all area names
        fig,axes = plt.subplots(nrows=2,ncols=3,figsize=(15,10)) # panel of all subplots

        for index,each_area in enumerate(all_area_names): # for each area plot in respective subplot a piechart of composition
            area_sample = complete_lisc_comp[complete_lisc_comp['BOROUGH'] == each_area]
            percentages = area_sample['Perecentage of Collisions']
            labels  = area_sample['DRIVER_LICENSE_STATUS']
            color_palette = plt.viridis()
            pie_ax = axes.flatten()[index] 
            pie_ax.pie(
                percentages, 
                labels=None, 
                colors=color_palette, 
                autopct='%1.1f%%', 
                startangle=25,
                pctdistance=1.15
            )
            pie_ax.set_title(each_area)   
        fig.legend(labels=labels, loc='center right', title="Driver License Status")         
        fig.tight_layout(rect=[0, 0, 0.85, 1])
        plt.show()

    def pie_chart_borough_collision_composition(self):
        """Produces a collection of piecharts, one representative of the total population and other individualizaed
        by Borough demonstrating the proportion of collisions caused by inattention/inexperience, other causes, or are undefined
        """
        borough_collision_comp = self.get_borough_collision_composition()
        population_collision_comp = self.get_population_collision_composition()

        complete_collision_comp = pd.concat([population_collision_comp,borough_collision_comp]) # df of collision ocmposition for Boroughs and all NYC
        all_area_names = complete_collision_comp['BOROUGH'].unique().tolist() # collection of all area names and thus all future areas to have a pie chart
        fig,axes = plt.subplots(nrows=2,ncols=3,figsize=(15,10)) # panel of all subplots

        for index,each_area in enumerate(all_area_names): # for each area plot in respective subplot a piechart of composition
            area_sample = complete_collision_comp[complete_collision_comp['BOROUGH'] == each_area]
            percentages = area_sample['Perecentage of Collisions']
            labels  = area_sample['CONTRIBUTING FACTOR CLASS']
            color_palette = plt.viridis()
            pie_ax = axes.flatten()[index] 
            pie_ax.pie(
                percentages, 
                labels=None, 
                colors=color_palette, 
                autopct='%1.1f%%', 
                startangle=25,
                pctdistance=1.15
            )
            pie_ax.set_title(each_area)   
        fig.legend(labels=labels, loc='center right', title="Contributing Factor Class")         
        fig.tight_layout(rect=[0, 0, 0.85, 1])
        plt.show()

    def scatter_plot(self):
        """Produces scatter plot to demonstrate relationship between proportion of unliscened/permit drivers
        in a Borough and its number of insattention/inexperience motivated collisions
        """
        borough_collision_comp = self.get_borough_collision_composition()
        borough_lisc_comp = self.get_borough_liscense_composition()
        
        # perecentage of collisions with CF as inattention/inexperience
        borough_inattention_collisions = borough_collision_comp[borough_collision_comp['CONTRIBUTING FACTOR CLASS'] == 'Inattention/Inexeprience Related']

        # dataframe of sepearte percentages of all collisions in a single borough cause by both unliscned and permit drivers
        filtered_borough_lisc_comp = borough_lisc_comp[borough_lisc_comp['DRIVER_LICENSE_STATUS'] != 'Licensed']
        # dataframe that claculates the total percetnage of both unliscensed and permit frivers in a borough
        sum_borough_lisc_comp = filtered_borough_lisc_comp.groupby(by='BOROUGH',as_index=False)['Perecentage of Collisions'].sum()
        
        x_axis_percentage_of_drivers = sum_borough_lisc_comp['Perecentage of Collisions']
        y_axis_percentage_of_collisions = borough_inattention_collisions['Perecentage of Collisions']
        borough_names = sum_borough_lisc_comp['BOROUGH']
        #creating scatter plot based on known percentages
        plt.scatter(x=x_axis_percentage_of_drivers, y=y_axis_percentage_of_collisions)

        # annotate each point on plot with borough name
        for index, borough in enumerate(borough_names):
            plt.annotate(borough, (x_axis_percentage_of_drivers.iloc[index], y_axis_percentage_of_collisions.iloc[index]), 
                        textcoords="offset points", xytext=(5,5), ha='center')

        # produce linear regression of points and plot trend line
        polyfit = np.polyfit(x_axis_percentage_of_drivers, y_axis_percentage_of_collisions, 1)
        first_degree_polynomial = np.poly1d(polyfit)
        plt.plot(x_axis_percentage_of_drivers,first_degree_polynomial(x_axis_percentage_of_drivers),'r')

        # show scatter plot
        plt.title('Percentage of Unlicensed/Permit Drivers vs Inattention/Inexperience Collisions')
        plt.xlabel('Percentage of Unlicensed/Permit Drivers',labelpad=2)
        plt.ylabel('Percentage of Inattention/Inexperience Collisions',labelpad=2)
        plt.tight_layout()
        plt.show()
