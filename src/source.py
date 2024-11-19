import sys
import os
from configparser import ConfigParser, ParsingError
from src.vulpebot import discord_thread, new_token
from src.modules.socket_server import socket_server_thread

config = ConfigParser()

def verify_config():
    if os.path.isfile('./src/settings.ini') != True:
        print(f"[!] Error loading settings.ini\n")
        shutdown()

def init_launch():
    try:
        config.read("./src/settings.ini")
        if config['Init']['default'] == "True":
            new_token()
            update_init = config['Init']
            update_init['default'] = 'False'
            with open('./src/settings.ini', 'w') as config_file:
                config.write(config_file)
        return
    except (KeyError, ParsingError) as e:
        print(f"[!] Error reading settings.ini:\n[!] {e}\n\n")
        shutdown()

def shutdown():
    print("\n[x] Vulpe closed..")
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)

def main():
    os.system('clear')
    verify_config()
    init_launch()
    discord_thread()
    socket_server_thread()
