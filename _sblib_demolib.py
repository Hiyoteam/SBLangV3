def hello_world(args, runtime):
    print("Hello,world!")
    return runtime, 0  # runtime: Runtime Object     0: status code


def init(runtime):
    runtime.commandlist.addCommand("helloWorld", hello_world)
    return runtime
