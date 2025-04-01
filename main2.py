import sys
import requests
import os
from PIL import Image


# поиск долготы + широты
geocode = ' '.join(sys.argv[1:])
server_address = 'http://geocode-maps.yandex.ru/1.x/'
api_key = '8013b162-6b42-4997-9691-77b7074026e0'

# Выполняем запрос.
response = requests.get(server_address, params={'apikey': api_key, 'geocode': geocode, 'format': 'json'})

if response:
    # Преобразуем ответ в json-объект
    json_response = response.json()

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа, он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    lon_1, lat_1 = [float(i) for i in toponym['boundedBy']['Envelope']['lowerCorner'].split()]
    lon_2, lat_2 = [float(i) for i in toponym['boundedBy']['Envelope']['upperCorner'].split()]
    lon, lat = toponym["Point"]["pos"].split()
else:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")


# работа с картами
api_server = "https://static-maps.yandex.ru/v1"
api_key = '341350ef-a110-4b4b-bd5b-451cf362b837'
delta1 = str(lon_2 - lon_1)
delta2 = str(lat_2 - lat_1)
params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta1, delta2]),
    "apikey": api_key,
    'pt': ','.join([lon, lat, 'comma'])
}
response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
img = Image.open('map.png')
img.show()
os.remove(map_file)
