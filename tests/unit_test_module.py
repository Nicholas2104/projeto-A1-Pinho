# Verifying that visualization module dataframes are capable of discriminating between propperly formatted and no properly formatted datasets

import sys
import os
import unittest
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from src.visualizations import seasonal_alcohol
from src.visualizations import liscense_status_vis
from src.visualizations import crash_by_period_vis

class TestSeasonalAlcohol(unittest.TestCase):
    def test_data_processing(self):
        obj = seasonal_alcohol.SeasonalAlcoholColissions()
        df = pd.DataFrame({
        'A': np.random.randn(10),
        'B': np.random.randn(10)})
        obj.df = df
        self.assertEqual(obj.data_processing(),'Dataframe passed has inconsistent/unaccounted keys')

class TestLicenseStatusVis(unittest.TestCase):
    def test_get_borough_collision_composition(self):
        strange_obj = liscense_status_vis.LiscenseStatusTrends()
        df = pd.DataFrame({
        'A': np.random.randn(10),
        'B': np.random.randn(10)})
        strange_obj.collision_data = df
        self.assertEqual(strange_obj.get_borough_collision_composition(),'Dataframe passed has inconsistent/unaccounted keys')

class TestCrashByPeriodVis(unittest.TestCase):
    def test_get_contributing_factor_counts(self):
        strange_obj = crash_by_period_vis.CrashByPeriodTrends()
        accidents_data = pd.DataFrame({
        'A': np.random.randn(10),
        'B': np.random.randn(10)})
        strange_obj.accidents_data = accidents_data
        self.assertEqual(strange_obj.get_contributing_factor_counts(),'Dataframe passed has inconsistent/unaccounted keys')

unittest.main(verbosity=2)
