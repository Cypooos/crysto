import inspect
from time import gmtime, strftime
import sys 

class Log():

    def __init__(self,channel=None,**kwargs):
        self.log_levels = kwargs.get("log_level",["ALL"])
        self.channel = channel
        self.first = True
    
    async def __out(self,message,log_type):
        if self.first:
            print("["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] Bot started.`")
            sys.stdout.flush()
            await self.channel.send("** **\n\n\n["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] Bot started.")
            self.first = False
        stack = inspect.stack()
        modCaller = inspect.getmodule(stack[2][0])
        try:
            classCaller = str(stack[2][0].f_locals["self"].__class__)
        except KeyError:
            classCaller = ""
        if classCaller != "": classCaller +=" "
        methodCaller = stack[2][0].f_code.co_name
        log = "`"+log_type+" - ["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] {"+str(modCaller.__name__)+"} "+str(classCaller)+str(methodCaller)+": "+str(message)+'`'
        if log_type in self.log_levels or "ALL" in self.log_levels:
            print("["+log_type+"] "+str(classCaller)+str(methodCaller)+": "+str(message))
            sys.stdout.flush()
        await self.channel.send(""+log+"")

    async def debug(self,message):await self.__out(message,"DEBUG")
    async def info(self,message):await self.__out(message,"INFO")
    async def warn(self,message):await self.__out(message,"WARN")
    async def command(self,message):await self.__out(message,"COMMAND")
    async def error(self,message):await self.__out(message,"ERROR")
    async def message(self,message):await self.__out(message,"MSG")
    async def custom(self,message,logName):await self.__out(message,logName)


