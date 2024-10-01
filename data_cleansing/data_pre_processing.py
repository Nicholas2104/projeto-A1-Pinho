import geopandas.tools
import pandas as pd
import geopandas
import geodatasets
import matplotlib.pyplot as plt
import pgeocode

crashes = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Crashes.csv")
#persons = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Person_20240925.csv")
#vehicle = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Vehicles_20240925.csv")


class CrashLocationData():
    def __init__(self):
        self.full_geo_data = self.get_geo_data()
    def get_geo_data(self) -> pd.DataFrame:
        self.geo_data_df = crashes.copy(deep=True)
        self.geo_data_df.dropna(inplace=True,axis=0,subset=["LATITUDE", "LONGITUDE", "ZIP CODE"],thresh=3) #Dropping unusable rows
        self.geo_data_df.reset_index(inplace=True)
        full_geo_data_df = self.fill_lat_long_by_zip()
        return full_geo_data_df

    def fill_lat_long_by_zip(self) -> pd.DataFrame:
        data = self.geo_data_df
        data_with_zip = data[data["ZIP CODE"].isna() == False] # DataFrame of salvageable rows
        nomi = pgeocode.Nominatim('us') 
        # lambda function takes all values before "." i.e.: original_zip = xxx.z new_zip = xxx
        formatted_postal_codes = data_with_zip["ZIP CODE"].astype('str').apply(func=lambda row: row.split(".")[0]).to_list() # Reformatting to be in accordance to database postal codes
        coordinates = nomi.query_postal_code(formatted_postal_codes)
        coordinates.dropna(axis=0, inplace=True, subset=["latitude", "longitude"]) # Dropping zip codes not recorded in database
        data.loc[coordinates.index, "LONGITUDE"] = coordinates["longitude"]
        data.loc[coordinates.index, "LATITUDE"] = coordinates["latitude"]
        return data


    path_to_data = geodatasets.get_path("nybb")
    gdf = geopandas.read_file(path_to_data)
    gdf.plot()

    #geodf = gpd.GeoDataFrame(crashes, geometry=gpd.points_from_xy(crashes["LONGITUDE"], crashes["LATITUDE"]))
    #geodf.plot()
    #plt.show()