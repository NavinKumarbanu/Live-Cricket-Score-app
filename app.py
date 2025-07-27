def fetch_cricket_scores():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"  
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch recent matches. Status code:", response.status_code)
        return ["Error fetching data from API"]

    try:
        data = response.json()
        if 'typeMatches' not in data:
            print("typeMatches key not found in the response. Raw data:")
            print(json.dumps(data, indent=2))
            return ["API response structure changed or invalid key"]

        matches_data = []

        for match in data['typeMatches'][0]['seriesMatches'][0]['seriesAdWrapper']['matches']:
            table = [
                [f" {match['matchInfo']['matchDesc']} , {match['matchInfo']['team1']['teamName']} vs {match['matchInfo']['team2']['teamName']}"],
                ["Series Name", match['matchInfo']['seriesName']],
                ["Match Format", match['matchInfo']['matchFormat']],
                ["Result", match['matchInfo']['status']],
                [f"{match['matchInfo']['team1']['teamName']} Score", f"{match['matchScore']['team1Score']['inngs1']['runs']}/{match['matchScore']['team1Score']['inngs1']['wickets']} in {match['matchScore']['team1Score']['inngs1']['overs']} overs"],
                [f"{match['matchInfo']['team2']['teamName']} Score", f"{match['matchScore']['team2Score']['inngs1']['runs']}/{match['matchScore']['team2Score']['inngs1']['wickets']} in {match['matchScore']['team2Score']['inngs1']['overs']} overs"]
            ]
            matches_data.append(tabulate(table, tablefmt="html"))

        return matches_data

    except Exception as e:
        print("Exception while parsing API response:", e)
        return ["Error processing cricket scores"]
