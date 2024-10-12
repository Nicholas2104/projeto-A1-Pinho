import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from src.visualizations import seasonal_alcohol
from src.visualizations import position_lethality_vis
from src.visualizations import liscense_status_vis
from src.data_cleansing import data_pre_processing
from src.visualizations import cyc_ped__accidents_vis
from src.visualizations import crash_by_period_vis