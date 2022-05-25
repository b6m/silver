
# silver src 2.0

import httpx
import json
import re
import random
import string
import discord
from discord.ext import commands
from io import BytesIO
import time

keys = ["suckmyballsinthebathroom"]
client = commands.Bot(
    command_prefix=".",
    help_command=None,
    reconnect=True,
    activity=discord.Streaming(name="silver | .help", url="https://twitch.tv/twitch")
)

@client.event
async def on_ready():
    print("Silver is running")

@client.command()
async def gen(ctx, type="keys"):
    if ctx.author.id in json.loads(open("admins.json", "r").read()):
        key = random.choices(string.ascii_letters + string.digits, k=16)
        keys=json.loads(open("keys.json", "r").read())
        newkey = ""
        for lol in key:
            newkey += lol
        keys.append(newkey)
        with open('keys.json', 'w') as f:
            json.dump(keys, f)
        embed=discord.Embed(title="success", description="sent key to your dms!", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)
        await ctx.author.send(newkey)
    else:
        embed=discord.Embed(title="error", description="you are not an admin!", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)

@client.command()
async def redeem(ctx, key):
    if not ctx.author.id in json.loads(open("access.json", "r").read()):
        if key in json.loads(open("keys.json", "r").read()):
            keys=json.loads(open("keys.json", "r").read())
            keys.remove(key)
            with open('keys.json', 'w') as f:
                json.dump(keys, f)
            access=json.loads(open("access.json", "r").read())
            access.append(ctx.author.id)
            with open('access.json', 'w') as f:
                json.dump(access, f)
            embed=discord.Embed(title="success", description="reedemed your key!", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="error", description="key doesn't exist!", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="error", description="you already have access to silver!", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)

@client.command()
async def revoke(ctx, id):  
    if ctx.author.id in json.loads(open("admins.json", "r").read()):
        if int(id) in json.loads(open("access.json", "r").read()):
            access=json.loads(open("access.json", "r").read())
            access.remove(int(id))
            with open('access.json', 'w') as f:
                json.dump(access, f)
            embed=discord.Embed(title="success", description="removed premium from user!", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="error", description="user doesn't have premium!", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="error", description="you are not an admin!", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)

@client.command()
async def email(ctx, mail):
    if re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), mail):
        if int(ctx.author.id) in json.loads(open("access.json", "r").read()):
            async with httpx.AsyncClient() as client:
                info = await client.get(f'https://api.weleakinfo.to/api?value={mail}&type=email&key={random.choice(keys)}', headers={"user-agent": "Silver"}).json()
                if info["success"] == True:
                    if info["found"] > 0:
                        passwords = []
                        for elem in info['result']:
                            passwords.append({"name" : elem['line']})
                        content = '\n'.join(d['name'] for d in passwords)
                        if len(passwords) > 10:
                            buffer = BytesIO(content.encode('utf-8'))
                            file = discord.File(buffer, filename='passwords.txt')
                            embed=discord.Embed(title="success", description="please check the passwords using the file", color=0x33c4e1)
                            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                            embed.set_footer(text=ctx.author.name)
                            await ctx.send(embed=embed, file=file)
                            return
                        embed=discord.Embed(title="success", description="```" + content + "```", color=0x33c4e1)
                        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                        embed.set_footer(text=ctx.author.name)
                        await ctx.send(embed=embed, file=file)
                    else:
                        embed=discord.Embed(title="failed", description="no passwords found", color=0x33c4e1)
                        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                        embed.set_footer(text=ctx.author.name)
                        await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="failed", description=info["error"], color=0x33c4e1)
                    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                    embed.set_footer(text=ctx.author.name)
                    await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="error", description="you don't have access to silver!", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="error", description="thats not a valid email!", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)

@client.command()
async def passwords(ctx, user):
    if int(ctx.author.id) in json.loads(open("access.json", "r").read()):
        async with httpx.AsyncClient() as client:
            info=await client.get(f'https://api.weleakinfo.to/api?value={user}&type=email&key={random.choice(keys)}', headers={"user-agent": "Silver"}).json()
            if info["success"] == True:
                if info["found"] > 0:
                    passwords = []
                    for elem in info['result']:
                        passwords.append({"name" : elem['line']})
                    content = '\n'.join(d['name'] for d in passwords)
                    if len(passwords) > 10:
                        buffer = BytesIO(content.encode('utf-8'))
                        file = discord.File(buffer, filename='passwords.txt')
                        embed=discord.Embed(title="success", description="please check the passwords using the file", color=0x33c4e1)
                        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                        embed.set_footer(text=ctx.author.name)
                        await ctx.send(embed=embed, file=file)
                        return
                    embed=discord.Embed(title="success", description="```" + content + "```", color=0x33c4e1)
                    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                    embed.set_footer(text=ctx.author.name)
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="failed", description="no passwords found", color=0x33c4e1)
                    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                    embed.set_footer(text=ctx.author.name)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="failed", description=info["error"], color=0x33c4e1)
                embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                embed.set_footer(text=ctx.author.name)
                await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="error", description="you don't have access to silver!", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)

@client.command()
async def start(ctx):
    if int(ctx.guild.id) == 946141223612207154:
        if int(ctx.author.id) in json.loads(open("access.json", "r").read()):
            for channel in ctx.guild.channels:
                if channel.name == str(ctx.author.id):
                    embed=discord.Embed(title="error", description=f"you already have a priv channel in <#{channel.id}>", color=0x33c4e1)
                    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                    embed.set_footer(text=ctx.author.name)
                    await ctx.send(embed=embed)
                    return
            guild = ctx.guild
            user = ctx.message.author
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                user: discord.PermissionOverwrite(read_messages=True),
            }
            channel = await guild.create_text_channel(ctx.author.id, overwrites=overwrites)
            embed=discord.Embed(title="success", description=f"started private channel in <#{channel.id}>", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="error", description="you don't have access to silver!", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="error", description="this command only works in /bop", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)

@client.command()
async def close(ctx):
    if int(ctx.guild.id) == 946141223612207154:
        if int(ctx.author.id) in json.loads(open("access.json", "r").read()):
            for channel in ctx.guild.channels:
                if channel.name == str(ctx.author.id):
                    embed=discord.Embed(title="success", description=f"deleted <#{channel.id}>", color=0x33c4e1)
                    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
                    embed.set_footer(text=ctx.author.name)
                    await ctx.send(embed=embed)
                    time.sleep(1)
                    await channel.delete()
                    return
            embed=discord.Embed(title="error", description=f"couldn't find a priv channel", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="error", description="you don't have access to silver!", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="error", description="this command only works in /bop", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)
@client.command()
async def help(ctx):
    embed=discord.Embed(title="help", color=0x33c4e1)
    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
    embed.set_footer(text=ctx.author.name)
    embed.add_field(name=".leak", value="leakcheck cmds", inline=False)
    embed.add_field(name=".priv", value="priv cmds", inline=False)
    embed.add_field(name=".fn", value="fortnite cmds", inline=False)
    embed.add_field(name=".help", value="all cmds", inline=False)
    await ctx.send(embed=embed)
@client.command()
async def priv(ctx):
    embed=discord.Embed(title="priv cmds", color=0x33c4e1)
    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
    embed.set_footer(text=ctx.author.name)
    embed.add_field(name=".start", value="create a priv channel", inline=True)
    embed.add_field(name=".close", value="close a priv channel", inline=True)
    await ctx.send(embed=embed)
@client.command()
async def leak(ctx):
    embed=discord.Embed(title="leakcheck cmds", color=0x33c4e1)
    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
    embed.set_footer(text=ctx.author.name)
    embed.add_field(name=".email", value="leakcheck a email", inline=True)
    embed.add_field(name=".passwords", value="leakcheck a string/user", inline=True)
    await ctx.send(embed=embed)
@client.command()
async def fn(ctx):
    embed=discord.Embed(title="fortnite cmds", color=0x33c4e1)
    embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
    embed.set_footer(text=ctx.author.name)
    embed.add_field(name=".id", value="username to epic id", inline=True)
    embed.add_field(name=".cc", value="creator code to username", inline=True)
    await ctx.send(embed=embed)
@client.command()
async def id(ctx, *, uv):
  if int(ctx.author.id) in json.loads(open("access.json", "r").read()):
      async with httpx.AsyncClient() as client:
        epic = await client.get(f"https://fortnite-api.com/v1/stats/br/v2?name={uv}&accountType=epic", headers={"Authorization": "063b9646-9a84-4566-ad3d-1a817863cf27"}).json()
        psn = await client.get(f"https://fortnite-api.com/v1/stats/br/v2?name={uv}&accountType=psn", headers={"Authorization": "063b9646-9a84-4566-ad3d-1a817863cf27"}).json()
        xbl = await client.get(f"https://fortnite-api.com/v1/stats/br/v2?name={uv}&accountType=xbl", headers={"Authorization": "063b9646-9a84-4566-ad3d-1a817863cf27"}).json()
        if not epic["status"] == 200:
            epicid = "Couldn't Find ID"
        else:
            epicid = epic["data"]["account"]["id"]
        if not psn["status"] == 200:
            psnid = "Couldn't Find ID"
        else:
            psnid = psn["data"]["account"]["id"]
        if not xbl["status"] == 200:
            xblid = "Couldn't Find ID"
        else:
            xblid = xbl["data"]["account"]["id"]
        embed=discord.Embed(title=f"{uv}'s ids", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        embed.add_field(name="epic", value=epicid, inline=True)
        embed.add_field(name="psn", value=psnid, inline=True)
        embed.add_field(name="xbl", value=xblid, inline=True)
        await ctx.send(embed=embed)
  else:
        embed=discord.Embed(title="error", description="you don't have access to silver!", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)
@client.command()
async def cc(ctx, *, uv):
  if int(ctx.author.id) in json.loads(open("access.json", "r").read()):
      async with httpx.AsyncClient() as client:

        lol = await client.get(f"https://fortnite-api.com/v2/creatorcode?name={uv}", headers={"Authorization": "063b9646-9a84-4566-ad3d-1a817863cf27"}).json()
        if lol["status"] == 200:
            ccaccount=lol["data"]["account"]["name"]
            ccaccountid=lol["data"]["account"]["id"]
        embed=discord.Embed(title=f"{uv}'s ids", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        embed.add_field(name="username", value=ccaccount, inline=True)
        embed.add_field(name="id", value=ccaccountid, inline=True)
        await ctx.send(embed=embed)
  else:
        embed=discord.Embed(title="error", description="you don't have access to silver!", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)

@client.command()
async def clear(ctx):
    if int(ctx.guild.id) == 946141223612207154:
        if int(ctx.author.id) in json.loads(open("admins.json", "r").read()):
            for channel in ctx.guild.channels:
                if len(channel.name) == 18 and channel.name.isdigit():
                    await channel.delete()
            embed=discord.Embed(title="success", description="cleared all priv channels!", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="error", description="you aren't an admin", color=0x33c4e1)
            embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
            embed.set_footer(text=ctx.author.name)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="error", description="this command only works in /bop", color=0x33c4e1)
        embed.set_author(name="silver", url="https://discord.com/api/oauth2/authorize?client_id=972735257516331069&permissions=274878286928&scope=bot", icon_url="https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)
                

client.run("")
