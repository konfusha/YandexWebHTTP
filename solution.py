import requests
from io import BytesIO
from PIL import Image
import json
from YandexAPITools import find_spn_delta
from dotenv import load_dotenv
import os

path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path):
    load_dotenv(path)
    API_KEY = os.environ.get('API_KEY')
    

search_api_server = "https://search-maps.yandex.ru/v1/"

address_ll = "37.588392,55.734036"

search_params = {
    "apikey": API_KEY,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    #...
    pass

json_response = response.json()
json.dump(json_response, open('request0.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
spn_delta = find_spn_delta(json_response)

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": ",".join(map(str, spn_delta)),
    "apikey": apikey,
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2dgl".format(org_point)
}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()