# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from emora_stdm import DialogueFlow, Ngrams, Macro
from typing import Dict, Any, List
import json
import re


def MacroGetQuestionIntent(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r"(match)?(team)?")
        m = r.search(ngrams.text())
        if m is None: return False

        match = False
        if m.group(1):
            match = True

        if match:
            vars["TOPIC"] = "match"
        else:
            vars["TOPIC"] = "team"

        return True


def MacroGetKeyObs(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        return True


class MacroGetMatchStat(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        f = open("team_to_id.json")
        teams_dict = json.load(f)
        team_mentioned = []

        for team in teams_dict:
            if team in ngrams.raw_text():
                team_mentioned.append(team)

        vars["TEAM1"] = team_mentioned[0]
        vars["TEAM2"] = team_mentioned[1]

        return True


transitions = {
    'state': 'start',
    '`Hello. How can I help you?`': {
        '#GET_QUESTION_INTENT': {
            '`What `$TOPIC` do you want to talk about?`': 'end'
        }
    }
}

macros = {
    'GET_QUESTION_INTENT': MacroGetQuestionIntent()
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.add_macros(macros)

if __name__ == '__main__':
    df.run()
