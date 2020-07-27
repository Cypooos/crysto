import builtins

import sys, os
import shlex
import core.com.log as log

from time import gmtime, strftime
import asyncio, discord

client = discord.Client()

from core import security
security = security.Security(client)

from core import DiscordCommandLineGenerator
commandLine = DiscordCommandLineGenerator.CommandLine(client,security)

conf = {
    "logChannel":682643807359205389,
    "START_CHAR": '!'
}

import core.com.log as log_
log = log_.Log()
builtins.log = log
builtins.conf = conf
builtins.client = client
builtins.security = security
builtins.commandLine = commandLine


# importing commands in orders
import core.commands.cmd_Enigmes # the Enigmes interface
import core.commands.cmd_gen # help, ping and others



@client.event
async def on_message(message):
  if message.author.id != client.user.id: await log.message("<@!"+str(message.author.id)+"> said "+message.content)
  else: return

  if len(message.content)>2 and message.content[0] == conf["START_CHAR"]:
    message.content = message.content[1:]
    if not await security.checkCommand(message):return # SECURITY
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
