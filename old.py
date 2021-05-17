from mcstatus import MinecraftServer
from discord.ext import commands
from threading import Thread
from flask import Flask
import discord
import socket
import os

app = Flask('')

s = socket.socket()

TOKEN = os.getenv("TOKEN")
ip = os.getenv("ip")
inviteChannelID = int(os.getenv("inviteChannelID"))

port = 25565
banned_gifs = [
    "https://tenor.com/view/fortnite-batman-dancing-dance-orange-justice-gif-16354903"
]
custom = 0  # 0 = None, 1 = Down for maintenance
prefix = '?'
invitesToAccept_User_ID = []
invitesToAccept_ID = []
client = commands.Bot(command_prefix=prefix, help_command=None)


def getStatus():
	run = 1
	s = socket.socket()

	if custom == 0:
		if run == 1:
			try:
				s.connect((ip, port))
				run = 3
				s = None
			except:
				run = 2

		if run == 2:
			return 0

		if run == 3:
			return 1

	if custom == 1:
		return 2


def checkWeb():
	run = 1
	s = socket.socket()

	if custom == 0:
		if run == 1:
			try:
				s.connect((ip, port))
				run = 3
				s = None
			except:
				run = 2

		if run == 2:
			return 'The server is not on! {}:{}'.format(ip, port)

		if run == 3:
			return 'Server is on! at {}:{}!'.format(ip, port)
	elif custom == 1:
		return 'Server is down for maintenance!'


@app.route('/')
def main():
	global ip, port

	return '''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
	<a>Server Status for </a>
	<a>{}:{}</a>
	<br>
	<a>{}</a>
    <title>Minecraft Server Status</title>
  </head>
</html>'''.format(ip, port, checkWeb())


def run():
	app.run(host="0.0.0.0", port=8080)


def keep_alive():
	server = Thread(target=run)
	server.start()


@client.event
async def on_ready():
	keep_alive()


@client.command()
async def status(message):
	channel = message.channel

	server = MinecraftServer.lookup(ip + ":" + str(port))
	mcstat = server.status()

	status = getStatus()
	embed = discord.Embed(title="Minecraft Server Status")

	if status == 0:
		embed.add_field(name="69.131.81.140:25565",
		                value="Offline",
		                inline=True)
	elif status == 1:
		embed.add_field(name="69.131.81.140:25565",
		                value="Online",
		                inline=True)
		embed.add_field(name="Number of player online",
		                value="{}".format(mcstat.players.online),
		                inline=False)
	elif status == 2:
		embed.add_field(name="69.131.81.140:25565",
		                value="Server is down for maintenance",
		                inline=True)

	await channel.send(embed=embed)


@client.command()
async def active(message):
	server = MinecraftServer.lookup(ip + ":" + str(port))
	mcstat = server.status()

	users = server.query()
	print(users.players.names)


@client.command()
async def link(message):
	channel = message.channel

	await channel.send("https://Minecraft-Status-Bot.pizzarules668.repl.co")


async def test(*args):
	if str(args[1]) == "Pizzarules668#3499":
		for id, usernameID in zip(invitesToAccept_ID, invitesToAccept_User_ID):
			if id == args[0].message.id:
				print(usernameID)
				user = client.get_user(usernameID)
				print(user)
				await user.create_dm()
				await user.dm_channel.send("Hi")
				invitesToAccept_ID.pop(invitesToAccept_ID.index(id))
				invitesToAccept_User_ID.pop(
				    invitesToAccept_User_ID.index(usernameID))


@client.command()
async def requestWhiteList(message, *args):
	channel = client.get_channel(inviteChannelID)
	embed = discord.Embed(title="New Request")

	if len(args) == 1:
		embed.add_field(name="Discord Username",
		                value=str(args[0]),
		                inline=False)
		embed.add_field(name="Requested By",
		                value=message.author,
		                inline=False)
		request = await channel.send(embed=embed)
		await request.add_reaction("👍")
		await client.wait_for('reaction_add', check=test)

		await message.channel.send("Your request has been sent")

	elif len(args) == 2:
		embed.add_field(name="Discord Username",
		                value=str(args[0]),
		                inline=False)
		embed.add_field(name="Minecraft Username",
		                value=str(args[1]),
		                inline=False)
		embed.add_field(name="Requested By",
		                value=message.author,
		                inline=False)

		request = await channel.send(embed=embed)
		invitesToAccept_ID.append(request.id)
		invitesToAccept_User_ID.append(message.author.id)

		await request.add_reaction("👍")
		await client.wait_for('reaction_add', check=test)

		await message.channel.send("Your request has been sent")

	elif len(args) > 2 or len(args) == 0:
		await message.channel.send(
		    "You need atleast 1 arguments but no more then 2\nIn this order\nThe users Discord Tag\nOptional: The users Minecraft Username"
		)


@client.command()
async def help(message):
	channel = message.channel

	embed = discord.Embed(title="Help")

	embed.add_field(
	    name="?status",
	    value=
	    "Tells you if the server is online and how many people are online",
	    inline=False)
	embed.add_field(name="?link",
	                value="Give you link to the bots website",
	                inline=False)
	embed.add_field(name="?help",
	                value="Will generator this message",
	                inline=False)

	await channel.send(embed=embed)


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	await client.process_commands(message)

	for banned in banned_gifs:
		if message.content == banned:
			print("Banned")
			await message.delete()


if __name__ == "__main__":
	client.run(TOKEN)
