import discord
from discord.ext import commands
import re
import json
import random
import requests
import os
import asyncio

client = commands.Bot(command_prefix = ".", intents = discord.Intents.all())

with open("config.json", "r") as file:
    configurations = json.load(file)
token = configurations["bot_token"]

@client.event
async def on_ready():
    print("11n has loaded.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(token)    

asyncio.run(main())
