import requests
import json
import api_keys.py

api_keys.domain_client_id = 'client_4f52932edf1c7c94732d010ffb929f72'
api_keys.domain_client_secret = 'secret_52043591d95d3edc38d717c77319a8cd'
scopes = ['api_properties_read']
auth_url = 'https://auth.domain.com.au/v1/connect/token'
url_endpoint = 'https://api.domain.com.au/v1/salesResults/'
property_id = 'Sydney'


def get_property_info():
    response = requests.post(auth_url, data={
        'client_id': api_keys.client_id,
        'client_secret': api_keys.client_secret,
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

# Read Post Code File
post_c = pd.read_csv('../data/Post Codes.csv', names=['postcode'])

# Convert Post Code to generator
post_i = iter(post_c['postcode'].tolist())

# Create Url generator using Post Code
urls = ("https://www.domain.com.au/rent/?excludedeposittaken=1&postcode={}&page=1".format(i)
        for i in post_i)

limit = 100
list_data = []
multi_pages = []


def fetch(url, session):
    print("Scraping: " + url)
    async with session.get(url) as response:
        raw_data = await response.read()
        if response.status == 200:
            await parse(url, raw_data)


def parse(url, html):
    if str(html) != "None":
        print("Parsing Html!"+url)
        soup = BeautifulSoup(html, "html.parser")
        js = soup.find_all('script')
        for resultset in js:
            if str(resultset).startswith("<script>window.renderizrData = (window.renderizrData || {});"):
                js_data = str(resultset)
                js_data = js_data.replace(
                    "<script>window.renderizrData = (window.renderizrData || {}); window.renderizrData[\"page\"] = ",
                    " "). \
                    replace(
                        ";</script>", "").encode("utf-8").decode('utf-8', 'ignore').strip()

                json_data = (json.dumps(js_data))
                async with aiofiles.open('../data/data.json', 'w+') as file:
                    await file.write(json_data)

                if 'totalPages' in json.loads(js_data):
                    pages = ((json.loads(js_data)['totalPages']) + 1)
                    sub_pages_url = [n for n in range(2, pages)]
                    n_url = url.replace("&page=1", "&page={}")
                    nurls = list(n_url.format(i) for i in sub_pages_url)
                    await append(nurls)


def append(l):
    multi_pages.append(l)
