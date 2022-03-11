import sys
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
search_api_server = "https://search-maps.yandex.ru/v1/"
map_api_server = "http://static-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    print('error')
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
lower_corner = list(map(float, toponym["boundedBy"]["Envelope"][
    "lowerCorner"].split()))
upper_corner = list(map(float, toponym["boundedBy"]["Envelope"][
    "upperCorner"].split()))
delta1, delta2 = '0.5', '0.5'

search_params = {
    "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta1, delta2]),
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
if not response:
    pass
json_response = response.json()
organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
point = organization["geometry"]["coordinates"]
org_point = str(point[0]) + ',' + str(point[1]) + ',' + 'flag'

map_params = {
    "l": "map",
    "pt": ",".join(
        [toponym_longitude, toponym_lattitude]) + '~' + org_point
}
response = requests.get(map_api_server, params=map_params)

im = Image.open(BytesIO(response.content))

length = str(int(((float(toponym_longitude) - point[0]) ** 2 + (
        float(toponym_lattitude) - point[1]) ** 2) ** 0.5 * 111000))
draw_text = ImageDraw.Draw(im)
font = ImageFont.truetype('ARIALUNI.TTF', size=10)
draw_text.text(
    (0, 10),
    org_name,
    font=font,
    fill=('#1C0606'))
draw_text.text(
    (0, 20),
    org_address,
    font=font,
    fill=('#1C0606'))
draw_text.text(
    (0, 30),
    'Расстояние: ' + length + ' метров',
    font=font,
    fill=('#1C0606'))
im.show()
