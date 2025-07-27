from flask import Flask, render_template
import requests
import json
from tabulate import tabulate
import os

app = Flask(__name__)

# Set your RapidAPI key here (development use only – secure for production!)
RAPIDAPI_KEY = "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"

def fetch_cricket_scores():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        matches_data = []

        for match in data['typeMatches'][0]['seriesMatches'][0]['seriesAdWrapper']['matches']:
            table = [
                [f"{match['matchInfo']['matchDesc']} - {match['matchInfo']['team1']['teamName']} vs {match['matchInfo']['team2']['teamName']}"],
                ["Series Name", match['matchInfo']['seriesName']],
                ["Match Format", match['matchInfo']['matchFormat']],
                ["Result", match['matchInfo']['status']],
                [f"{match['matchInfo']['team1']['teamName']} Score", 
                 f"{match['matchScore']['team1Score']['inngs1']['runs']}/"
                 f"{match['matchScore']['team1Score']['inngs1']['wickets']} in "
                 f"{match['matchScore']['team1Score']['inngs1']['overs']} overs"],
                [f"{match['matchInfo']['team2']['teamName']} Score", 
                 f"{match['matchScore']['team2Score']['inngs1']['runs']}/"
                 f"{match['matchScore']['team2Score']['inngs1']['wickets']} in "
                 f"{match['matchScore']['team2Score']['inngs1']['overs']} overs"]
            ]
            matches_data.append(tabulate(table, tablefmt="html"))
        return matches_data

    except Exception as e:
        print(f"Error fetching recent matches: {e}")
        return []

def fetch_upcoming_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/schedule/v1/international"
    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }

    upcoming_matches = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        match_schedules = data.get('matchScheduleMap', [])

        for schedule in match_schedules:
            if 'scheduleAdWrapper' in schedule:
                date = schedule['scheduleAdWrapper']['date']
                matches = schedule['scheduleAdWrapper']['matchScheduleList']

                for match_info in matches:
                    for match in match_info['matchInfo']:
                        description = match.get('matchDesc', 'No Description')
                        team1 = match.get('team1', {}).get('teamName', 'Team 1')
                        team2 = match.get('team2', {}).get('teamName', 'Team 2')
                        match_data = {
                            'Date': date,
                            'Description': description,
                            'Teams': f"{team1} vs {team2}"
                        }
                        upcoming_matches.append(match_data)

    except Exception as e:
        print(f"Error fetching upcoming matches: {e}")

    return upcoming_matches

@app.route('/')
def index():
    cricket_scores = fetch_cricket_scores()
    upcoming_matches = fetch_upcoming_matches()
    return render_template('index.html', cricket_scores=cricket_scores, upcoming_matches=upcoming_matches)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)
