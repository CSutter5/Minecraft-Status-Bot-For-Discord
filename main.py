from mcstatus import MinecraftServer
from discord.ext import commands
from discord import Embed
import discord
import os

class MinecraftBot(commands.Bot):
    def __init__(self, command_prefix, self_bot=False):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)

        self.server = MinecraftServer.lookup(os.getenv("ip"))
        self.ip = self.server.host + ":" + str(self.server.port)

        self.banned = ["https://tenor.com/view/fortnite-batman-dancing-dance-orange-justice-gif-16354903", "https://tenor.com/view/music-mood-beat-dance-turnip-the-beet-gif-12844742"]

        self.role = [["<@&837850925656834051>", "As a test role", "\N{EGG}"]]

        self.registerCommands()
        self.registerEvents()

    async def on_ready(self):
        print("Bot is now Online")

        #                                  Channel Id of Self Role 
        selfRoleChannel = self.get_channel(837850727656718357)


        #                                                     Message Id of Self Role 
        selfRoleMessage = await selfRoleChannel.fetch_message(840958907681472522) 
        
        for _, _, emoji in self.role:
            await selfRoleMessage.add_reaction(emoji)
        
        await self.wait_for('reaction_add', check=self.autoRole)

    def registerCommands(self):
        # ?status
        @self.command(name="status", help="Gives information about the server like, ping, number of people online, and minecraft version.", brief="Status and Info about Minecraft Server.")
        async def status(message):
            try:
                embed = Embed(title="Status")
                channel = message.channel

                mcstatus = self.server.status()

                embed.add_field(name="Server is Online",
                                value=self.ip,
                                inline=False)

                embed.add_field(name="Ping",
                                value=self.server.ping(),
                                inline=False)

                embed.add_field(name="Number of players online",
                                value="{} out of {}".format(mcstatus.players.online, mcstatus.players.max),
                                inline=True)

                embed.add_field(name="Minecraft Version", value=mcstatus.version.name, inline=False)

                await channel.send(embed=embed)

            except:
                embed = Embed(title="Status")
                embed.add_field(name="Server is Offline",
                                value=self.ip,
                                inline=False)
                await channel.send(embed=embed)

        # ?online
        @self.command(name="online", help="Shows the number of users online.", brief="Number of people online.")
        async def online(message):
            try:
                embed = Embed(title="Online")
                channel = message.channel

                mcstatus = self.server.status()

                embed.add_field(name="Number of people online",
                                value="{} out of {}".format(mcstatus.players.online, mcstatus.players.max),
                                inline=False)

                #embed.add_field(name="People online",
                #                value="{}".format(", ".join(mcstatus.players.names)),
                #                inline=False)

                await channel.send(embed=embed)

            except:
                pass

    def registerEvents(self):
        @self.event
        async def on_message(message):
            await self.process_commands(message)
            print(dir(message))
        
            for ban in self.banned:
                if (ban.lower() in message.content.lower()): 
                    print("Message By: {} It was deleted\n Content: {}".format(message.author, message.content))
                    await message.delete()
                    return

                
                '''elif len(message.attachements) > 0:
                    for attachement in message.attachements:
                        if ".gif" in attachement.filename.lower():
                            print("Gif")'''


    async def autoRole(self, *args):
        print("test")
        # Check to make sure its not a bot
        # Add user to that role
        pass

if __name__ == "__main__":
    bot = MinecraftBot(command_prefix="?")
    bot.run(os.getenv("TOKEN"))
