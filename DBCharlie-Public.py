import json

import discord
import mysql.connector
import re
from discord.ext.commands import bot

REACTIONROLECHANNELID = 0000000
SERVERID = 0000000000
WELCOMECHANNELID = 0000000
DELETEDMESSAGECHANNELID = 000000000
BOTTOKEN = ""

SERVER = None


def connect_sql():
    mydb = mysql.connector.connect(
        host="host",
        user="user",
        password="password",
        database='database'
    )
    return mydb


def disconnect_sql(connection):
    connection.disconnect()


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    global SERVER
    SERVER = discord.utils.get(bot.guilds, id=SERVERID)

    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="It's less broken"))


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == REACTIONROLECHANNELID:

        # custom emoji role adder
        custom_emoji_role_dict = {999999: "role name", 00000000: "role name"}

        for roleid in custom_emoji_role_dict:
            if payload.emoji.id == roleid:
                await payload.member.add_roles(discord.utils.get(SERVER.roles, name=custom_emoji_role_dict.get(roleid)))
                break

        builtin_emoji_role_dict = {"emoji name": "role name", "emoji name": "role name",
                                   "emoji name": "role name"}

        for roleid in builtin_emoji_role_dict:
            if payload.emoji.name == roleid:
                await payload.member.add_roles(
                    discord.utils.get(SERVER.roles, name=builtin_emoji_role_dict.get(roleid)))
                break


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(SERVER.channels, id=WELCOMECHANNELID)
    await channel.send("Sample Welcome Message")


@bot.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))

    if "Sample in-message trigger" in message.content.lower():
        await message.channel.send("Sample in-message response")

    if re.match("t.*e.*s.*t", message.content.lower()):
        emoji_to_add = discord.utils.get(message.author.guild.emojis, id=878813655406370847)
        await message.add_reaction(emoji_to_add)

    if message.content == "thisisastartupmessageandhopefullynoonetriggersit":
        embedVar = discord.Embed(title="This is where you obtain roles", description="", color=0x123456)
        embedVar.add_field(name="Simply react using the colour you want and you will receive that colour",
                           inline=False)
        await message.channel.send(embed=embedVar)

    if message.content.startswith("!create-command"):
        if message.author.id == SERVER.owner_id:
            processed = message.content.split(maxsplit=2)
            with open("commands.json", "r") as open_file:
                commands = json.load(open_file)
                commands[processed[1]] = processed[2]
            json_commands = json.dumps(commands)
            with open("commands.json", "w") as outfile:
                outfile.write(json_commands)
            embedVar = discord.Embed(title="Command Created",
                                     description="With trigger: " + processed[1] + " and response: " + processed[2],
                                     color=0x123456)
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

    if message.content[0] == "!" or message.content.lower()[0] == "e":
        mydb = connect_sql()
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM commands")
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[0] == message.content.lower():
                await message.channel.send(x[1])
        mycursor.close()
        disconnect_sql(mydb)

        mydb = connect_sql()
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("SELECT * FROM commandsThatDelete")
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[0] == message.content.lower():
                await message.delete()
                await message.channel.send(x[1])
        mycursor.close()
        disconnect_sql(mydb)


@bot.event
async def on_message_delete(message):
    if message.channel.id != DELETEDMESSAGECHANNELID:
        deleted_message_channel = discord.utils.get(SERVER.channels, id=DELETEDMESSAGECHANNELID)
        await deleted_message_channel.send(str(message.author) + ": " + message.content)
        for attachment in message.attachments:
            convert = await attachment.to_file(use_cached=True)
            await deleted_message_channel.send(file=convert)


bot.run(BOTTOKEN)
