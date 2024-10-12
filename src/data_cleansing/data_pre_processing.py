# MODULE RESPONSIBLE FOR CLEANSING AND SELECTING DATA FOR LATER VISUALIZATION
import pandas as pd
import pgeocode

try:
    crashes = pd.read_csv("src/dados/Motor_Vehicle_Collisions_-_Crashes.csv") # collect info from crashes csv to df 
    vehicle = pd.read_csv("src/dados/Motor_Vehicle_Collisions_-_Vehicles.csv") # collect info from vehicles csv to df
except FileNotFoundError as error:
    return 'File path passed for data sources is invalid"
class CrashLocationData:
    """Class responsible for creating a dataframe of collisions with complete geographical data
    """
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
        try:
            geo_data_df = crashes.copy(deep=True) # initially we make a copy of the large unfiltered dataframe
            geo_data_df.dropna(inplace=True,axis=0,subset=["LATITUDE", "LONGITUDE", "ZIP CODE"],how='all') # we then drop all unusable rows
            geo_data_df.reset_index(inplace=True) # after drop we reset index to make dataframe more manageable and allow for fill of empty calues
            full_geo_data_df = self.fill_lat_long_by_zip(geo_data_df) # fill empty geographical data through aproximations made by zip-code
            return full_geo_data_df # return dataframe of collisions with complete geographical data
        except KeyError as error:
            return 'Dataframe passed has inconsistent/unaccounted keys'
            

    def fill_lat_long_by_zip(self,data:pd.DataFrame) -> pd.DataFrame:
        """
        Fills latitude and longitude of rows that only have zipcode info

        Returns
        -------
        pd.DataFrame
            A complete dataframe with all the geographic info available
        """
        try:
            data_with_zip = data[data["ZIP CODE"].isna() == False] # DataFrame of salvageable rows 
            missing_geo_df = data_with_zip[data_with_zip["LATITUDE"].isna() == True] # select all rows with missing geographical data
            nomi = pgeocode.Nominatim('us') # realtional database of american zipcodes and latitude and longitude

            # lambda function takes all values before "." i.e.: original_zip = xxx.z new_zip = xxx
            formatted_postal_codes = missing_geo_df["ZIP CODE"].astype('str').apply(func=lambda row: row.split(".")[0]).to_list() # Reformatting to be in accordance to database postal codes

            coordinates = nomi.query_postal_code(formatted_postal_codes) # map all formatted postal codes to their respective lat/lon
            coordinates.dropna(axis=0, inplace=True, subset=["latitude", "longitude"], how="any") # Dropping zip codes not recorded in database
            data.loc[coordinates.index, "LONGITUDE"] = coordinates["longitude"] # fill missing lat
            data.loc[coordinates.index, "LATITUDE"] = coordinates["latitude"] # fill missing lon
            return data # return completed dataset
        except TypeError as error:
            return 'Paramater passed was not a pandas.DataFrame'
        except KeyError as error:
            return 'Dataframe passed has inconsistent/unaccounted keys'
class LiscenseStatusCollisionData:
    """Class responsible for cleaning a selecting collision data to be used to asses composition and distribuition of 
    specfic collisions by Driver liscense status of those involved
    """
    def __init__(self):
        self.complete_liscense_status_df = self.get_liscense_and_collision_info()
    def get_liscense_and_collision_info(self) -> pd.DataFrame:
        """cleans crashes & vehicle df mergin both and segments into 4 essential collumns

        Returns:
            pd.DataFrame: Dataframe of collisions with driver liscese status CF1 & CF2, with no NaN values
        """
        try:
            collision_data = crashes.copy(deep=True)[['COLLISION_ID','BOROUGH']] # select unique key and location info from crashes
            vehicle_data = vehicle.copy(deep=True) # copy all vehicle df
            liscense_data_df = vehicle_data[['COLLISION_ID','DRIVER_LICENSE_STATUS','CONTRIBUTING_FACTOR_1','CONTRIBUTING_FACTOR_2']] # Select 4 essential collumns from vehicle data
            liscense_data_df = pd.merge(liscense_data_df, collision_data, on='COLLISION_ID', how='left') # merge liscense data and collision data give unique key identifies COLLISION ID to be able to identify each collision by Borough
            liscense_data_df.dropna(how='any',subset=['DRIVER_LICENSE_STATUS','BOROUGH'],inplace=True) # rows without info on borough cannot be used
            return liscense_data_df
        except KeyError as error:
            return 'Dataframe passed has inconsistent/unaccounted keys'
    
class CrashByPeriodData:
    """Class responsible for creating and cleaning dataframe with all accident data encompassing all CF and the time of the collision
    """
    def __init__(self):
        self.complete_crash_period_data = self.get_crash_data()
    def get_crash_data(self) -> pd.DataFrame:
        try:
            accidents_data = crashes.copy(deep=True)[[
                                                    'CRASH TIME', 
                                                    'CONTRIBUTING FACTOR VEHICLE 1',
                                                    'CONTRIBUTING FACTOR VEHICLE 2',
                                                    'CONTRIBUTING FACTOR VEHICLE 3',
                                                    'CONTRIBUTING FACTOR VEHICLE 4',
                                                    'CONTRIBUTING FACTOR VEHICLE 5']] # collect all contributiing factor and the time they happened
            accidents_data.dropna(how='any', subset=['CRASH TIME', 'CONTRIBUTING FACTOR VEHICLE 1'], inplace=True) #Any row without date-time cannot be anlysed - if CFV 1 doesn't exist, others don't too'

            # ignore all rows with unspecified CF
            accidents_data = accidents_data[accidents_data['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified']
            accidents_data = accidents_data[accidents_data['CONTRIBUTING FACTOR VEHICLE 2'] != 'Unspecified']
            accidents_data = accidents_data[accidents_data['CONTRIBUTING FACTOR VEHICLE 3'] != 'Unspecified']
            accidents_data = accidents_data[accidents_data['CONTRIBUTING FACTOR VEHICLE 4'] != 'Unspecified']
            accidents_data = accidents_data[accidents_data['CONTRIBUTING FACTOR VEHICLE 5'] != 'Unspecified']
            
            return accidents_data
        except KeyError as error:
            return 'Dataframe passed has inconsistent/unaccounted keys'
