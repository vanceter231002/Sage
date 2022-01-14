import os
import random
from dotenv import load_dotenv
import discord
import requests
from bs4 import BeautifulSoup 
from discord.ext import commands
from tabulate import tabulate

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')#getting discord token from .env file

bot=commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')

#command created to give a random office quote
@bot.command(name='office', help="responds with a random quote from the office")
async def nine_nine(ctx):
    office_quotes=[("Sometimes I’ll start a sentence and I don’t even know where it’s going."
                   "I just hope I find it along the way."),
                   ("I’m not superstitious,"
                    "but I am a little stitious.."),
                    ("I wish there was a way to know you’re"
                     "in the good old days, before you’ve actually left them.")]
    response=random.choice(office_quotes)
    await ctx.send(response)
                                                        



#command created to stimulate rolling of dice
@bot.command(name="roll_dice", help="(!roll_dice {number_of_die} {number_of_sides}) to roll dice")

async def roll_dice(ctx,number_of_dice: int ,number_of_sides: int):
    response=""
    for i in range(number_of_dice):
        rand_int=random.choice(list(range(1,number_of_sides+1)))
        response+=str(rand_int)+" "  
    await ctx.send(response)
    
#a command to find horoscope for today based on zodiac sign
@bot.command(name="horoscope",help="(!horoscope {Zodiac Sign}) for your horoscope of today")

async def horoscope(ctx,zodiac_sign):
    zodiac_dictionary={"aries":1,"taurus":2,"gemini":3,"cancer":4,"leo":5,"virgo":6,"libra":7,"scorpio":8,
                       "sagittarius":9,"capricon":10,"aquarius":11,"pisces":12}
    url=f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={zodiac_dictionary[zodiac_sign.lower()]}"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,"html.parser")
    results=soup.find_all("div",class_="main-horoscope")[0]
    for line in results:
        try:
            if(str(line)[1]=="p"):
                for i in range(len(line.text)):
                    if(line.text[i]=="."):
                        flag=i
            await ctx.send(line.text[:flag+1])
            break
        except:
            pass
        
#command created to give a list of top 10 movies sorted by popularity from imdb
@bot.command(name="popular_movies",help="(!popular_movies) for listing the top 10 movies in imdb by popularity")

async def movies(ctx):
    url="https://www.imdb.com/search/title/?groups=top_250"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,"html.parser")
    results=soup.find(class_="lister list detail sub-list")
    movie_elements=results.find_all("div",class_="lister-item-content")
    data=[]
    for i in range(10):
        title_element=movie_elements[i].find("a")
        rating_element=movie_elements[i].find("div",class_="inline-block ratings-imdb-rating")["data-value"]
        data.append([title_element.text,rating_element])
    head=["Title","Imdb Rating"]    
    final_string=tabulate(data,headers=head,tablefmt="grid")
    final_string="`"+final_string+"`"
    await ctx.send(final_string)
    
bot.run(TOKEN)




