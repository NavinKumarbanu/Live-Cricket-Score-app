import requests
from tabulate import tabulate

def fetch_cricket_scores():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"
    }

    response = requests.get(url, headers=headers)
    
    try:
        data = response.json()
    except ValueError:
        print("Invalid JSON response from API")
        return

    try:
        matches = data['typeMatches'][0]['seriesMatches'][0]['seriesAdWrapper']['matches']
    except (KeyError, IndexError):
        print("Unable to parse match data from API response")
        return

    for match in matches:
        table = []

        try:
            match_info = match['matchInfo']
            team1 = match_info['team1']['teamName']
            team2 = match_info['team2']['teamName']

            table.append(["Match Description", f"{match_info['matchDesc']} , {team1} vs {team2}"])
            table.append(["Match Details", ""])
            table.append(["Series Name", match_info['seriesName']])
            table.append(["Match Format", match_info['matchFormat']])
            table.append(["Result", match_info.get('status', 'Not Available')])

            # Scores
            match_score = match.get('matchScore', {})
            team1_score = match_score.get('team1Score', {}).get('inngs1', {})
            team2_score = match_score.get('team2Score', {}).get('inngs1', {})

            if team1_score:
                table.append([team1, f"{team1_score.get('runs', 'N/A')}/{team1_score.get('wickets', 'N/A')} in {team1_score.get('overs', 'N/A')} overs"])
            else:
                table.append([team1, "Score not available"])

            if team2_score:
                table.append([team2, f"{team2_score.get('runs', 'N/A')}/{team2_score.get('wickets', 'N/A')} in {team2_score.get('overs', 'N/A')} overs"])
            else:
                table.append([team2, "Score not available"])

            print(tabulate(table, headers=["Key", "Value"], tablefmt="grid"))
            print("\n")

        except KeyError as e:
            print(f"Skipping match due to missing field: {e}")
            continue

fetch_cricket_scores()
