import os 
import random

class Enigme():
  def __init__(self,name,description,solution,solvers=[],no_points_solvers=[],max_solves=0,result=None,maj_sensitive=False,help_=""):
    self.name = name
    self.description = description
    self.solution = solution
    if isinstance(solvers,list):self.solvers = solvers
    elif isinstance(solvers,str) and solvers != "":self.solvers = [int(x) for x in solvers.split(",")]
    else:self.solvers = []
    if isinstance(no_points_solvers,list):self.no_points_solvers = no_points_solvers
    if isinstance(no_points_solvers,str) and no_points_solvers != "": self.no_points_solvers = [int(x) for x in no_points_solvers.split(",")]
    else:self.no_points_solvers = []
    self.max_solves = int(max_solves)
    self.result = int(result)
    self.maj_sensitive = (maj_sensitive == 'True')
    self.help = help_
    if self.help == None: self.help = ""

  @staticmethod
  def fromLine(line):
    return Enigme(*[x.replace("|up|","|") for x in line.replace("|nl|","\n").split("|sl|")])

  def save(self):
    def _set(x):
      return str(x).replace("|","|up|").replace("\n","|nl|")
    return "|sl|".join([_set(x) for x in [
      self.name,
      self.description,
      self.solution,
      ",".join([str(x) for x in self.solvers]),
      ",".join([str(x) for x in self.no_points_solvers]),
      str(self.max_solves),
      str(self.result),
      str(self.maj_sensitive),
      self.help
    ]])

class User():
  def __init__(self,discordId,bio,solved=[],no_points_solve=[],points=0):
    self.discordId = int(discordId)
    self.bio = bio
    if isinstance(solved,list):self.solved = solved
    if isinstance(solved,str) and solved !='':self.solved = [int(x) for x in solved.split(",")]
    else:self.solved = []
    if isinstance(no_points_solve,list):self.no_points_solve = no_points_solve
    if isinstance(no_points_solve,str) and no_points_solve != "":self.no_points_solve = [int(x) for x in no_points_solve.split(",")]
    else:self.no_points_solve = []
    self.points = int(points)

  @staticmethod
  def fromLine(line):
    return User(*[x.replace("|up|","|") for x in line.replace("|nl|","\n").split("|sl|")])

  def save(self):
    def _set(x):return x.replace("|","|up|").replace("\n","|nl|")
    return "|sl|".join([_set(x) for x in [
      str(self.discordId),
      self.bio,
      ",".join([str(x) for x in self.solved]),
      ",".join([str(x) for x in self.no_points_solve]),
      str(self.points)
    ]])

class EnigmesManager():

  def __init__(self,enigmesPath,userPath):
    self.enigmesPath = enigmesPath
    self.userPath = userPath
    self.enigmes = {}
    self.users = {}
    self.reload()
  
  def reload(self):
    self.enigmes = {};self.users = {}

    file = open(self.enigmesPath,"r")
    for line in file.readlines():self.enigmes[int(line[:-1].split(":")[0])] = Enigme.fromLine(":".join(line[:-1].split(":")[1:]))
    file.close()

    file = open(self.userPath,"r")
    for line in file.readlines():self.users[int(line[:-1].split(":")[0])] = User.fromLine(":".join(line[:-1].split(":")[1:]))
    file.close()
  
  def addEnigme(self,name,description,solution,max_solves=3,result=None,maj_sensitive=False,help_=None):
    val = random.randint(0,999)
    while str(val) in self.enigmes.keys():val += random.randint(0,999)
    self.enigmes[str(val)] = Enigme(name,description,solution,[],[],max_solves,result,maj_sensitive,help_)
  
  def addUser(self,discordID,bio):
    self.users[str(discordID)] = User(discordID,bio)

  def getEnigme(self,id_):
    print(id_,self.enigmes)
    if int(id_) in self.enigmes.keys():return self.enigmes[int(id_)]
    return None
  
  def getUser(self,id_):
    print(id_,self.users)
    if int(id_) in self.users.keys():return self.users[int(id_)]
    return None

  def play(self,eID,dID,soluce):
    if not dID in self.users.keys(): return "Vous n'avez pas de compte."
    user = [x for x in self.users.values() if x.discordId == dID][0]
    if not int(eID) in self.enigmes.keys(): return "L'énigme n'existe pas."
    enigme = self.enigmes[eID]
    sol = enigme.solution
    if dID in enigme.solvers:return "Vous y avez déjà répondu :D"
    if not enigme.maj_sensitive:sol = sol.lower();soluce = soluce.lower()
    if soluce != sol: return "Mauvaise réponse..."
    if len(enigme.solvers) >= enigme.max_solves: # no more rooms
      enigme.no_points_solvers.append(dID)
      user.no_points_solve.append(eID)
      return "L'enigme ne vaux plus rien, mais GG :D"
    else:
      enigme.solvers.append(dID)
      user.solved.append(eID)
      if enigme.result>0:
        user.points += enigme.result
        return "Tu as gagné "+str(enigme.result)+"pts, GG :D"
      else:
        return 'Ceci est totalement une invitation discord.gg/XXXXX'
      return "Tu l'a réussi, mais on ne te donne rien. Un peu triste."

  def save(self,pathEni="",pathUsr=""):
    if pathEni == "":pathEni = self.enigmesPath
    if pathUsr == "":pathUsr = self.userPath
    if os.path.exists(pathEni):os.remove(pathEni)
    if os.path.exists(pathUsr):os.remove(pathUsr)

    file = open(pathEni,"w")
    for key, enigme in self.enigmes.items(): file.write(str(key)+":"+enigme.save()+"\n")
    file.close()

    file = open(pathUsr,"w")
    for key, user in self.users.items(): file.write(str(key)+":"+user.save()+"\n")
    file.close()
    self.reload()

