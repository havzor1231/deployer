# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from emora_stdm import DialogueFlow

transitions = {
    'state': 'start',
    '`Hello. How can I help you?`': {

    }
}

macros = {

}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.add_macros(macros)

if __name__ == '__main__':
    df.run()

