import requests
from tabulate import tabulate

def fetch_cricket_scores():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"  # Replace if needed
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Safely get matches from first match type (usually International)
        match_types = data.get('typeMatches', [])
        if not match_types:
            print("No match types found.")
            return

        series_matches = match_types[0].get('seriesMatches', [])
        if not series_matches:
            print("No series matches found.")
            return

        for series in series_matches:
            matches = series.get('seriesAdWrapper', {}).get('matches', [])
            for match in matches:
                try:
                    match_info = match['matchInfo']
                    team1 = match_info['team1']['teamName']
                    team2 = match_info['team2']['teamName']
                    desc = match_info['matchDesc']
                    series_name = match_info.get('seriesName', 'N/A')
                    match_format = match_info.get('matchFormat', 'N/A')
                    status = match_info.get('status', 'N/A')

                    table = []
                    table.append(["Match Description", f"{desc} | {team1} vs {team2}"])
                    table.append(["Series Name", series_name])
                    table.append(["Match Format", match_format])
                    table.append(["Result", status])

                    # Check for scores
                    match_score = match.get('matchScore', {})
                    team1_score = match_score.get('team1Score', {}).get('inngs1', {})
                    team2_score = match_score.get('team2Score', {}).get('inngs1', {})

                    if team1_score:
                        t1_runs = team1_score.get('runs', 'N/A')
                        t1_wkts = team1_score.get('wickets', 'N/A')
                        t1_overs = team1_score.get('overs', 'N/A')
                        table.append([f"{team1}", f"{t1_runs}/{t1_wkts} in {t1_overs} overs"])
                    else:
                        table.append([team1, "Score not available"])

                    if team2_score:
                        t2_runs = team2_score.get('runs', 'N/A')
                        t2_wkts = team2_score.get('wickets', 'N/A')
                        t2_overs = team2_score.get('overs', 'N/A')
                        table.append([f"{team2}", f"{t2_runs}/{t2_wkts} in {t2_overs} overs"])
                    else:
                        table.append([team2, "Score not available"])

                    print(tabulate(table, headers=["Key", "Value"], tablefmt="grid"))
                    print("\n")

                except KeyError as e:
                    print(f"Skipped a match due to missing data: {e}")
                    continue

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")

# Run the function
fetch_cricket_scores()
