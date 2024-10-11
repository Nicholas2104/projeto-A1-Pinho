import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from data_cleansing.data_pre_processing import LiscenseStatusCollisionData

class LiscenseStatusTrends:
    def __init__(self):
        self.collsion_data = LiscenseStatusCollisionData().complete_liscense_status_df
    def classify_contributing_factor(self,row):
        contributing_factor_1 = row['CONTRIBUTING_FACTOR_1']
        contributing_factor_2 = row['CONTRIBUTING_FACTOR_2']
        important_factors = ['Driver Inattention/Distraction','Driver Inexperience']
        if contributing_factor_1 in important_factors or contributing_factor_2 in important_factors:
            return 'Inattention/Inexeprience Related'
        elif contributing_factor_1 == 'Unspecified' and contributing_factor_2 == 'Unspecified':
            return 'Unspecified'
        else:
            return 'Other'
        
    def get_borough_collision_composition(self) -> pd.DataFrame:
        self.collsion_data['CONTRIBUTING FACTOR CLASS'] = self.collsion_data.apply(self.classify_contributing_factor,axis=1)
        borough_group_collisions = self.collsion_data.groupby(by='BOROUGH')[['CONTRIBUTING FACTOR CLASS']].value_counts(normalize = True).reset_index(name='Perecentage of Collisions')
        return borough_group_collisions
    
    def get_population_collision_composition(self) -> pd.DataFrame:
        self.collsion_data['CONTRIBUTING FACTOR CLASS'] = self.collsion_data.apply(self.classify_contributing_factor,axis=1)
        population_collision_composition = self.collsion_data[['CONTRIBUTING FACTOR CLASS']].value_counts(normalize = True).reset_index(name='Perecentage of Collisions')
        population_collision_composition['BOROUGH'] = 'All NYC'
        return population_collision_composition
    
    def get_borough_liscense_composition(self) -> pd.DataFrame:
        borough_lisecense_composition = self.collsion_data.groupby(by='BOROUGH')['DRIVER_LICENSE_STATUS'].value_counts(normalize=True).reset_index(name='Perecentage of Collisions')
        return borough_lisecense_composition
    
    def get_population_liscense_composition(self) -> pd.DataFrame:
        population_lisecense_composition = self.collsion_data['DRIVER_LICENSE_STATUS'].value_counts(normalize=True).reset_index(name='Perecentage of Collisions')
        population_lisecense_composition['BOROUGH'] = 'All NYC'
        return population_lisecense_composition
    
    def pie_chart_borough_license_composition(self):
        """Produces a collection of piecharts, one representative of the total population and other individualizaed
        by Borough demonstrating the proportion of collisions involving liscensed, unliscensed, and permit drivers
        """
        borough_lisc_comp = self.get_borough_liscense_composition()
        population_lisc_comp = self.get_population_liscense_composition()

        complete_lisc_comp = pd.concat([population_lisc_comp,borough_lisc_comp])

        all_area_names = complete_lisc_comp['BOROUGH'].unique().tolist()
        fig,axes = plt.subplots(nrows=2,ncols=3,figsize=(15,10))

        for index,each_area in enumerate(all_area_names):
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

        complete_collision_comp = pd.concat([population_collision_comp,borough_collision_comp])
        all_area_names = complete_collision_comp['BOROUGH'].unique().tolist()
        fig,axes = plt.subplots(nrows=2,ncols=3,figsize=(15,10))

        for index,each_area in enumerate(all_area_names):
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
        
        borough_inattention_collisions = borough_collision_comp[borough_collision_comp['ONTRIBUTING FACTOR CLASS'] == 'Inattention/Inexeprience Related']
        

        print(borough_lisc_comp)

c = LiscenseStatusTrends().scatter_plot()