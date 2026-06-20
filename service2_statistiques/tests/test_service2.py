import requests

adresse = "http://127.0.0.1:5002"

print("Test /stats/describe")
reponse = requests.post(adresse + "/stats/describe", json={
    "data": [12, 15, 8, 21, 13, 10]
})
print(reponse.json())

print("Test /stats/correlation")
reponse = requests.post(adresse + "/stats/correlation", json={
    "x": [1, 2, 3, 4],
    "y": [2, 4, 6, 8]
})
print(reponse.json())

print("Test /stats/test_normalite")
reponse = requests.post(adresse + "/stats/test_normalite", json={
    "data": [12, 13, 14, 15, 16, 14, 13, 15]
})
print(reponse.json())