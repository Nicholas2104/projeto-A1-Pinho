import pandas as pd
import geopandas as gpd
import geodatasets
import matplotlib.pyplot as plt
import pgeocode

crashes = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Crashes.csv")
#persons = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Person_20240925.csv")
#vehicle = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Vehicles_20240925.csv")
path_to_data = geodatasets.get_path("nybb")
gdf = gpd.read_file(path_to_data)
gdf.plot()

#print(crashes.columns)
#print(crashes[["LONGITUDE","LATITUDE", "ZIP CODE"]])

print(crashes["ZIP CODE"].isna().sum())
#geodf = gpd.GeoDataFrame(crashes, geometry=gpd.points_from_xy(crashes["LONGITUDE"], crashes["LATITUDE"]))



#geodf.plot()



#plt.show()