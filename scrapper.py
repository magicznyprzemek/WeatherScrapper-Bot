import discord
import os
import random
import scrapper
from discord.ext import commands
from bs4 import BeautifulSoup as bs
import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
LANGUAGE = "pl-PL,pl;q=0.5"

def get_weather_data(city):
    url = F"https://www.google.com/search?q=weather+{city}"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    soup = bs(html.text, "html.parser")
    result = {}
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
    result['image'] = soup.find("img", {"id": "wob_tci"})["src"][6:]
    print(result['image'])
    return result
  
def farenheit_to_celsius(farenheit):
    celsius = (farenheit - 32) * 5/9
    return round(celsius, 1)
  
def get_embed(city):
  info=get_weather_data(city)
  descriptionString= F"Temperatura: **{farenheit_to_celsius(float(info['temp_now']))}°**"
  descriptionString+= F"\nPogoda: **{info['weather_now']}**"
  descriptionString+= F"\nOpady: **{info['precipitation']}**"
  descriptionString+= F"\nWilgotność: **{info['humidity']}**"
  descriptionString+= F"\nWiatr: **{info['wind']}**"
  embed=discord.Embed(title=info['region'], description=F"*{descriptionString}*", color=0x0000FF)
  embed.set_thumbnail(url=F"http://{info['image']}")
  return embed
