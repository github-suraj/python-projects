'''
    Module file for unit test cases for currency conversion
'''

import unittest
import pandas as pd
from currency_conversion import get_exchange_rate, get_raw_data, get_data

class TestCurrencyConversion(unittest.TestCase):
    '''
        Class for unit test cases
    '''
    identifier = "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"
    currency_code = "GBP"
    columns = ['TIME_PERIOD', 'OBS_VALUE']

    def test_get_raw_data_invalid_currency_identifier(self):
        '''
            Function to test Exception for invalid currency Identifier
                While calling get_raw_data function
        '''
        identifier = "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR1._T.T.N"
        with self.assertRaises(ValueError) as error:
            get_raw_data(identifier)
        self.assertEqual(str(error.exception), f'InValid Identifier {identifier}')

    def test_get_exchange_rate_invalid_currency_code(self):
        '''
            Function to test Exception for invalid currency code
                While calling get_exchange_rate function
        '''
        currency_code = "GBP1"
        with self.assertRaises(ValueError) as error:
            get_exchange_rate(currency_code)
        self.assertEqual(str(error.exception), f'InValid Identifier M.{currency_code}.EUR.SP00.A')

    def test_get_data_invalid_currency_identifier(self):
        '''
            Function to test Exception for invalid currency Identifier
                While calling get_data function for final dataframe
        '''
        identifier = "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR1._T.T.N"
        with self.assertRaises(ValueError) as error:
            get_data(identifier, self.currency_code)
        self.assertEqual(str(error.exception), f'InValid Identifier {identifier}')

    def test_get_data_invalid_currency_code(self):
        '''
            Function to test Exception for invalid currency code
                While calling get_data function for final dataframe
        '''
        currency_code = "GBP1"
        with self.assertRaises(ValueError) as error:
            get_data(self.identifier, currency_code)
        self.assertEqual(str(error.exception), f'InValid Identifier M.{currency_code}.EUR.SP00.A')

    def test_get_raw_data_valid_currency_identifier(self):
        '''
            Function to test get_raw_data for valid currency Identifier
        '''
        identifier = "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"
        dataframe = get_raw_data(identifier)
        self.assertTrue(isinstance(dataframe, pd.DataFrame))
        columns = dataframe.columns.to_list()
        self.assertEqual(columns, self.columns)

    def test_get_exchange_rate_valid_currency_code(self):
        '''
            Function to test get_exchange_rate for valid currency code
        '''
        currency_code = "GBP"
        dataframe = get_exchange_rate(currency_code)
        self.assertTrue(isinstance(dataframe, pd.DataFrame))
        columns = dataframe.columns.to_list()
        self.assertEqual(columns, self.columns)

    def test_get_data(self):
        '''
            Function to test get_data for both
                Currency Identifier & Currency Code
        '''
        dataframe = get_data(self.identifier, self.currency_code)
        self.assertTrue(isinstance(dataframe, pd.DataFrame))
        columns = dataframe.columns.to_list()
        self.assertEqual(columns, self.columns)

    def test_get_data_only_currency_identifier(self):
        '''
            Function to test get_data for only Currency Identifier
        '''
        dataframe = get_data(self.identifier)
        self.assertTrue(isinstance(dataframe, pd.DataFrame))
        columns = dataframe.columns.to_list()
        self.assertEqual(columns, self.columns)
