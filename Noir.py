import discord
import logging
import random
import time
import urllib.request
from chatterbot import ChatBot

# log code
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# static vars
client = discord.Client()
chatbot = ChatBot('Noir')
# these need to be global in on_message
pepe_time = 0


def file_to_list(name):
    try:
        f = open(name)
        a = f.read().splitlines()
        f.close()
    except IOError:
        g = open(name, 'w')
        g.close()
        a = []
    return a

mod_ids = file_to_list('mod_id.txt')
admin_ids = file_to_list('admin_id.txt')
allowed_channels = file_to_list('allowed_channel_id.txt')

# join new server derp code
if input('Configure?(y/n)') == 'y':
    if input('Join a new server?(y/n)') == 'y':
        invCode = input('Paste invite URL or code here: ')
        client.accept_invite(invCode)
    if input('Add new admin discord user ID?(y/n)') == 'y':
        new_id = input('Paste ID here: ')
        admin_ids.append(new_id)
        print('Current admin ID list: ' + str(admin_ids))
print('Connecting to discord servers...')


def list_to_file(file_name, save_list):
    file = open(file_name, 'w')
    for x in range(0, len(save_list)):
        file.write(save_list[x] + '\n')
    file.close()


def in_list(check_id, check_list):
    if check_id in check_list:
        return True
    else:
        return False


def remove_noir_mention(message):
    if message.find('<@' + client.user.id + '> ') == -1:
        return message.replace('<@' + client.user.id + '>', '')
    else:
        return message.replace('<@' + client.user.id + '> ', '')


def get_haiku():
    u = 'http://www.randomhaiku.com/'
    f = urllib.request.urlopen(u)
    cont = str(f.read())
    f.close()
    verso = []
    for i in range(0, 3):
        beg = cont.find('line') + 6
        end = cont.find('</div><')
        verso.append(cont[beg:end])
        cont = cont.replace('line', '', 1)
        cont = cont.replace('</div><', '', 1)
    return '```' + verso[0] + '\n' + verso[1] + '\n' + verso[2] + '\n' + '```'


def get_first_mention(message):
    return message.raw_mentions[0]


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    global pepe_time
    global mod_ids
    global allowed_channels
    author_id = message.author.id

    admin = in_list(author_id, admin_ids)
    mod = in_list(author_id, mod_ids)

    # add/remove channel IDs to allowed_channels
    if message.content.startswith('noir ') and (admin or mod):
        if message.content.startswith('come', 5):
            allowed_channels.append(message.channel.id)
            await client.send_message(message.channel, "I'm here")
        if message.content.startswith('leave', 5):
            allowed_channels.remove(message.channel.id)
            await client.send_message(message.channel, 'Call me when you need me.')

    # client.logout() on "noir kill"
    if message.content.startswith('noir ') and admin:
        if message.content.startswith('kill', 5):
            await client.send_file(message.channel, fp='img/okay.png')
            await client.logout()

    # check if message.channel in allowed_channels
    if in_list(message.channel.id, allowed_channels):

        # active commands ----------------------------------------------------------------------------------------------

        # ping pong
        if message.content.startswith('!ping'):
            await client.send_message(message.channel, 'pong!')

        # chat-bot reply
        if message.content.startswith('<@' + client.user.id + '> '):
            print('>' + remove_noir_mention(message.content))
            await client.send_message(message.channel, '<@' + message.author.id + '> ' +
                                      chatbot.get_response(remove_noir_mention(message.content)))

        # call-sign commands -------------------------------------------------------------------------------------------
        if message.content.startswith('noir '):

            # admin only commands --------------------------------------------------------------------------------------
            if admin:

                # add mod
                if message.content.startswith('add mod ', 5):
                    if message.get_raw_mentins()[0] in mod_ids:
                        await client.send_message(message.channel, '<@' + message.get_raw_mentions[0] +
                                                  '> is already a bot mod.')
                    else:
                        mod_ids.append(get_first_mention(message))
                        await client.send_message(message.channel, 'Added <@' + get_first_mention(message) +
                                                  '> as a bot mod.')

                # remove mod
                if message.content.startswith('del mod ', 5):
                    mod_ids.pop(mod_ids.index(get_first_mention(message)))
                    await client.send_message(message.channel, 'Removed <@' + get_first_mention(message) +
                                              '> as a bot mod.')

            # mod commands ---------------------------------------------------------------------------------------------
            if admin or mod:

                # change Playing" status
                if message.content.startswith('status', 5):
                    await client.change_status(game=discord.Game(name=message.content.replace('noir status ', '')))
                if message.content.startswith('status none', 5):
                    await client.change_status(game=None)

            # free commands --------------------------------------------------------------------------------------------

            # test if admin or mod
            if message.content.startswith('rank', 5):
                if author_id in mod_ids:
                    await client.send_message(message.channel, '<@' + author_id + '> you have bot mod rank.')
                elif author_id in admin_ids:
                    await client.send_message(message.channel, '<@' + author_id + '> you have bot admin rank.')
                else:
                    await client.send_message(message.channel, '<@' + author_id + '> you are just a dirty peasant')

            # help
            if message.content.startswith('help', 5):
                await client.send_message(message.channel, '<@' + author_id + '> `help is a lie.`')

            # reply with game
            if message.content.startswith('gimme game', 5):
                await client.send_message(message.channel, message.author.game)

            # reply message.author.id function
            if message.content.startswith('gimme id', 5):
                await client.send_message(message.channel,
                                          '<@' + message.author.id + '> ' + 'Your user ID is: ' + message.author.id)

            # pepe
            if message.content.startswith('pepe', 5):
                pepe_num = random.randint(1, 64)

                # rate limiter, check if time elapsed since last pepe > 10
                if time.time() - pepe_time > 10:
                    if message.content.startswith('<@', 10):
                        await client.send_message(message.channel, '<@' + get_first_mention(message) + '>')
                        await client.send_file(message.channel, fp='img/' + str(pepe_num) + '.png')
                        pepe_time = time.time()
                    else:
                        await client.send_message(message.channel, '<@' + author_id + '>')
                        await client.send_file(message.channel, fp='img/' + str(pepe_num) + '.png')
                        pepe_time = time.time()
                else:
                    await client.send_message(message.channel, '<@' + author_id +
                                              '> Wait at least 10 seconds between pepes please.')

            if message.content.startswith('haiku', 5):
                if message.content.startswith('<@', 11):
                    await client.send_message(message.channel,
                                              '<@' + get_first_mention(message) + '>\n' + get_haiku())
                else:
                    await client.send_message(message.channel, '<@' + author_id + '>\n' + get_haiku())

    list_to_file('mod_id.txt', mod_ids)
    list_to_file('admin_id.txt', admin_ids)
    list_to_file('allowed_channel_id.txt', allowed_channels)


client.run('seckbot@gmail.com', 'botlife929')
