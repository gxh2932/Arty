import discord
import asyncio, re, time
from model import create_model
from generate import generate_with_seed

model = create_model()
model.load_weights('arty.h5')

MAX_GEN_LEN = 300

with open('token.txt') as file:
    token = file.read()

loop = asyncio.get_event_loop()
client = discord.Client()

loop.run_until_complete(client.login(token))

reverse_emote_regex = re.compile(r':[a-zA-Z]+:')
emote_regex = re.compile(r'<:[a-zA-Z]+:[0-9]+>')

emote_dict = {}

def update_emotes():
    global emote_dict
    
    emote_dict = {}
    
    for emote in client.get_all_emojis():
        emote_dict[":"+emote.name+":"] = str(emote)
        emote_dict[str(emote)] = ":"+emote.name+":"

@client.event
@asyncio.coroutine
def on_ready():
    
    update_emotes()
    
    print('Ready')

@client.event
@asyncio.coroutine
def on_message(msg):
    
    content = msg.clean_content
    
    if msg.author == client.user or not (client.user.mentioned_in(msg) or content.startswith('!arty')):
        return
    
    for i, j in zip(emote_regex.findall(content), [i[1:i[2:].index(':')+3] for i in emote_regex.findall(content)]):
        content = content.replace(i, j)
        
    yield from client.send_typing(msg.channel)
    
    if content == '!arty' or content.startswith('!arty '):
        seed = bytes(content[5:].strip(), encoding='utf-8')

        model.reset_states()
        if content == '!arty':
            response = str(generate_with_seed(model, seed, MAX_GEN_LEN), encoding='utf-8', errors='backslashreplace').split(':',1)[1]
        else:
            response = str(generate_with_seed(model, seed, MAX_GEN_LEN), encoding='utf-8', errors='backslashreplace')

    elif content.startswith('!arty-pt'):
        print('hey')
        mentions = msg.mentions if msg.mentions else (msg.author.mention,)
        response = ' '.join(i.mention for i in mentions) + ' :PogTard:'

    elif client.user.mentioned_in(msg):
        seed = bytes("", encoding='utf-8')
        model.reset_states()
        response = str(generate_with_seed(model, seed, MAX_GEN_LEN), encoding='utf-8', errors='backslashreplace').split(':',1)[1]
    
        response = '{0.author.mention} {1}'.format(msg, response[1:])
        
    else:
        response = '{0.author.mention} :FailFish:'.format(msg)
        
    for potential_emote in set(reverse_emote_regex.findall(response)):
        if potential_emote in emote_dict:
            response = response.replace(potential_emote, emote_dict[potential_emote])
        
    for i in (str(msg.author)+': '+msg.clean_content).split('\n'):
        print('<<<', i)
    for i in response.split('\n'):
        print('>>>', i)
    
    yield from client.send_message(msg.channel, response)


while True:

    try:
        loop.run_until_complete(client.connect())
    except KeyboardInterrupt:
        break
    except:
        try:
            loop.run_until_complete(client.login(token))
        except:
            pass
        time.sleep(5)
        
