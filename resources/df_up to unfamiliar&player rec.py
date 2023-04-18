import random
from enum import Enum
from typing import Dict, Any

import requests
from emora_stdm import DialogueFlow
from emora_stdm import Macro, Ngrams
from typing import Dict, Any, List
import re

import openai
from emora_stdm import DialogueFlow
import utils
from utils import MacroGPTJSON, MacroNLG

PATH_USER_INFO = 'resource/userinfo.json'

team_dict = {
    'arsenal': 'Arsenal',
    'aston villa': 'Aston Villa',
    'brentford': 'Brentford',
    'brighton': 'Brighton & Hove Albion',
    'burnley': 'Burnley',
    'chelsea': 'Chelsea',
    'crystal palace': 'Crystal Palace',
    'everton': 'Everton',
    'leeds united': 'Leeds United',
    'leicester city': 'Leicester City',
    'liverpool': 'Liverpool',
    'manchester city': 'Manchester City',
    'manchester united': 'Manchester United',
    'newcastle united': 'Newcastle United',
    'norwich city': 'Norwich City',
    'southampton': 'Southampton',
    'tottenham': 'Tottenham Hotspur',
    'watford': 'Watford',
    'west ham united': 'West Ham United',
    'wolverhampton': 'Wolverhampton Wanderers'
}


class V(Enum):
    interested = 0


class MacroGetInterested(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        interested = vars[V.interested.name][0]
        print("interested value:")
        print(interested)
        if interested == 'true':
            vars['INTERESTED'] = 'true'
            print('true')
        else:
            vars['INTERESTED'] = 'false'
            print('false')


class MacroHome(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        user_input = input().lower()
        if user_input in team_dict:
            team_name = team_dict[user_input]
            # make team_name into team id
            url = "https://sofascores.p.rapidapi.com/v1/teams/rankings"
            querystring = {"name": team_name}
            headers = {
                "X-RapidAPI-Key": "dbad2f5186msh2f81b29abdc6d29p17a232jsndd11cefd33a8",
                "X-RapidAPI-Host": "sofascores.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()['data']
            ranking = data[0]['ranking']
            year = data[0]['year']
            vars['home_team_ranking'] = ranking
            # [team name] ranked [rank] in [2021]
            print(team_name + " is ranked #" + str(ranking) + " in " + str(year))
        else:
            print('That team is not part of EPL')


transitions = {
    'state': 'start',
    '`Hi, I am dEPLoyer! Have you ever heard of Manchester United?`': {
        '[yes]': 'familiar',
        '[no]': 'unfamiliar',
    },
}

familiar = {
    'state': 'familiar',
    '`Do you watch EPL in your free time?`': {
        '[yes]': {
            '`I do too! Do you have a favorite team?`': {
                '#GET_HOME_TEAM': 'end'
            },
            '[no]': {
                '`okay`': 'end'
            },
        }
    },

    '[no]': {
        '`Why do you not watch it?`': {
            '[not interested]': {
                '`I love EPL for xxxxxxx, does this interest you?` ': {
                    '[yes]': 'end'
                }
            },
            '[dont know]': 'introducing EPL'
        }
    },
}

unfamiliar = {
    'state': 'unfamiliar',
    '`Manchester United is part of EPL.  The Premier League was founded in 1992, '
    'replacing the First Division as the top tier of English football. Does this sound interesting to you?`': {
        '[yes]': {
            '`Great! Let\'s start with one of the most successful teams in the EPL historically! Manchester United is one of the most successful teams in the English Premier League. The famous player '
            'Cristiano Ronaldo was once a member of Manchester United!`': {
                '#SET_INTERESTED #GET_INTERESTED': {
                    '#IF($INTERESTED=true) `Manchester United can be one of my favorite teams. Do you have any favorite team in EPL so far?`': {
                        '[yes]': {
                            '`Good for you! `': 'match_discussion'
                        },
                        'error': {
                            '`Oh that\'s fine. I watched Manchester United\'s recent game with Sevilla, another team in EPL. It was so intense! They got 2-2 eventually.`': {
                                '#SET_INTERESTED #GET_INTERESTED': {
                                    '#IF($INTERESTED=true) `I know! Sabitzer from Manchester United had the first goal 14 minutes after the game for his team! '
                                    'That is such a quick goal! Given that the average first goal for soccer game is after 30 minutes on average!`': {
                                        '#SET_INTERESTED #GET_INTERESTED': {
                                            '#IF($INTERESTED=true)`Manchester United’s squad is one of the biggest in the Premier League and it’s filled up with quality players in every position. '
                                            'They are actually gonna have a game with Tottenham Hotspur soon.'
                                            'They have long been rivals with each other and Hotspur currently ranks one below Manchester United!'
                                            'Do you bother betting on their results?`': {
                                                '#UNX': {
                                                    '` I would say 2-0. It somehow made me recall their game last '
                                                    'year in October. They had 0-0 at half time.`':
                                                        'player_recommendation'
                                                },
                                            }
                                        },
                                             '#IF($INTERESTED=false)': 'fun_fact'
                                    },
                                        '#IF($INTERESTED=false)': 'fun_fact'
                                }
                            }
                        },

                    },
                        '#IF($INTERESTED=false)': 'fun_fact'
                },
                '#IF($INTERESTED=false)': 'fun_fact'
            }
        }
    },
    '`[no]`': 'player_recommendation'

}

player_recommendation = {
    'state': 'player_recommendation',
    '#GATE `Do you want to know more about some players? Marcus Rashford is my favorite from Manchester United. Well, if you\'re looking for a football player who can run faster than a cheetah on Red Bull, score goals like it\'s his job (oh wait,'
    'it actually is his job), and make the opposing team\'s defense look like a bunch of lost toddlers, then Marcus Rashford is your man. `': 'rashford_rec',
    '#GATE `Do you want to know more about some players? Harry Kane is my favorite from Tottenham Hotspur. He is not '
    'just a goal-scoring machine, he\'s also a great team player.'
    ' He has a knack for creating chances for his teammates and can change the course of a game with his passing and playmaking abilities.`': 'kane_rec',
    '#GATE `Do you want to know more about some players? Kevin De Bruyne is my favorite Manchester City player. If you love players who can play any offensive role'
    'and passes beautifully, you would love De Bruyne!`': 'de_bruyne_rec',
    '#GATE `Do you want to know more about some players? Kante is my favorite Chelsea player. He\'s one of the most hard playing players I have ever seen.'
    'he always runs non-stop to take back possession from the opponent and he\'s very good at it too! What he is also good at is passing the ball and linking it with his fellow teammates'
    'Overall, he\'s a wonderful team player and a truly devoted player!`': 'kante_rec'
}

rashford_rec = {
    'state': 'rashford_rec',
    '`In fact, if football was a video game, Marcus would be the cheat code that everyone wants to unlock. `': {
        '#SET_INTERESTED #GET_INTERESTED': {
            '#IF($INTERESTED=true)`Rashford appeared 233 times in this season and had 74 goals. He is absolutely one of the heated players. Do you want to look at some of his game stats?`':{
                '[yes]': {
                    '`stats Speaking of this, I am a big fan of Manchester United as well. Do you think you would like Manchester United? Manchester United is a team with a rich history and a tradition of excellence.'
                    'If you want to support a team that has consistently been among the best in the world, then Manchester United is a great choice.`': {
                        '[yes]': {
                            '`You know what, they are gonna meet their long-time enemy team Chelsea! The rivalry between Manchester United'
                            'and Chelsea is one of the most intense in English football, and every game between these two teams is a must-watch for fans. They were 1-1 last time! How intense!'
                            ' What do you think will be the score this time?`': {
                                '#UNX': {
                                    '`I would say Manchester United 2 and Chelsea 1. People are accusing of Chelsea being bad at coopertion these days. So who knows haha!`': 'personal_story'
                                }
                            }
                        },
                        '[no]': 'team_recommendation'
                    }
                },
                '[no]': 'player_recommendation'
            },
            '#IF($INTERESTED=false)': 'personal_story'
        }
    }
}

kane_rec = {
    'state': 'kane_rec',
    '`Despite his success on the field, Harry Kane remains humble and grounded.`': {
        '#SET_INTERESTED #GET_INTERESTED': {
            '#IF($INTERESTED=true) `Harry Kane appeared 313 times and had 206 goals. You can call him one of the most successful commissioned players. Do you want to know how he performed?`': {
                    '[yes]': {
                        '`stats Tottenham Hotspur is viral these days! Some of their players made wonderful performance at the World Cup.'
                        'I personally like this team a lot! Do you think you would like it?`': {
                            '[yes]': {
                                '`Great haha another Hotspur fan! Their next game is with team New Castle. I somehow think that New Castle has a decent ranking (they exceeds Hotspur sometime these days!) because they made lots of draws.'
                                'Last time when they met, New Castle had 2 and Tottenham Hotspur had 1. What do you think will be their next score?`': {
                                    '#UNX': {
                                        '`I would just say they will have another draw. From my perspective, New Castle is known for fast-paced games but Tottenham Hotspur'
                                        'plays possession-based games and has won two league titles. Who knows haha!`': 'personal_story'
                                    },
                                }
                            },
                            '[no]': 'team_recommendation'
                        }
                    },
                    '[no]': 'player_recommendation'
                },
            '#IF($INTERESTED=false)': 'personal_story'
            },

        }
    }


de_bruyne_rec = {
    'state': 'de_bruyne_rec',
    '`He is such an outstanding player!`': {
        '#SET_INTERESTED #GET_INTERESTED': {
            '#IF($INTERESTED=true)`De Bruyne appeared almost 240 times in the premier league and had 101 assists! He created 160 big chances for his teamates. Truly, he is on top of his league. Do you want to know more about how he performed?`': {
                    '[yes]': {
                        '`stats Manchester City is truly one of the strongest team in all of Europe! However, even this team is impacted by whether De Bruyne is playing or not.'
                        'In other words, he is the focal point of the playstyle of Manchester City that highlights possession which requires good passing. I like the style of Manchester City a lot! Do you think you would like this team?`': {
                            '[yes]': {
                                '`Good choice for you since Manchester City really made the history of English Premier League and as I recalled, they rank at the second place.'
                                ' Their next game is with Arsenal and dude! That\'s gonna be such a tough game since Arsenal currenly rank the first. And let me tell you, I don\'t buy it. Anyways, Arsenal did win 13 league titles.'
                                'It\'s gonna be very hard for Manchester City but I count on their quick and incisive passing to break down opposition defenses. What do you think, who between them will win?`': {
                                    '#UNX': {
                                        '`Though as a big fan of Manchester City, Arsenal has indeed been the top one for a while. Maybe Mamchester City will lose this time.`': 'personal_story'
                                    }
                                }
                            },
                            '[no]': 'team_recommendation'
                        }
                    },
                    '[no]': 'player_recommendation'
                },
                '#IF($INTERESTED=false)': 'personal_story'
            },
        }
    }


kante_rec = {
    'state': 'kante_rec',
    '`He is a star!`': {
        '#SET_INTERESTED #GET_INTERESTED': {
            '#IF($INTERESTED=true) `Kante appeared around 230 games in the premier league. He made a staggering 505 interceptions and 1685 recoveries, which means he did astonishingly well in recovering the ball! Do you want to know more about how he performed?`': {
                    '[yes]': {
                        '`stats Chelsea historically has a very strong performance! Although Kante is not the type of player that gets the spotlight, Chelsea holds differently whenever Kante is playing for them'
                        'When he plays, there\'s always a stability to Chelsea that makes them look very hard to beat! Chelsea is known for its passionate fans and iconic blue jerseys. Do you think you will like Chelsea?`': {
                            '[yes]': {
                                '`Yay! Chelsea\'s next game is with Bretford. Surprisingly, during their recent games, Chelsea had exactly one wining, one loss, and one draw.'
                                'Chelsea\'s manager Thomas Tuchel really knows how to operate the teams and led the team to their recent success. But Bretford is known for using good data analytics. Who do you think will win?`': {
                                    '#UNX': {
                                        '`I would say, let\'s see, that Bretford would win. I recalled that Bretford won 4-1 to Chelsea, just last year in April. Uhh, bad memory. Anyways.`': 'personal_story'
                                    },
                                }
                            },
                            '[no]': 'team_recommendation'
                        }
                    },
                    '[no]': 'player_recommendation'
                },
            '#IF($INTERESTED=false)': 'personal_story'
            },
        }
    }

personal_story = {
    'state': 'personal_story',
    '#GATE`You know I remember I never wanted to do any exercise before I watched EPL. After watching that I found it really cool to just run freely on the field and even sweating makes me feel happy!`':{
        '/.*/':{
            '`Haha, you know how people say soccer really cheers people up. That is exactly what I feel. Speaking of that, i want to share this video with you. I really feel the same.`':'video'
        }
    },
    '#GATE `I once had a big fight with my dad because he really thought Arsenal would win but I thought Manchester City would win the champion. I mean I got it right. But we ended up just having a wonderful time watching the final together with beer and barbecue! It was such a wonderful time!':'fun_fact'
}

team_recommendation = {
    'state': 'team_recommendation',
    '#GATE `Do you want to hear about the teams in Premier League then? `': 'end'
}
fun_fact={
    'state':'fun_fact',
    '`fun facts`':'end'
}

macros = {
    'GET_HOME_TEAM': MacroHome(),
    'SET_INTERESTED': MacroGPTJSON(
        'Do you think the user is interested in knowing more?',
        {V.interested.name: ["true", "false"]}
    ),
    'GET_INTERESTED': MacroGetInterested()
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.load_transitions(familiar)
df.load_transitions(unfamiliar)
df.load_transitions(player_recommendation)
df.load_transitions(rashford_rec)
df.load_transitions(kane_rec)
df.load_transitions(team_recommendation)
df.load_transitions(de_bruyne_rec)
df.load_transitions(kante_rec)
df.load_transitions(personal_story)
df.load_transitions(fun_fact)
df.add_macros(macros)

if __name__ == '__main__':
    openai.api_key_path = utils.OPENAI_API_KEY_PATH
    df.run()