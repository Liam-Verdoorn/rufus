""" commands -- rufus.py """
import random
import config as c
import os.path
import urllib.request, json, webbrowser
import wolframalpha
import wikipedia
import requests
from googletrans import Translator
import time
from time import gmtime, strftime
import discord
from discord.ext import commands


class Commands:
    """ commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def len(self, *, string: str):
        """ Find length of string.
        """
        await self.bot.say('``' + str(len(str(string))) + '``')

    @commands.command()
    async def chars(self, *, string: str):
        """ Find amount of characters in a string, excludes spaces.
        """
        await self.bot.say('``' + str(len(str(string).replace(' ', '').replace('　', ''))) + '``')

    @commands.command(pass_context=True)
    async def roll(self, *, max: int):
        """ Rolls a random number. Default: 0-100.
        """
        if max <= 0:
            max = 100;
        droll = random.randint(0, max)
        if droll == 1:
            suffix = ''
        else:
            suffix = 's'
        if droll <= 0:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')
            await self.bot.say('You need to git gud, rolling isn\'t a joke -.-')
        elif droll == 100:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')
            await self.bot.say('GG!')
        else:
            await self.bot.say('```' + ctx.message.author.name +
                               ' rolls ' + str(droll) + ' point' + str(suffix) + '```')

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        """ Flip a coin.
        """
        cflip = random.choice(['Heads', 'Tails'])
        if cflip == 'Heads':
            await self.bot.add_reaction(ctx.message, '⚪')
            await self.bot.add_reaction(ctx.message, '🇭')
            # await self.bot.add_reaction(ctx.message, '🇪')
            # await self.bot.add_reaction(ctx.message, '🇦')
            # await self.bot.add_reaction(ctx.message, '🇩')
            # await self.bot.add_reaction(ctx.message, '🇸')
        elif cflip == 'Tails':
            await self.bot.add_reaction(ctx.message, '⚫')
            await self.bot.add_reaction(ctx.message, '🇹')
            # await self.bot.add_reaction(ctx.message, '🇦')
            # await self.bot.add_reaction(ctx.message, '🇮')
            # await self.bot.add_reaction(ctx.message, '🇱')
            # await self.bot.add_reaction(ctx.message, '🇸')

    @commands.command()
    async def btc(self):
        """ Show BitCoin price in USD.
        """
        BTC_URL = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        DATA = requests.get(BTC_URL).json()
        BTC_USD = DATA['bpi']['USD']['rate']
        await self.bot.say('```' + 'BTC price is currently at $' + BTC_USD + ' USD' + '```')

    @commands.command()
    async def trump(self, *, searchString: str = 'random'):
        """ Search the extensive database of Tronald Dump for rich knowledge.
        """
        if searchString == 'random':
            URL = 'https://api.tronalddump.io/random/quote'
            DATA = requests.get(URL).json()
            OUT = DATA['value']
            await self.bot.say(OUT)
        else:
            URL = 'https://api.tronalddump.io/search/quote?query={}'.format(searchString)
            DATA = requests.get(URL).json()
            COUNT = DATA['count']
            if COUNT <= 0:
                await self.bot.say('Sorry, Trump never said anything about ``{}``.'.format(searchString))
            else:
                OUT = DATA['_embedded']['quotes'][random.randint(0, COUNT-1)]['value']
                await self.bot.say(OUT)

    @commands.command()
    async def query(self, *, query: str = ''):
        """ Search wolfram alpha for query, if no answer is found, search Wikipedia.
        """
        try:
            client = wolframalpha.Client(c.wolfram_api_key)
            res = client.query(query)
            answer = next(res.results).text
            await self.bot.say(answer)
        except StopIteration:
            try:
                wikipedia.set_lang("en")
                await self.bot.say(wikipedia.summary(query))
            except Exception:
                await self.bot.say('Sorry, no matches were found for ``{}``.'.format(query))

    @commands.command()>translate jp ln dk
    async def translate(self, fromLanguage: str = '', toLanguage: str = '', *, text: str = ''):
        """ Search Google Translate.
        """
        translator = Translator()
        if fromLanguage == '' or toLanguage == '' or text == '':
            await self.bot.say('Missing information.')
        else:
            translatedList = translator.translate([text], src=fromLanguage, dest=toLanguage)
            for translated in translatedList:
                await self.bot.say(translated.origin, '->', translated.text)

    @commands.command(pass_context=True)
    async def poke(self, ctx, user: discord.User = '', *, message: str = ''):
        """ Poke user.
        """
        if user == '':
            await self.bot.say('GRRR..')
        else:
            if message == '':
                await self.bot.say('*{} poked {}*'.format(ctx.message.author.name, user))
            else:
                await self.bot.say('*{} poked {}; ``{}``*'.format(ctx.message.author.name, user, message))

    @commands.command(pass_context=True)
    async def pat(self, ctx, user: discord.User = '', *, message: str = ''):
        """ Pat user uwu.
        """
        if user == '':
            await self.bot.say('uwu')
        else:
            if message == '':
                await self.bot.say('*{} patted {} and is probably a disgusting weeb!*'.format(ctx.message.author.name, user))
            else:
                await self.bot.say('*{} patted {} {}*'.format(ctx.message.author.name, user, message))

    @commands.command(pass_context=True)
    async def hug(self, ctx, *, user: str = ''):
        """ Hug user.
        """
        mcont = ctx.message.content
        if user == '':
            await self.bot.say('*{} tries to hug the air*'.format(ctx.message.author.name))
        elif user == 'me':
            await self.bot.say('*I hugged {}*'.format(ctx.message.author.name))
        elif user == '<@{}>'.format(ctx.message.author.id):
            await self.bot.say('Aaaaaaall by myseeeeeeeelf.')
        elif user == '<@{}>'.format(self.bot.user.id):
            await self.bot.say(' OwO wat dis? Am I being hugger?' +
                               ' Hmmmm... always be a mystery it will')
        else:
            await self.bot.say('{} hugged {} :hearts:'.format(ctx.message.author.name, user))

    @commands.command()
    async def timer(self, *, seconds: int):
        """ Starts a countdown timer.
        """
        os = seconds
        msg = await self.bot.say('`` {} ``'.format(seconds))
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            await self.bot.edit_message(msg, '`` {} ``'.format(seconds))
        await self.bot.edit_message(msg, '`` Timer expired. ``')
        await self.bot.say('Time is up! {} seconds have passed.'.format(os))

    @commands.command(pass_context=True)
    async def echo(self, ctx, *, text: str):
        """ Make the bot say something.
        """
        await self.bot.delete_message(ctx.message)
        await self.bot.say(text)

    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.User = ''):
        """ User info.
        """
        if not user:
            user=ctx.message.author
        #userDescription = """
#id: {}
#nick: {}
#created at: {}
#joined at: {}
#game: {}
#top role: {}
#bot? {}
#avatar: {}
        #""".format(user.id, user.nick, user.created_at, user.joined_at, user.game, user.top_role, user.bot, user.avatar_url)
        embed=discord.Embed(title='{}#{}'.format(user.name, user.discriminator), color=0x114455)
        embed.set_thumbnail(url=(user.avatar_url))
        embed.set_footer(text=strftime("%d-%m-%Y %H:%M:%S", gmtime()))
        embed.add_field(name="id:", value=user.id, inline=False)
        embed.add_field(name="nick:", value=user.nick, inline=False)
        embed.add_field(name="created at:", value=user.created_at, inline=False)
        embed.add_field(name="joined at:", value=user.joined_at, inline=False)
        embed.add_field(name="game:", value=user.game, inline=False)
        embed.add_field(name="top role:", value=user.top_role, inline=False)
        embed.add_field(name="bot?", value=user.bot, inline=False)
        embed.add_field(name="avatar:", value=user.avatar_url, inline=False)
        await self.bot.say(embed=embed)


def setup(bot):
    """ defines setup """
    bot.add_cog(Commands(bot))
