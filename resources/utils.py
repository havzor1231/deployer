import requests
from emora_stdm import Macro, Ngrams
from typing import Any, Dict, List
import json

headers = {
    "X-RapidAPI-Key": "1b0a42ee93msh3c60044810c2171p15d22bjsn431cea4eea20",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}


def get_key_observations(team1, team2, month, day, year):
    # get fixture id of mentioned match
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"

    with open('team_to_id.json', 'r') as f:
        data = json.load(f)

        team1_id = data[team1]["team_id"]
        team2_id = data[team2]["team_id"]

        h2h = "{id1}-{id2}".format(id1=team1_id, id2=team2_id)
        date = f'{year:02}-{month:02}-{day:02}'
        # print(date)

    querystring = {"h2h": h2h, "date": date}

    response = requests.request("GET", url, headers=headers, params=querystring)
    loaded_r = json.loads(response.text)

    for fixture in loaded_r["response"]:
        fixture_id = fixture["fixture"]["id"]
        score_dict = fixture["score"]
        home_away = {"home": fixture["teams"]["home"]["name"], "away": fixture["teams"]["away"]["name"]}
        # print(home_away)

    # get fixture statistics
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"

    querystring = {"fixture": fixture_id}

    response = requests.request("GET", url, headers=headers, params=querystring)
    loaded_r = json.loads(response.text)

    curr_dict = {}

    for team in loaded_r["response"]:
        name = team["team"]["name"]

        stat = team["statistics"]
        temp = {}

        # add statistics to dict
        for curr in stat:
            curr_type, val = curr["type"], curr["value"]
            temp[curr_type] = val

        curr_dict[name] = temp

    # add halftime and fulltime score to statistics
    for ele in score_dict:
        home_score = score_dict[ele]["home"]
        away_score = score_dict[ele]["away"]

        home_team = home_away["home"]
        away_team = home_away["away"]

        curr_dict[home_team][ele] = home_score
        curr_dict[away_team][ele] = away_score

    return curr_dict

def get_key_stats(team1, team2, month, day, year):
    # get fixture id of mentioned match
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"

    with open('team_to_id.json', 'r') as f:
        data = json.load(f)

        team1_id = data[team1]["team_id"]
        team2_id = data[team2]["team_id"]

        h2h = "{id1}-{id2}".format(id1=team1_id, id2=team2_id)
        date = f'{year:02}-{month:02}-{day:02}'
        # print(date)

    querystring = {"h2h": h2h, "date": date}

    response = requests.request("GET", url, headers=headers, params=querystring)
    loaded_r = json.loads(response.text)

    for fixture in loaded_r["response"]:
        fixture_id = fixture["fixture"]["id"]
        score_dict = fixture["score"]
        home_away = {"home": fixture["teams"]["home"]["name"], "away": fixture["teams"]["away"]["name"]}
        # print(home_away)

    # get fixture statistics
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"

    querystring = {"fixture": fixture_id}

    response = requests.request("GET", url, headers=headers, params=querystring)
    loaded_r = json.loads(response.text)

    curr_dict = {}

    for team in loaded_r["response"]:
        name = team["team"]["name"]

        stat = team["statistics"]
        temp = {}

        # add statistics to dict
        for curr in stat:
            curr_type, val = curr["type"], curr["value"]
            temp[curr_type] = val

        curr_dict[name] = temp

    # add halftime and fulltime score to statistics
    for ele in score_dict:
        home_score = score_dict[ele]["home"]
        away_score = score_dict[ele]["away"]

        home_team = home_away["home"]
        away_team = home_away["away"]

        curr_dict[home_team][ele] = home_score
        curr_dict[away_team][ele] = away_score

    return curr_dict