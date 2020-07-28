from builtins import commandLine, client, conf, security, main

from ..EnigmesManager import EnigmesManager

from random import choice 

import discord, asyncio
import time

default_bios = [
  "I am a super person :D",
  "Oups, I forgot to write my bio. But I am awesome still.",
  "This server is like so cool.",
  "This is thecnically my bio ?",
  "Awosome_bio.mp4","`bio.mp3`"
  "Is it OwOsome ?",
  "I'm not a bot, I swear :P",
  "So smart right now.",
  "Wanna chat ? I'm super nice ^v^",
  "<Insert coolness/>"
  "No you","Yes, me","Maybe here ?","Yes","NoOOoooo"
  "UwU", "O.O","._.","^v^","^-^","^^",
  "BIO","TALK","WORDS",
  "This is not random I swear :/",
  "Absolutly not a default bio here",
  "I'm so nice come ^^",
  "Is 50 bios automatically generated eghth ?",
  "AUTOMATICA","I love Crysto such a cool guy",
  "I love mysteries <3",
  "1+1+1+1+1+1",
  "I'm a person here.",
  "Howdey, I'm Flowey the Flower",
  "Sans be like: Bone appetit",
  "Do you know antichamber ?",
  "nothing","empty ?","r/wooosh","420/69/42"
]

@commandLine.addFunction()
async def register(**kwargs) -> "register":
  """Register yourself
  Give you the role 'user' to allow you to play and gain points.
  Once register you can not un-register."""
  d = choice(default_bios)
  main.addUser(commandLine.message.author.id,d)
  main.save()
  await commandLine.message.author.add_roles(discord.utils.get(commandLine.message.author.guild.roles, name="user"))
  return "You have been registered.\nChange your BIO using `!bio <YOU BIO>`; For now, it is set as `"+d+'`\nYou can see your profile using `!info user`'


@security.roleNeeded('admin')
@commandLine.addFunction()
async def addEnigme(name:str,solution:str,isMaj:bool,pts:int,uses:int,description:max,**kwargs) -> "add <name> <solution> <is_maj> <pts> <uses> <*DESCRIPTION>":
  """Add a enigme
  Add a enigme to the list. It'll be playable imediatelly."""
  main.addEnigme(name,description,solution,uses,pts,isMaj)
  main.save()
  return "Done with sucess."

@security.roleNeeded('user')
@commandLine.addFunction()
async def listAllEnigme(type_:(str,"all")) -> 'list [all|unsolved|solved|pointsInv|points]':
  """list all enigmes
  List all enigmes.
   - `all` to list them all.
   - `unsolved` to list them by less solved.
   - `solved` to list them by most solved.
   - `pointsInv` to list them by less points.
   - `points` to list them by most points.
  """
  type_ = type_.lower()
  ret = "__Listes des énigmes :__"
  isR = not (type_ in ["unsolved","pointsInv"])
  def key(item):
    if type_ in ["unsolved",'solved']:return len(item[1].solvers)/item[1].max_solves
    elif type_ in ["pointsInv","points"]:return item[1].result
    else:return item[0]
  for key,value in sorted(main.enigmes.items(),key=key,reverse=isR):
    ret += "\n - énigme `"+str(key)+"`: "+value.name + ", pour "
    if value.result <0: ret += "une invitation."
    else: ret+=str(value.result)+"pts"
  return ret


@security.roleNeeded('user')
@commandLine.addFunction()
async def listAllPLayers(type_:(str,"all")) -> 'players [all|pointsInv|points]':
  """list all players.
  List all players.
   - `all` to list them all.
   - `pointsInv` to list them by less points.
   - `points` to list them by most points.
  """
  type_ = type_.lower()
  ret = "__Listes des joueurs :__\n"
  isR = (type_ in ["pointsInv"])
  def key(item):
    if type_ in ["pointsInv","points"]:return item[1].points
    else:return item[0]
  for key,value in sorted(main.users.items(),key=key,reverse=isR):
    usr = await client.fetch_user(int(key))
    ret += " - joueur "+usr.name+" (`<@"+str(key)+">`): avec "+str(value.points)+"pts"
  return ret

@security.roleNeeded('user')
@commandLine.addFunction()
async def changeBio(text:max) -> 'bio *<text>':
  """Change your bio
  Allow yourself to change your biography.
  Everything is allow. Even backline.
  """
  main.getUser(commandLine.message.author.id).bio = text
  main.save()
  return 'Bio changed.'

@security.roleNeeded('user')
@commandLine.addFunction()
async def info(type_:str,id_:(int,None),**kwargs) -> "info (enigme <ID> | user [<ID>]) ":
  """get informations
  Acces information about enigmes or user.
  """
  if type_ == "enigme":

    if id_ == None: return "Empty enigme's ID."
    eni = main.getEnigme(id_)
    if eni == None: return "unknow enigme."

    embed=discord.Embed(title=eni.name, description=eni.description, color=0x013fb)
    if eni.maj_sensitive: embed.set_author(name="Vous cherchez à la majuscule pret.")
    else: embed.set_author(name="Les majuscules n'ont pas d'importances.")
    text = "Vous pouvez gagnez "+str(eni.result)+"pts."
    if len(eni.solvers) >= eni.max_solves:
      text = "Trop de personnes ont répondu à l'énigmes, plus de points."
    elif (eni.result < 0):
      text = "Vous pouvez gagnez une invitation."
    embed.set_footer(text=text)

    await commandLine.message.channel.send("Enigme #`"+str(id_)+"`",embed=embed)

  elif type_ == "user":
    if id_ == None: id_ = commandLine.message.author.id
    usr = main.getUser(id_)
    if usr == None: return "unknow user."
    
    user___ = await client.fetch_user(int(id_))
    embed=discord.Embed(title=user___.name, description=usr.bio, color=0x0013fb)
    
    text = "Cet utillisateur à "+str(usr.points)+"pts."
    embed.set_footer(text=text)
    print("solved:",usr.solved,usr.no_points_solve)
    if usr.solved != []:embed.add_field(name="Enigmes réussies", value="\n".join(["#`"+str(x)+"`"+main.getEnigme(int(x)).name for x in usr.solved]))
    else:embed.add_field(name="Enigmes réussies", value="-")
    if usr.no_points_solve != []:embed.add_field(name="Enigmes réussies (sans points)", value="\n".join(["#`"+str(x)+"`"+main.getEnigme(int(x)).name for x in usr.no_points_solve ]))
    else:embed.add_field(name="Enigmes réussies (sans points)", value="-")

    await commandLine.message.channel.send("Utillisateur #`"+str(id_)+"`",embed=embed)

  else:return "Unknow action to perform info on."

@security.roleNeeded('user')
@commandLine.addFunction()
async def play(enigmeID:int,solution:str,**kwargs) -> "play <enigmeID> <solution> ":
  ret = main.play(enigmeID,commandLine.message.author.id,solution)
  main.save()
  return ret


@security.roleNeeded('admin','botmoderator')
@commandLine.addFunction()
async def data(action:str,name:(str,""),**kwargs) -> "data (save|reload) [backup]":
  """Save or reload data
  Use to save the user's data or to reload if new enigmes have been added.
  Reload can be dangerous if non-saved changed has been made."""
  
  if action == "save":
    if name != "backup":main.save()
    else:main.save("core/databases/backup/Eni-"+str(time.strftime("%H-%M-%S", time.localtime()))+".csv","core/databases/backup/Usr-"+str(time.strftime("%H-%M-%S", time.localtime()))+".csv")
  elif action == "reload":main.reload()
  else:return "Unknow action"
  return 'Executed with sucess.'