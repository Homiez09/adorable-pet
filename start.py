# Made by Phumrapee Soenvanichakul (jannnn1235)
# Github: https://github.com/Jannnn1235/NENEbot

import discord
import os
import random
import typepet

from discord import Embed
from firebase import firebase
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

firebase = firebase.FirebaseApplication(
    os.getenv("URLDB"), None
)

blue = 0x84c5e6
yellow = 0xD4AC0D
green = 0x2ECC71
red = 0xC70039

client = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=discord.Intents().all())

@client.event
async def on_ready():
    print('{0.user}'.format(client), 'is ready')
    await client.change_presence(
        activity=discord.Game(
            name="!startpet"
        )
    )

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after >= 3600:
            embed = discord.Embed(description='**You need to wait {:.0f} hours'.format(error.retry_after/3600), color=0xC70039)
            await ctx.channel.send(embed=embed, delete_after=error.retry_after/3600)
        elif error.retry_after >= 360:
            embed = discord.Embed(description='**You need to wait {:.0f} minutes'.format(error.retry_after/60), color=0xC70039)
            await ctx.channel.send(embed=embed, delete_after=error.retry_after/60)
        else:
            embed = discord.Embed(description='**You need to wait {:.0f} seconds'.format(error.retry_after), color=0xC70039)
            await ctx.channel.send(embed=embed, delete_after=error.retry_after)

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.command()
async def howtoplay(message):
    ...

@client.command(name='startpet', aliases=['sp'])
@commands.cooldown(1,5,commands.BucketType.user)
async def startpet(message):
    result = firebase.get(os.getenv("DB"), '')
    #nametag = nametag
    #if nametag != "none" and len(nametag) <= 10:
    if not str(message.author.id) in result:
        playerdata = {
            "pet": [
                {
                    "name": "None",
                    "level": 0,
                    "happy": 0,
                    "id": random.randint(1,18),
                    "type": random.choice(typepet.typepet),
                },
            ],
            "inv":{
                    "nametag": 5
                    },
            "set": 1
        }

        result = firebase.put('dbcaat', str(message.author.id), playerdata)
        print(result)
        embed = discord.Embed(description="```You have been added to the database.\n!pet list(check pet id)\n!pet rename {id} {name}```", color=blue)
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(description="You already have a pet.", color=red)
        await message.channel.send(embed=embed)

    """ else:
        embed = discord.Embed(description="use !startpet <nametag>", color=red)
        embed.set_footer(text="A-Za-zก-ฮ limit 10 letter.")
        await message.channel.send(embed=embed) """

@client.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def pet(message, mode="none", set=0, rename="none"):
    result = firebase.get(os.getenv("DB"), '')
    mode = mode
    set = set
    if str(message.author.id) in result:
        num = int(result[str(message.author.id)]["set"])-1
        pic = result[str(message.author.id)]["pet"][num]["id"]
        typer = result[str(message.author.id)]["pet"][num]["type"]
        rn = rename
        urlp = f'https://raw.githubusercontent.com/Jannnn1235/adorable-pet/master/{typer}/{pic}.png'
        if mode == "none":
            embed = discord.Embed(title=f"{message.author.name}'s pet", color=blue)
            embed.add_field(name="Name", value=result[str(message.author.id)]["pet"][num]["name"], inline=False)
            embed.add_field(name="Lv", value=result[str(message.author.id)]["pet"][num]["level"], inline=True)
            embed.add_field(name="happy", value=result[str(message.author.id)]["pet"][num]["happy"], inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_image(url = urlp)
            await message.channel.send(embed=embed)
    
        elif mode == "set" and set > 0 and set <= len(result[str(message.author.id)]["pet"]):
            embed = discord.Embed(
                description=f'<@{message.author.id}>, Your pet is now {result[str(message.author.id)]["pet"][set-1]["name"]}', 
                color=green
                )
            await message.channel.send(embed=embed)

            result = firebase.put(f'/dbcaat/{message.author.id}', "set", set)

        elif mode == "list":
            embed = discord.Embed(title=f"{message.author.name}'s pet")         
            list(map(lambda x: embed.add_field(
                name="\u2705", value=f"id: {x+1} | {result[str(message.author.id)]['pet'][x]['name']}", 
                inline=False
                ), list(range(len(result[str(message.author.id)]["pet"])))))
            await message.channel.send(embed=embed)

        elif mode == "rename" and rename != "none":
            if result[str(message.author.id)]["inv"]["nametag"] > 0:
                embed = discord.Embed(
                    description=f'<@{message.author.id}>, You changed the name of your pet to ```{rn}```', 
                    color=green
                    )
                await message.channel.send(embed=embed)
                result = firebase.put(f'/dbcaat/{message.author.id}/inv', "nametag", int(result[str(message.author.id)]["inv"]["nametag"]) - 1)
                result = firebase.put(f'/dbcaat/{message.author.id}/pet/{set-1}', "name", rn)
            else:
                embed = discord.Embed(
                    description=f"<@{message.author.id}>, You don't have name tag.", 
                    color=red
                    )

        else:
            embed = discord.Embed(description="Error: Something is wrong | !pet help", color=red)
            await message.channel.send(embed=embed)
            
    else:
        embed = discord.Embed(description="Not found your data.", color=red)
        await message.channel.send(embed=embed)

@client.command(name='walk', aliases=['w', 'wa', 'ด', 'เดิน'])
@commands.cooldown(1,7200,commands.BucketType.user)
async def walk(message):
    result = firebase.get(os.getenv("DB"), '')
    if str(message.author.id) in result:
        eventw = random.randint(10,40)
        set = int(result[str(message.author.id)]["set"])
        namecat = result[str(message.author.id)]["pet"][set-1]["name"]

        updatedb = int(result[str(message.author.id)]["pet"][set-1]["happy"]) + eventw
        result = firebase.put(f'/dbcaat/{message.author.id}/pet/{set-1}', "happy", updatedb)

        f_embed = Embed(description="Walking...", color=yellow)
        n_embed = Embed(description=f'{namecat} got +{eventw} happy.', color=green)

        msg = await message.send(embed=f_embed)
        await msg.edit(embed=n_embed)
 
    else:
        embed = discord.Embed(description="Not found your data.", color=red)
        await message.channel.send(embed=embed)

@client.command(name='feed', aliases=['fed', 'eat'])
@commands.cooldown(1,3600,commands.BucketType.user)
async def feed(message):
    result = firebase.get(os.getenv("DB"), '')
    if str(message.author.id) in result:
        eventf = random.randint(2,10)
        set = int(result[str(message.author.id)]["set"])
        namecat = result[str(message.author.id)]["pet"][set-1]["name"]

        updatedb = int(result[str(message.author.id)]["pet"][set-1]["happy"]) + eventf
        result = firebase.put(f'/dbcaat/{message.author.id}/pet/{set-1}', "happy", updatedb)

        f_embed = Embed(description="eating...", color=yellow)
        n_embed = Embed(description=f'{namecat} got +{eventf} happy.', color=green)

        msg = await message.send(embed=f_embed)
        await msg.edit(embed=n_embed)
    else:
        embed = discord.Embed(description="Not found your data.", color=red)
        await message.channel.send(embed=embed)

@client.command(name='github', aliases=['git', 'gh'])
async def github(message):
    embed = discord.Embed(description=os.getenv("GITHUB"), color=red)
    await message.channel.send(embed=embed)

@client.command()
async def shop(message, mode="none", id=0, amount=1):
    if mode=="none":
        embed = Embed(
            title="Pet Shop",
            color=yellow,
            )
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Jannnn1235/LalisaMusicBot/master/assets/logo.gif")
        embed.add_field(
            name="═════════ cat ══════════",
            value="```1. cat egg (C)        200$\n2. cat egg (S)      1,000$```",
            inline=False
        )
        embed.add_field(
            name="═════════ dog ══════════",
            value="```1. dog egg (C)      1,000$\n2. dog egg (S)      5,000$```",
            inline=False
        )
        embed.add_field(
            name="To buy an item",
            value="!shop buy {id} {amount}",
            inline=False
        )
        embed.set_footer(text="Thank you.")

        await message.channel.send(embed=embed) 
    elif mode == "buy" and id != 0:
        print(f"{message.author.name} bought someting.")
        await message.channel.send("Closed.")

client.run(os.getenv("TOKEN"))