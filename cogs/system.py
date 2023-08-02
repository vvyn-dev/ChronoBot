import httpx
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord.commands import slash_command
import psutil
import time

load_dotenv("../.env")
PTERO_KEY = os.getenv("API_TOKEN")


class Sys_info(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="system", description="Shows system info and performance")
    async def system(self, ctx):
        await ctx.defer()
        header = {"Authorization": f"Bearer {PTERO_KEY}", "User-Agent": "DBH"}
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://panel.danbot.host/api/client/servers/6b8c2da7/resources",
                headers=header,
            )
            data = r.json()
        embed = discord.Embed(title="Bot resources usage:", color=0x008B8B)
        embed.add_field(
            name="<:cpu:1136195600770158652> CPU Absoulute Usage (%)",
            value=data["attributes"]["resources"]["cpu_absolute"],
            inline=False,
        )
        embed.add_field(
            name="<:ram1:1136195409295966239> Ram Usage (MB)",
            value=f'{round(data["attributes"]["resources"]["memory_bytes"] / (1024 * 1024))}MB',
            inline=False,
        )
        embed.add_field(
            name="<:floppydisk:1136195809856208968> Disk Usage (MB)",
            value=f'{round(data["attributes"]["resources"]["disk_bytes"] / (1024 * 1024))}MB',
            inline=False,
        )
        embed.add_field(
            name="<:accept:1136196178443243520> Uptime (hour)",
            value=f'{round(data["attributes"]["resources"]["uptime"] / (1000 * 60 * 60))}hr',
            inline=False,
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Sys_info(bot))
