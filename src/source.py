import sys
import os
from configparser import ConfigParser, ParsingError
from src.server.discord_server import discord_thread
from src.server.socket_server import socket_server_thread

config = ConfigParser()

def verify_config():
    if os.path.isfile('./src/settings.ini') != True:
        os.system('clear')
        print(f"[!] Error loading settings.ini\n\n[-] Closing Vulpe..")
        sys.exit(130)

def init_launch():
    try:
        config.read("./src/settings.ini")
        if config['Init']['default'] == "True":
            token = input('[>] Enter discord bot token: ')
            os.system('clear')
            updated_token = config['Discord']
            updated_token['token'] = token
            update_init = config['Init']
            update_init['default'] = 'False'
            with open('./src/settings.ini', 'w') as config_file:
                config.write(config_file)
            print('[*] Discord token added successfully')
        return
    except (KeyError, ParsingError) as e:
        os.system('clear')
        print(f"[!] Error reading settings.ini:\n[!] {e}\n\n[-] Closing Vulpe..")
        sys.exit(130)

def main():
    verify_config()
    init_launch()
    discord_thread()
    socket_server_thread()
