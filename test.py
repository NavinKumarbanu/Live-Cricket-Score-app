import requests
import json

# Cricbuzz Recent Matches API endpoint
url = 'https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent'

# RapidAPI headers with your key
headers = {
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
    "X-RapidAPI-Key": "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Handle the response
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))  # Pretty print JSON
else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")
