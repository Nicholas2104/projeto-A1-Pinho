NYC Car Accident Data Analysis

This repository contains code and visualizations used in a scientific article analyzing car accident data in New York City.

Getting Started

Prerequisites

Make sure you have Python 3.13.0 installed. You will also need to install the required Python libraries and download the datasets.
To install all necessary libraries, first clone the repository:
git clone https://github.com/Nicholas2104/projeto-A1-Pinho.git
cd projeto-A1-Pinho
Then, install the required libraries:
pip install -r requirements.txt

Downloading the Dataset

Create 'dados' folder
You will need to download the dataset used for the analysis. Please download the dataset from the link below and place it in 'dados' directory:
https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data
https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu/about_data
https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4/about_data
in case of file not found error verify that dados folder is in src directory
if problem persists rename files according to example:
Motor_Vehicle_Collisions_-_Crashes_20241010.csv -> Motor_Vehicle_Collisions_-_Crashes.csv

Running the Project

After installing the dependencies and downloading the dataset, you can run the project:
python main.py

