import os 


class Enigme():
  def __init__(self,name,description,solution,solvers=[],no_points_solvers=[],max_solves=0,result=None,maj_sensitive=False,help_=None):
    self.name = name
    self.description = description
    self.solution = solution
    self.solvers = [int(x) for x in solvers.split(",")]
    self.no_points_solvers = [int(x) for x in no_points_solvers.split(",")]
    self.max_solves = int(max_solves)
    self.result = result
    self.maj_sensitive = bool(maj_sensitive)
    self.help = help_

  @staticmethod
  def fromLine(line):
    return Enigme(*[x.replace("|up|","|") for x in line.replace("|nl|","\n").split("|sl|")])

  def save(self):
    def _set(x):return x.replace("|","|up|").replace("\n","|nl|")
    return "|sl|".join([_set(x) for x in [
      self.name,
      self.description,
      self.solution,
      ",".join(self.solvers),
      ",".join(self.no_points_solvers),
      str(self.max_solves),
      self.result,
      str(self.maj_sensitive),
      self.help
    ]])

class User():
  def __init__(self,discordId,bio,solved=[],no_points_solve=[],points=0):
    self.discordId = int(discordId)
    self.bio = bio
    self.solved = [int(x) for x in solvers.split(",")]
    self.no_points_solve = [int(x) for x in no_points_solve.split(",")]
    self.points = int(points)

  @staticmethod
  def fromLine(line):
    return User(*[x.replace("|up|","|") for x in line.replace("|nl|","\n").split("|sl|")])

  def save(self):
    def _set(x):return x.replace("|","|up|").replace("\n","|nl|")
    return "|sl|".join([_set(x) for x in [
      str(self.discordId),
      self.bio,
      ",".join(self.solved),
      str(self.points)
    ]])

class EnigmesManager():

  def __init__(self,enigmesPath,userPath):
    self.enigmesPath = enigmesPath
    self.userPath = userPath
    self.enigmes = [] # index = id = line number in file. 
    self.users = []
    self.reload()
  
  def reload(self):
    self.enigmes = [];self.users = []

    file = open(self.enigmesPath,"r")
    for line in file.readlines():self.enigmes.append(Enigme.fromLine(line))
    file.close()

    file = open(self.userPath,"r")
    for line in file.readlines():self.users.append(User.fromLine(line))
    file.close()
  
  def addEnigme(self,name,description,solution,result=None,maj_sensitive=False,help_=None):
    self.enigmes.append(Enigme(name,description,solution,[],result,maj_sensitive,help_))
  
  def addUser(self,discordID,bio):
    self.users.append(User(discordID,bio,[],[],0))

  def play(self,eID,dID,soluce):
    if not dID in [x.discordId for x in self.users]: return "Vous n'avez pas de compte."
    user = [x for x in self.users if x.discordID == dID][0]
    if not eID < len(self.enigmes): return "L'énigme n'existe pas."
    enigme = self.enigmes[eID]
    sol = self.enigmes[eID].solution
    if sol.maj_sensitive:sol.lower();soluce.lower()
    if not soluce == sol: return "Mauvaise réponse..."
    if len(enigme.solvers) == enigme.max_solves: # no more rooms
      enigme.no_points_solvers.append(dID)
      user.no_points_solve.append(eID)
      return "L'enigme ne vaux plus rien, mais GG :D"
    else:
      enigme.solvers.append(dID)
      user.solved.append(eID)
      if isinstance(enigme.result,int):
        user.points += enigme.result
        return "Tu as gagné "+str(enigme.result)+"pts, GG :D"
      return "Tu l'a réussi, mais on ne te donne rien. Un peu triste."

  def save(self):
    os.remove(self.enigmesPath);os.remove(self.userPath)

    file = open(self.enigmesPath,"w")
    for enigme in self.enigmes: file.write(enigme.save())
    file.close()

    file = open(self.userPath,"r")
    for user in self.users:file.write(user.save())
    file.close()

