import disnake
from disnake.ext import commands
from bs4 import BeautifulSoup
import requests

from n7_stats import N7_Stats_Module

intents = disnake.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Создаем экземпляр бота
intents = disnake.Intents.default()
intents.messages = True  # Разрешаем боту получать информацию о сообщениях
bot = commands.Bot(command_prefix='!', intents=intents)
token='MTE5ODUxMTkxMDAzNTkyMjk0NA.Gh8lPj.K6AuuOKlIG_HLLoM3ONpzd-3tYDLgVFkQozJbM'

bot.add_cog(N7_Stats_Module(bot))

# Запускаем бота
bot.run(token)