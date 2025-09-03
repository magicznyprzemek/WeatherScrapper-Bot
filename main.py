import discord
import os
import random
import scrapper
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
key = {"!pogoda"}
@client.event
async def on_ready():
    print('>Zalogowano jako: {0.user}'.format(client))
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  if any(word in msg for word in key):
    try:
      city=msg.split(' ', 1)[1]
      embed=scrapper.get_embed(city)
      await message.channel.send(embed=embed) 
    except:
     await message.channel.send(F"Nie znaleziono *{city}*")

client.run(os.getenv('TOKEN'))