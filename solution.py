import sys
from io import BytesIO
from YandexAPITools import find_spn_delta
import json
import os
from dotenv import load_dotenv
import requests
from PIL import Image


path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path):
    load_dotenv(path)
    SEARCH_API_KEY = os.environ.get('SEARCH_API_KEY')
    GEOCODER_API_KEY = os.environ.get('GEOCODER_API_KEY')
    STATIC_MAP_API_KEY = os.environ.get('STATIC_MAP_API_KEY')
# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": GEOCODER_API_KEY,
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_api_server = "https://search-maps.yandex.ru/v1/"
search_params = {
    "apikey": SEARCH_API_KEY,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": toponym_longitude + ',' + toponym_lattitude,
    "type": "biz"
}
 
response = requests.get(search_api_server, params=search_params)
if not response:
    #...
    pass
 
pharmacy_response = response.json()
json.dump(pharmacy_response, open('request0.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

# Получаем первую найденную организацию.
organization = pharmacy_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

work_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]

# Получаем координаты ответа.
pharmacy_point = organization["geometry"]["coordinates"]
org_point = f"{pharmacy_point[0]},{pharmacy_point[1]}"
distance = ((float(toponym_longitude) - pharmacy_point[0]) ** 2 + (float(toponym_longitude) - pharmacy_point[0]) ** 2) ** 0.5
print(f"Адрес: {org_address}\nНазвание: {org_name}\nВремя работы: {work_time}\nРасстояние: {distance}")


map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(map(str, find_spn_delta(json_response, pharmacy_response))),
    "apikey": STATIC_MAP_API_KEY,
    "pt": "{0},pm2dgl".format(org_point) + "~" + "{0},pm2rdl".format(toponym_longitude + ',' + toponym_lattitude)

}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()  # Создадим картинку и тут же ее покажем встроенным просмотрщиком операционной системы
