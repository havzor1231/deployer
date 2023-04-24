from emora_stdm import DialogueFlow

transitions = {
    'state': 'start',
    '`I watched the movie Babble recently! It\'s such an impressive movie. For me, in Babel,'
    'there are no villains, only victims of fate and circumstance, and most importantly, the victims of failed communications.'
    'Is there any moment of the movie that stands out to you?`': {
        '[{Abudullah, dad, father, goatherd}]': {
            '`I know. I really understand how parents would sacrifice everything to protect their children after watching this movie.`': 'opinion'
        },
        '[{Yussef, Ahmed, son, sons,boy,boys,children, brother, brothers,rifle,hassan}]': {
            '`Yeah. For me, the moment when the younger brother gave out the rifle is legendary. Without saying anything, his apology comes off the page.`': 'opinion'
        },
        '[{susan,richard,american,couple,wife,husband}]': {
            '`You know, I always find it very ironic how the couple really didn\'t not do well in talking to each other until Susan\'s life was threatened.'
            'I guess people truly open their hearts when they feel like they will not have a chance to be cordial to each other again haha.`': 'opinion'
        },
        '[{debbie,mike,children,nanny,mexican,mexico,amelia,nephew,santiago}]': {
            '`Yeah I always feel like Ameilia, Santiago,and Richard, they all had their intentions, not necessarily in a wrong way. But when they insist with their'
            'intentions, faults added up and lead to a irreversible bad consequence.`': 'opinion'
        },
        '[{chieko, wataya,yasujiro,japanese, japanese dad, japanese father, japanese daughter, japanese girl, japanese woman, kenji,mamiya, police}]': {
            '` Yeah, some of my friends were shocked when seeing Chieko throwing herself sexually to the police. But I guess it makes sense since the life of silence and being ignored is driving her to extremes.` ':'opinion'
        },
        'error':'opinion'
    }

}
opinion={
    'state':'opinion',
    '`For me, the most impressive moment is exactly when the boy gave out his gun, the gun that made everything start. Do you think there is anyone or anything that is essentially bad in this movie?`':{
        '[{japanese,japanese dad, japanese father, yasujiro, wataya}]':{
            '`I kinda think in the same way, if it was not him giving the gun, nothing would start. And he gave the gun to Morrocans,he didn\'t warn or teach them about using it wisely.`':'communication'
        },
        'error':{
            '`Right. I don\'t think anyone is seriously doing bad things. They are just a little off from their life, or, they are just not doing what other expect. But all the things aggregates to create ripple effects.`':'communication'
        }
    }
}
communication={
    'state':'communication',
    '`What do you think is a big theme of this movie?`':{
        '[{ripple, miscommunication, communication, understanding, misunderstanding}]':{
            '`I personally also think "miscommunication" kind of theme is the major melody of the movie. It is really not a matter of what language you speak, because the couple who speak the same'
            'language but still could not communicate well. But it is a matter of language, because you see how people exaggerate and randomly judge people who they don\'t linguistically understand.`':'rate'
        },
        'error':{
            '`I think that makes sense. Even more separated are cultures that do not share languages, values, frames of reference, or physical realities. `':'rate'
        }
    }
}

rate={
    'state':'rate',
    '`Overall, how do you think of this movie?`':{
        '/.*/':{
            '`That is insightful. Do you think the concept from this movie may help the development of AI and our chatbot?`':{
                 '/.*/':{
                     '` Thank you so much for your advice!`':'end'
                 },
            }

        }
    }
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.load_transitions(opinion)
df.load_transitions(communication)
df.load_transitions(rate)

if __name__ == '__main__':
    df.run()