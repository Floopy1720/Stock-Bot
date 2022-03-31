from tinydb import TinyDB, Query
import pickledb
import os
from os import path
import discord
from discord.ext import commands
import random
import json
import ast

activity = discord.Activity(type=discord.ActivityType.watching, name="$help")
cilent = commands.Bot(command_prefix='$', help_command=None, activity=activity, status=discord.Status.dnd)
point = Query()


def check(check):
	if path.exists(check) == False:
		raise Exception("Err: File Not found")
		pass
	else:
		pass
	pass
#db.set('key', 'value')
def checks():
	return msg.author == ctx.author and msg.channel == ctx.channel

def con(con):
	con = "{}.json".format(con)
	return con
	pass
@cilent.event
async def on_ready():
	print("Works!")
	pass

@cilent.command()
@commands.has_permissions(administrator=True)
async def create_cat(ctx, name):
	try:
		check(con(name))
		await ctx.send("Looks like you already have a Catogory named {}".format(name))
		pass
	except:
		db = TinyDB(con(name))
		await ctx.send("Catogory Created!")
		pass

@cilent.command()
@commands.has_permissions(administrator=True)
async def create(ctx, cat, name, *,text):
	cat = con(cat)
	try:
		check(cat)
		db = TinyDB(cat)
		db.insert({"Name": name, "Text": text})
		await ctx.send("Value Created!")
		pass
	except:
		await ctx.send("Looks like you don't have any Catogory nammed {}".format(cat))
		pass

@cilent.command()
@commands.has_permissions(administrator=True)
async def gen_cat(ctx):
	files = os.listdir()
	files.remove("main.py")
	files = '\n'.join(files)
	embed = discord.Embed(description=files, colour=discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
	await ctx.send(embed=embed)

@cilent.command()
@commands.has_permissions(administrator=True)
async def gen(ctx, name):
	name = con(name)
	try:
		check(name)
		db = TinyDB(name)
		list = [r['Name'] for r in db]
		#list = db.getall()
		list = '\n'.join(list)
		embed = discord.Embed(description=list, colour=discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
		await ctx.send(embed=embed)
		pass
	except:
		await ctx.send("Looks like the Catogory doesn't exist")

@cilent.command()
@commands.has_permissions(administrator=True)
async def view(ctx, cat, name):
	cat = con(cat)
	try:
		check(cat)
		db = TinyDB(cat)
		value = db.search(point.Name == name)
		value = str(value)
		value = value[1:-1]
		jsn = value
		if bool(value) == False:
			raise Exception("Err: Value Not Found")
		else:
			#jsn = json.dumps(value)
			#jsn = json.loads(jsn)
			jsn = ast.literal_eval(jsn)
			embed = discord.Embed(title=jsn["Name"], description=jsn["Text"], colour=discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
			await ctx.send(embed=embed)
	except:
		await ctx.send("Looks like the Catogory/Vale doesn't exist")
	pass

@cilent.command()
@commands.has_permissions(administrator=True)
async def del_cat(ctx, name):
	org = name
	name = con(name)
	try:
		check(name)
		msg = await ctx.send("Are you sure want to delete {}".format(org))
		await msg.add_reaction(u"\U0001F44D")
		await msg.add_reaction(u"\U0001F44E")
		try:
			reaction, user = await cilent.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\U0001F44D", u"\U0001F44E"], timeout=30.0)
		except asyncIo.TimeoutError:
			await ctx.send("Timed out")
		else:
			if reaction.emoji == u"\U0001F44D":
				os.remove(name)
				await ctx.send("Category Deleted!")
			else:
				await ctx.send("Process Cancelled")
	except:
		await ctx.send("Looks like the Catogory doesn't exist or You have timed out")
		pass

@cilent.command()
@commands.has_permissions(administrator=True)
async def delete(ctx, name, value):
	org = name
	name = con(name)
	try:
		check(name)
		db = TinyDB(name)
		msg = await ctx.send("Are you sure want to delete this value {}".format(value))
		await msg.add_reaction(u"\U0001F44D")
		await msg.add_reaction(u"\U0001F44E")
		try:
			reaction, user = await cilent.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\U0001F44D", u"\U0001F44E"], timeout=30.0)
		except asyncIo.TimeoutError:
			await ctx.send("Timed out")
		else:
			if reaction.emoji == u"\U0001F44D":
				db.remove(point.Name == value)
				await ctx.send("Value Deleted!")
			else:
				await ctx.send("Process Cancelled")
	except:
		await ctx.send("Looks like the Catogory/Value doesn't exist or You have timed out")
		pass

@cilent.command()
@commands.has_permissions(administrator=True)
async def help(ctx):
	embed=discord.Embed(colour=discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
	embed.add_field(name="$create_cat (name)", value="Creates a Catogory", inline=False)
	embed.add_field(name="$create (cat name) (name) (text)", value="Creates a value", inline=False)
	embed.add_field(name="$gen_cat", value="Lists avalible Catogory", inline=False)
	embed.add_field(name="$gen (cat name)", value="Lists avalible Values", inline=False)
	embed.add_field(name="$view (cat_name) (name)", value="Views the content of the Value", inline=False)
	embed.add_field(name="$del_cat (name)", value="Deletes the Catogory", inline=False)
	embed.add_field(name="$delete (cat_name) (name)", value="Delets the Value", inline=False)
	await ctx.send(embed=embed)
	pass
cilent.run("Paste Your Token")
