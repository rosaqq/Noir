class Cmd:

    def __init__(self, client, msg):
        self.client = client
        self.msg = msg

    async def play(self, sound: str):
        if not self.msg.author.voice_channel:
            return await self.client.send_message(self.msg.channel, 'You are not in a voice channel.')

        voice = self.client.voice_client_in(self.msg.server)
        if voice is None:
            voice = await self.client.join_voice_channel(self.msg.author.voice_channel)
        player = voice.create_ffmpeg_player('sounds/' + sound + '.mp3')
        player.start()
        return

    async def stop(self):
        voice = self.client.voice_client_in(self.msg.server)
        if voice is None:
            return await self.client.send_message(self.msg.channel, 'I\'m in a voice channel.')
        return await voice.disconnect()

    async def test(self):
        '''
        l = []
        for em in self.msg.server.emojis:
            l.append(em.name)

        for x,y in zip(l, self.msg.server.emojis):
            print(x, y)
        '''
        if 'SeckGasm' in [x.name for x in self.msg.server.emojis]:
            return await self.client.add_reaction(self.msg, 'SeckGasm:358591039902318592')
        else:
            return await self.client.add_reaction(self.msg, '👌')

    async def ping(self):
        return await self.client.send_message(self.msg.channel, 'pong')