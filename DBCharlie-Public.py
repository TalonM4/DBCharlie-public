import json

import discord
import asyncio
import random
from discord.ext.commands import bot


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="It's less broken"))


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 757090693054201896:
        Among_Us = discord.utils.get(payload.member.guild.roles, name="Among Us")
        blue = discord.utils.get(payload.member.guild.roles, name="Blue")
        green = discord.utils.get(payload.member.guild.roles, name="Green")
        red = discord.utils.get(payload.member.guild.roles, name="Red")
        orange = discord.utils.get(payload.member.guild.roles, name="Orange")
        pink = discord.utils.get(payload.member.guild.roles, name="Pink")
        yellow = discord.utils.get(payload.member.guild.roles, name="Yellow")
        white = discord.utils.get(payload.member.guild.roles, name="White")
        brown = discord.utils.get(payload.member.guild.roles, name="Brown")
        cyan = discord.utils.get(payload.member.guild.roles, name="Cyan")
        turquoise = discord.utils.get(payload.member.guild.roles, name="Turquoise")

        role_dict = {"<:Orange:757310955817533521>": orange, "<:Red:757310294228861049>": red,
                     "<:Green:757310606524153896>": green, "<:Blue:757310582213836850>": blue,
                     "<:Among_Us:757479359471812710>": Among_Us, "<:Pink:759153160404598845>": pink,
                     "<:Yellow:759157709596524595>": yellow, "<:White:759261673906634772>": white,
                     "<:Brown:759261638288736306>": brown, "<:Cyan:759261608684814438>": cyan,
                     "<:Turquoise:759603495896088596>": turquoise}
        for role in role_dict:
            if str(payload.emoji) == role:
                await payload.member.add_roles(role_dict.get(role))
                break

        if str(payload.emoji) == "<:RedX:757655095763533914>":
            all_roles = [Among_Us, blue, green, red, orange, pink, yellow, white, brown, cyan, turquoise]
            for role in all_roles:
                await payload.member.remove_roles(role)

    if payload.channel_id == 767146533476630588:
        if payload.emoji.name == "❌":
            for channel in payload.member.guild.voice_channels:
                if len(channel.members) != 0:
                    for member in channel.members:
                        if channel.id != 767119448099782676:
                            await member.edit(mute=True)

    if payload.channel_id == 767146533476630588:
        if payload.emoji.name == "🎙️":
            for channel in payload.member.guild.voice_channels:
                if len(channel.members) != 0:
                    for member in channel.members:
                        await member.edit(mute=False)



@bot.event
async def on_member_join(member):

    channel = discord.utils.get(member.guild.channels, id=674455987188400140)
    if member.id != 757311999997771776:
        await channel.send("Welcome to the Edward's Official Only Fan's Discord Server " + member.mention +
                           ". Please ensure that you have https://onlyfans.com/edwardshumongousstrips "
                           "bookmarked for the opportunity "
                           "to interact with the legendary Edward. "
                           "If you require assistance please type `help`.")



@bot.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if message.content == "help":
        channel = message.channel
        await channel.send("How can I help you today?")
        await asyncio.sleep(10)
        await channel.send(
            "Jokes on you, that's above my paygrade." + "However, <@272531524648173569> will be happy to assist "
                                                        "you.")

    if message.content == "thisisastartupmessageandhopefullynoonetriggersit":
        embedVar = discord.Embed(title="This is where you obtain roles", description="", color=0x123456)
        embedVar.add_field(name="Simply react using the colour you want and you will recieve that colour",
                           value="Please note that the colours are listed in order of decreasing strength " +
                                 "(i.e you will need to clear roles to obtain a colour on the right)",
                           inline=False)
        await message.channel.send(embed=embedVar)


    if message.content.startswith("!among-us"):
        code = message.content[9:]
        for channel in message.author.guild.channels:
            if str(channel) == "among-us-notifs":
                embedVar = discord.Embed(title=" A New Among Us Game Has Started",
                                         description="The Code is " + code, color=0x123456)
                await channel.send(embed=embedVar)
                await channel.send("<@&757092321442660493>")

    if str(message.channel) == "talon-voice":
        strtosend = message.content
        await message.channel_mentions[0].send(strtosend[strtosend.index(' ') + 1:])

    if message.channel.id == 766542511702933525:
        to_kick = discord.utils.get(message.guild.members, display_name=message.content)
        if to_kick != None:
            await message.guild.kick(to_kick)
            to_delete = message.channel
            await to_delete.delete()

    if message.content.startswith("!create-command"):
        if str(message.author) == "TalonM4#4077":
            processedOnce = message.content[message.content.index(" ") + 1:]
            processedDefinition = processedOnce[processedOnce.index(" ") + 1:]
            processedKey = processedOnce[: processedOnce.index(" "):]
            with open("commands.json", "r") as open_file:
                commands = json.load(open_file)
                commands[processedKey] = processedDefinition
            json_commands = json.dumps(commands)
            with open("commands.json", "w") as outfile:
                outfile.write(json_commands)
            embedVar = discord.Embed(title="Command Created",
            description="With trigger: " + processedKey + " and response: " + processedDefinition, color=0x123456)
            await message.channel.send(embed=embedVar)



    with open("commands.json", "r") as open_command:
        commands = json.load(open_command)
        for key in commands:
            if key == message.content or key == message.content.lower():
                await message.channel.send(commands.get(key))

    with open("commandsdeleted.json", "r") as open_command:
        commandstd = json.load(open_command)
        for key in commandstd:
            if key == message.content or key == message.content.lower():
                await message.delete()
                await message.channel.send(commandstd.get(key))


    if message.content == "!mute-all":
        if message.author.id == 272531524648173569:
            for channel in message.author.guild.voice_channels:
                if len(channel.members) != 0:
                    for member in channel.members:
                        await member.edit(mute=True)

    if message.content == "!unmute-all":
        if message.author.id == 272531524648173569:
            for channel in message.author.guild.voice_channels:
                if len(channel.members) != 0:
                    for member in channel.members:
                        await member.edit(mute=False)

    if message.content == "!dead":
        invc = False
        for channel in message.author.guild.voice_channels:
            for member in channel.members:
                if member == message.author:
                    invc = True
        if invc:
            moveTo = discord.utils.get(message.guild.voice_channels, id=767119448099782676)
            await message.author.move_to(moveTo)
        else:
            await message.channel.send("You need to be in a VC.")

    if message.content == "!seth":
        await message.channel.send("image-url")

        if random.randrange(100) == 4:
            if message.author.dm_channel == None:
                await message.author.create_dm()

            await message.author.dm_channel.send("Roses are red"
                                                 "\nviolets are blue"
                                                 "\nyou don't like Seth"
                                                 "\nso I'll kick you")

            invite = await message.channel.create_invite(max_age = 120, max_uses = 1)

            await message.author.dm_channel.send(invite.url)

            await message.author.kick()


    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    for channel in message.author.guild.channels:
        if str(channel) == "deleted-messages":
            if str(message.channel) != "deleted-messages":
                await channel.send(str(message.author) + ": " + message.content)
                for attachment in message.attachments:
                    convert = await attachment.to_file(use_cached=True)
                    await channel.send(file=convert)


bot.run('')
