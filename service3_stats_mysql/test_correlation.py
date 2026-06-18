import requests

url = "http://127.0.0.1:5003/db/stats/correlation"

params = {
    "serie_x": "serie_A",
    "serie_y": "serie_B"
}

r = requests.get(url, params=params)

print(r.json())