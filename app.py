from flask import Flask, render_template
import requests

app = Flask(__name__)

def fetch_cricket_scores():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

    headers = {
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
        "X-RapidAPI-Key": "327a4f3817msh0e716c198181c52p17c0ffjsn0e7e53feb9b3"  # Replace this with your actual API key
    }

    response = requests.get(url, headers=headers)
    
    try:
        data = response.json()
    except ValueError:
        return [{"error": "Invalid JSON response from API"}]

    type_matches = data.get('typeMatches')
    if not type_matches:
        return [{"error": "No match data found or unexpected API format"}]

    matches = []
    try:
        series_matches = type_matches[0].get('seriesMatches', [])
        for series in series_matches:
            series_wrapper = series.get('seriesAdWrapper')
            if not series_wrapper:
                continue
            for match in series_wrapper.get('matches', []):
                team1 = match['team1']['teamName']
                team2 = match['team2']['teamName']
                status = match.get('status', 'Status not available')
                matches.append({
                    'team1': team1,
                    'team2': team2,
                    'status': status
                })
    except Exception as e:
        return [{"error": f"Error parsing match data: {str(e)}"}]

    return matches

@app.route('/')
def index():
    cricket_scores = fetch_cricket_scores()
    return render_template('index.html', matches=cricket_scores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
