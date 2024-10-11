import pandas as pd
import pgeocode

crashes = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Crashes_20241001.csv")
#persons = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Person_20240925.csv")
#vehicle = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Vehicles_20240925.csv")


class CrashLocationData:
    def __init__(self):
        self.full_geo_data = self.get_geo_data()

    def get_geo_data(self) -> pd.DataFrame:
        """
        Cleans rows that doesn't have geographic data and fills the salvageable rows based on zipcode
        
        Returns
        -------
        pd.DataFrame
            A complete dataframe with all the geographic info available
        """
        self.geo_data_df = crashes.copy(deep=True)
        self.geo_data_df.dropna(inplace=True,axis=0,subset=["LATITUDE", "LONGITUDE", "ZIP CODE"],how='all') #Dropping unusable rows
        self.geo_data_df.reset_index(inplace=True)
        full_geo_data_df = self.fill_lat_long_by_zip()
        return full_geo_data_df

    # Some rows didn't have latitude or longitude values, but have a zipcode value, using this value we can fill the missing longitude and latitude
    def fill_lat_long_by_zip(self) -> pd.DataFrame:
        """
        Fills latitude and longitude of rows that only have zipcode info

        Returns
        -------
        pd.DataFrame
            A complete dataframe with all the geographic info available
        """
        data = self.geo_data_df
        data_with_zip = data[data["ZIP CODE"].isna() == False] # DataFrame of salvageable rows 
        missing_geo_df = data_with_zip[data_with_zip["LATITUDE"].isna() == True]
        nomi = pgeocode.Nominatim('us') 
        # lambda function takes all values before "." i.e.: original_zip = xxx.z new_zip = xxx
        formatted_postal_codes = missing_geo_df["ZIP CODE"].astype('str').apply(func=lambda row: row.split(".")[0]).to_list() # Reformatting to be in accordance to database postal codes
        coordinates = nomi.query_postal_code(formatted_postal_codes)
        coordinates.dropna(axis=0, inplace=True, subset=["latitude", "longitude"], how="any") # Dropping zip codes not recorded in database
        data.loc[coordinates.index, "LONGITUDE"] = coordinates["longitude"]
        data.loc[coordinates.index, "LATITUDE"] = coordinates["latitude"] 
        return data

class LiscenseStatusCollisionData:
    def __init__(self):
        self.complete_liscense_status_df = self.get_liscense_and_collision_info()
    def get_liscense_and_collision_info(self) -> pd.DataFrame:
        collision_data = crashes.copy(deep=True)[['COLLISION_ID','BOROUGH']]
        liscense_data_df = pd.read_csv("./dados/Motor_Vehicle_Collisions_-_Vehicles_20241001.csv")[['COLLISION_ID','DRIVER_LICENSE_STATUS','CONTRIBUTING_FACTOR_1','CONTRIBUTING_FACTOR_2']]
        liscense_data_df = pd.merge(liscense_data_df, collision_data, on='COLLISION_ID', how='left')
        liscense_data_df.dropna(how='any',subset=['DRIVER_LICENSE_STATUS','BOROUGH'],inplace=True)
        return liscense_data_df
    


