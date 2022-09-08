'''
    Module file for Transactions Aggregations
'''

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


def get_transactions(identifier: str) -> pd.DataFrame:
    '''
        Function to fetch the yearly transactions details from the REST API URL
        and convert it to a pandas DataFrame
            Input:
                Identifier for which transactions details needed
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
    data_frame.insert(0, 'IDENTIFIER', identifier)
    return data_frame

if __name__ == '__main__':
    IDENTIFIER = "Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N"
    dataframe = get_transactions(IDENTIFIER)
    print(dataframe)
