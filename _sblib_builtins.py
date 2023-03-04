import logging


class Function:
    def __init__(self):
        self.commands = []

    def runAll(self, runtime):
        logging.debug(f"Call func: {self}")
        for command in self.commands:
            runtime.execute(command)
        return runtime
    def __repr__(self) -> str:
        return f"[SBLangV3 Function Object](cmdlen={len(self.commands)})"


def out(args, runtime):
    string = runtime.vars[args[0]]
    print(string, end="", flush=True)
    return 0


def string(args, runtime):
    varname = args[0]
    logging.debug(f"Assign string: {args}")
    vardata = " ".join(args[1:])
    runtime.vars[varname] = vardata
    return 0


def import_(args, runtime):
    # import the lib
    logging.debug(f"Import lib: {args[0]}")
    runtime = __import__(f"_sblib_{args[0]}").init(runtime)
    return 0  # 0:status code


def define(args, runtime):
    logging.debug(f"Define new function: {args}")
    if runtime.data.get("DEFINEING", False):
        logging.critical("'define' called twice")
        if runtime.exitorerr:
            exit(1)
        return 1
    name = "".join(args)
    runtime.data["DEFINEING"] = True
    runtime.data["DEFINE_NAME"] = name
    runtime.data["DEFINE_OBJECT"] = Function()
    logging.debug(
        f"Adding DEFINEING, DEFINE_NAME, DEFINE_OBJECT into runtime data")
    return 0


def d_process(args, runtime):
    command = " ".join(args)
    if not runtime.data.get("DEFINEING", False):
        logging.critical("d called outside define")
        if runtime.exitorerr:
            exit(1)
        return 1
    if command == "end":
        logging.debug("Processing d end command")
        runtime.data["DEFINEING"] = False
        def_name = runtime.data["DEFINE_NAME"]
        def_obj = runtime.data["DEFINE_OBJECT"]
        runtime.vars[def_name] = def_obj
        runtime.data["DEFINE_NAME"] = None
        runtime.data["DEFINE_OBJECT"] = None
        logging.debug(
            "Cleaned up and put the function object into runtime var list")
        return 0
    runtime.data["DEFINE_OBJECT"].commands.append(command)
    return 0

def checkD(runtime,command):
    logging.debug("Checking define")
    if runtime.data.get("DEFINEING", False) and not command.startswith("d "):
        logging.critical("'d end' missing")
        if runtime.exitonerr:
            exit(1)
        return 1
    return 0

def callfun(args, runtime):
    logging.debug(f"Call function: {args}")
    name = args[0]
    if type(runtime.vars[name]) != Function:
        logging.critical(f"Not a function.")
        if runtime.exitorerr:
            exit(1)
        return 1
    runtime = runtime.vars[name].runAll(runtime)
    return 0

def comment(args,runtime):
    return 0
    
def init(runtime):
    runtime.commandlist.addCommand("out", out)
    runtime.commandlist.addCommand("string", string)
    runtime.commandlist.addCommand("import", import_)
    runtime.commandlist.addCommand("define", define)
    runtime.commandlist.addCommand("d", d_process)
    runtime.commandlist.addCommand("call", callfun)
    runtime.commandlist.addCommand("//",comment)
    runtime.globalChecker.append(checkD)
    return runtime
