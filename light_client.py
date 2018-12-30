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
        
    y=0
    
    if msg.author == client.user:
        return    
        
    elif content == '!arty' or content.startswith('!arty '):
        y=1
        yield from client.send_typing(msg.channel)
        if content.rstrip() == '!arty':
            seed = bytes(" ", encoding='utf-8')
        else:
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
        

        yield from client.send_message(msg.channel, response)
        
    elif "@Arty" in content and "!arty" not in content:
        y=1
        yield from client.send_typing(msg.channel)
        seed = bytes(" ", encoding='utf-8')
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
        
        
        response = '{0.author.mention}'.format(msg) + response

        yield from client.send_message(msg.channel, response)
        
    elif content.startswith('!arty-pt'):
        y=1
        yield from client.send_typing(msg.channel)
        
        if content.rstrip() == '!arty-pt':
            response = '{0.author.mention}'.format(msg) + " " + "<:PogTard:518227662892957707>"
        
        else:
            response = ""
            
            for user in msg.mentions:
                response = response + user.mention + " "
            
            response = response + "<:PogTard:518227662892957707>"
        
        yield from client.send_message(msg.channel, response)
        
    elif content.startswith('!arty-pt'):
        y=1
        yield from client.send_typing(msg.channel)
        
        if content.rstrip() == '!arty-pt':
            response = '{0.author.mention}'.format(msg) + " " + "<:PogTard:518227662892957707>"
        
        else:
            response = ""
            
            for user in msg.mentions:
                response = response + user.mention + " "
            
            response = response + "<:PogTard:518227662892957707>"
        
        yield from client.send_message(msg.channel, response)
        
    elif '!arty' in content and y==0:
        yield from client.send_typing(msg.channel)
        response = '{0.author.mention}'.format(msg) + " " + "<:FailFish:462463087396782081>"
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
        
