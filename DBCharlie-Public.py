import json

import discord
import asyncio
import random
from discord.ext.commands import bot



REACTIONROLECHANNELID = None
SERVERID = 0000000000
WELCOMECHANNELID = 0000000
DELETEDMESSAGECHANNEL = 000000000
BOTTOKEN = ""






SERVER = None


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    SERVER = discord.utils.get(bot.guilds, id=SERVERID)

    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="It's less broken"))


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == REACTIONROLECHANNELID:

        # custom emoji role adder
        custom_emoji_role_dict = {999999: "role name", 00000000: "role name"}

        for roleid in custom_emoji_role_dict:
            if payload.emoji.id == roleid:
                await payload.member.add_roles(discord.utils.get(SERVER.roles,name=custom_emoji_role_dict.get(roleid)))
                break

        builtin_emoji_role_dict = {"emoji name": "role name", "emoji name": "role name",
                     "emoji name": "role name"}

        for roleid in builtin_emoji_role_dict:
            if payload.emoji.name == roleid:
                await payload.member.add_roles(discord.utils.get(SERVER.roles,name=builtin_emoji_role_dict.get(roleid)))
                break





@bot.event
async def on_member_join(member):

    channel = discord.utils.get(SERVER.channels, id=WELCOMECHANNELID)
    await channel.send("")



@bot.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))

    if message.content == "thisisastartupmessageandhopefullynoonetriggersit":
        embedVar = discord.Embed(title="This is where you obtain roles", description="", color=0x123456)
        embedVar.add_field(name="Simply react using the colour you want and you will recieve that colour",
                           value="Please note that the colours are listed in order of decreasing strength " +
                                 "(i.e you will need to clear roles to obtain a colour on the right)",
                           inline=False)
        await message.channel.send(embed=embedVar)




    if message.content.startswith("!create-command"):
        if message.author.id == SERVER.owner_id:
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



@bot.event
async def on_message_delete(message):
    deleted_message_channel = discord.utils.get(SERVER.channels, id=DELETEDMESSAGECHANNEL)
    if message.channel != deleted_message_channel:
        await deleted_message_channel.send(str(message.author) + ": " + message.content)
        for attachment in message.attachments:
            convert = await attachment.to_file(use_cached=True)
            await deleted_message_channel.send(file=convert)


bot.run(BOTTOKEN)