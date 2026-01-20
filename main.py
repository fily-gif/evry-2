import discord
from discord.ext import commands
import config
import httpx
import asyncio
#! HACK: for some reason, py-cord doesnt make the loop..?
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
bot = discord.Bot()

async def get_song_info():
    async with httpx.AsyncClient() as web:
        response = await web.get("http://127.0.0.1:8080/api")
        return response.json() if response.status_code == 200 else None

@bot.slash_command()
async def hi(ctx):
    await ctx.defer()
    song = await get_song_info()
    await ctx.respond(f'currently listening to {song['title']} by {song['artist']} ({song['position']}/{song['duration']})')

@bot.event
async def on_ready():
    print(f'{bot.user} ({bot.user.id}) is ready!')
    print(f"owner(s): {', '.join(str(owner) for owner in config.bot_owner)}")

bot.run(config.bot_token)