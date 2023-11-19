from discord.ext import commands

class generic(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog: generic.py is ready")

    @commands.command()
    async def ping(self, ctx):
        """shows latency of the bot"""
        await ctx.send(f"Current latency: {self.client.latency}")

    @commands.command()
    async def repeat(self, ctx, expr):
        """repeats what you say"""
        await ctx.send(f"{expr}")

async def setup(client):
    await client.add_cog(generic(client))
