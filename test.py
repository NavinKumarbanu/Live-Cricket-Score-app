import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
    "X-RapidAPI-Key": "f33c97bc66mshe003db879159c21p123f11jsn4c9a3f5a812d"
}

response = requests.get(url, headers=headers)
print(response.json())
