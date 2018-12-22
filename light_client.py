import discord
import asyncio, re, time
from model import create_model
from generate import generate_with_seed

model = create_model()
model.load_weights('arty.h5')

MAX_GEN_LEN = 300

token = ''

assert len(token) != 0

loop = asyncio.get_event_loop()
client = discord.Client()

loop.run_until_complete(client.login(token))

reverse_emote_regex = re.compile(r':[a-zA-Z]+:')
 
@client.event
@asyncio.coroutine
def on_ready():
    print('Ready')

@client.event
@asyncio.coroutine
def on_message(msg):

    content = msg.clean_content
    
    emote_regex = re.compile(r'<:[a-zA-Z]+:[0-9]+>')
    for i, j in zip(emote_regex.findall(content), [i[1:i[2:].index(':')+3] for i in emote_regex.findall(content)]):
        content = content.replace(i, j)
        
    if msg.author == client.user:
        return    
        
    elif content == '!arty' or content.startswith('!arty ') or "@Arty" in content:
        yield from client.send_typing(msg.channel)
        seed = bytes(content[5:].strip(), encoding='utf-8')
        model.reset_states()
        response = str(generate_with_seed(model, seed, MAX_GEN_LEN), encoding='utf-8', errors='backslashreplace')
        
        # fix this shit, it's O(n²)
        
        for potential_emote in set(reverse_emote_regex.findall(response)):
            for available_emote in list(client.get_all_emojis()):
                if potential_emote[1:-1] == available_emote.name:
                    response = response.replace(potential_emote, str(available_emote))
                    break
        
        for i in (str(msg.author)+': '+msg.clean_content).split('\n'):
            print('<<<', i)
        for i in response.split('\n'):
            print('>>>', i)
        
        if "@Arty" in content:
            response = '{0.author.mention}'.format(msg) + " " + response

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
        
