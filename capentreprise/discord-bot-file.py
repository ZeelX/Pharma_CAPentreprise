import discord
import requests
from discord.ext import commands
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command()
async def fetchData(ctx):
    try:
        response = requests.get('YOUR_API_ENDPOINT')
        data = response.json()

        channel = bot.get_channel(YOUR_CHANNEL_ID)  # Remplacez YOUR_CHANNEL_ID par l'ID de votre channel

        await channel.send(f"Voici les données récupérées depuis l'API : {data}")

    except Exception as e:
        print('Erreur lors de la récupération des données depuis l\'API:', e)

# Remplacez 'YOUR_DISCORD_TOKEN' par le token de votre bot Discord
bot.run('MTIxNTI4NTUwOTY4MTg0ODMzMQ.Gxp8dc.OpVJ-8HJ2XaC8KDSf0vhZWicRyIw639mnWB4oE')
