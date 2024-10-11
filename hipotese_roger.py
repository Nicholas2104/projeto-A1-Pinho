import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# table that contains details for people involved in the crash where each row represents a person
df_person_colision = pd.read_csv("pessoas_colisoes.csv")

"""
My hypothesis:
Which car seat is most dangerous in accidents where a seat belt is not used?

Points to analyze:
- Position in which the passenger was
- If you were wearing a seat belt
- Severity of the accident 

columns that I will use:
df_person_colision:

-PERSON_TYPE
-PERSON_INJURY
-SAFETY_EQUIPMENT
-COMPLAINT      
-POSITION_IN_VEHICLE  

filters:

-Select only accidents only accidents in which the columns SAFETY_EQUIPMENT, COMPLAINT and POSITION_IN_VEHICLE have known values
-Select only accidents in which seat belts were not used
-Remove cyclists and pedestrians
-Select the lines that are null, that is, those cases in which safety equipment was not used
"""


def remove_lines(df_person_colision):
    """
    A function that receives as a parameter a DataFrame with the data that will be used in the hypothesis and cleans it

    Parameters
    ----------
    df_person_colision : pandas.core.frame.DataFrame
        The DataFrame that contains all the data used in the hypothesis

    Returns
    -------
    df_person_colision

    """
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
    df_person_colision = df_person_colision[df_person_colision['SAFETY_EQUIPMENT'].isna()]

    return df_person_colision

def replace_values(df_person_colision):
    """
    A function that replaces the values ​​in the POSITION_IN_VEHICLE column with smaller values, so that they are easier to understand

    Parameters
    ----------
    df_removed_lines : pandas.core.frame.DataFrame
        The DataFrame that contains all the data used in the hypothesis, but with lines removed, according to the restrictions established in the function: remove_lines(df_person_colision)

    Returns
    -------
    df_person_colision

    """
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

    # Replacing the values ​​in the POSITION_IN_VEHICLE column
    df_person_colision['POSITION_IN_VEHICLE'] = df_person_colision['POSITION_IN_VEHICLE'].replace(replace_values)

    return df_person_colision

def data_processing(positions, accident_count, df_person_colision):
    """
    A function that groups the data and prepares it for plotting on the graph

    Parameters
    ----------
    positions : list
        a list containing all possible seating positions in the vehicle
    
    accident_count : numpy.ndarray
        An array that contains only 0's, but will be filled according to the number of minor, medium or serious accidents that occurred
    
    replaced_lines : pandas.core.frame.DataFrame
        The DataFrame with rows removed and values ​​changed
         
    Returns
    -------
    accident_count

    """
    # Iterating over all rows of the df_pessoas DataFrame
    for index, row in df_person_colision.iterrows():

        # Find the position index
        idx = positions.index(row['POSITION_IN_VEHICLE'])
        
        # If the person died, we will classify it as a serious accident as well
        if row['PERSON_INJURY'] == "Killed":
            accident_count[idx][0] += 1 
        
        # Checking the type of injury and increment the correct count
        elif row['COMPLAINT'] in serious:
            accident_count[idx][0] += 1
        elif row['COMPLAINT'] in moderate:
            accident_count[idx][1] += 1
        elif row['COMPLAINT'] in minor:
            accident_count[idx][2] += 1

    return accident_count

def show_graph(positions, accident_count):
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
    plt.ylabel('Number of Accidents')
    plt.legend(title='Injury Severity')

    # Showing the graph
    return plt.show()


# Declaration of variables and Calling the functions

# Division of accident types according to severity (Minor, Moderate, Serious):

# Injuries in this category have significant consequences and can permanently alter the individual's life. They often require complex and prolonged treatments. Examples include amputations and paralysis, which can lead to lifelong disability and necessitate extensive rehabilitation.
serious = np.array(["Amputation", "Paralysis", "Severe Burn", "Severe Lacerations", "Severe Bleeding"])

# These injuries are not fatal but can still cause intense pain and may require medical intervention. While they are less severe than critical injuries, they still pose a significant risk to the individual's health. For instance, fractures and moderate burns may require surgical treatment and recovery time, impacting the individual's daily life
moderate = np.array(["Moderate Burn", "Fracture - Dislocation", "Internal", "Fracture - Distorted - Dislocation"])

# Minor injuries are generally treatable at home or do not require extensive medical care. While they may cause discomfort, they are unlikely to result in long-term disability. Injuries such as minor burns and abrasions typically heal quickly and can often be managed without professional medical assistance
minor = np.array(["Minor Burn", "Crush Injuries", "Concussion", "Whiplash", "Abrasion", "Contusion - Bruise", "Minor Bleeding", "None Visible", "Complaint of Pain", "Complaint of Pain or Nausea"])

df_person_colision = remove_lines(df_person_colision)

df_person_colision = replace_values(df_person_colision)
# Putting in a list all the possible positions in which people were in the vehicle
positions = df_person_colision['POSITION_IN_VEHICLE'].unique().tolist()

# 3 columns with 0's (minor, moderate and severe) for each vehicle position
accident_count = np.zeros((len(positions), 3)) 

data_processing(positions, accident_count, df_person_colision)

print(show_graph(positions, accident_count))