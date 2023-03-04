import logging,_sblib_builtins,sblangv2

logging.basicConfig(format="[%(asctime)s] %(filename)s:%(lineno)d, in %(funcName)s(): %(levelname)s: %(message)s",level=logging.DEBUG)

commands="""
import WebsocketLib
string a {"cmd":"join","channel":"your-channel","nick":"SBLbotV2"}
string b {"cmd":"chat","text":"Hello the motherfucking world!"}
websocket ws
ws.set ws wsAddr wss://hack.chat/chat-ws
ws.set ws allowInsecure true
ws.connect ws
ws.send ws a
ws.send ws b
ws.close ws
""".strip('\n')

runtime = sblangv2.Runtime(False)
runtime.namespace.addCommand("import", _sblib_builtins.import_)
runtime.execute("import builtins")
for command in commands.split('\n'):
    runtime.execute(command)
