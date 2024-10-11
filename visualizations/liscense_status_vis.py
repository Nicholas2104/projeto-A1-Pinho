import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from data_cleansing.data_pre_processing import LiscenseStatusCollisionData

class LiscenseStatusTrends():
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
    def get_borough_liscense_composition(self) -> pd.DataFrame:
        borough_lisecense_composition = self.collsion_data.groupby(by='BOROUGH')['DRIVER_LICENSE_STATUS'].value_counts(normalize=True).reset_index(name='Perecentage of Collisions')
        return borough_lisecense_composition
    def pie_chart_borough_license_composition():
        """Produces a collection of piecharts, one representative of the total population and other individualizaed
        by Borough demonstrating the proportion of collisions involving liscensed, unliscensed, and permit drivers
        """
    def pie_chart_borough_collision_composition():
        """Produces a collection of piecharts, one representative of the total population and other individualizaed
        by Borough demonstrating the proportion of collisions caused by inattention/inexperience, other causes, or are undefined
        """
    def scatter_plot(self):
        """Produces scatter plot to demonstrate relationship between proportion of unliscened/permit drivers
        in a Borough and its number of insattention/inexperience motivated collisions
        """
            
c = LiscenseStatusTrends().scatter_plot()