import discord
import os
from discord.ext import commands
from webserver import keep_alive
import json
from discord.utils import get
import youtube_dl
import asyncio

intents = discord.Intents(messages=True, guilds=True, members=True)
client = commands.Bot(command_prefix="!",intents=discord.Intents.all())

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('boost ALEPH0000'))
  print('IM RE_adY 2B USed! {0.user}'.format(client))
  client.load_extension('cogs.music')

@client.event
async def on_message(message):
  emoji = "a:wbutterfly:901802466125971458"
  emoji2 = "a:white_hearts:901802466478272532"
  emoji3 = "a:wings:901802466201464893"
  if message.author == client.user:
    return
  
  if message.content.startswith('wlc'):
    await message.add_reaction(emoji)
    await message.add_reaction(emoji2)
    await message.add_reaction(emoji3)
  await client.process_commands(message)

@client.command()
async def check(ctx):
  await ctx.send('"AZERO" BOt i_S W0RKINg!!')

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'BY E {member} !!..')

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'bye 4 good .. {member}')

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')
  for ban_entry in banned_users:
    user = ban_entry.user
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'what why sure tho {user.name}#{user.discriminator}')
      return

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=21):
  amount = amount + 1
  if amount > 1001:
    await ctx.send('ERR_or! LIMIT == 1000;')
  else:
    await ctx.channel.purge(limit=amount)
    await ctx.send('DONe')

@client.command()
async def roles(ctx, emoji, role: discord.Role,*,message):
  emb = discord.Embed(description=message)
  msg = await ctx.channel.send(embed=emb)
  await msg.add_reaction(emoji)
  with open('roles.json') as json_file:
    data = json.load(json_file)
    new_react_role = {
      'role_name':role.name,
      'role_id':role.id,
      'emoji':emoji,
      'message_id':msg.id
    }
    data.append(new_react_role)
  with open('roles.json', 'w') as j:
    json.dump(data,j,indent=4)
  
@client.event
async def on_member_join(member):
  autorole = discord.utils.get(member.guild.roles, name=',, REGULAR')
  await member.add_roles(autorole)
  channel = client.get_channel(899346794125885443)
  embed = discord.Embed(
    colour = 0x99aab5
  )
  embed.set_footer(text='- aether & daria')
  embed.set_author(name=member.name, icon_url=member.avatar_url)
  embed.add_field(name='WLC TO AZERO_UNITED', value="""<#899350884406931507> 
  ﹒<#899350900001357844>
  <#899351811432017960>
  """)
  await channel.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
  if payload.member.bot:
    pass
  else:
    with open('roles.json') as react_file:
      data = json.load(react_file)
      for x in data:
        if x['emoji'] == payload.emoji.name:
          role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

          await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
  with open('roles.json') as react_file:
    data = json.load(react_file)
    for x in data:
      if x['emoji'] == payload.emoji.name:
        role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])
        await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

keep_alive()

client.run(os.getenv('TOKEN'))