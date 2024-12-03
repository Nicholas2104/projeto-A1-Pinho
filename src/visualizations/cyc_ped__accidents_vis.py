# Module that creates visualizations about cyclist and pedestrians accidents in New York City

import geopandas.tools
import geopandas
import colorcet as cc
import hvplot.pandas
import geoviews # Although we don't explicitly use geoviews, it is used by holoviews in the background
import seaborn
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx


#import sys
#import os
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

#from data_cleansing import data_pre_processing

class AEDVCARAIO:
    def __init__(self):
        data = pd.DataFrame(columns=['GENERAL INCIDENTS'], data=[42, 37, 32, 30, 29])
        geometry = [Point(-73.989842, 40.757277),
                    Point(-73.937445, 40.804389),
                    Point(-73.931167, 40.668834),
                    Point(-73.956279, 40.813389),
                    Point(-73.990639, 40.751)]
        self.df = geopandas.GeoDataFrame(data=data, geometry=geometry, crs="EPSG:4326")
        self.df = self.df.to_crs(epsg=3857)
    

    def plot(self):
        fig, ax = plt.subplots(figsize=(120,120))
        self.df.plot(ax=ax, color='blue', markersize=1)
        self.df.plot(
        ax=ax,
        markersize=self.df['GENERAL INCIDENTS'] * 10,  # Scale the bubbles
        color='orange',
        alpha=0.7,
        edgecolor='black'
        )
        ctx.add_basemap(ax,source=ctx.providers.OpenStreetMap.Mapnik)

        ax.axis('off')
        ax.autoscale()

        plt.show()

    def lalala(self):
        return self.df
    
test = AEDVCARAIO()
test.plot()