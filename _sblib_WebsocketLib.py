import websocket,ssl,logging

class Websocket:
    def __init__(self):
        self.wsAddr=""
        self.allowInsecure=False
        self._connected=False
        self.wsObj=None
        logging.debug(f"New Websocket Object: {self}")
        
    def connect(self):
        logging.debug(f"Connect to {self.wsAddr}, allowInsecure:{self.allowInsecure}")
        sslopt={}
        if self.allowInsecure:
            sslopt={"cert_reqs":ssl.CERT_NONE}

        self.wsObj=websocket.create_connection(self.wsAddr,sslopt=sslopt)
        self._connected=True
        logging.debug("Connected to ws")
        return 0
        
    def send(self,data:str):
        if not self._connected:
            return 1
            
        self.wsObj.send(data)
        logging.debug(f"Sent data into ws(length={len(data)})")
        return 0
        
    def recv(self):
        logging.debug(f"Recv data from ws")
        if self._connected:
            return self.wsObj.recv()
        else:
            return 1


def _createws(args,runtime):
    name=args[0]
    runtime.vars[name]=Websocket()
    return runtime,0

    
def _setWsAttr(args,runtime):
    available_choices=["wsAddr","allowInsecure"]
    var=args[0]
    name=args[1]
    if name not in available_choices:
        logging.critical(f"Invaild websocket Attribute")
        if runtime.exitonerr:
            exit(1)
        return runtime,1
    value=" ".join(args[2:])
    ws=runtime.vars.get(var)
    if type(ws) != Websocket:
        logging.critical(f"{var} is not a websocket object")
        if runtime.exitonerr:
            exit(1)
        return runtime,1
    if name == "wsAddr":
        ws.wsAddr=value
    elif name == "allowInsecure":
        ws.allowInsecure=value.lower() == "true"
    runtime.vars[var]=ws
    return runtime,0

    
def _wsConn(args,runtime):
    ws=runtime.vars.get(args[0])
    if type(ws) != Websocket:
        logging.critical(f"{args[0]} is not a websocket object")
        if runtime.exitonerr:
            exit(1)
        return runtime,1
    ws.connect()
    return runtime,0
    
    
def _wsSend(args,runtime):
    ws=runtime.vars.get(args[0])
    if type(ws) != Websocket:
        logging.critical(f"{args[0]} is not a websocket object")
        if runtime.exitonerr:
            exit(1)
        return runtime,1
    ws.send(runtime.vars.get(args[1]))
    return runtime,0

def _wsRecv(args,runtime):
    ws=runtime.vars.get(args[0])
    if type(ws) != Websocket:
        logging.critical(f"{args[0]} is not a websocket object")
        if runtime.exitonerr:
            exit(1)
        return runtime,1
    runtime.vars[args[1]]=ws.recv()
    return runtime,0
    
def _wsClose(args,runtime):
    ws=runtime.vars.get(args[0])
    if type(ws) != Websocket:
        logging.critical(f"{args[0]} is not a websocket object")
        if runtime.exitonerr:
            exit(1)
        return runtime,1
    runtime.vars[args[0]].wsObj.close()
    del runtime.vars[args[0]]
    return runtime,0

def init(runtime):
    runtime.commandlist.addCommand("websocket",_createws)
    runtime.commandlist.addCommand("ws.set",_setWsAttr)
    runtime.commandlist.addCommand("ws.connect",_wsConn)
    runtime.commandlist.addCommand("ws.send",_wsSend)
    runtime.commandlist.addCommand("ws.recv",_wsRecv)
    runtime.commandlist.addCommand("ws.close",_wsClose)
    return runtime