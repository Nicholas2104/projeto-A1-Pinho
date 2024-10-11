import geopandas.tools
import geopandas
import colorcet as cc
import hvplot.pandas
import geoviews # Although we don't explicitly use geoviews, it is used by holoviews in the background
import seaborn
import pandas as pd
import matplotlib.pyplot as plt

# TODO correct the data_cleansing import by using the sys path
import sys
import os
sys.path.append(os.path.abspath('../data_cleansing'))
from data_cleansing import data_pre_processing


class PedestriansAccidents():
    """
    Used to filter and plot the data related to pedestrians and cyclists accidents based on known geographical data
    """
    def __init__(self):
        self.df = data_pre_processing.CrashLocationData().full_geo_data
        self.geodf = geopandas.GeoDataFrame(self.df, 
                                    # x is longitude and y is latitude, geopandas works very oddly
                                    geometry=geopandas.points_from_xy(self.df["LONGITUDE"], self.df["LATITUDE"]))
    
    def clean_df(self) -> geopandas.GeoDataFrame:
        """
        Filter by demographic involved and removes anomolous and invalid points

        Returns
        -------
        geopandas.GeoDataFrame
            A data frame with all relevant geographic data related to motorvehicle accidents
            which involve the injury or death of pedestrians and/or pedestrians
        """
        # Getting rid of all rows that doesn't have data about cyclists or pedestrians
        self.geodf.dropna(inplace=True, axis=0, subset=[
            'NUMBER OF PEDESTRIANS INJURED',
            'NUMBER OF PEDESTRIANS KILLED',
            'NUMBER OF CYCLIST INJURED',
            'NUMBER OF CYCLIST KILLED'], how='all')
        # Using a mask to clean all rows that doesn't involve cyclists or pedestrians
        mask = (self.geodf[[
            'NUMBER OF PEDESTRIANS INJURED',
            'NUMBER OF PEDESTRIANS KILLED',
            'NUMBER OF CYCLIST INJURED',
            'NUMBER OF CYCLIST KILLED']] != 0).any(axis=1)
        filtered_geodf = self.geodf[mask]
        filtered_geodf.reset_index(inplace=True, drop=True)
        filtered_geodf = filtered_geodf[~filtered_geodf.is_empty] # Cleaning points that doesn't have a geographic point to plot
        filtered_geodf = filtered_geodf[filtered_geodf['LATITUDE']!=0] # Cleaning some outliers that had Latitude=0
        return filtered_geodf

    def plot_accidents(self):
        """
        Plots all accidents involving pedestrians and/or cyclists across the city of new york
        """
        filtered_geodf = self.clean_df()
        hvplot.extension('bokeh') # HoloViews plots are ideal for large quantities of data
        plot =filtered_geodf.hvplot.points(x='LONGITUDE', 
                                        y='LATITUDE', 
                                        frame_width=800, 
                                        frame_height=800, 
                                        rasterize=True, 
                                        dynspread=True,
                                        cnorm='eq_hist', 
                                        cmap=cc.fire[100:], 
                                        bgcolor='black')
        hvplot.show(plot)


class PedestriansAccidentsGraphs():
    """
    Used to plot pedestrian and cyclists accidents with a bar chart
    """
    def __init__(self):
        self.crash_data = PedestriansAccidents().clean_df()
    
    def streets_accidents(self) -> geopandas.GeoDataFrame:
        # Filters the dataframe by dropping rows without street name
        self.crash_data = self.crash_data[self.crash_data['ON STREET NAME'].isna() == False]
        self.crash_data["PEDESTRIANS INCIDENTS"] = self.crash_data['NUMBER OF PEDESTRIANS INJURED'] + self.crash_data['NUMBER OF PEDESTRIANS KILLED']
        self.crash_data["CYCLISTS INCIDENTS"] = self.crash_data['NUMBER OF CYCLIST INJURED'] + self.crash_data['NUMBER OF CYCLIST KILLED']
        self.crash_data["GENERAL INCIDENTS"] = self.crash_data['PEDESTRIANS INCIDENTS'] + self.crash_data['CYCLISTS INCIDENTS']
        # Group each street and then sum the values of each selected column to count the accidents by victim
        incidents_by_street = self.crash_data.groupby(['ON STREET NAME'])[['ON STREET NAME','GENERAL INCIDENTS', 
                                                                'NUMBER OF CYCLIST INJURED',
                                                                'NUMBER OF CYCLIST KILLED',
                                                                'NUMBER OF PEDESTRIANS INJURED',
                                                                'NUMBER OF PEDESTRIANS KILLED']].sum()
        # Sort the incidents count in a descending order, so the first ones have more accidents
        incidents_by_street.sort_values(by='GENERAL INCIDENTS',ascending=False, inplace=True)
        return incidents_by_street

    def accidents_graphs_plot(self):
        """
        Plots a bar graph with the 5 streets with most accidents involving cyclists or pedestrians and what are their conditions
        """
        incidents_df = self.streets_accidents()
        incidents_df = incidents_df.head() # Take the first 5 streets with most incidents throgouth the years
        modified_df = pd.melt(incidents_df, id_vars='ON STREET NAME',var_name='victim class', value_name='number of victims')
        # Creates a bar graph to show the data
        g = seaborn.catplot(data=modified_df, 
                            x='ON STREET NAME',
                            y='number of victims', 
                            hue='victim class', 
                            kind='bar', 
                            height=5, 
                            aspect=1)
        g.set_xticklabels(labels=['Broadway', '3rd Av', '5th Av', '2nd Av', 'Atlantic Av']) # Labelling the x-axis
        g._legend.set_bbox_to_anchor((1, 0.75)) # Moving the legend for it not to overlap with the graph
        g._legend.set_frame_on(True)
        plt.tight_layout() # Ensure that all visualizations are correctly displayed
        plt.show()
        