

import requests
from enum import Enum
from emora_stdm import DialogueFlow
from emora_stdm import Macro, Ngrams
from typing import Dict, Any, List
from typing import Dict, Any, List
import json
import pickle
import re
import os

class MacroVisits(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        vn = 'VISITS'

        if vn not in vars:
            vars[vn] = 1
            return 'Quick pop quiz. What is Newcastle\'s nickname?'
        else:
            count = vars[vn] + 1
            vars[vn] = count
            match count:
                case 2: return 'What do you want to talk about?'
                case 3: return 'What brings you here today?'
                case default:
                    return 'What do you want to talk about?'
class MacroLeading(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        querystring = {"season": "2022", "league": "39"}
        headers = {
            "X-RapidAPI-Key": "dbad2f5186msh2f81b29abdc6d29p17a232jsndd11cefd33a8",
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response_data = json.loads(response.text)

        # Access the ranking of the first team in the response
        first_team_ranking = response_data['response'][0]['league']['standings'][0][0]['team']['name']
        first_team_points = response_data['response'][0]['league']['standings'][0][0]['points']

        output_string = f"{first_team_ranking} is currently at the top of the EPL table with {first_team_points} points."

        return output_string


class MacroRank(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):

        team_mentioned = []

        f = open("team_to_id.json")
        teams_dict = json.load(f)
        for team in teams_dict:
            if team in ngrams.raw_text():
                team_mentioned.append(team)
                team_name = team_mentioned[0]
                vars['team_name'] = team_name

        url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        querystring = {"season": "2022", "league": "39"}
        headers = {
            "X-RapidAPI-Key": "dbad2f5186msh2f81b29abdc6d29p17a232jsndd11cefd33a8",
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response_data = json.loads(response.text)

        team_name = vars['team_name']

        for team in response_data['response'][0]['league']['standings'][0]:
            if team['team']['name'].lower() == team_name:
                    team_ranking = response_data['response'][0]['league']['standings'][0][0]['team']['rank']
                    team_points = response_data['response'][0]['league']['standings'][0][0]['points']
                    output_string1 = f"{team_name.title()} is currently at rank {team_ranking} in the EPL table with {team_points} points."
                    return output_string1
            else:
                output_string2 = f"Sorry, I could not find information about {team_name.title()} in the EPL table."
                return output_string2
        else:
            output_string3 = "Please provide a team name to get its rank and points."
            return output_string3

class MacroHome(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):


        team_mentioned = []

        f = open("team_to_id.json")
        teams_dict = json.load(f)
        for team in teams_dict:
            if team in ngrams.raw_text():
                team_mentioned.append(team)
                team_name = team_mentioned[0]
                vars['team_name'] = team_name
                return True

champions = {
            "1992-1993": {"team": "Manchester United", "score": 84, "top_goalscorer": "Teddy Sheringham"},
            "1993-1994": {"team": "Manchester United", "score": 92, "top_goalscorer": "Andrew Cole"},
            "1994-1995": {"team": "Blackburn Rovers", "score": 89, "top_goalscorer": "Alan Shearer"},
            "1995-1996": {"team": "Manchester United", "score": 82, "top_goalscorer": "Alan Shearer"},
            "1996-1997": {"team": "Manchester United", "score": 75, "top_goalscorer": "Alan Shearer"},
            "1997-1998": {"team": "Arsenal", "score": 78,
                          "top_goalscorer": ["Dion Dublin", "Chris Sutton", "Michael Owen"]},
            "1998-1999": {"team": "Manchester United", "score": 79,
                          "top_goalscorer": ["Jimmy Floyd Hasselbaink", "Michael Owen", "Dwight Yorke"]},
            "1999-2000": {"team": "Manchester United", "score": 91, "top_goalscorer": "Kevin Phillips"},
            "2000-2001": {"team": "Manchester United", "score": 80,
                          "top_goalscorer": "Jimmy Floyd Hasselbaink"},
            "2001-2002": {"team": "Arsenal", "score": 87, "top_goalscorer": "Thierry Henry"},
            "2002-2003": {"team": "Manchester United", "score": 83, "top_goalscorer": "Ruud van Nistelrooy"},
            "2003-2004": {"team": "Arsenal", "score": 90, "top_goalscorer": "Thierry Henry"},
            "2004-2005": {"team": "Chelsea", "score": 95, "top_goalscorer": "Thierry Henry"},
            "2005-2006": {"team": "Chelsea", "score": 91, "top_goalscorer": "Thierry Henry"},
            "2006-2007": {"team": "Manchester United", "score": 89, "top_goalscorer": "Didier Drogba"},
            "2007-2008": {"team": "Manchester United", "score": 87, "top_goalscorer": "Cristiano Ronaldo"},
            "2008-2009": {"team": "Manchester United", "score": 90, "top_goalscorer": "Nicolas Anelka"},
            "2009-2010": {"team": "Chelsea", "score": 86, "top_goalscorer": "Didier Drogba"},
            "2010-2011": {"team": "Manchester United", "score": 80,
                          "top_goalscorer": ["Dimitar Berbatov", "Carlos Tevez"]},
            "2011-2012": {"team": "Manchester City", "score": 89, "top_goalscorer": "Robin van Persie"},
            "2012-2013": {"team": "Manchester United", "score": 89, "top_goalscorer": "Robin van Persie"},
            "2013-2014": {"team": "Manchester City", "score": 86, "top_goalscorer": "Luis Suarez"},
            "2014-2015": {"team": "Chelsea", "score": 87, "top_goalscorer": "Sergio Aguero"},
            "2015-2016": {"team": "Leicester City", "score": 81, "top_goalscorer": "Harry Kane"},
            "2016-2017": {"team": "Chelsea", "score": 93, "top_goalscorer": "Harry Kane"},
            "2017-2018": {"team": "Manchester City", "score": 100, "top_goalscorer": "Mohamed Salah"},
            "2018-2019": {"team": "Manchester City", "score": 98,
                          "top_goalscorers": ["Mohamed Salah", "Pierre-Emerick Aubameyang", "Sadio Mane"]},
            "2019-2020": {"team": "Liverpool", "score": 99, "top_goalscorer": "Jamie Vardy"},
            "2020-2021": {"team": "Manchester City", "score": 86, "top_goalscorer": "Harry Kane"},
            "2021-2022": {"team": "Manchester City", "score": 93,
                          "top_goalscorer": ["Mohamed Salah", "Son Heung-Min"]}
        }

class MacroChampions(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):

        team_mentioned = []

        f = open("team_to_id.json")
        teams_dict = json.load(f)
        for team in teams_dict:
            if team in ngrams.raw_text():
                team_mentioned.append(team)
                team_name = team_mentioned[0]
                vars['team_name'] = team_name

                count = 0

                for season, data in champions.items():
                    if team_name == data['team']:
                        count = count + 1

                if count >=1:

                    max_score = 0
                    max_year = ""
                    for year, data in champions.items():
                        if team_name == data['team']:
                            if data["score"] > max_score:
                                max_score = data["score"]
                                max_year = year


                    print(team_name + " has won " + str(count) + " times." + team_name +"\'s highest score was " + str(max_score) +" in season " + str(max_year) )

                else:
                    print(team_name + "did not win any trophies.")


def visits() -> DialogueFlow:
    transitions = {
        'state': 'start',
        '`Welcome! I am dEPLoyer, English Premier League Chatbot.` #VISITS': {
            '[Magpies]': {
                '`That is correct. What team is Mohamed Salah in currently?`': {
                    '[{liverpool,liverpool fc, liverpool f.c., the reds}]': {
                        '`Wow! You must have some knowledge in soccer. Let\'s get started!`': 'familiar'},
                    'error': 'fun_fact'
                }
            },
            'error': 'unfamiliar'
        }
    }

    macros = {
        'VISITS': MacroVisits(),
        'GET_HOME_TEAM': MacroHome(),
        'GET_LEADING_TEAM': MacroLeading(),
        'GET_TEAM_RANK': MacroRank(),
        'GET_CHAMPIONS': MacroChampions()
    }

    df = DialogueFlow('start', end_state='end')
    df.load_transitions(transitions)
    df.load_transitions(familiar),
    df.load_transitions(branch),
    df.load_transitions(ranks),
    df.load_transitions(match),
    df.load_transitions(players)
    df.add_macros(macros)
    return df


familiar = {
        'state': 'familiar',
        '`I can talk about a specific match, team, or player. '
        'What are you interested in talking about?`': {

            #current stats: user is generally interested in top performing teams: example: Which team is currently at the top of the EPL table?
            '[{top, first, first place, leading, summit, table}]': {
                #GET_LEADING_TEAM macro will return: Arsenal is currently at the top of the EPL table with 73 points.
                '#GET_LEADING_TEAM': {
                    '[{what about, how about, how is}] #GET_HOME_TEAM [{doing}]':'ranks'
                }
            },

            #historic stats: ex) how many times did Manchester United win trophies? or how many EPL trophies have Liverpool won?
            '[{total,champion, championships, crown, trophies, history}] #GET_CHAMPIONS [{win,won}]' : {
                '`Are you a fan of` $team_name `? We can continue talking about` $team_name.': {
                    '[{yes,sure,ok}]':'branch',
                    '[{no,different team, another team}]':{
                        '`Which team would you like to talk about?` #GET_HOME_TEAM': 'branch'
                    },
                    '[{no}] #GET_HOME_TEAM':'branch'

                }
            },

            #user is interested in a specific team: i want to talk about Manchester City
            '[{talk about, talk }] #GET_HOME_TEAM': {
                'state':'branch'}
        }
}

branch = {
    'state':'branch',
    '`I am a huge fan of` $team_name `! What do you want to know about` $team_name `?`' :{
        #if a user is interested in players go to players state
        '[{player,players}]':'players',
        # if a user is interested in a team's rank go to macro #GET_TEAM_RANK
        '[{rank}]':'ranks',
        #if a user is interested in a specific match go to match state.
        '[{vs, versus}]':'match'
    }
},

ranks = {
    'state' : 'ranks',
        #follow-up question by user for another team's rank: ex) What about Liverpool's rank?
       '#GET_TEAM_RANK': {
            #should return: '`$Liverpool` is in _rank with 52 points. It's been a tough season for them. What else are you interested in? '
              ' ': {
                  '`Would you like to talk more about` $team_name `?`': {
                      '[{yes,ok}]':'branch'}
                }
       }
},

match = {
    'state':'match',
    '`Which game do you want to talk about?`' :{
                    #get match macro: user specifies a game
                    #user asks "What's been the most exciting match of the season so far?"
                }
    },

players = {
    'state':'players',
        '`Which player do you want to talk about?`':'end' #build player macro here
            }




def save(df: DialogueFlow, varfile: str):
    d = {k: v for k, v in df.vars().items() if not k.startswith('_')}
    pickle.dump(d, open(varfile, 'wb'))

def load(df: DialogueFlow, varfile: str):
    d = pickle.load(open(varfile, 'rb'))
    df.vars().update(d)
    df.run()
    save(df, varfile)

load(visits(), '/Users/hasongcho/PycharmProjects/deployer/resources/visits.pkl')
