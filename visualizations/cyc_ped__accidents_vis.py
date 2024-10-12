from data_cleansing import data_pre_processing

import geopandas.tools
import geopandas
import colorcet as cc
import hvplot.pandas
import geoviews # Although we don't explicitly use geoviews, it is used by holoviews in the background


class PedestriansAccidents:
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
