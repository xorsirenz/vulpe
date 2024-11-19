import asyncio
import os
import threading
import discord
from discord.ext import commands
from configparser import ConfigParser, ParsingError
from src import source

config = ConfigParser()

def new_token():
    try:
        config.read("./src/settings.ini")
        token = input('[>] Enter discord bot token: ')
        os.system('clear')
        updated_token = config['Discord']
        updated_token['token'] = token
        with open('./src/settings.ini', 'w') as config_file:
            config.write(config_file)
        print('[*] Discord token added successfully')
        return token
    except (KeyError, ParsingError) as e:
        print(f"[!] Error reading settings.ini:\n[!] {e}\n\n")
        source.shutdown()

def load_token():
    config.read("./src/settings.ini")
    if config['Discord']['token'] != '':
        token = config['Discord']['token']
    else:
        token = new_token()
    return token

def discord_thread():
    dt = threading.Thread(target=run_bot)
    dt.daemon = True
    dt.start()

def run_bot():
    token = load_token()
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='-', intents=intents)

    @bot.event
    async def on_ready():
        print(f'\n[+] {bot.user} had successfully loaded\n[+] discord id: {bot.user.id}\n[>] ', end="")
    
    @bot.command(brief='// <extension>')
    async def load(ctx, extension):
        await bot.load_extension(f'src.cogs.{extension}')
        print(f'[+] Loaded extension: {extension}')

    @bot.command(brief='// <extension>')
    async def reload(ctx, extension):
        await bot.unload_extension(f'src.cogs.{extension}')
        await bot.load_extension(f'src.cogs.{extension}')
        await ctx.message.delete()
        print(f'[*] Reloaded extension: {extension}')

    @bot.command(brief='// <extension>')
    async def unload(ctx, extension):
        await bot.unload_extension(f'src.cogs.{extension}')
        print(f'[!] Unloaded extension: {extension}')

    async def load_ext():
        for file in os.listdir('./src/cogs'):
            if file.endswith('.py'):
                await bot.load_extension(f'src.cogs.{file[:-3]}')
                print(f'[+] loaded extension {file}')

    async def init_bot():
        try:
            async with bot:
                await load_ext()
                await bot.start(token)
        except discord.LoginFailure as e:
            print(f'\n[!] Vulpe Bot login error:\n{e}')
            source.shutdown()


    asyncio.run(init_bot())