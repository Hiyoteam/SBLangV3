import sblangv2
import logging
import _sblib_builtins
logging.basicConfig(
    format="[%(asctime)s] %(filename)s:%(lineno)d, in %(funcName)s(): %(levelname)s: %(message)s", level=logging.DEBUG)
commands = ["import builtins", "define awa","d string owo Hello world","d out owo","d end","out awa","call awa"]
runtime = sblangv2.Runtime()
runtime.namespace.addCommand("import", _sblib_builtins.import_)
for command in commands:
    runtime.execute(command)
