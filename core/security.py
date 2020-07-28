from builtins import log,conf,client
import discord, asyncio

async def delete(messages,time):
  await asyncio.sleep(time)
  for message in messages:
    try:await message.delete()
    except discord.errors.NotFound:continue
    except discord.errors.Forbidden:continue

# La classe de la ligne de commande
class Security():

  ADMINS = ["admin","botmoderator"]

  def __init__(self,client,**kwargs):
    self.client = client
    return

  def canExecute(self,function,author):
    auth = function.authGroup
    if function.authGroup == None: return True
    if isinstance(function.authGroup, str): auth = [function.authGroup]
    for x in auth:
      if x.lower() in [y.name.lower() for y in author.roles]:
        return True
    return False

  def setFunctVars(self,funct):
    try: funct.authGroup
    except AttributeError:
      funct.authGroup = None
    return funct
  
  def roleNeeded(self,*roles): # add the authgroup data
    def inner(funct):
      funct.authGroup = roles
      return funct
    return inner

  async def send_warn(self,title,reason,message):
    await log.warn("De <@"+str(message.author.id)+">, titre: "+title+"\nReason: "+reason)
    embed=discord.Embed(title=title, description=reason, color=0xfb0013)
    embed.set_author(name="TUTUTUTU")
    embed.set_thumbnail(url="https://media.tenor.com/images/a4fd1165d9d64832bc2b0fda3ecdf0e1/tenor.gif")
    embed.set_footer(text="Ce message ce détruira au bout de "+str(conf["deleteWarnTime"])+" secondes.")
    to_destroy = await message.channel.send("**__WARN:__** <@"+str(message.author.id)+">",embed=embed)
    await message.delete()
    asyncio.get_running_loop().run_in_executor(None, await delete([to_destroy],conf["deleteWarnTime"]))

  async def checkCommand(self,message):
    if "admin" in [y.name.lower() for y in message.author.roles]:return True
    if "\n" in message.content:await self.send_warn("Les commandes sont en une ligne !","Sinon, c'est limite du spam.\n\nTu peux utillise `\\n` si tu as besoin de marquer des retours à la ligne.",message);return False
    if len(message.content)>200:await self.send_warn("Les commandes sont en moins de 200 charactères !","Encore, ça fais beaucoup là non ?\nTu en as tant besoin que cela ?",message);return False
    if len(message.content.split(";")) > 4:await self.send_warn("Vous utillisez trop de commandes.","La limite est de 4.\nTu en as tant besoin que cela ?",message);return False
    return True
