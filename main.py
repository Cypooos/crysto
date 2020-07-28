import builtins

import core.com.log as log_
log = log_.Log()
builtins.log = log

import sys, os
import shlex

from time import gmtime, strftime
import asyncio, discord

client = discord.Client()

conf = {
    "logChannel":682643807359205389,
    "START_CHAR": '!',
    "deleteWarnTime":30,
}

builtins.conf = conf
builtins.client = client

from core import security
security = security.Security(client)
builtins.security = security

from core import DiscordCommandLineGenerator
commandLine = DiscordCommandLineGenerator.CommandLine(client,security)
builtins.commandLine = commandLine

from core.EnigmesManager import EnigmesManager
main = EnigmesManager("core/databases/Enigmes.csv","core/databases/Users.csv")
builtins.main = main

# importing commands in orders
import core.commands.cmd_Enigmes # the Enigmes interface
import core.commands.cmd_gen # help, ping and others



@client.event
async def on_message(message):
  if message.author.id != client.user.id: await log.message("<@!"+str(message.author.id)+"> said "+message.content)
  else: return

  if len(message.content)>2 and message.content[0] == conf["START_CHAR"]:
    message.content = message.content[1:]
    message.author = log.channel.guild.get_member(message.author.id) # adding the server context, so PM still have "roles"
    
    for x in main.users.keys():
      message.content = message.content.replace("<@"+str(x)+">",str(x)).replace("<@!"+str(x)+">",str(x))
      usr = await client.fetch_user(int(x))
      message.content = message.content.replace("#"+usr.name,str(x))
    if not await security.checkCommand(message):return # SECURITY
    message.content = message.content.replace("\\n","\n")
    print(message.content)
    ret = await commandLine.execute(message)
    if ret != None and ret != "": await message.channel.send(ret)
  


@client.event
async def on_ready():
  log.channel = client.get_channel(conf["logChannel"])
  await log.info("Username: "+client.user.name+";    ID: "+str(client.user.id))



try:
  f = open("core/secret.txt")
  token = f.read()
  f.close()
except FileNotFoundError:
  print("Exit because TOKEN not found")
  exit()

print("TOKEN:",token)

client.run(token)
