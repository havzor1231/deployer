import requests
from enum import Enum
from emora_stdm import DialogueFlow
from emora_stdm import Macro, Ngrams
from typing import Dict, Any, List
import openai
from typing import Dict, Any, List
import re
import os

transitions = {
    'state': 'start',
    '#GATE `Hi, I am dEPLoyer! Have you ever heard of Manchester United? `': {
        '[yes]': 'familiar',
        '[no]': 'unfamiliar',
        'error': 'fun_fact'
    },
    '#GATE `Hi, I am dEPLoyer! Pop quiz: Who was the 2022 EPL champion?`': {
        '[manchester city]': 'familiar',
        'error': 'unfamiliar',
    },
}

familiar = {
    'state': 'familiar',
    '`Do you watch EPL in your free time?`': {
        '[yes]': {
            ' I do too! Do you have a favorite team or a player?`': {
                '[yes]': {
                    '`I love him too.`': 'end'
                },
                '[no]': {
                    '`okay`': 'end'
                },
            }
        }

        '[no]': {
            '`Why do you not watch it?`': {
                '[not interested]': {
                    '`I love EPL for xxxxxxx, does this interest you?` ': {
                        '[yes]': 'end'
                    }
                }
                '[dont know]': 'introducing EPL'
            }
        },
    },
}
}

unfamiliar = {
'state': 'unfamiliar',
'`Manchester United is part of EPL.  The Premier League was founded in 1992, ' \
'replacing the First Division as the top tier of English football. Some of ' \
'the most famous players you might have heard of are _, _, _. Does this sound interesting to you?`': {

}

}
