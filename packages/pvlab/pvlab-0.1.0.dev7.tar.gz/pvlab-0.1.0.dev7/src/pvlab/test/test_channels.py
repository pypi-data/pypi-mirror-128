# -*- coding: utf-8 -*-
"""Perform tests for module ``channels``."""

import logging
import unittest
from pvlab.io.channels import set_channels
from pvlab.io.channels import set_channels_grouped

logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.DEBUG)


class SetChannelsTest(unittest.TestCase):
    def test_normaluse(self):
        logging.info('\nFunction: set_channels\nTesting case: normal use.\n')
        numbers = [101, 115]
        names = ['(Time stamp)', '(VDC)']
        test = set_channels(numbers, names)
        expected = ['101(Time stamp)', '101(VDC)', '115(Time stamp)',
                    '115(VDC)']
        self.assertEqual(test, expected, 'incorrect')

    def test_nonumbers(self):
        logging.info('\nFunction: set_channels\nTesting case: no numbers.\n')
        numbers = []
        names = ['(Time stamp)', '(VDC)']
        test = set_channels(numbers, names)
        expected = ['(Time stamp)', '(VDC)']
        self.assertEqual(test, expected, 'incorrect')

    def test_nonames(self):
        logging.info('\nFunction: set_channels\nTesting case: no names.\n')
        numbers = [101, 115, 207]
        names = []
        test = set_channels(numbers, names)
        expected = ['101', '115', '207']
        self.assertEqual(test, expected, 'incorrect')

    def test_emptylists(self):
        logging.info('\nFunction: set_channels\nTesting case: empty lists.\n')
        numbers = []
        names = []
        with self.assertRaises(ValueError):
            set_channels(numbers, names)


class SetChannelsGroupedTest(unittest.TestCase):
    def test_normaluse(self):
        logging.info('\nFunction: set_channels_grouped\nCase: normal use.\n')
        numbers1 = [101]
        names1 = ['(Time stamp)', '(VDC)']
        numbers2 = [115]
        names2 = ['(Time stamp)', '(Temp)']
        test = set_channels_grouped([numbers1, numbers2], [names1, names2])
        expected = ['101(Time stamp)', '101(VDC)', '115(Time stamp)',
                    '115(Temp)']
        self.assertEqual(test, expected, 'incorrect')

    def test_nonequallength(self):
        logging.info('\nFunction: set_channels_grouped.')
        logging.info('\nTest case: no equal length.\n')
        numbers1 = [101]
        names1 = ['(Time stamp)', '(VDC)']
        numbers2 = [115]
        names2 = ['(Time stamp)', '(Temp)']
        test = set_channels_grouped([numbers1, numbers2, []], [names1, names2])
        expected = ['101(Time stamp)', '101(VDC)',
                    '115(Time stamp)', '115(Temp)']
        self.assertEqual(test, expected, 'incorrect')

    def test_emptylistgroups(self):
        logging.info('\nFunction: set_channels_grouped.')
        logging.info('\nTest case: groups of empty lists.\n')
        with self.assertRaises(ValueError):
            set_channels_grouped([[], []], [[], []])


if __name__ == '__main__':
    unittest.main(verbosity=1)
