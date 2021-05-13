import json
import time
import random

from twitchio.ext import commands
from twitchio.ext.commands.bot import Bot

@commands.cog()
class Economy:
	def __init__(self, bot : Bot):
		self.bot = bot
		self.data = self.start()
		self.currency = "GAM3R CoinZ"

	def start(self):
		with open("data/economy.json", "r") as f:
			return json.load(f)

	def save(self):
		with open("data/economy.json", "w") as f:
			json.dump(self.data, f, indent = 4)
	
	def get(self, user, value):
		return self.data[user].get(value)

	def add(self, user):
		self.data[user] = {"wallet": 2000, "bank": 0}

	def update(self, user, wallet = None, bank = None):
		if bank == None:
			self.data[user].update({"wallet": wallet})
		elif wallet == None:
			self.data[user].update({"bank": bank})
		else:
			self.data[user].update({"wallet": wallet})
			self.data[user].update({"bank": bank})

	async def verify(self, target):
		chatters = await self.bot.get_chatters("drunklockholmes")
		user = chatters[1].count(target)
		if user == 1:
			return True
		else:
			return False
	
	@classmethod
	def uformat(cls, string):
		if string.startswith("@"):
			string = string[1:]
			string = string.lower()
			return string
	
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
			amount = abs(amount)
			if amount != 0:
				current_wallet = self.get(user, "wallet")
				if current_wallet >= amount:
					new_bank =	self.get(user, "bank")
					new_wallet = self.get(user, "wallet")
					self.update(user, bank = (new_bank + amount))
					self.update(user, wallet = (new_wallet - amount))
					self.save()
					await ctx.send(f"{amount} transfered to your bank!")
				else:
					await ctx.send("You don't have that much in your wallet!")
			elif amount == 0:
				await ctx.send("You can't deposit zero silly!")
		except Exception:
			await ctx.send("Error! Not a number! Did the operator enjoy this witticism?")
	
	@commands.command(name = "withdrawal", aliases = ["Withdrawal"])
	async def withdrawal(self, ctx, amount):
		user = ctx.message.author.name
		if user not in self.data:
			self.add(user)
			self.save()
			pass
		try:
			amount = int(amount)
			amount = abs(amount)
			if amount != 0:
				current_bank = self.get(user, "bank")
				if current_bank >= amount:
					new_wallet = self.get(user, "wallet")
					new_bank = self.get(user, "bank")
					self.update(user, wallet_val = (new_wallet + amount))
					self.update(user, bank_val = (new_bank - amount))
					self.save()
					await ctx.send(f"{amount} transfered out of your bank!")
				else:
					await ctx.send("You don't have that much in your bank!")
			elif amount == 0:
				await ctx.send("You can't deposit zero silly!")
		except Exception:
			await ctx.send("Error! Not a number! Did the operator enjoy this witticism?")
		
	@commands.command(name = "give", aliases = ["Give"])
	async def give(self, ctx, receiver, amount):
		sender = ctx.message.author.name
		receiver = self.uformat(receiver)
		r_exists = await self.verify(target = receiver)
		if r_exists == True:
			if receiver not in self.data:
				self.add(receiver)
			else:
				try:
					amount = int(amount)
					amount = abs(amount)
					if amount > 0:
						senderbal = self.get(sender, "wallet")
						if senderbal >= amount:
							receiverbal = self.get(receiver, "wallet")
							self.update(sender, wallet = (senderbal - amount))
							self.update(receiver, wallet = (receiverbal + amount))
							self.save()
							await ctx.send(f"{sender} gave {receiver} {amount} {self.currency}")
					elif amount < 0:
						await ctx.send("Don't be mean and try to scam :(")
					else:
						await ctx.send("Wow, trying to give people nothing...what a shame.")
				except Exception:
					if isinstance(Exception, ValueError):
						await ctx.send("Error! Not a number! Did the operator enjoy this witticism?")

	@commands.command(name = "rob", aliases = ["Rob"])
	async def rob(self, ctx, victim):
		user = ctx.message.author.name
		if user not in self.data:
			self.add(user)
			self.save()
			pass
		victim = self.uformat(victim)
		v_exists = await self.verify(victim)
		if v_exists is True:
			if victim not in self.data:
				self.add(victim)
				self.save()
				pass
		random.seed(time.time())
		if victim != user:
			chances = random.randint(0, 300)
			if chances >= 275:
				vwallet = self.get(victim, "wallet")
				uwallet = self.get(user, "wallet")
				stolen = random.randint(0, vwallet)
				self.update(victim, wallet = (vwallet - stolen))
				self.update(user, wallet = (uwallet + stolen))
				self.save()
				await ctx.send(f"{user} robbed {victim} of {stolen} {self.currency}")
			elif chances >= 100:
				vwallet = self.get(victim, "wallet")
				uwallet = self.get(user, "wallet")
				stolen = random.randint(0, 100)
				self.update(victim, wallet = (vwallet - stolen))
				self.update(user, wallet = (uwallet + stolen))
				self.save()
				await ctx.send(f"{user} robbed {victim} of {stolen} {self.currency}")
			elif chances < 100:
				await ctx.send(f"{victim} caught you and you gained nothing but a black eye.")
		else:
			await ctx.send("You cannot rob yourself!")

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
			if amount > 0 or amount < 0:
				balance = self.get(user, "wallet")
				if balance >= amount:
					random.seed(time.time())
					chances = random.randint(0,1)
					if chances == 1:
						self.update(user, wallet = (balance + (amount * 2)))
						self.save()
						await ctx.send(f"{user} won {amount * 2} {self.currency}!")
					else:
						self.update(user, wallet = (balance - amount))
						self.save()
						await ctx.send(f"{user} lost {amount} {self.currency}!")
				else:
					ctx.send("You cant bet more than you have!")
			elif amount == 0:
				ctx.send("You can't bet nothing")
		except Exception:
			if isinstance(Exception, ValueError):
				await ctx.send("Error! Not a number! Did the operator enjoy this witticism?")
