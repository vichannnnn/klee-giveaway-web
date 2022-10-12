import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette_discord import DiscordOAuthClient
import discord
from discord.ext import commands
import asyncio
import yaml
from fastapi_login import LoginManager
import requests


class NotAuthenticatedException(Exception):
    print("Unauthenticated access: Redirecting to log in page.")


with open("authentication.yaml", "r", encoding="utf8") as stream:
    yaml_data = yaml.safe_load(stream)

redirect_uri = "http://dev.himaa.me/callback"
discord_client = DiscordOAuthClient(yaml_data['CLIENT_ID'], yaml_data['CLIENT_SECRET'],
                                    redirect_uri, scopes=('identify', 'guilds'))
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

manager = LoginManager('', token_url="/callback", use_cookie=True, custom_exception=NotAuthenticatedException)
manager.cookie_name = "Authentication"

@bot.command()
async def ping(ctx):
    print("Command successfully executed.")
    await ctx.send('pong')


def init_app():
    app = FastAPI()

    @app.exception_handler(NotAuthenticatedException)
    def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
        return RedirectResponse(url='/login')

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

    @app.get('/user')
    async def user(request: Request):
        headers = {
            'Authorization': f"Bearer {request.cookies['Authentication']}",
        }
        resp = requests.get('https://discord.com/api/users/@me', headers=headers).json()
        channel = bot.get_channel(936646790105673809)
        session = discord_client.session_from_token({"access_token": request.cookies['Authentication']})
        user = await session.identify()
        user_obj = bot.get_user(user.id)

        guild = {}
        for gld in user_obj.mutual_guilds:
            guild[gld.id] = gld.name

        resp["guilds"] = guild
        print(resp)
        return resp

    @app.get('/guilds/{guild_id}/')
    async def guild_roles(request: Request, guild_id: str):

        headers = {
            'Authorization': f"Bearer {request.cookies['Authentication']}",
        }
        resp = requests.get('https://discord.com/api/users/@me', headers=headers).json()
        channel = bot.get_channel(936646790105673809)
        session = discord_client.session_from_token({"access_token": request.cookies['Authentication']})
        user = await session.identify()
        user_obj = bot.get_user(user.id)

        guild = {}
        for gld in user_obj.mutual_guilds:
            guild[gld.id] = gld.name

        resp["guilds"] = guild

        if int(guild_id) not in guild.keys():
            return {'Error': 'The user is not in the guild.'}

        role = dict((i.id, i.name) for i in bot.get_guild(int(guild_id)).roles)
        return role

    @app.get('/guilds/{guild_id}/{role_id}')
    async def guild_roles(request: Request, guild_id: str, role_id: str):

        headers = {
            'Authorization': f"Bearer {request.cookies['Authentication']}",
        }
        resp = requests.get('https://discord.com/api/users/@me', headers=headers).json()
        channel = bot.get_channel(936646790105673809)
        session = discord_client.session_from_token({"access_token": request.cookies['Authentication']})
        user = await session.identify()
        user_obj = bot.get_user(user.id)

        guild = {}
        for gld in user_obj.mutual_guilds:
            guild[gld.id] = gld.name

        resp["guilds"] = guild

        if int(guild_id) not in guild.keys():
            return {'Error': 'The user is not in the guild.'}

        role = dict((i.id, i.name) for i in bot.get_guild(int(guild_id)).roles)

        if int(role_id) in role.keys():
            return dict((i.id, {i.name, i.discriminator}) for i in bot.get_guild(int(guild_id)).get_role(int(role_id)).members if not i.bot)


    @app.get('/callback')
    async def finish_login(request: Request, code: str):
        session = discord_client.session(code)
        user = await session.identify()
        user_obj = bot.get_user(user.id)

        response = RedirectResponse(url="/", status_code=302)
        manager.set_cookie(response, session.token['access_token'])

        guild = {}
        for gld in user_obj.mutual_guilds:
            guild[gld.id] = gld.name
        return response
    return app


app = init_app()
