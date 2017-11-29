import discord
import configparser
import logging
from Cmd import Cmd
from types import FunctionType

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()
config = configparser.ConfigParser()
config.read('secret.ini')

cs = 'noir'


async def parser(msg: str, cs: str):
    a = msg.replace(cs, '').split()
    return a[0], a[1:]


async def vjoin(msg):
    vo = client.voice_client_in(msg.server)
    if vo is None:
        vo = await client.join_voice_channel(msg.author.voice_channel)
    return vo


async def play(sound, msg):
    vo = await vjoin(msg)
    vo.create_ffmpeg_player('sounds/'+sound+'.mp3').start()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith(cs):
        cmd = Cmd(client, message)
        funcs = [x for x, y in Cmd.__dict__.items() if type(y) == FunctionType if not x.startswith('_')]
        com, args = await parser(message.content, cs)
        if com in funcs:
            try:
                await eval('cmd.' + com + '(*args)')
            except TypeError as meme:
                await client.send_message(message.channel, meme)
        else:
            await client.send_message(message.channel, 'No such command')







client.run(config['AUTH']['token'])