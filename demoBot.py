import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

TOKEN = 'MTE2Mzc1ODg1NTY1NDc1MjM2Ng.Goe6Pw.hbmKHFyDEXOGDIHma79TNaSOU5qN5mdCNYhAFA'

# oauth spotify client
mainID_oauth = SpotifyClientCredentials(client_id = '113ad026d252490b9b2efe6ec7765d9e', client_secret = '9739daf596c84ef297704cf73657c2b6')
sp = spotipy.Spotify(client_credentials_manager = mainID_oauth)

# setting discord intends
intents = discord.Intents.default()
intents.typing = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("The bot is online!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hi !! I'm a Bot.")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel()
    await channel.send('Welcome to the server {0.name}'.format(member))

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        voice_channel_id = ctx.author.voice.channel.id
        voice_channel = discord.utils.get(ctx.guild.voice_channels, id = int(voice_channel_id))
        await voice_channel.connect()
    else:
        await ctx.send('You aren\'t in a voice channel')

@bot.command()
async def leave(ctx):
    if ctx.author_client:
        
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Not in a voice channel")

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        return
    else:
        await ctx.send('Music isn\'t playing')

loop = False
nowplaying = ''
@bot.command()
async def play(ctx, query):
    voice_client = ctx.voice_client
    loop = False
    result = sp.search(q = query, type = 'track')
    if result['tracks']['items']:
        track_uri = result['tracks']['items'][0]['uri']
        nowplaying = track_uri
        voice_client.play(discord.FFmpegPCMAudio(track_uri))
    else:
        await ctx.send("Can't find this song")    

@bot.command()
async def loop(ctx):
    loop = True
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        current_song = voice_client.source.title
        while loop == True:
            await voice_client.play(discord.FFmpegPCMAudio(nowplaying))
    else:
        await ctx.send("None!")

@bot.command()
async def stoploop(ctx):
    if loop == True:
        loop = False
bot.run(TOKEN)
