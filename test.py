import requests

url = 'https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent'

headers = {
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
    "X-RapidAPI-Key": "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"  # Replace with your key
}

response = requests.get(url, headers=headers)

# Check status
if response.status_code == 200:
    print(response.json())
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
