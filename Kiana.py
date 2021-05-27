from twitchio.ext import commands
from Economy import Economy

Kiana = commands.Bot(
	irc_token = "<IRC_TOKEN>",
	client_id = "<CLIENT_ID>",
	nick = "<NICK>",
	prefix = "<PREFIX>",
	initial_channels = ["drunklockholmes"]
)

@Kiana.event
async def event_ready():
	print("Ready! - Kiana")

@Kiana.command(name = "ping", aliases = ["Ping"])
async def ping(ctx):
	await ctx.send("Pong!")

if __name__ == "__main__":
	Kiana.add_cog(Economy(Kiana))
	Kiana.run()
