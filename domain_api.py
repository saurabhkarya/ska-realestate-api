import requests
import json
import keys.py

keys.domain_client_id = 'client_4f52932edf1c7c94732d010ffb929f72'
client_secret = 'secret_52043591d95d3edc38d717c77319a8cd'
scopes = ['api_properties_read']
auth_url = 'https://auth.domain.com.au/v1/connect/token'
url_endpoint = 'https://api.domain.com.au/v1/salesResults/'
property_id = 'Sydney'


def get_property_info():
    response = requests.post(auth_url, data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': scopes,
        'Content-Type': 'text/json'
    })
    json_res = response.json()
    access_token = json_res['access_token']
    print(access_token)
    auth = {'Authorization': 'Bearer ' + access_token}
    url = url_endpoint + property_id
    res1 = requests.get(url, headers=auth)
    r = res1.json()
    print(r)


get_property_info()
