import json

from time import time
from random import randint, seed
from twitchio.ext import commands

@commands.cog()
class Economy:
	def __init__(self, bot):
		self.bot = bot
		self.currency = "GAM3R CoinZ"
		self.data = None

	def start(self):
		with open("data/economy.json", "r") as f:
			self.data = json.load(f)
			f.close()
	
	def save(self):
		with open("data/economy.json", "w") as f:
			json.dump(self.data, f, indent = 4)
			f.close()

	def get(self, name, value):
		return self.data[name].get(value)
	
	def add(self, name):
		self.data[name] = {"wallet": 2000, "bank": 0}

	def update(self, name, wallet_val = None, bank_val = None):
		if bank_val == None:
			self.data[name].update({"wallet": wallet_val})
		elif wallet_val == None:
			self.data[name].update({"bank": bank_val})
		else:
			self.data[name].update({"wallet": wallet_val})
			self.data[name].update({"bank": bank_val})

	# Revised!
	@commands.command(name = "balance", aliases = ["Balance"])
	async def balance(self, ctx):
		user = ctx.message.author.name
		if user not in self.data:
			self.add(user)
			self.save()
			pass
		bank_balance = self.get(user, "bank")
		wallet_balance = self.get(user, "wallet")
		await ctx.send(f"You have {bank_balance} in your bank and {wallet_balance} in your wallet @{user}!")


	@commands.command(name = "deposit", aliases = ["Deposit"])
	async def deposit(self, ctx, amount):
		user = ctx.message.author.name
		if user not in self.data:
			self.add(user)
			self.save()
			pass
		try:
			amount = int(amount)
			if amount > 0:
				current_wallet = self.get(user, "wallet")
				if current_wallet >= amount:
					new_bank =	self.get(user, "bank") + amount
					new_wallet = self.get(user, "wallet") - amount
					self.update(user, bank_val = new_bank)
					self.update(user, wallet_val = new_wallet)
					self.save()
					await ctx.send(f"{amount} transfered to your bank!")
				else:
					await ctx.send("You don't have that much in your wallet!")
			elif amount < 0:
				amount = abs(amount)
				current_bank = self.get(user, "bank")
				if current_bank >= amount:
					new_wallet = self.get(user, "wallet") + amount
					new_bank = self.get(user, "bank") - amount
					self.update(user, wallet_val = new_wallet)
					self.update(user, bank_val = new_bank)
					self.save()
					await ctx.send(f"{amount} transfered out of your bank!")
				else:
					await ctx.send("You don't have that much in your bank!")
			else:
				await ctx.send("You can't deposit zero silly!")
		except Exception:
			await ctx.send("Send a valid number.")

	@commands.command(name = "withdrawal", aliases = ["Withdrawal"])
	async def withdrawal(self, ctx, amount):
		user = ctx.message.author.name
		if user not in self.data:
			self.add(user)
			self.save()
			pass
		try:
			amount = int(amount)
			if amount > 0:
				current_bank = self.get(user, "bank")
				if current_bank >= amount:
					new_wallet = self.get(user, "wallet") + amount
					new_bank = self.get(user, "bank") - amount
					self.update(user, wallet_val = new_wallet)
					self.update(user, bank_val = new_bank)
					self.save()
					await ctx.send(f"{amount} transfered out of your bank!")
				else:
					await ctx.send("You don't have that much in your bank!")
			elif amount < 0:
				amount = abs(amount)
				current_wallet = self.get(user, "wallet")
				if current_wallet >= amount:
					new_bank = self.get(user, "bank") + amount
					new_wallet = self.get(user, "wallet") - amount
					self.update(user, bank_val = new_bank)
					self.update(user, wallet_val = new_wallet)
					self.save()
					await ctx.send(f"{amount} transfered to your bank!")
				else:
					await ctx.send("You don't have that much in your wallet!")
			else:
				await ctx.send("You can't deposit zero silly!")
		except Exception:
			await ctx.send("Send a valid number.")

	# * Todo
	@commands.command(name = "buy", aliases = ["Buy"])
	async def buy(self, ctx):
		pass
	
	# * Todo
	@commands.command(name = "sell", aliases = ["Sell"])
	async def sell(self, ctx):
		pass

	@commands.command(name = "give", aliases = ["Give"])
	async def give(self, ctx, receiver, amount):
		sender = ctx.message.author.name
		if receiver.startswith("@"):
			receiver = receiver[1:]
			receiver = receiver.lower()
		if receiver not in self.data:
			self.add(receiver)
			pass
		try:
			amount = int(amount)
			if amount > 0:
				sbalance = self.get(sender, "wallet")
				if sbalance >= amount:
					rbalance = self.get(receiver, "wallet")
					self.update(sender, wallet_val = sbalance - amount)
					self.update(receiver, wallet_val = rbalance + amount)
					self.save()
					await ctx.send(f"{sender} gave {receiver} {amount} {self.currency}")
			elif amount < 0:
				await ctx.send("Don't be mean and try to scam :(")
			else:
				await ctx.send("Wow, trying to give people nothing...what a shame.")
		except Exception:
			await ctx.send("Send a valid number.")
		

	@commands.command(name = "rob", aliases = ["Rob"])
	async def rob(self, ctx, victim):
		user = ctx.message.author.name
		victim = victim.lower()
		if victim.startswith("@"):
			victim = victim[1:]
			victim = victim.lower()
			pass
		if victim not in self.data:
			self.add(victim)
			self.save()
			pass
		if user not in self.data:
			self.add(user)
			self.save()
			pass
		seed(time())
		chances = randint(0, 300)
		if chances >= 275:
			vwallet = self.get(victim, "wallet")
			uwallet = self.get(user, "wallet")
			stolen = randint(0, vwallet)
			self.update(victim, wallet_val = vwallet - stolen)
			self.update(user, wallet_val = uwallet + stolen )
			self.save()
			await ctx.send(f"{user} robbed {victim} of {stolen} {self.currency}")
		elif chances >= 100:
			vwallet = self.get(victim, "wallet")
			uwallet = self.get(user, "wallet")
			stolen = randint(0, 50)
			self.update(victim, wallet_val = vwallet - stolen)
			self.update(user, wallet_val = uwallet + stolen )
			self.save()
			await ctx.send(f"{user} robbed {victim} of {stolen} {self.currency}")
		elif chances < 100:
			await ctx.send(f"{victim} caught you and you gained nothing but a black eye.")


	@commands.command(name = "gamble", aliases = ["Gamble"])
	async def gamble(self, ctx, amount):
		user = ctx.message.author.name
		if user not in self.data:
			self.add(user)
			self.save()
			pass
		try:
			amount = int(amount)
			amount = abs(amount)
			if amount > 0:
				balance = self.get(user, "wallet")
				if balance >= amount:
					seed(time())
					chances = randint(0,1)
					if chances == 1:
						self.update(user, wallet_val = balance + (amount * 2))
						self.save()
						await ctx.send(f"{user} won {amount * 2} {self.currency}!")
					else:
						self.update(user, wallet_val = balance - amount)
						self.save()
						await ctx.send(f"{user} lost {amount} {self.currency}!")
				else:
					ctx.send("You cant bet more than you have!")
			elif amount < 0:
				amount = abs(amount)
				balance = self.get(user, "wallet")
				if balance >= amount:
					seed(time())
					chances = randint(0,1)
					if chances == 1:
						self.update(user, wallet_val = balance + (amount * 2))
						self.save()
						await ctx.send(f"{user} won {amount * 2} {self.currency}!")
					else:
						self.update(user, wallet_val = balance - amount)
						self.save()
						await ctx.send(f"{user} lost {amount} {self.currency}!")
				else:
					ctx.send("You can't bet nothing")
		except Exception:
			await ctx.send("Send a valid number.")

	# Shop Stuff

	# * Todo
	@commands.command(name = "shop", aliases = ["Shop"])
	async def shop(self, ctx):
		pass
	
	# * Todo
	@commands.command(name = "inventory", aliases = ["Inventory"])
	async def inventory(self, ctx):
		pass

	# Leaderboard
	
	# * Todo
	@commands.command(name="lb", aliases=["LB"])
	async def leaderboard(self, ctx):
		pass