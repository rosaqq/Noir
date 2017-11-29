import os

class Cmd:

    def __init__(self, client, msg):
        self.client = client
        self.msg = msg

    async def play(self, sound: str):
        """
        :param sound: string - name of sound to play

        available sounds are:
            +ayylmao
            +daddy
            +dedgiv
            +fainger
            +fky
            +god
            +manigga
            +niggahehe
            +soge
            +timefodat"""
        if not self.msg.author.voice_channel:
            return await self.client.send_message(self.msg.channel, 'You are not in a voice channel.')

        voice = self.client.voice_client_in(self.msg.server)
        if voice is None:
            voice = await self.client.join_voice_channel(self.msg.author.voice_channel)
        if sound not in os.listdir('sounds'):
            return await self.client.send_message(self.msg.channel, 'No such sound.')
        player = voice.create_ffmpeg_player('sounds/' + sound + '.mp3')
        player.start()
        return

    async def stop(self):
        """
        disconnects from voice channel"""
        voice = self.client.voice_client_in(self.msg.server)
        if voice is None:
            return await self.client.send_message(self.msg.channel, 'I\'m not in a voice channel.')
        return await voice.disconnect()

    async def test(self):
        """
        test function"""
        if 'SeckGasm' in [x.name for x in self.msg.server.emojis]:
            return await self.client.add_reaction(self.msg, 'SeckGasm:358591039902318592')
        else:
            return await self.client.add_reaction(self.msg, '👌')

    async def ping(self):
        """
        try it"""
        return await self.client.send_message(self.msg.channel, 'pong')