import requests
from bs4 import BeautifulSoup
from disnake import Embed, Color
from disnake.ext import commands
import datetime

class N7_Stats_Module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_player_info(self, name, platform):
        url = f'http://n7hq.masseffect.com/home/overview/?name={name}&platform={platform}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        player_info = self.extract_player_info(soup)
        return player_info

    def extract_player_info(self, soup):
        charactername_element = soup.select_one('.characterinfo .charactertext .charactername')
        character_name = charactername_element.contents[0].strip()
        character_title = charactername_element.contents[1].text.strip()
        extracted_player_info = {
            "Character Name": character_name,
            "Character Title": character_title,
            "Time Played": soup.select_one('.plstatstable .playerstat.pstimeplayed').text,
            "Games Played": soup.select_one('.plstatstable .playerstat.psgameplayed').text,
            "Credits": soup.select_one('.plstatstable .playerstat.pscredits').text,
            "N7 Rank": soup.select_one('.characterinfo .charactertext .n7rank').text,
            "Achievement Points": soup.select_one('.characterinfo .charactertext .pointscore').text
        }
        return extracted_player_info

    @commands.slash_command(
        name='n7_stats',
        description='Show Mass Effect 3 player stats'
    )
    async def n7stats_command(self, ctx, name: str = commands.Param(description='Type EA App nickname'), platform: str = commands.Param(description='Type platform where you play in: pc, xbox360 or ps3')):
        await ctx.response.defer()
        player_info = self.get_player_info(name, platform)
        platform_mapping = {
            'pc': 'PC Version',
            'xbox360': 'Xbox 360 Version',
            'ps3': 'PlayStation 3 Version'
        }
        platform_version = platform_mapping.get(platform.lower(), platform)

        embed = Embed(
            title="ME3 Player Stats",
            description=f"Информация об игроке :pencil: **{name}** на платформе :electric_plug: **{platform_version}**",
            color=Color.blue(),
            timestamp=datetime.datetime.now(),
        )

        embed.set_thumbnail(url="https://i.postimg.cc/vTxkD598/Nova-Corps-mass-effect.png")
        embed.set_author(
            name="Provided by N7 HQ",
            url=f"http://n7hq.masseffect.com/home/overview/?name={name}&platform={platform}",
            icon_url="https://n7hq.masseffect.com/resources/images/n7hq.png",
        )
        embed.set_footer(
            text="Type /n7_stats to check personal profile or someone else",
            icon_url="https://i.postimg.cc/vTxkD598/Nova-Corps-mass-effect.png",
        )

        embed.add_field(name=":pencil: **Player Name**", value=f"{player_info['Character Name']}", inline=True)
        embed.add_field(name=":pushpin: **Player Title**", value=f"{player_info['Character Title']}", inline=True)
        embed.add_field(name="\n", value="\n", inline=False)
        embed.add_field(name=":bar_chart: N7 Rank", value=f"{player_info['N7 Rank']}", inline=True)
        embed.add_field(name=":chart_with_upwards_trend: Achievement Points", value=f"{player_info['Achievement Points']}", inline=True)
        embed.add_field(name=":moneybag:Credits Amount", value=f"{player_info['Credits']}", inline=True)
        embed.add_field(name="\n", value="\n", inline=False)
        embed.add_field(name=":arrow_forward: Games Played", value=f"{player_info['Games Played']}", inline=True)
        embed.add_field(name=":clock3: Time Played", value=f"{player_info['Time Played']}", inline=True)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(N7_Stats_Module(bot))
