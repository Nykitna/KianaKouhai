import difflib
import random
import time

import twitchio
from twitchio.ext import commands
from library.Database import Database
from library.Errors import *
from Utility import Checks

class Economy(commands.Cog):
	def __init__(self, bot : commands.Bot):
		self.bot = bot
		self.d = Database("library/data/wealth.json")
	
	@commands.command(name = "bal", aliases = ["Bal"])
	async def bal(self, ctx : commands.Context):
		user_id = str(ctx.author.id)
		if user_id not in self.d.filedata:
			self.d.add(user_id)
			pass
		wallet = self.d.filedata[user_id].get("wallet")
		bank = self.d.filedata[user_id].get("bank")
		await ctx.send(f"{ctx.author.name}, you have {wallet} credits in your wallet and {bank} credits in your bank.")
	
	@commands.command(name = "deposit")
	async def deposit(self, ctx : commands.Context, amount):
		user_id = str(ctx.author.id)
		if user_id not in self.d.filedata:
			self.d.add(user_id)
			pass
		try:
			amount = int(amount)
			if self.d.filedata[user_id].get("wallet") >= amount:
				wallet = self.d.filedata[user_id].get("wallet")
				bank = self.d.filedata[user_id].get("bank")
				self.d.filedata[user_id].update({"wallet": (wallet - amount)})
				self.d.filedata[user_id].update({"bank": (bank + amount)})
				await ctx.send(f"Successfully moved {amount} to your bank.")
				self.d.save()
			else:
				await ctx.send("You do not have enough credits in your wallet.")
		except Exception as E:
			if isinstance(E, ValueError):
				if amount == "all":
					wallet = self.d.filedata[user_id].get("wallet")
					bank = self.d.filedata[user_id].get("bank")
					self.d.filedata[user_id].update({"wallet" : (wallet - wallet)})
					self.d.filedata[user_id].update({"bank": (bank + wallet)})
					await ctx.send(f"Successfully moved {wallet} credits to your bank.")
					self.d.save()
	
	@commands.command(name = "withdrawal", aliases = ["withdrawl", "withdraw"])
	async def withdrawal(self, ctx: commands.Context, amount):
		user_id = str(ctx.author.id)
		if user_id not in self.d.filedata:
			self.d.add(user_id)
			pass
		try:
			amount = int(amount)
			if self.d.filedata[user_id].get("bank") >= amount:
				wallet = self.d.filedata[user_id].get("wallet")
				bank = self.d.filedata[user_id].get("bank")
				self.d.filedata[user_id].update({"wallet": (wallet + amount)})
				self.d.filedata[user_id].update({"bank": (bank - amount)})
				await ctx.send(f"Successfully moved {amount} to your wallet.")
				self.d.save()
			else:
				await ctx.send("You do not have enough credits in your bank.")
		except Exception as E:
			if isinstance(E, ValueError):
				if amount == "all":
					wallet = self.d.filedata[user_id].get("wallet")
					bank = self.d.filedata[user_id].get("bank")
					self.d.filedata[user_id].update({"bank": (bank - bank)})
					self.d.filedata[user_id].update({"wallet": (wallet + bank)})
					await ctx.send(f"Successfully moved {bank} credits to your wallet.")
					self.d.save()
				else:
					await ctx.send("Invalid command argument.")

	@commands.command(name = "gamble", aliases = ["Gamble", "Bet", "bet", 'slots', "Slots"])
	async def gamble(self, ctx : commands.Context, amount):
		user_id = str(ctx.author.id)
		if user_id not in self.d.filedata is True:
			self.d.add(user_id)
			pass
		try:
			amount = int(amount)
			rint = random.randint(0,1)
			if self.d.filedata[user_id].get("wallet") >= amount:
				if rint == 1:
					wallet = self.d.filedata[user_id].get("wallet")
					wallet += amount * 2
					self.d.filedata[user_id].update({"wallet": wallet})
					await ctx.send(f"You won {amount * 2} credits!")
					self.d.save()
				elif rint == 0:
					wallet = self.d.filedata[user_id].get("wallet")
					wallet -= amount
					self.d.filedata[user_id].update({"wallet": wallet})
					await ctx.send(f"You lost {amount} credits. Better luck next time.")
					self.d.save()
			else:
				await ctx.send("You do not have enough credits in your wallet.")
		except Exception as E:
			if isinstance(E, ValueError):
				if amount == "all":
					rint = random.randint(0, 1)
					if rint == 1:
						wallet = self.d.filedata[user_id].get("wallet")
						wallet = wallet * 2
						self.d.filedata[user_id].update({"wallet": wallet})
						await ctx.send(f"You won {wallet * 2} credits!")
						self.d.save()
					elif rint == 0:
						self.d.filedata[user_id].update({"wallet": 0})
						await ctx.send(f"You lost {amount} credits. Better luck next time.")
						self.d.save()
			
	@commands.command(name = "rob", aliases = ["steal", "Rob", "Steal"])
	async def rob(self, ctx : commands.Context, member : twitchio.User):
		user_id = str(ctx.author.id)
		vict_id = str(member.id)
		if user_id not in self.d.filedata:
			self.d.add(user_id)
			self.d.save()
			pass
		if vict_id not in self.d.filedata:
			self.d.add(vict_id)
			self.d.save()
			pass
		userwallet = self.d.filedata[user_id].get("wallet")
		victwallet = self.d.filedata[vict_id].get("wallet")
		random.seed(time.time())
		chances = random.randint(1,3)
		if chances == 3:
			stolen = random.randint(0, victwallet)
			userwallet += stolen
			victwallet -= stolen
			self.d.filedata[user_id].update({"wallet": userwallet})
			self.d.filedata[vict_id].update({"wallet": victwallet})
			await ctx.send(f"{ctx.author.name} robbed {stolen} credits from {member.name}.")
			self.d.save()
		elif chances == 2:
			stolen = random.randint(0, 100)
			if Checks.WalletCheck(vict_id, stolen) is True:
				userwallet += stolen
				victwallet -= stolen
				self.d.filedata[user_id].update({"wallet": userwallet})
				self.d.filedata[vict_id].update({"wallet": victwallet})
				await ctx.send(f"{ctx.author.name} robbed {stolen} credits from {member.name}.")
				self.d.save()
			else:
				stolen = random.randint(0, victwallet)
				userwallet += stolen
				victwallet -= stolen
				self.d.filedata[user_id].update({"wallet": userwallet})
				self.d.filedata[vict_id].update({"wallet": victwallet})
				await ctx.send(f"{ctx.author.name} robbed {stolen} credits from {member.name}.")
				self.d.save()
		else:
			await ctx.send(f"{ctx.author.name} was caught!")
	
	@commands.command(name = "give")
	async def give(self, ctx, amount, member : twitchio.User):
		uid = str(ctx.author.id)
		rid = str(member.id)
		try:
			amount = int(amount)
			print(rid)
			if uid not in self.d.filedata:
				self.d.add(uid)
				self.d.save()
			uwallet = self.d.filedata[uid].get("wallet")
			rwallet = self.d.filedata[rid].get("wallet")
			self.d.filedata[uid].update({"wallet": uwallet - amount})
			self.d.filedata[rid].update({"wallet": rwallet + amount})
			await ctx.send(f"{ctx.author.name} gave {member.name} {amount} credits")
			self.d.save()
		except Exception as E:
			if isinstance(E, ValueError):
				if amount == "all":
					uwallet = self.d.filedata[uid].get("wallet")
					rwallet = self.d.filedata[rid].get("wallet")
					self.d.filedata[uid].update({"wallet": uwallet - uwallet})
					self.d.filedata[rid].update({"wallet": rwallet + uwallet})
					await ctx.send(f"{ctx.author} gave {member.name} {amount} credits")
					self.d.save()
	
	@commands.command(name = "grant")
	async def grant(self, ctx, amount, target : twitchio.User):
		invid = str(ctx.author.id)
		if invid == "468972149":
			tid = str(target.id)
			print(tid)
			if tid not in self.d.filedata:
				self.d.add(tid)
				self.d.save()
				pass
			wallet_target = self.d.filedata[tid].get("wallet")
			self.d.filedata[tid].update({"wallet": wallet_target + int(amount)})
			self.d.save()
			await ctx.send(f"Granted {target.name} {amount} credits.")
		else:
			await ctx.send("Dev only command.")
