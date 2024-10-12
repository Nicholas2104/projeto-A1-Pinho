# Module documentation

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_person_colision = pd.read_csv("src/dados/Motor_Vehicle_Collisions_-_Person.csv")
class CarSeatDangers:
    def __init__(self):
        self.df = df_person_colision.copy(deep=True)
        self.serious = np.array(["Amputation", 
                                 "Paralysis", 
                                 "Severe Burn", 
                                 "Severe Lacerations", 
                                 "Severe Bleeding"])
        self.moderate = np.array(["Moderate Burn", 
                                  "Fracture - Dislocation", 
                                  "Internal", 
                                  "Fracture - Distorted - Dislocation"])
        self.minor = np.array(["Minor Burn", 
                               "Crush Injuries", 
                               "Concussion", 
                               "Whiplash", 
                               "Abrasion", 
                               "Contusion - Bruise", 
                               "Minor Bleeding", 
                               "None Visible", 
                               "Complaint of Pain", 
                               "Complaint of Pain or Nausea"])
        

    def remove_lines(self, df_person_colision: pd.DataFrame) -> pd.DataFrame:
        """
        A function that receives as a parameter a DataFrame with the data that will be used in the hypothesis and cleans it

        Parameters
        ----------
        df_person_colision : pandas.core.frame.DataFrame
            The DataFrame that contains all the data used in the hypothesis

        Returns
        -------
        self.df

        """
        try:
            # List of conditions for removal:
            removal_conditions = [
                df_person_colision['PERSON_TYPE'].isin(["Bicyclist", "Pedestrian"]),
                df_person_colision['SAFETY_EQUIPMENT'].isin(["Unknown", "Other"]),
                df_person_colision['COMPLAINT'].isin(["Does Not Apply", "Unknown"]),
                df_person_colision['POSITION_IN_VEHICLE'].isin(["Unknown", "Does Not Apply", "nan"])
            ]

            # Removing columns as per the above conditions and those that are null
            df_person_colision.drop(df_person_colision[np.any(removal_conditions, axis=0)].index, inplace=True)
            df_person_colision.dropna(subset=['POSITION_IN_VEHICLE'], inplace=True)

            # Selecting the lines that are null, that is, those cases in which safety equipment was not used
            df_person_colision = df_person_colision[df_person_colision['SAFETY_EQUIPMENT'].isna() == True]
            df_person_colision.reset_index(inplace=True)
            return df_person_colision
        except KeyError as error:
            print(f'{error.__class__}: Dataframe passed has inconsistent/unaccounted keys')
    def replace_values(self):
        """
        A function that replaces the values in the POSITION_IN_VEHICLE column with smaller values, so that they are easier to understand

        Parameters
        ----------
        df_removed_lines : pandas.core.frame.DataFrame
            The DataFrame that contains all the data used in the hypothesis, but with lines removed, according to the restrictions established in the function: remove_lines(df_person_colision)

        Returns
        -------
        df_person_colision

        """
        try:
            # replacement of values ​​in the POSITION_IN_VEHICLE column with smaller values
            replace_values = {
                'Driver': 'Driver',
                'Front passenger, if two or more persons, including the driver, are in the front seat': 'Front Passenger',
                'Right rear passenger or motorcycle sidecar passenger': 'Right Rear Passenger',
                'Left rear passenger, or rear passenger on a bicycle, motorcycle, snowmobile': 'Left Rear Passenger',
                'Any person in the rear of a station wagon, pick-up truck, all passengers on a bus, etc': 'Rear Passenger',
                'Middle rear seat, or passenger lying across a seat': 'Middle Rear Seat',
                'Middle front seat, or passenger lying across a seat': 'Middle Front Seat',
                'Riding/Hanging on Outside': 'Riding Outside',
                'If one person is seated on another person&apos;s lap': 'Sitting on Lap'
            }
            clean_df = self.remove_lines(self.df)
            # Replacing the values ​​in the POSITION_IN_VEHICLE column
            clean_df['POSITION_IN_VEHICLE'] = clean_df['POSITION_IN_VEHICLE'].replace(replace_values)
            
            return clean_df
        except KeyError as error:
            print(f'{error.__class__}: Dataframe passed has inconsistent/unaccounted keys')

    def data_processing(self):
        """
        A function that groups the data and prepares it for plotting on the graph

        Parameters
        ----------
        positions : list
            a list containing all possible seating positions in the vehicle
        
        accident_count : numpy.ndarray
            An array that contains only 0's, but will be filled according to the number of minor, medium or serious accidents that occurred
        
        replaced_lines : pandas.core.frame.DataFrame
            The DataFrame with rows removed and values changed
            
        Returns
        -------
        accident_count
        """
        try:
            self.positions = self.replace_values()['POSITION_IN_VEHICLE'].unique().tolist()
            accident_count = np.zeros((len(self.positions), 3)) 
            clean_df = self.replace_values()
            clean_df['position_idx'] = clean_df['POSITION_IN_VEHICLE'].map(lambda pos: self.positions.index(pos))

            # Iterating over all rows of the df_pessoas DataFrame
            for _, row in clean_df.iterrows(): # iterrows returns a tuple (index, data), but only data value is needed
                # Find the position index
                idx = self.positions.index(row['POSITION_IN_VEHICLE'])
                
                # If the person died, we will classify it as a serious accident as well
                if row['PERSON_INJURY'] == "Killed":
                    accident_count[idx][0] += 1      
                # Checking the type of injury and increment the correct count
                elif row['COMPLAINT'] in self.serious:
                    accident_count[idx][0] += 1
                elif row['COMPLAINT'] in self.moderate:
                    accident_count[idx][1] += 1
                elif row['COMPLAINT'] in self.minor:
                    accident_count[idx][2] += 1

            return np.array(accident_count)
        except KeyError as error:
            print(f'{error.__class__}: Dataframe passed has inconsistent/unaccounted keys')
    def show_graph(self):
        """
        A function that joins the data, modifies the graph and displays the graph

        Parameters
        ----------
        positions : list
            a list containing all possible seating positions in the vehicle
        
        accident_count : numpy.ndarray
            An array that contains only 0's, but will be filled according to the number of minor, medium or serious accidents that occurred
        
        Returns
        -------
        plt.show()
        
        """
        try:
            accident_count = self.data_processing()
            positions = self.replace_values()['POSITION_IN_VEHICLE'].unique().tolist()

            # Separating the 'accident_count' matrix into distinct columns in the DataFrame
            df = pd.DataFrame({
                'position_in_vehicle': positions,
                'Serious': np.log(accident_count[:, 0]),
                'Moderate': np.log(accident_count[:, 1]),
                'Minor': np.log(accident_count[:, 2])
            })

            # Putting 'position_in_vehicle' as index
            df.set_index('position_in_vehicle', inplace=True)

            # Plotting the Stacked Bar Chart
            df.plot(kind='bar', stacked=True)

            # Customizing the chart
            plt.title('Severity of Accidents by Seat Position (Without Using a Belt)')
            plt.xlabel('Seat Position')
            plt.ylabel('Logaritimic number of Accidents')
            plt.legend(title='Injury Severity')

            # Showing the graph
            plt.show()
        except KeyError as error:
            print(f'{error.__class__}: Dataframe passed has inconsistent/unaccounted keys')