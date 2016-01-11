import discord
import logging
import random
import time
from chatterbot import ChatBot

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

chatbot = ChatBot('Noir')
client = discord.Client()
active = True
pepe_time = 0

mod_load = open('mod_id.txt')
mod_ids = mod_load.read().splitlines()
mod_load.close()

channel_load = open('channel_id.txt',)
channel_ids = channel_load.read().splitlines()
channel_load.close()

adminIds = ['128469181178970112']
client.login('seckbot@gmail.com', 'botsy999')

# join new server
if input('join? ') == 'y':
    invCode = input('Invite URL: ')
    client.accept_invite(invCode)


@client.event
def on_message(message):
    global active
    global mod_ids
    global channel_ids
    global pepe_time
    author_id = message.author.id

    # set mod
    if author_id in mod_ids:
        mod = True
    else:
        mod = False

    # set admin
    if author_id in adminIds:
        admin = True
    else:
        admin = False

    # set active by channel
    if message.channel.id in channel_ids:
        active = True
    else:
        active = False

    # DEFINING onlyContent: correctly removing the @Noir from message.content
    if message.content.find('<@134723912129839104> ') == -1:
        only_content = message.content.replace('<@134723912129839104>', '')
    else:
        only_content = message.content.replace('<@134723912129839104> ', '')

    # bot speak/no speak
    if message.content.startswith('noir ') and (admin or mod):
        if message.content.startswith('come', 5):
            channel_ids.append(message.channel.id)
            client.send_message(message.channel, "I'm here")
        if message.content.startswith('leave', 5):
            channel_ids.pop(channel_ids.index(message.channel.id))
            client.send_message(message.channel, 'Call me when you need me.')

    if message.content.startswith('noir ') and admin:
        if message.content.startswith('kill', 5):
            client.send_file(message.channel, fp='img/okay.jpg')
            client.logout()

    if active:
        if message.content.startswith('noir '):

            if admin:
                # add mod
                if message.content.startswith('add mod ', 5):
                    mod_ids.append(message.get_raw_mentions()[0])
                    client.send_message(message.channel, 'Added <@' + message.get_raw_mentions()[0] + '> as a bot mod.')
                # remove mod
                if message.content.startswith('del mod ', 5):
                    mod_ids.pop(mod_ids.index(message.get_raw_mentions()[0]))
                    client.send_message(message.channel,
                                        'Removed <@' + message.get_raw_mentions()[0] + '> as a bot mod.')
                # change status
                if message.content.startswith('status', 5):
                    client.change_status(game=discord.Game(name=message.content.replace('noir status ', '')))
                if message.content.startswith('status none', 5):
                    client.change_status(game=None)

            # help
            if message.content.startswith('help', 5):
                client.send_message(message.channel, '<@' + author_id + '> `help is a lie.`')
            # reply with game
            if message.content.startswith('gimme game', 5):
                client.send_message(message.channel, message.author.game)
            # reply message.author.id function
            if message.content.startswith('gimme id', 5):
                client.send_message(message.channel,
                                    '<@' + message.author.id + '> ' + 'Your user ID is: ' + message.author.id)
            # pepe me
            if message.content.startswith('pepe ', 5):
                pepe_num = random.randint(1, 56)
                if time.time() - pepe_time > 10:
                    if message.content.startswith('me', 10):
                        client.send_message(message.channel, '<@' + author_id + '>')
                        client.send_file(message.channel, fp='img/' + str(pepe_num) + '.png')
                        pepe_time = time.time()
                    else:
                        client.send_message(message.channel, '<@' + message.get_raw_mentions()[0] + '>')
                        client.send_file(message.channel, fp='img/' + str(pepe_num) + '.png')
                        pepe_time = time.time()
                else:
                    client.send_message(message.channel, '<@' + author_id +
                                        '> Wait at least 10 seconds between pepes please.')

        # ping pong
        if message.content.startswith('!ping'):
            if author_id == '108272892197806080':
                client.send_message(message.channel,
                                    'Here, have a special _pong_ just for you ' + message.author.mention())
            elif author_id == '95105078385446912':
                client.send_message(message.channel, 'For you, the greatest of all _pongs_, a Pong-Under-Blade ' +
                                    message.author.mention())
            elif message.content.startswith(' kiss', 5):
                client.send_message(message.channel, '<@' + author_id +
                                    '> sent you a Pong-Under-Blade <@95105078385446912>')
            else:
                client.send_message(message.channel, 'pong!')

        # chat-bot reply
        if message.content.startswith('<@134723912129839104> '):
            print('>' + only_content)
            client.send_message(message.channel, '<@' + message.author.id + '> ' + chatbot.get_response(only_content))

    mod_file = open('mod_id.txt', 'w')
    for mod_id_index in range(0, len(mod_ids)):
        mod_file.write(mod_ids[mod_id_index] + '\n')
    mod_file.close()

    channel_file = open('channel_id.txt', 'w')
    for channel_id_index in range(0, len(channel_ids)):
        channel_file.write(channel_ids[channel_id_index] + '\n')
    channel_file.close()


@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run()
