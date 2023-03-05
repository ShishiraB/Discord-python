import discord
import youtube_dl
from env.key import token

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '.hi':
        await message.channel.send('Namaste')
    
    
    if message.content.startswith('.play'):
        query = message.content.split(' ', 1)[1]
        voice_channel = message.author.voice.channel
        await voice_channel.connect()
        player = await play_music(query, voice_channel)
        await message.channel.send('Playing ' + player.title)

    if message.content.startswith('.stop'):
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                await vc.disconnect()

async def play_music(query, voice_channel):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['formats'][0]['url']
        title = info['title']
        vc = await voice_channel.connect()
        player = vc.play(discord.FFmpegPCMAudio(url))
        return player

client.run(token)
