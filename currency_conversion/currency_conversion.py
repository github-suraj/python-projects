'''
    Module file for Currency conversion
'''

from typing import Optional
from xml.etree import ElementTree
import requests
import pandas as pd

BASE_URL = "https://sdw-wsrest.ecb.europa.eu/service/data"

def get_data_from_rest_api(endpoint: str, identifier: str) -> str:
    '''
        Function to call REST API URL for an endpoint & identifier
        and return the response content
            Input:
                1. endpoint -> Endpoint for a service
                2. identifier -> Identifier for which data needed
            Output:
                string containing content of the rest api response
    '''
    url = f"{BASE_URL}/{endpoint}/{identifier}?detail=dataonly"
    response = requests.get(url)
    if response.status_code == 404:
        raise ValueError(f"InValid Identifier {identifier}")
    return response.content


def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    '''
        Function to fetch the yearly exchange rate data from the REST API URL
        and convert it to a pandas DataFrame
            Input:
                1. source currency code
                2. target currency code
            Output:
                dataframe containing two columns TIME_PERIOD and OBS_VALUE
    '''
    identifier = f"M.{source}.{target}.SP00.A"
    content = get_data_from_rest_api("EXR", identifier)
    etree_root = ElementTree.fromstring(content)

    namespaces = {
        'generic': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'
    }
    rows = []
    for item in etree_root.findall('.//generic:Obs', namespaces=namespaces):
        obsd = item.find('.//generic:ObsDimension', namespaces=namespaces)
        obsv = item.find('.//generic:ObsValue', namespaces=namespaces)
        rows.append((obsd.attrib.get('value'), obsv.attrib.get('value')))

    data_frame = pd.DataFrame(rows, columns=['TIME_PERIOD', 'OBS_VALUE'])
    data_frame['OBS_VALUE'] = data_frame['OBS_VALUE'].apply(lambda x: round(float(x), 6))
    data_frame.set_index('TIME_PERIOD', inplace=True)
    return data_frame


def get_raw_data(identifier: str) -> pd.DataFrame:
    '''
        Function to fetch the yearly currency data from the REST API URL
        and convert it to a pandas DataFrame
            Input:
                Identifier for which data needed
            Output:
                dataframe containing two columns TIME_PERIOD and OBS_VALUE
    '''
    content = get_data_from_rest_api("BP6", identifier)
    etree_root = ElementTree.fromstring(content)

    namespaces = {
        'generic': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'
    }
    rows = []
    for item in etree_root.findall('.//generic:Obs', namespaces=namespaces):
        obsd = item.find('.//generic:ObsDimension', namespaces=namespaces)
        obsv = item.find('.//generic:ObsValue', namespaces=namespaces)
        rows.append((obsd.attrib.get('value'), obsv.attrib.get('value')))

    data_frame = pd.DataFrame(rows, columns=['TIME_PERIOD', 'OBS_VALUE'])
    data_frame['OBS_VALUE'] = data_frame['OBS_VALUE'].apply(lambda x: round(float(x), 6))
    data_frame.set_index('TIME_PERIOD', inplace=True)
    return data_frame


def get_data(
    identifier: str,
    target_currency: Optional[str] = None
) -> pd.DataFrame:
    '''
        Function to fetch the yearly converted currency
            Input:
                1. Identifier to fetch yearly currency data
                2. Target Currency [Optional]
                        to convert the data from the source currency
                        (Ex.- EUR -> GBP)
                    If Not Provided
                        will retrun yearly currency data for Identifier
            Output:
                resulting dataframe with converted currency
                    (currency for Identifier * exchange rate)
    '''
    df_raw = get_raw_data(identifier)
    if target_currency:
        df_exr = get_exchange_rate(target_currency)
        df_raw *= df_exr
    df_raw.fillna(value=0, inplace=True)
    return df_raw


if __name__ == '__main__':
    IDENTIFIER = "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"
    CURRENCY_CODE = "GBP"
    print(get_data(IDENTIFIER, CURRENCY_CODE))
    print(get_data(IDENTIFIER))
