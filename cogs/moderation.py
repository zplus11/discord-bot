import discord
from discord.ext import commands
import json
from datetime import datetime

with open("config.json", "r") as file:
    configurations = json.load(file)

log_channel_id = configurations["logs_channel"]
moderator_role = configurations["moderator_role"]
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log_channel_id = log_channel_id

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog: moderation.py is ready")

    @commands.command(aliases = ["nick", "setnick"])
    @commands.has_permissions(manage_nicknames = True)
    async def nickname(self, ctx, member: discord.Member, *, name: str = None):
        """changes the nickname of the provided user"""
        try:
            await member.edit(nick=name)
            message = f"Changed **{member.name}'s** nickname to **{name}**"
            log_channel = self.client.get_channel(log_channel_id)
            if name is None:
                message = f"Reset **{member.name}'s** nickname."
            await ctx.send(message)
            await log_channel.send(f":pencil: `{timestamp}`\n**{ctx.author}** changed **{member.name}**'s nickname to **{name}**.")
        except Exception as e:
            await ctx.send(e)
            # await log_channel.send(f":warning: `{timestamp}`\n**{ctx.author}** tried changing **{member.name}**'s nickname but an error occurred. [Jump to message]({ctx.message.jump_url}). Original message quoted below:\n> {ctx.message.content}")

    @commands.command(aliases = ["clear", "clean"])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, number:int = 1):
        """deletes given number of recent messages in chat. In absence of arguments, deletes the most recent message"""
        try:
            if number > 0 and number < 51:
                await ctx.channel.purge(limit = number + 1)
                await ctx.send(f"Deleted **{number + 1}** recent messages.")
                log_channel = self.client.get_channel(log_channel_id)
                await log_channel.send(f":white_check_mark: `{timestamp}`\n**{ctx.author}** has deleted **{number}** messages from <#{ctx.channel.id}>.")
            else:
                await ctx.send(":warning: Number of messages to delete cannot exceed 50 at a time.")
        except Exception as e:
            await ctx.send(e)
            
    @commands.command(aliases = [])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = ""):
        """kicks a member from the server"""
        reason = f"[Requested by {ctx.author}] " + reason
        message = f"Kicked **{member.name}** from the server. Reason: {reason}"
        if reason == "":
            message += f"N/A"
        try:
            await member.kick(reason = reason)
            await ctx.send(message)
            log_channel = self.client.get_channel(log_channel_id)
            await log_channel.send(f":boot: `{timestamp}`\n**{member.name}** was kicked from the server. **Reason:** {reason}")
        except Exception as e:
            await ctx.send(e)
            # await log_channel.send(f":warning: `{timestamp}`\n{ctx.author} tried kicking {member.name} from the server but an error occurred. [Jump to message]({ctx.message.jump_url}). Original message quoted below:\n> {ctx.message.content}")

    @commands.command(aliases = [])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = ""):
        """bans a member from the server"""
        reason = f"[Requested by {ctx.author}] " + reason
        message = f"Banned **{member.name}** from the server. Reason: {reason}"
        if reason == "":
            message += f"N/A"
        try:
            await member.ban(reason = reason)
            await ctx.send(message)
            log_channel = self.client.get_channel(log_channel_id)
            await log_channel.send(f":hammer: `{timestamp}`\n**{member.name}** was banned from the server. **Reason:** {reason}")
        except Exception as e:
            await ctx.send(e)
            # await log_channel.send(f":warning: `{timestamp}`\n{ctx.author} tried banning {member.name} from the server but an error occurred. [Jump to message]({ctx.message.jump_url}). Original message quoted below:\n> {ctx.message.content}")

    @commands.command(aliases = [])
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member: discord.Member, *, reason: str = ""):
        """unbans a member from the server"""
        reason = f"[Requested by {ctx.author}] " + reason
        message = f"Unbanned {member.name} from the server. Reason: {reason}"
        if reason == "":
            message += f"N/A"
        try:
            await member.unban(reason = reason)
            await ctx.send(message)
            log_channel = self.client.get_channel(log_channel_id)
            await log_channel.send(f":white_check_mark: `{timestamp}`\n**{member.name}** was unbanned from the server. **Reason:** {reason}")
        except Exception as e:
            await ctx.send(e)
            # await log_channel.send(f":warning: `{timestamp}`\n{ctx.author} tried unbanning {member.name} from the server but an error occurred. [Jump to message]({ctx.message.jump_url}). Original message quoted below:\n> {ctx.message.content}")
            
async def setup(client):
    await client.add_cog(moderation(client))
