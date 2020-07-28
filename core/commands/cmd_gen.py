from builtins import commandLine, client, conf, security
import discord, asyncio

async def delete(messages,time=0):
  await asyncio.sleep(time)
  for message in messages:
    try:await message.delete()
    except discord.errors.NotFound:continue
    except discord.errors.Forbidden:continue


@security.roleNeeded('botmoderator')
@commandLine.addFunction()
async def evaluate(commands:max,**kwargs) -> "eval *PYTHON":
  """Execute du code python.
  Execute du code python.
  **A éviter !** une fausse manip pourrais casser le bot ou détruire des données.
  **IL N'Y A PAS DE RETOUR EN ARRIERE POSSIBLE**
  Prévenir <@349114853333663746> en cas de problème."""
  try:ret = eval(commands)
  except:ret = sys.exc_info()[0]
  return "__Return:__\n```python\n"+str(ret)+"```\n"


@commandLine.addFunction()
async def ping(**kwargs) -> 'ping':
  """return "Pong"
  That's a nice and very useful command"""
  return "Pong"

@security.roleNeeded('admin')
@commandLine.addFunction()
async def deleteCmd(nbMsg:(int,1),**kwargs) -> "delete [INT]":
  """Supprimme X messages.
Ne rien indiqué surprimme le dernier message. Nous ne comptons pas la commande dans le nombre message."""
  async for message in commandLine.message.channel.history(limit=int(nbMsg)):
    await message.delete()


# ---- HELP COMMAND ----
@commandLine.addFunction()
async def help(info:(str,""),**kwargs) -> "help [COMMAND|cmd]":
  '''Affiche l'aide d'une commande.
Affiche de l'aide sur une commande, ou sur les commandes en général.
Les aides sont détaillé au possible, en utillisant la syntaxe usuele.
Tapez `help cmd` pour une aide sur le fonctionnement des commandes'''
  message = commandLine.message

  COLORS = {"everyone":0x80ffff,"user":0xff80ff,"botmoderator":0x13fb00,"admin":0xfb0013}
  saw = []
  if info == "":
    to_destroy = []
    for key,value in COLORS.items():
      if key != "everyone" and not key.lower() in [y.name.lower() for y in commandLine.message.author.roles]:continue
      embed=discord.Embed(title="__Liste des commandes "+str(key)+"__", color=value)
        
      if key == "everyone":
        embed.add_field(name="Nom", value="\n".join(["`"+fct.__name__.split(" ")[0]+"`" for fct in commandLine.funct if fct.authGroup == None or fct.authGroup == []]), inline=True)
        embed.add_field(name="Description", value="\n".join([fct.__doc__.split("\n")[0] for fct in commandLine.funct if fct.authGroup == None or fct.authGroup == []]), inline=True)
      else:
        fcts = [fct for fct in commandLine.funct if fct.authGroup != None and key in fct.authGroup]
        if fcts != []:
          embed.add_field(name="Nom", value="\n".join(["`"+fct.__name__.split(" ")[0]+"`" for fct in fcts]), inline=True)
          embed.add_field(name="Description", value="\n".join([fct.__doc__.split("\n")[0] for fct in fcts]), inline=True)
          
      embed.set_footer(text="Ce message d'aide ce détruira au bout de 30 secondes.")

      embed.set_thumbnail(url="https://media3.giphy.com/media/B7o99rIuystY4/source.gif")
      embed.set_footer(text="Le bot Crystos a été créé par Cyprien Bourotte, du studio `<Discursif/>`")
      ele = ""
      if key == "everyone":ele = "Je t'incite à faire `!help COMMANDE` pour plus d'infos, ou encore `!help cmd` pour des informations complémentaire"
      to_destroy.append(await message.channel.send(ele,embed=embed))

    asyncio.get_running_loop().run_in_executor(None, await delete(to_destroy,30))
    return 

  for funct in commandLine.funct:
    if funct.__name__.split(" ")[0] == info:
      if security.canExecute(funct,message.author):
        # HELP FUNCTION
        embed=discord.Embed(title="Commande : "+funct.__name__.split(" ")[0], description=str("\n".join(funct.__doc__.split("\n")[1:])), color=0x80ffff)
        embed.set_footer(text="Ce message d'aide ce détruira au bout de 30 secondes.")
        embed.set_author(name="Aide")
        embed.set_thumbnail(url="https://media1.giphy.com/media/IQ47VvDzlzx9S/giphy.gif")
        embed.add_field(name="Syntaxe :", value="`"+funct.__name__+"`", inline=False)
        if funct.authGroup != None: embed.set_footer(text="Cette commande n'est utilisable seulement avec le role "+str(" ou ".join(funct.authGroup).lower()))
        to_destroy = await message.channel.send(embed=embed)
        asyncio.get_running_loop().run_in_executor(None, await delete([to_destroy],30))
        return 
      else:
        # DONT ALLOW
        security.send_warn("Vous n'avez pas accès à cette commande.","Cette commande n'est utilisable seulement avec le role "+str(" ou ".join(funct.authGroup).lower(),commandLine.message))
        return
  if info.lower() == "cmd":
    embed=discord.Embed(title="__Aide sur l'utillisation des commandes__", description="Les messages qui sont des commandes doivent commancer par `!`\nLes commandes marchent en message privé.", color=0xfbe800)
    embed.set_thumbnail(url="https://media1.giphy.com/media/IQ47VvDzlzx9S/giphy.gif")
    embed.set_footer(text="Le bot Cryptos a été créé par Cyprien Bourotte, du studio <Discursif/>.")
    to_destroy = await message.channel.send(embed=embed)
    asyncio.get_running_loop().run_in_executor(None, await delete([to_destroy],30))
    return 
  return "Commande pour l'aide inconnue.\nTapez `!help` pour la liste des commandes.\nTapez `help cmd` pour les informations d'utillisation des commandes."

