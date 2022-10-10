import uvicorn
from fastapi import FastAPI, Request
from starlette_discord import DiscordOAuthClient
import discord
from discord.ext import commands
import asyncio
import yaml

with open("authentication.yaml", "r", encoding="utf8") as stream:
    yaml_data = yaml.safe_load(stream)

redirect_uri = "http://localhost:8000/callback"
discord_client = DiscordOAuthClient(yaml_data['CLIENT_ID'], yaml_data['CLIENT_SECRET'],
                                    redirect_uri, scopes=('identify', 'guilds'))
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(yaml_data['TOKEN']))
    print(f"{bot.user} has connected to Discord!")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/login')
async def start_login():
    return discord_client.redirect()


@bot.command()
async def ping(ctx):
    print("Command successfully executed.")
    await ctx.send('pong')


@app.get('/callback')
async def finish_login(code: str):
    session = discord_client.session(code)
    guilds = await session.guilds()
    user = await session.identify()
    token = session.token
    user_obj = bot.get_user(user.id)

    guild = {}
    for gld in user_obj.mutual_guilds:
        guild[gld.id] = gld.name

    resp = {
        'user': user,
        # 'token': token,
        'guilds': guild,
    }

    channel = bot.get_channel(936646790105673809)
    await channel.send(f"```\n{resp}\n```")
    return resp


if __name__ == "__main__":
    uvicorn.run("main:app", host="dev.himaa.me", port=80, reload=True)
