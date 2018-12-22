import asyncio, discord

token = ''

assert len(token) > 0

loop = asyncio.get_event_loop()

client = discord.Client()


loop.run_until_complete(client.login(token))

@client.event
@asyncio.coroutine
def on_ready():
    channels = list(client.get_all_channels())
    text_channels = [i for i in channels if i.type==discord.ChannelType.text]
    
    print("server"+" "*9+"| channel"+" "*12+"| logs | read | send")
    for channel in text_channels:
        server, name, perms = channel.server, channel.name, channel.permissions_for(channel.server.me)
        print("{:<16} {:<20} {:<6} {:<6} {:<6}".format(str(server), name, str(perms.read_message_history), str(perms.read_messages), str(perms.send_messages)))
        
        # fix this shit, check server id instead
        
        if str(server) == 'Cleabum\'s abode' and perms.read_message_history:
            logs = client.logs_from(channel, limit=1e7)
            messages = []
            
            count = 0
            
            while True:
                try:
                    msg = yield from logs.__anext__()
                    messages.append(" ".join([str(msg.timestamp), str(msg.author.display_name)+'\\n:', str(msg.clean_content)]))
                    count += 1
                    if count % 10 == 0:
                        print('\r'*25+str(count)+' messages', end='')
                except StopAsyncIteration:
                    break
                
            with open('logs/logs_'+str(channel)+'.txt', 'w') as file:
                file.write('\n'.join(messages))
            print()
        
    loop.stop()

try:
    loop.run_until_complete(client.connect())
except RuntimeError:
    pass
