import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
    "X-RapidAPI-Key": "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"
}

response = requests.get(url, headers=headers)
print(response.json())
