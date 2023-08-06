# -*- coding: utf-8 -*-
"""
Testing of module dfdicts.

Created on Thu Oct 14 12:07:18 2021

@author: josepedro
"""
import unittest
import pandas
from pvlab.dataframes.dfdicts import dict_to_df


class Dfdicts(unittest.TestCase):
    def test_result(self):
        """Check if fuction dict_to_df returns the right result."""
        dictionary = {'START_1': (2021, 5, 5, 8, 1, 0),
                      'END_1': (2021, 5, 6, 22, 52, 0)}
        columns = ['%Y', '%m', '%d', '%H', '%M', '%S']
        result = dict_to_df(dictionary, columns)
        expected = pandas.core.frame.DataFrame
        self.assertEqual(type(result), expected, 'incorrect')

    def test_exception(self):
        """Check if non-equal lengths of dictionary values
and columns generate a TypeException."""
        dictionary = {'START_1': (2021, 5, 5, 8, 1, 0),
                      'END_1': (2021, 5, 6, 22, 52, 0)}
        columns = ['%Y', '%m', '%d', '%H', '%M']
        with self.assertRaises(ValueError):
            dict_to_df(dictionary, columns)


if __name__ == '__main__':
    unittest.main(verbosity=1)
