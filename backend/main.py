from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette_discord import DiscordOAuthClient
import discord
from discord import User
from discord.ext import commands
import asyncio
import yaml
from fastapi_login import LoginManager
import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from datetime import timedelta, datetime
from typing import Dict


class NotAuthenticatedException(Exception):
    print("Unauthenticated access: Redirecting to log in page.")


with open("authentication.yaml", "r", encoding="utf8") as stream:
    yaml_data = yaml.safe_load(stream)

discord_client = DiscordOAuthClient(yaml_data['CLIENT_ID'], yaml_data['CLIENT_SECRET'],
                                    yaml_data['REDIRECT_URI'], scopes=('identify', 'guilds'))
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.command()
async def ping(ctx):
    # TODO: Testing function, should be removed in production.
    print("Command successfully executed.")
    await ctx.send('pong')


def get_mutual_guilds(user: User) -> Dict[int, str]:
    guild = {}
    for gld in user.mutual_guilds:
        guild[gld.id] = gld.name
    return guild


async def validate_session(request: Request, url: str):
    try:
        headers = {
            'Authorization': f"Bearer {request.cookies['Authentication']}",
        }

    except KeyError:
        raise NotAuthenticatedException

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.json()


def init_app():
    app = FastAPI(root_path='/api')

    @app.exception_handler(NotAuthenticatedException)
    def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
        return RedirectResponse(url=request.scope.get("root_path") + "/login")

    @app.exception_handler(ClientResponseError)
    def client_response_exception_handler(request: Request, exc: ClientResponseError):
        return RedirectResponse(url=request.scope.get("root_path") + "/login")

    @app.on_event("startup")
    async def startup_event():
        asyncio.create_task(bot.start(yaml_data['TOKEN']))
        print(f"{bot.user} has connected to Discord!")

    @app.get('/login')
    async def start_login():
        return discord_client.redirect()

    @app.get('/user')
    async def user(request: Request):
        resp = await validate_session(request, 'https://discord.com/api/users/@me')
        session = discord_client.session_from_token({"access_token": request.cookies['Authentication']})
        user = await session.identify()
        user_obj = bot.get_user(user.id)

        guild = {}

        if not user_obj.mutual_guilds:
            return {"Error": "The user does not share any mutual guilds with Klee."}
        for gld in user_obj.mutual_guilds:
            guild[gld.id] = gld.name
        resp["guilds"] = guild
        return resp

    @app.get('/guilds/{guild_id}')
    async def guild_roles(request: Request, guild_id: str):

        resp = await validate_session(request, 'https://discord.com/api/users/@me')
        session = discord_client.session_from_token({"access_token": request.cookies['Authentication']})
        user = await session.identify()
        user_obj = bot.get_user(user.id)
        resp["guilds"] = get_mutual_guilds(user_obj)

        if int(guild_id) not in resp["guilds"].keys():
            return {'Error': 'The user is not in the guild.'}

        role = dict((i.id, i.name) for i in bot.get_guild(int(guild_id)).roles)
        return role

    @app.get('/guilds/{guild_id}/{role_id}')
    async def get_role_members(request: Request, guild_id: str, role_id: str):

        resp = await validate_session(request, 'https://discord.com/api/users/@me')
        session = discord_client.session_from_token({"access_token": request.cookies['Authentication']})
        user = await session.identify()
        user_obj = bot.get_user(user.id)
        resp["guilds"] = get_mutual_guilds(user_obj)

        if int(guild_id) not in resp["guilds"].keys():
            return {'Error': 'The user is not in the guild.'}

        role = dict((i.id, i.name) for i in bot.get_guild(int(guild_id)).roles)

        if int(role_id) in role.keys():
            role_members = bot.get_guild(int(guild_id)).get_role(int(role_id)).members

            if not len(role_members):
                return {'Error': 'There are no members in the selected role.'}

            return dict(
                (i.id, {i.name, i.discriminator}) for i in role_members
                if not i.bot)
        else:
            return {'Error': 'The role provided is invalid.'}

    @app.get('/callback')
    async def finish_login(request: Request, code: str):
        session = discord_client.session(code)
        user = await session.identify()
        user_obj = bot.get_user(user.id)

        # Redirects back to homepage and sets the cookie with authentication header for the user.
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="Authentication", value=f"Bearer {session.token['access_token']}",
                            expires=int(datetime.timestamp(datetime.now() + timedelta(minutes=15))),
                            httponly=True, secure=True)

        # Includes the list of mutual guilds belonging to the user for frontend, just in case.
        guild = {}
        for gld in user_obj.mutual_guilds:
            guild[gld.id] = gld.name
        return response

    return app


app = init_app()
