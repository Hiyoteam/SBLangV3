import logging,traceback


class CommandList:
    def __init__(self):
        logging.debug(f"New CommandList Object: {self}")
        self.commands = {}

    def addCommand(self, name, function):
        self.commands[name] = function

    def getCommand(self, name):
        return self.commands.get(name)


class Command:
    def __init__(self, line, runtime):
        logging.debug(f"New Command Object: {self}")
        self.line = line
        self.runtime = runtime
        self._resolve()  # Resolve the command

    def _resolve(self):
        command = self.line.split(" ")
        self.command = command[0]
        self.args = []
        if len(command) > 1:
            self.args = command[1:]
        logging.debug(f"Resolve command: {command}")

    def execute(self, commandlist):
        try:
            command = commandlist.getCommand(self.command)
            if command:
                logging.debug(f"Run command: {command}")
                return command(self.args, self.runtime)
            logging.debug(
                f"Command not found, return current runtime with status 1")
            return self.runtime, 1
        except:
            logging.critical(f"Error when executeing {self.command} with args {self.args}. Traceback:\n{traceback.format_exc()}")
            if self.runtime.exitonerr:
                exit(1)
            return self.runtime, 1


class Runtime:
    def __init__(self, exitOnError=True):
        logging.debug(f"New runtime Object at: {self}")
        self.errored = False
        self.vars = {}
        self.data = {}
        self.pointerdata = []
        self.commandlist = CommandList()
        self.exitonerr = exitOnError
        self.globalChecker = []
        for _ in range(256):
            self.pointerdata.append(0)
        self.pointer = 0

    def _get_pointer_data(self):
        return self.pointerdata[self.pointer]

    def execute(self, __command):
        # execute GlobalBinder first
        for function in self.globalChecker:
            status= function(self,__command)
        cmd = Command(__command, self)
        result = cmd.execute(self.commandlist)
        if result != 0:
            if self.exitonerr:
                logging.fatal(f"Function {__command} execute failed. Exiting")
                exit(1)
