from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract and organize data
    recent_matches = []
    upcoming_matches = []

    for match in data.get('matches', []):
        match_info = {
            "team1": match.get("team1", {}).get("name", "Team 1"),
            "team2": match.get("team2", {}).get("name", "Team 2"),
            "status": match.get("status", "N/A"),
            "start_time": match.get("startDate", "N/A")
        }

        if match.get('matchInfo', {}).get('state') == "Complete":
            recent_matches.append(match_info)
        elif match.get('matchInfo', {}).get('state') == "Preview":
            upcoming_matches.append(match_info)

    return render_template('index.html', recent_matches=recent_matches, upcoming_matches=upcoming_matches)

if __name__ == '__main__':
    app.run(debug=True)
