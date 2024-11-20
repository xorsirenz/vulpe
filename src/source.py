import os
import sys
from configparser import ConfigParser, ParsingError
from src.vulpebot import discord_thread
from src.modules.socket_server import socket_server_thread

config = ConfigParser()

def banner():
    ascii = """
                   ,--.
 ,--.  ,--.,--.,--.|  | ,---.  ,---.
  \  `'  / |  ||  ||  || .-. || .-. :
   \    /  '  ''  '|  || '-' '\   --.
    `--'    `----' `--'|  |-'  `----'
        [xorsirenz]    `--'
    """
    os.system('clear')
    print(ascii)

def verify_config():
    if os.path.isfile('./src/settings.ini') != True:
        print(f"\n[!] Error loading settings.ini")
        shutdown()

def update_default_config():
    try:
        config.read("./src/settings.ini")
        update_init = config['Init']
        update_init['default'] = 'False'
        with open('./src/settings.ini', 'w') as config_file:
            config.write(config_file)
        return
    except (KeyError, ParsingError) as e:
        print(f"\n[!] Error reading settings.ini:\n[!] {e}\n\n")
        shutdown()

def init_launch():
    try:
        config.read("./src/settings.ini")
        if config['Init']['default'] == "True":
            print("[!]Detected default settings.ini file\n\n[1] Setup new config\n[2] Use current config\n[3] Quit Vulpe")
            answer = input(f"[>] ")
            match (answer.lower()):
                case "1" | "y" | "yes":
                    update_default_config()
                case "2" | "n" | "no":
                    pass
                case "3" | "q" | "quit":
                    shutdown()
                case _:
                    print("\n[!] Command not recognized")
                    init_launch()
    except (KeyError, ParsingError) as e:
        print(f"\n[!] Error reading settings.ini:\n[!] {e}\n\n")
        shutdown()

def shutdown():
    print("\n[x] Vulpe closed..")
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)


def main():
    banner()
    init_launch()
    discord_thread()
    socket_server_thread()
