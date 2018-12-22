import re, os

messages = []

timestamp_regex = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6} ')
emote_regex = re.compile(r'<:[A-Za-z0-9]*:[0-9]{18}>')

files = set(os.listdir('logs')) - {'logs_botcommands.txt', 'logs_content-feed.txt', 'logs_bottest.txt'}

for filename in files:

    with open('logs/'+filename) as file:
        msg = ""
        name = ""
        for line in file:
            if timestamp_regex.match(line):
                if len(msg.strip()):
                    if name in {'ArtificialChatter', 'Rythm', 'PenguBot', 'Dyno', 'Ayana', 'MEE6', 'Pepo'} or msg.startswith('!') or msg.startswith('?') or '@ArtificialChatter' in msg:
                        name=""
                        msg=""
                        continue
                    full_msg = (name+': '+msg).strip()
                    
                    replacements = []
                    for i in emote_regex.findall(full_msg):
                        replacements.append((i, i[1:i.index(':', 2)+1]))
                    
                    for i in replacements:
                        full_msg = full_msg.replace(*i)
                    
                    messages.append(full_msg)
                    name=""
                    msg=""
                    
                name = line[27:line.index(r'\n:')]
                msg = line[line.index(r'\n:')+4:]
                msg = msg.strip()+'\n'
            else:
                if not len(line.strip()):
                    continue
                msg += line.strip()+'\n'

with open('train_log', 'w') as file:
    file.write("\n".join([repr(i) for i in messages[::-1]]))
        
