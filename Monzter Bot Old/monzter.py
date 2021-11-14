import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import requests
from datetime import datetime

client = commands.Bot(command_prefix = "^")
client.remove_command('help')

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name = f'^help' , url = "https://www.twitch.tv/pokimane"))
	print('online')


 
@client.command()
@commands.has_permissions(kick_members=True)
async def purge(ctx,amount=100):
    await ctx.channel.purge(limit=amount+1)
    await ctx.channel.send(f"Cleared **{amount} messages**")
    await ctx.channel.purge(limit=1)
 
@client.command()
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
  if member is None:
  	embed = discord.Embed(title = "Invalid Arguements" , description = "Please mention a member!" , colour = discord.Colour.green())
  	await ctx.send(f"{ctx.author.mention}" , embed=embed)
  	return
  
  if reason is None:
  	embed = discord.Embed(title = "Banned" , colour = ctx.author.colour, timestamp = ctx.message.created_at)
  	embed.set_author(name = f"{ctx.author.name}#{ctx.author.discriminator}" , icon_url = ctx.author.avatar_url)
  	embed.add_field(name = "**•Server:**" , value = ctx.guild.name)
  	embed.add_field(name = "**•Moderator:**" , value = f"{ctx.author.name}#{ctx.author.discriminator} (id: {ctx.author.id})" , inline = False)
  	embed.add_field(name = "**•Reason:**" , value = f"No reason specified." , inline = False)
  	await ctx.author.send(embed=embed)
  	await ctx.send(f"Successfully banned {member.name} from the server!" , embed=embed)
  	await member.ban(reason = f"Member banned by {ctx.author.name}.\nReason: Not specified.")
  	
  else:
  	embed = discord.Embed(title = "Ban" , colour = ctx.author.colour, timestamp = ctx.message.created_at)
  	embed.set_author(name = f"{ctx.author.name}#{ctx.author.discriminator}" , icon_url = ctx.author.avatar_url)
  	embed.add_field(name = "**•Server:**" , value = ctx.guild.name)
  	embed.add_field(name = "**•Moderator:**" , value = f"{ctx.author.name}#{ctx.author.discriminator} (id: {ctx.author.id})" , inline = False)
  	embed.add_field(name = "**•Reason:**" , value = reason , inline = False)
  	await ctx.author.send(embed=embed)
  	await ctx.send(f"Successfully banned {member.name} from the server!" , embed=embed)
  	await member.ban(reason = f"Member banned by {ctx.author.name}.\nReason: {reason}.")	

 
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member = None, *,reason=None):
	if member.id == ctx.author.id:
		await ctx.send("Hey! You can't kick yourself!")
		return
	if member is None:
		await ctx.send("Please mention a member!")
		return
	if reason is None:
		embed = discord.Embed(title = f"Succesfuly kicked {member.name} from the server!" , description = f"**Reason** = No reason specified.\n**Responsible Moderator** : {ctx.author.name}#{ctx.author.discriminator}" , colour = discord.Colour.green())
		await ctx.send(embed=embed)
		await member.kick(reason = "No reason specified. Member kicked by {ctx.author.name} (id: {ctx.author.id})")
	
	else:
		embed = discord.Embed(title = f"Succesfuly kicked {member.name} from the server!" , description = f"**Reason** = {reason}\n**Responsible Moderator** : {ctx.author.name}" , colour = discord.Colour.green())
	await ctx.send(embed=embed)
	await member.kick()
 
 
@client.command()
@commands.has_permissions(kick_members = True)
async def mute(ctx, member: discord.Member = None, *,reason = None):
	if member is None:
		await ctx.send(f"{ctx.author.mention}, Please mention a user.")
		
	if reason is None:
		guild = ctx.guild
		role_id = int(844485629580017664)
		role = await client.fetch_role(id = role_id)
		await member.add_roles(role)
		await member.edit(name = f"[MUTED] {member.name}")

		embed = discord.Embed(title = f"Success!" , colour = ctx.author.color)
		embed.add_field(Name = f"**Server**" , value = ctx.guild.name,  inline = False)
		embed.add_field(name = "**Responsible Moderator:**" , value = f"{ctx.author.name}#{ctx.author.discriminator}" , inline = False)
		embed.add_field(name = f"**Reason:**" , value = "Not specified." , inline = False)
		embed.set_thumbnail(url = ctx.author.avatar_url)
		embed.set_image(url = "https://media.tenor.com/images/5c38c2b35ef65b0ba8be3e81d419cdab/tenor.gif" )
		await ctx.send(embed=embed)
		
	else:
		guild = ctx.guild
		role_id = 845264863466094602
		role = get(guild.roles, id= role_id)
		await member.add_roles(role)
		await member.edit(name = f"[MUTED] {member.name}")
		embed = discord.Embed(title = f"Success!" , colour = ctx.author.color)
		embed.add_field(Name = f"**Server**" , value = ctx.guild.name,  inline = False)
		embed.add_field(name = "**Member:**" , value = f"{member.name}#{member.discriminator} (id: {member.id})")
		embed.add_field(name = "**Responsible Moderator:**" , value = f"{ctx.author.name}#{ctx.author.discriminator} (id: {ctx.author.id})" , inline = False)
		embed.add_field(name = f"**Reason:**" , value = f"{reason}" , inline = False)
		embed.set_thumbnail(url = ctx.author.avatar_url)
		embed.set_image(url = "https://media.tenor.com/images/5c38c2b35ef65b0ba8be3e81d419cdab/tenor.gif" )
		await ctx.send(embed=embed)

@client.command()
async def unmute(ctx, member: discord.Member = None):
	if member is None:
		await ctx.send(f"{ctx.author.mention} , Please mention a member!")
		
	else:
		guild = ctx.guild
		role_id = 844485629580017664
		role = get(guild.roles, id= role_id)
		await member.add_roles(role)
		await member.edit(name = member.name)
		embed = discord.Embed(title = "Success!" ,description = f"I have successfully unmuted {member.name}#{member.discriminator}.", colour = ctx.author.colour)
		await ctx.send(embed=embed)

		
 
@client.command()
async def userinfo(ctx, member: discord.Member = None):

							
	member = ctx.author if not member else member
	roles = [role for role in member.roles]
	embed = discord.Embed(title = f"{member.name}'s Userinfo!" , colour = member.colour , timestamp = ctx.message.created_at)
 
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(text = f"Requested by {ctx.author.name}" , icon_url = ctx.author.avatar_url)
	embed.add_field(name = f"**Name:**" , value = f"{member.name}" , inline = True)
	embed.add_field(name = "**Discriminator:**" , value = f"#{member.discriminator}")
	embed.add_field(name = f"**Nickname:**" , value = f" {member.display_name}")
	embed.add_field(name = "Id" , value = f"{member.id}")
	embed.add_field(name = "**Account Created On:**" , value = member.created_at.strftime("%a, %d %B %Y , %I %M %p UTC"))
	embed.add_field(name = '**Joined This Server On:**' , value = member.joined_at.strftime("%a, %d %B %Y , %I %M %p UTC"))
	embed.add_field(name = "**Roles**" , value = f" ".join([role.mention for role in roles]))
	await ctx.send(embed=embed)		

@client.command()
async def info(ctx):
	embed = discord.Embed(title = "Our games and Projects!" ,description = "**MONzTER Games:**\n\t**Beat 'n Boom** : [Click here](https://monzter-games.itch.io/beat-n-boom)\n\t**Dodge the block** : [Click here.](https://monzter-games.itch.io/dodge-the-block) \n\t**Click Ball** : [Click here](https://monzter-games.itch.io/click-ball) \n\n **Projects:**\n\t_BlackOut, BeatWorkout and Our own game developers website._\n\t Stay Tuned!" ,color = ctx.author.colour)
	embed.set_thumbnail(url = ctx.author.avatar_url)
	embed.set_footer(text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}" , icon_url = ctx.author.avatar_url)
	await ctx.send(embed=embed)

	

@client.command()
async def fox(ctx):
	url = "https://randomfox.ca/floof"
	a = requests.get(url)
	p = a.json()
	i = p['image']
	
	if i.endswith == ".mp4":
		return
	else:
		embed = discord.Embed(title = "A cute picture of a fox!" , color = ctx.author.colour)
		embed.set_image(url = i)
		embed.set_footer(text = f"Requested by {ctx.author.name}" , icon_url = ctx.author.avatar_url)
		await ctx.send(embed=embed)
	

@client.command()
async def avatar(ctx , member: discord.Member = None):
	member = ctx.author if not member else member
	embed = discord.Embed(title = f"Avatar for {member.name}" , description = f"[Click here to download the avatar]({ctx.author.avatar_url})" , color = member.colour)
	embed.set_image(url = f"{member.avatar_url}")
	embed.set_footer(text = f"Requested by {member.name}" , icon_url = member.avatar_url)
	await ctx.send(embed=embed)

@client.command()
async def joke(ctx):
	api = "https://official-joke-api.appspot.com/random_joke"
	a = requests.get(api)
	p = a.json()
	await ctx.send(f'{p["setup"]}\n{p["punchline"]}')

	
@client.command()
async def uptime(ctx):
    starttime = datetime.utcnow()
    now = datetime.utcnow()
    elapsed = now - starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    embed = discord.Embed(title = f"{client.user.name}'s uptime" , description = "I have been Online Since {}d {}h {}m {}s Ago!".format(elapsed.days, hours, minutes, seconds) , color = ctx.author.colour)
    await ctx.send(embed=embed)

@client.command()
async def dog(ctx):
	url = "https://random.dog/woof.json"
	a = requests.get(url)
	p = a.json()
	i = p['url']
	
	if i.endswith == ".mp4":
		return
		
	else:
		embed = discord.Embed(title = "A cute picture of a dog!" , color = ctx.author.colour)
		embed.set_image(url = i)
		embed.set_footer(text = f"Requested by {ctx.author.name}" , icon_url = ctx.author.avatar_url)
		await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    embed = discord.Embed(title = "Pong!" , description = f'{round(client.latency * 1000)} ms' , colour = discord.Colour.green())
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
	contents = ['Page: 1', 'Page: 2' , 'Page: 3']
	pages = 3
	current_page = 1
	
	embed = discord.Embed(title = f"{client.user.name}'s help command" , description = f"**Server Prefix: ^**\nTotal Pages: {current_page}/{pages}\nCurrent Page: {contents[current_page-1]}" , color = ctx.author.colour , timestamp = ctx.message.created_at)
	embed.add_field(name = "**•Info:**" , value = "-> Tells about our games and our upcoming projects.\nUsage: _^info_" , inline = False)
	embed.add_field(name = "**•Userinfo:**" , value = "-> Get your account info.\nUsage: _^userinfo [member]_" , inline = False)
	embed.add_field(name = "**•Avatar:**" , value = "-> Show's your profile picture.\nUsage: _^avatar [member]_", inline = False)
	embed.add_field(name = "**•Ping:**" , value = "-> Tells you the bot ping.\nUsage: _^ping_" , inline = False)
	embed.set_thumbnail(url = ctx.author.avatar_url)
	embed.set_footer(text = f"Requested by {ctx.author.name}" , icon_url = ctx.author.avatar_url)
	
	msg = await ctx.send(embed=embed)
	
	
	await msg.add_reaction("◀️")
	await msg.add_reaction("▶️")
	
	def check(reaction, user):
		return user == ctx.author and str(reaction.emoji) in ['◀️' , '▶️' , '🧨']
		
	while True:
		try:
			reaction, user = await client.wait_for("reaction_add" , timeout = 30 , check = check)
			
			if str(reaction.emoji) == "▶️" and current_page != pages:
				current_page += 1
				
				if str(reaction.emoji) == "🧨 ":
					await msg.delete()
				
				if current_page == 2:
					em = discord.Embed(title = f"{client.user.name}'s help command" , description = f"_Total Pages : {current_page}/{pages}_\n_Current Page : {contents[current_page-1]}_" , timestamp = ctx.message.created_at , color = ctx.author.colour)
					em.add_field(name = "**•Uptime:**" , value = "-> Get the bot's uptime. \n Usage: _^uptime_" , inline = False)
					em.add_field(name = "**•Fox:**", value = "-> Get a sweet pic of a fox.\n Usage: _^fox_" , inline = False)
					em.add_field(name = "**•Dog:**" , value = "-> Get an awesome pic of a dog. \n Usage: _^dog_" , inline = False)
					em.add_field(name = "**•Joke:**" , value = "-> Get's a random joke.\nUsage: _^joke_" , inline = False)
					em.set_thumbnail(url = ctx.author.avatar_url)
					em.set_footer(text = f"Requested by {ctx.author.name}" , icon_url = ctx.author.avatar_url)
					await msg.edit(embed=em)
					await msg.remove_reaction(reaction, user)
					
				elif current_page == 3:
					emb = discord.Embed(title = f"{client.user.name}'s help command" , description = f"Moderation Commands:\n_Total Pages : {current_page}/{pages}_\n_Current Page : {contents[current_page-1]}_" , color = ctx.author.colour , timestamp = ctx.message.created_at)
					emb.add_field(name = "**•Mute:**\n-> Mute a user.\n", value = "Usage: _^mute [member]_" , inline = False)
					emb.add_field(name = "**•Purge:**" , value = "-> Delete the messages.\nUsage: _^purge [number]" , inline = False)
					emb.add_field(name = "**•Ban:**" , value = "-> Ban a user.\nUsage: _^ban [member]" , inline = False)
					emb.add_field(name = "**•Unban:**" , value = "-> Unban a user.\nUsage: _^unban [member]_" , inline = False)
					embed.add_field(name = "**•Unmute:**" , value = "-> Unmute a user.\nUsage: _^unmute [member]" , inline = False)
					emb.add_field(name = "**•Change Status:**" , value = "-> Changes the status of the bot. (This command can only be used by Mr.Sloth)\nUsage: _^changepresence [text]_" , inline = False)
					emb.add_field(name = "**•Change Url:**" , value = "-> Changes the url of the stream. (This command can only be used by Mr.Sloth)\nUsage: _^changeurl [url]_" , inline = False)
					emb.add_field(name = "**•Lead bot developer:**", value = "Mr.Sloth#1917" , inline = False)
					emb.set_thumbnail(url = ctx.author.avatar_url)
					emb.set_footer(text = f"Requested by {ctx.author.name}" , icon_url = ctx.author.avatar_url)
					await msg.edit(embed=emb)
					await msg.remove_reaction(reaction, user)				
				
			elif str(reaction.emoji) == "◀️" and current_page > 1:
				current_page -= 1
				
				if current_page == 2:
					await msg.edit(embed=em)
					await msg.remove_reaction(reaction, user)
					
				elif current_page == 1:
					await msg.edit(embed=embed)
					await msg.remove_reaction(reaction, user)
					
								
			else:
				await msg.remove_reaction(reaction, user)
				
		except asyncio.TimeoutError:
				await message.delete()
				await ctx.author.send(f"You didn't reacted on the message. I have deleted it in the {ctx.channel.mention}.")
				break	
				
@client.command()
async def changepresence(ctx,*,text):
    		if ctx.author.id == 707198291246579732:
    			await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name = f"{text}" , url = "https://www.twitch.tv/pokimane"))
    			await ctx.message.add_reaction('✅')
    		else:
    		  await ctx.message.add_reaction('❎')


@client.command()	
async def changeurl(ctx, url):
	if ctx.author.id == 707198291246579732:
		
		if url is None:
			await ctx.send(f"{ctx.author.mention}, Please menion a url.")
		else:
			await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name = f"{text}" , url = f"{url}"))
			await ctx.message.add_reaction('✅')
	else:
		return
	
@client.command()
async def say(ctx, *,text = None):
	if ctx.author.id == 707198291246579732:
		await ctx.message.delete()
		await ctx.send(f"{text}")
	
	else:
		await ctx.message.delete()
		

client.run("TOKEN")
