"""
MonBot v2 - bot Discord d'exemple pour ALPACA (mise à jour de test)
Commandes :
  !ping   ->  embed "Pong !" avec la latence, la mémoire et le temps en ligne
  !aide   ->  liste des commandes
  !info   ->  infos sur le serveur Discord actuel

Le token est fourni par ALPACA dans la variable d'environnement DISCORD_TOKEN.
"""
import math
import os
import time

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # nécessaire pour lire "!ping" (à activer aussi sur le portail Discord)

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
START_TIME = time.time()
VERSION = "2.0"
GREEN, BLURPLE = 0x57F287, 0x5865F2


def memory_mb():
    """Mémoire utilisée par le bot, en Mo."""
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) / 1024  # valeur en Ko
    except OSError:
        pass
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def uptime_text(seconds):
    """Durée lisible : '6 jours', '3 h 05', '12 min', '40 s'."""
    seconds = int(seconds)
    days, rest = divmod(seconds, 86400)
    hours, rest = divmod(rest, 3600)
    minutes, secs = divmod(rest, 60)
    if days:
        return f"{days} jour{'s' if days > 1 else ''}"
    if hours:
        return f"{hours} h {minutes:02d}"
    if minutes:
        return f"{minutes} min"
    return f"{secs} s"


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} (id {bot.user.id})")
    print(f"Présent sur {len(bot.guilds)} serveur(s)")
    print(f"MonBot version {VERSION} chargée : commandes !ping, !aide, !info")
    await bot.change_presence(activity=discord.Game(name="!aide"))


@bot.command(name="ping")
async def ping(ctx):
    latency = bot.latency * 1000
    latency_text = "…" if math.isnan(latency) or math.isinf(latency) else f"{round(latency)} ms"

    embed = discord.Embed(title="Pong !", color=GREEN)
    embed.add_field(name="Latence", value=latency_text, inline=True)
    embed.add_field(name="Mémoire", value=f"{round(memory_mb())} Mo", inline=True)
    embed.add_field(name="En ligne depuis", value=uptime_text(time.time() - START_TIME), inline=True)
    embed.set_footer(text=f"MonBot v{VERSION} · hébergé sur ALPACA")
    await ctx.send(embed=embed)


@bot.command(name="aide")
async def aide(ctx):
    embed = discord.Embed(title="Commandes de MonBot", color=BLURPLE,
                          description="Préfixe : `!`")
    embed.add_field(name="!ping", value="Latence, mémoire et temps en ligne du bot.", inline=False)
    embed.add_field(name="!info", value="Informations sur ce serveur.", inline=False)
    embed.add_field(name="!aide", value="Affiche ce message.", inline=False)
    embed.set_footer(text=f"MonBot v{VERSION}")
    await ctx.send(embed=embed)


@bot.command(name="info")
async def info(ctx):
    guild = ctx.guild
    if guild is None:
        await ctx.send("Cette commande fonctionne uniquement sur un serveur.")
        return
    embed = discord.Embed(title=guild.name, color=BLURPLE)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Membres", value=str(guild.member_count), inline=True)
    embed.add_field(name="Salons", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="Créé le", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.set_footer(text=f"MonBot v{VERSION}")
    await ctx.send(embed=embed)


if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN manquant : ajoute le token du bot dans ALPACA.")
    bot.run(token)
