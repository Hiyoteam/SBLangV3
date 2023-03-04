import json


def objFromJson(args, runtime):
    jsonName=args[0]
    targetName = args[1]
    runtime.vars[targetName] = json.loads(runtime.vars[jsonName])
    return runtime,0


def objToJson(args, runtime):
    objName=args[0]
    targetName = args[1]
    runtime.vars[targetName] = json.dumps(runtime.vars[objName])
    return runtime,0


def CIsGetAFromB(args, runtime):
    dictName=args[1]
    keyName=args[0]
    targetName = args[2]
    runtime.vars[targetName] = runtime.vars[dictName][keyName]
    return runtime,0

def setAOfBtoC(args, runtime):
    dictName=args[1]
    keyName=args[0]
    sourceName = args[2]
    runtime.vars[dictName][keyName] = runtime.vars[sourceName]
    return runtime,0


def init(runtime):
    for i, j in [('obj|get', CIsGetAFromB), ('obj|set', setAOfBtoC), ('obj|fromjson', objFromJson), ('obj|tojson', objToJson)]:
        runtime.namespace.addCommand(i, j)
    return runtime
