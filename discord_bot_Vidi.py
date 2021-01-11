import requests
from bs4 import BeautifulSoup
import os
import schedule
import discord
from discord.ext import commands
import time

from dotenv import load_dotenv

load_dotenv('discord_info.env')
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='-')


def time_start():
    return "Stock Market Opens"


def time_stop():
    return "Stock Market Closes"


@bot.command(name='99')
async def loser_loser(ctx):
    await ctx.send('Loser')


@bot.command(name='stock')
async def stock_tesla(ctx, arg):
    news = requests.get('https://finance.yahoo.com/quote/{}/'.format(arg))
    page = news.content

    info = BeautifulSoup(page, 'lxml')

    final_info = info.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')

    try:
        gain = info.find_all('span', class_='Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)')
        print(gain[0])

    except IndexError:
        gain = info.find_all('span', class_='Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)')

    try:
        # Price
        s = str(final_info[0]).replace('<span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="50">', '')
        f = s.replace('<span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="33">', '')

        n = f.replace('</span>', '')
        u = n.replace(',', '')

        # Gain or Loss
        e = str(gain[0]).replace('<span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)" data-reactid="51">', '')
        g = e.replace('<span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)" data-reactid="51">', '')

        o = g.replace('<span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)" data-reactid="34">', '')
        l = o.replace('<span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)" data-reactid="34">', '')

        x = l.replace('</span>', '')

        # Check whether it has a price
        if float(u) >= 0:
            await ctx.send("**" + arg + ": " + n + "**")
            await ctx.send('`' + x + '`')
        else:
            await ctx.send('Invalid')

    except IndexError:
        await ctx.send('Not valid')


@bot.command(name='name_stock')
async def stock_name(ctx, arg):
    pass



#@bot.listen("on_message")
#async def on_message(message):
#    c = bot.get_channel(message)

#    if message.content == 'loop-time-start':
#        schedule.every().day.at("18:30").do(time_start)
#        # schedule.every().day.at("01:00").do(time_stop)
#        schedule.every().second.do(time_stop)
#        while True:
#            schedule.run_pending()
#            time.sleep(1)


bot.run(TOKEN)

