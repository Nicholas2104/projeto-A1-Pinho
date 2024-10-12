# NYC Car Accident Data Analysis

This repository contains code and visualizations used in a scientific article analyzing car accident data in New York City. The project aims to analyze five hypotheses regarding car accidents in the city:

1. **Which streets/intersections are the most dangerous for pedestrians and cyclists?**  
   Handled by: `cyc_ped_accidents_vis.py`

2. **Which car seat is the most dangerous in accidents where seat belts are not used?**  
   Handled by: `position_lethality_vis.py`

3. **Does the number of accidents caused by psychotropic substance use vary seasonally?**  
   Handled by: `seasonal_alcohol.py`

4. **What is the most frequent cause of accidents at different times of the day (morning, afternoon, evening, night)?**  
   Handled by: `crash_by_period_vis.py`

5. **Do neighborhoods with the highest number of collisions caused by unlicensed drivers or those with a permit have a higher proportion of accidents caused by driver inattention?**  
   Handled by: `liscense_status_vis.py`
# Getting Started

## Prerequisites

Make sure you have Python 3.13.0 installed. You will also need to install the required Python libraries and download the datasets.

To install all necessary libraries, first clone the repository:
``
git clone https://github.com/Nicholas2104/projeto-A1-Pinho.git
cd projeto-A1-Pinho
``
Then, install the required libraries:
``pip install -r requirements.txt``

# Downloading the Dataset

## Create 'dados' folder

You will need to download the dataset used for the analysis. Please download the dataset from the link below and place it in the 'dados' directory:

- [Motor Vehicle Collisions - Crashes](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data)
- [Motor Vehicle Collisions - Person](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu/about_data)
- [Motor Vehicle Collisions - Vehicles](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4/about_data)

In case of a file not found error, verify that the 'dados' folder is in the 'src' directory.

If the problem persists, rename files according to this example:
Motor_Vehicle_Collisions_-Crashes_20241010.csv -> Motor_Vehicle_Collisions-_Crashes.csv

# Running the Project

After installing the dependencies and downloading the dataset, you can run the project:

```bash
python main.py

