import hipotese_roger
import unittest
import numpy as np

class TestRemoveLines(unittest.TestCase):
    def test_is_not_none(self):
        self.assertIsNotNone(hipotese_roger.remove_lines(hipotese_roger.df_person_colision))

class TestrReplaceValues(unittest.TestCase):
    def test_is_not_none(self):
        self.assertIsNotNone(hipotese_roger.replace_values(hipotese_roger.df_person_colision))

class TestrDataProcessing(unittest.TestCase):
    def test_type_return(self):
        self.assertEqual(type(hipotese_roger.data_processing(hipotese_roger.positions, hipotese_roger.accident_count, hipotese_roger.df_person_colision)), np.ndarray)

class TestShowGraph(unittest.TestCase):
    def test_type_return(self):
        self.assertEqual(type(hipotese_roger.show_graph(hipotese_roger.positions, hipotese_roger.accident_count)), None)
