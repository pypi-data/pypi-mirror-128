# -*- coding: utf-8 -*-
"""Perform tests for dictmaker module."""
import logging
import unittest
import io
from pvlab.io.dictmaker import get_dict
from pvlab.io.dictmaker import get_dicts_list

logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.DEBUG)


class GetDictTest(unittest.TestCase):
    def test_int(self):
        logging.info('\nFunction: get_dict\nTesting case: integer data.\n')
        source = "readings:21\nminG:600\nrefG:1000"
        test = get_dict(io.StringIO(source), dtype='int', isStringIO=True)
        expected = {'readings': 21, 'minG': 600, 'refG': 1000}
        self.assertEqual(test, expected, 'incorrect')

    def test_float(self):
        logging.info('\nFunction: get_dict\nTesting case: float data.\n')
        source = "maxdev:0.02\noffsetthreshold:2.0"
        test = get_dict(io.StringIO(source), dtype='float', isStringIO=True)
        expected = {'maxdev': 0.02, 'offsetthreshold': 2.0}
        self.assertEqual(test, expected, 'incorrect')

    def test_str(self):
        logging.info('\nFunction: get_dict\nTesting case: str data.\n')
        source = "man.:'manufacturer'\nmod.:'model'\nsn.:'seriesnr'"
        test = get_dict(io.StringIO(source), dtype='str', isStringIO=True)
        expected = {'man.': 'manufacturer', 'mod.': 'model', 'sn.': 'seriesnr'}
        self.assertEqual(test, expected, 'incorrect')

    def test_noseparator(self):
        logging.info('\nFunction: get_dict\nTesting case: no sep warning.\n')
        source = "'noseparatorline'\nmod.:'model'\nsn.:'seriesnr'"
        test = get_dict(io.StringIO(source), dtype='str', isStringIO=True)
        expected = {}
        self.assertEqual(test, expected, 'incorrect')


class GetDictsList(unittest.TestCase):
    def test_floatandstring(self):
        message = '\nFunction: get_dicts_list\nCase: float and str data.\n'
        logging.info(message)
        data_1_float = "maxdev:0.02\noffsetthreeshold:2.0"
        source_1 = io.StringIO(data_1_float)
        data_2_str = "mode_refpyr:'voltage'\nmode_dut:'currentloop'"
        source_2 = io.StringIO(data_2_str)
        isstringio = ['True', 'True']  # io.StringIO type? defaults False
        test = get_dicts_list([source_1, source_2],
                              ['float', 'str'],
                              isStringIO=isstringio)
        expected = [{'maxdev': 0.02, 'offsetthreeshold': 2.0},
                    {'mode_refpyr': 'voltage', 'mode_dut': 'currentloop'}]
        self.assertEqual(test, expected, 'incorrect')


if __name__ == '__main__':
    unittest.main(verbosity=1)
