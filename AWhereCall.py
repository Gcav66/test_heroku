import json
from requests_oauthlib import OAuth2
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
import pandas as pd

class AWhereCall(object):
    """Use this joint to get you some weather data"""
    
    field_url = 'https://api.awhere.com/v2/fields'
    body = {
    "id": "", #gus_
    "farmId": "", #senegal
    "centerPoint": {
        "latitude": "", #14.69,
        "longitude": "", #17.45
        }
    }
    
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        
    def fetch_token(self):
        client = BackendApplicationClient(client_id = self.key)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://api.awhere.com/oauth/token', client_id=self.key, client_secret=self.secret)
        client = OAuth2Session(self.key, token=token)
        return client
    
    def get_fields(self):
        session = self.fetch_token()
        try:
            lst = session.get(self.field_url)
        except TokenExpiredError as e:
            session = x.fetch_token()
            lst = session.get(self.field_url)
        out = lst.json()
        ids = [x['id'] for x in out['fields']]
        return ids
    
    def create_field(self, field_lat, field_long, field_id, farm_id):
        """Lat, Long, a unique id for your field, and an id for the farm"""
        session = self.fetch_token()
        self.body['id'] = field_id
        self.body['farmId'] = farm_id
        self.body['centerPoint']['latitude'] = field_lat
        self.body['centerPoint']['longitude'] = field_long
        out = session.post(self.field_url, json=self.body)
        return out
    
    def get_observations(self, field_id):
        session = self.fetch_token()
        obsv_url = r'https://api.awhere.com/v2/weather/fields/' + field_id + '/observations'
        obsvs = session.get(obsv_url)
        return obsvs.json()
    
    def get_forecasts(self, field_id):
        session = self.fetch_token()
        frcst_url = r'https://api.awhere.com/v2/weather/fields/' + field_id + '/forecasts'
        frcsts = session.get(frcst_url)
        return frcsts.json()
    
    def flatten_observations(self, obsvs):
        obsvData = []
        for obsv in obsvs['observations']:
            myRow = {}
            myRow = {'date': obsv['date'],
                     'precipitation': obsv['precipitation']['amount'],
                     'solar': obsv['solar']['amount'],
                     'humid_max': obsv['relativeHumidity']['max'],
                     'humid_min': obsv['relativeHumidity']['min'],
                     'wind_avg': obsv['wind']['average'],
                     'temp_max': obsv['temperatures']['max'],
                     'temp_min': obsv['temperatures']['min']}
            obsvData.append(myRow)
        return obsvData
    
    def save_to_excel(self, table, name):
        obsv_df = pd.DataFrame(table)
        file_name = name + '.xlsx'
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        obsv_df.to_excel(writer, sheet_name='Sheet1')
        writer.save()