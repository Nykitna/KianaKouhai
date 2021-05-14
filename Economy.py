import random
import time
import KianaExceptions as ke

from twitchio.ext import commands
from KianaFileIO import KianaFileIO

@commands.cog()
class Economy:
	def __init__(self, bot: commands.Bot):
		self.bot = bot  # Required for class initiation
		self.file = KianaFileIO("data/economy.json")
		self.data = self.file.json_load()
		self.currency = "GAM3R CoinZ"
	
	@classmethod
	def sformat(cls, string):
		if string.startswith("@"):
			string = string[1:]
		return string.lower()
	
	def add_user(self, user):
		self.data[user] = {"wallet": 2000, "bank": 0}
		self.file.json_save(self.data)
	
	def get_v(self, user, key):
		return self.data[user].get(key)
	
	def set_v(self, user, key, value):
		self.data[user].update({key: value})
		self.file.json_save(self.data)
	
	async def verify(self, user, channel = "drunklockholmes"):
		self.sformat(user)
		chatters = await self.bot.get_chatters(channel)
		exp = chatters[1].count(user)
		if exp == 1:
			return True
		elif exp == 0:
			raise ke.UserNotFound()
	
	@commands.command(name = "balance", aliases = ["Balance", "Bal", "bal"])
	async def balance(self, ctx):
		user = ctx.message.author.name
		if user not in self.data:
			self.add_user()
		bankbal = self.get_v(user, "bank")
		walletbal = self.get_v(user, "wallet")
		await ctx.send(f"{user.capitalize()} has {walletbal} in their wallet and {bankbal} in their bank.")
	
	@commands.command(name = "deposit", aliases = ["Deposit"])
	async def deposit(self, ctx, amount):
		if amount.isnumeric() is True:
			amount = int(amount)
			user = ctx.message.author.name
			if user not in self.data:
				self.add_user(user)
			if amount != 0:
				bank = self.get_v(user, "bank")
				wallet = self.get_v(user, "wallet")
				if wallet >= amount:
					self.set_v(user, "wallet", (wallet - amount))
					self.set_v(user, "bank", (bank + amount))
					await ctx.send(f"{amount} transferred out of your bank!")
				else:
					await ctx.send("You don't have that much in your wallet!")
			elif amount == 0:
				await ctx.send("Depositing zero...Pointless.")
		else:
			await ctx.send("Error! Not a number! Did the operator enjoy this witticism?")
	
	@commands.command(name = "withdrawal", aliases = ["Withdrawal"])
	async def withdrawal(self, ctx, amount):
		if amount.isnumeric() is True:
			amount = int(amount)
			user = ctx.message.author.name
			if user not in self.data:
				self.add_user(user)
			if amount != 0:
				bank = self.get_v(user, "bank")
				wallet = self.get_v(user, "wallet")
				if bank >= amount:
					self.set_v(user, "wallet", (wallet + amount))
					self.set_v(user, "bank", (bank - amount))
					await ctx.send(f"{amount} transferred into your wallet!")
				else:
					await ctx.send("You don't have that much in your bank!")
			elif amount == 0:
				await ctx.send("Withdrawing zero...Pointless.")
		else:
			await ctx.send("Error! Not a number! Did the operator enjoy this witticism?")
	
	@commands.command(name = "give", aliases = ["Give"])
	async def give(self, ctx, amount, target):
		user = ctx.message.author.name
		if user not in self.data:
			self.add_user(user)
		if self.verify(target) is True:
			target = self.sformat(target)
			if target not in self.data:
				self.add_user(target)
		else:
			await ctx.send("User defined doesn't exist")
		if amount.isnumeric() is True:
			amount = int(amount)
			if amount != 0:
				walletu = self.get_v(user, "wallet")
				wallett = self.get_v(target, "wallet")
				if walletu >= amount:
					self.set_v(user, "wallet", (walletu - amount))
					self.set_v(target, "wallet", (wallett + amount))
					await ctx.send(f"{user} gave {target} {amount} {self.currency}")
			elif amount == 0:
				await ctx.send("Giving zero...that's not nice.")
		else:
			await ctx.send("Error! Not a number! Did the operator enjoy this witticism?")
	
	@commands.command(name = "rob", aliases = ["Rob"])
	async def rob(self, ctx, target):
		user = ctx.message.author.name
		if user not in self.data:
			self.add_user(user)
		if self.verify(target) is True:
			target = self.sformat(target)
			if target not in self.data:
				self.add_user(target)
		random.seed(time.time())
		if target != user:
			chances = random.randint(0, 300)
			if chances >= 275:
				walletu = self.get_v(user, "wallet")
				wallett = self.get_v(target, "wallet")
				amount = random.randint(1, wallett)
				self.set_v(user, "wallet", (walletu + amount))
				self.set_v(user, "wallet", (wallett - amount))
				await ctx.send(f"{user} robbed {target} of {amount} {self.currency}")
			elif chances >= 100:
				walletu = self.get_v(user, "wallet")
				wallett = self.get_v(target, "wallet")
				amount = random.randint(1, 100)
				if wallett > amount:
					self.set_v(user, "wallet", (walletu + amount))
					self.set_v(user, "wallet", (wallett - amount))
					await ctx.send(f"{user} robbed {target} of {amount} {self.currency}")
				elif wallett < amount:
					amount = random.randint(0, wallett)
					self.set_v(user, "wallet", (walletu + amount))
					self.set_v(user, "wallet", (wallett - amount))
					await ctx.send(f"{user} robbed {target} of {amount} {self.currency}")
				else:
					await ctx.send(f"{target} has no money to steal.")
			else:
				await ctx.send(f"{target} caught you. All you got was a black eye.")
		else:
			await ctx.send("You cannot rob yourself!")

	@commands.command(name = "gamble", aliases = ["Gamble"])
	async def gamble(self, ctx, amount):
		if amount.isnumeric() is True:
			user = ctx.message.author.name
			amount = int(amount)
			if user not in self.data:
				self.add_user(user)
			balance = self.get_v(user, "wallet")
			if balance >= amount:
				random.seed(time.time())
				chances = random.randint(0,1)
				if chances == 1:
					self.set_v(user, "wallet", balance + (amount * 2))
					await ctx.send(f"{user} won {amount * 2} {self.currency}!")
				else:
					self.set_v(user, "wallet", balance - amount)
					await ctx.send(f"{user} lost {amount} {self.currency}!")
			else:
				await ctx.send("You can't bet more than you have!")
		else:
			await ctx.send("Error! Not a number! Did the operator enjoy this witticism?")
