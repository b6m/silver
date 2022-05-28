# author -> b6m
# date -> 2022/5/22
# enjoy

import discord
from discord.ext import commands
import json
import random
import string
import re
import httpx
from io import BytesIO

thumbnail = 'https://i.pinimg.com/originals/eb/01/15/eb011574e03abaa674e804eb2d5be0be.jpg'

with open('config.json') as f:
    config = json.load(f)

__guild__ = config['Discord']['Guild']
silver = commands.Bot(
    command_prefix=config['Discord']['Prefix'],
    case_insensitive=True,
    activity = discord.Streaming(name="silver | .help", url="https://twitch.tv/twitch"),
    help_command = None,
    intents = discord.Intents.all()
    )


keys = 'api_key_for_weleak_info_.to'


def admin(ctx):
    return str(ctx.author.id) in json.loads((open('data/admins.json', 'r')).read())

def access(ctx):
    return str(ctx.author.id) in json.loads((open('data/access.json', 'r')).read())

async def send_embed(ctx, title, description):
    embed = discord.Embed(title=title, description=description, color=0x33c4e1)
    embed.set_footer(text=ctx.author.name)
    embed.set_thumbnail(url=thumbnail)
    await ctx.reply(embed=embed)

async def send_errmbed(ctx, title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    embed.set_footer(text=ctx.author.name)
    embed.set_thumbnail(url=thumbnail)
    await ctx.reply(embed=embed) 


@silver.command()
async def gen(ctx):
    if not admin(ctx):
        return await send_errmbed(ctx, "Error", "You are not an admin!")

    else:
        key = random.choices(
            string.ascii_letters + string.digits,
            k = 16
        )
        keys = json.loads(
            open('data/keys.json', 'r').read()
        )
        key = ''.join(key)
        keys.append(key)
        with open('data/keys.json', 'w') as f:
            json.dump(keys, f)
        await send_embed(ctx, "Success", 'Check Your Dms!')
        direct_message = await ctx.author.create_dm()
        await direct_message.send(f'Your key is: {key}')


@silver.command()
async def redeem(ctx, key):
    if access(ctx):
        return await send_errmbed(ctx, "You are not an admin!", "You are not an admin!")

    else:
        keys = json.loads(open('data/keys.json', 'r').read())
        if key in keys:
            keys.remove(key)
            with open('data/keys.json', 'w') as f:
                json.dump(keys, f)
            with open('data/access.json', 'r') as f:
                access = json.load(f)
            access.append(str(ctx.author.id))
            await send_embed(ctx, "Success", "Key has been redeemed!")

@silver.command()
async def revoke(ctx, id):
    if not admin(ctx):
        return await send_errmbed(ctx, "Error", "You are not an admin!")

    else:
        access = json.loads(open('data/access.json', 'r').read())
        access.remove(id)
        with open('data/access.json', 'w') as f:
            json.dump(access, f)
            await send_embed(ctx, 'Success', f'{id} | Has Been Revoked!')

@silver.command()
async def email(ctx, email):
    if not access(ctx):
        return await send_errmbed(ctx, "Error", "You do not have access!")
    else:
        if re.fullmatch(
            re.compile(
                r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'),email
                ):
            async with httpx.AsyncClient() as client:
                data = await client.get(
                    f'https://api.weleakinfo.to/api?value={email}&type=email&key={keys}',
                    headers = {
                        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
                    }
                ).json()
                if data['status'] == 'success':
                    if data['found'] > 0:
                        passwords = []
                        for password in data['result']:
                            passwords.append(
                                {
                                    'name': password['line']
                                }
                            )
                        content = '\n'.join(
                            d['name'] for d in passwords
                        )
                        if len(passwords) > 10:
                            buffer = BytesIO(content.encode('utf-8'))
                            await ctx.reply(file=discord.File(buffer, filename='passwords.txt'))
                            return
                        else:
                            return await ctx.reply(f'```{content}```')

                else:
                    return await send_errmbed(ctx, f"Error", f"Something went wrong! | {data['error']}")

@silver.command()
async def passwords(ctx, name):
    if not access(ctx):
        return await send_errmbed(ctx, "Error", "You do not have access!")
    else:
        async with httpx.AsyncClient() as client:
            data = await client.get(
                f'https://api.weleakinfo.to/api?value={name}&type=name&key={keys}',
                headers = {
                    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
                }
            ).json()
            if data['status'] == 'success':
                if data['found'] > 0:
                    passwords = []
                    for password in data['result']:
                        passwords.append(
                            {
                                'name': password['line']
                            }
                        )
                    content = '\n'.join(
                        d['name'] for d in passwords
                    )
                    if len(passwords) > 10:
                        buffer = BytesIO(content.encode('utf-8'))
                        await ctx.reply(file=discord.File(buffer, filename='passwords.txt'))
                        return
                    else:
                        return await ctx.reply(f'```{content}```')
                else:
                    return await send_errmbed(ctx, "Error", f"{name} | No Passwords Found")
            else:
                return await send_errmbed(ctx, "Error", f"Something went wrong! | {data['error']}")


@silver.command()
async def start(ctx):
    if int(ctx.guild.id) == __guild__:
        if access(ctx):
            for channel in ctx.guild.channels:
                if channel.name == int(ctx.author.id):
                    return await send_errmbed(ctx, "Error", "You Already Have A Channel!")
                
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                    ctx.author: discord.PermissionOverwrite(read_messages=True),
                }
                channel = await ctx.guild.create_text_channel(
                    int(ctx.author.id),
                    overwrites = overwrites
                )
                await channel.send(f"Welcome {ctx.author.mention}")
                await send_embed(ctx, 'Success', f'{ctx.author.mention} Has Been Given A Priv Channel!')
        else:
            return await send_errmbed(ctx, "Error", "You do not have access!")


@silver.command()
async def close(ctx):
    if int(ctx.guild.id) == __guild__:
        if access(ctx):
            for channel in ctx.guild.channels:
                if channel.name == int(ctx.author.id):
                    await channel.delete()
                    await send_embed(ctx, 'Success', f'{ctx.author.mention} Has Been Closed!')

@silver.command()
async def clear(ctx):
    if not admin(ctx):
        return await send_errmbed(ctx, "Error", "You are not an admin!")

    else:
        if int(ctx.guild.id) == __guild__:
            for channel in ctx.guild.channels:
                if len(channel.name) == 18 and channel.name.isdigit():
                    await channel.delete()
                    await send_embed(ctx, 'Success', f'{channel.name} Has Been Closed!')
                else:
                    await send_errmbed(ctx, "Error", f"{channel.name} is not a valid channel!")

@silver.command()
async def help(ctx, command = None):
    if command == None:
        embed = discord.Embed(
                title = "Help",
                description = "List of Commands",
                colour = discord.Colour.blue()
            )
        embed.add_field(
                name = "Admin",
                value = "`clear`, `gen`, `revoke <id>`",
                inline = False
            )
        embed.add_field(
                name = "Access",
                value = "`email <email>`, `passwords <username>`, `id <username>`, `start`, `close`",
                inline = False
            )
        embed.add_field(
                name = "Other",
                value = '`redeem <key>`',
                inline = False
        )
        embed.set_footer(
                text = f"Requested by {ctx.author.name}"
            )
        await ctx.send(embed = embed)
    else:
        if command == 'gen':
            await send_embed(ctx, 'Help', '`gen` - Generates a new key')
        elif command == 'revoke':
            await send_embed(ctx, 'Help', '`revoke <id>` - Revokes a key')
        elif command == 'email':
            await send_embed(ctx, 'Help', '`email <email>` - Searches for passwords')
        elif command == 'passwords':
            await send_embed(ctx, 'Help', '`passwords <username>` - Searches for passwords')
        elif command == 'id':
            await send_embed(ctx, 'Help', '`id <username>` - Searches for users')
        elif command == 'start':
            await send_embed(ctx, 'Help', '`start` - Creates a private channel')
        elif command == 'close':
            await send_embed(ctx, 'Help', '`close` - Closes a private channel')
        elif command == 'redeem':
            await send_embed(ctx, 'Help', '`redeem <key>` - Redeems a access key')
        elif command == 'clear':
            await send_embed(ctx, 'Help', '`clear` - Closes all private channels')
        else:
            await send_errmbed(ctx, "Error", "Command Not Found")


    
@silver.command()
async def id(ctx, *, uv):
    if not access(ctx):
        return await send_errmbed(ctx, "Error", "You do not have access!")
    else:
        async with httpx.AsyncClient() as client:
            epic = await client.get(f"https://fortnite-api.com/v1/stats/br/v2?name={uv}&accountType=epic", headers={"Authorization": "063b9646-9a84-4566-ad3d-1a817863cf27"}).json()
            psn = await client.get(f"https://fortnite-api.com/v1/stats/br/v2?name={uv}&accountType=psn", headers={"Authorization": "063b9646-9a84-4566-ad3d-1a817863cf27"}).json()
            xbl = await client.get(f"https://fortnite-api.com/v1/stats/br/v2?name={uv}&accountType=xbl", headers={"Authorization": "063b9646-9a84-4566-ad3d-1a817863cf27"}).json()
            epic = epic['data']['account']['id'] if epic['data']['account'] != None else "Not Found"
            psn = psn['data']['account']['id'] if psn['data']['account'] != None else "Not Found"
            xbl = xbl['data']['account']['id'] if xbl['data']['account'] != None else "Not Found"
            embed = discord.Embed(
                title = f"{uv}",
                description = f"Epic: {epic}\nPSN: {psn}\nXBL: {xbl}",
                colour = discord.Colour.blue()
            )
            await ctx.send(embed = embed)

@silver.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await send_errmbed(ctx, "Error", "Command Not Found\nUse `help` To See A List Of Commands")
    elif isinstance(error, commands.MissingRequiredArgument):
        await send_errmbed(ctx, "Error", "Missing Required Argument\nUse `help` To See A List Of Commands")
if __name__ == '__main__':
    silver.run(config['Discord']['Token'])
