import sys
import urllib.request

def check_internet_connection():
    try:
        urllib.request.urlopen('http://google.com')
    except Exception as err:
        print('No Internet Connection!')
        sys.exit()
