import commandLine, os


x = commandLine.CLI(os.getlogin(), "C:\\")
print("\x1bc\x1b[H")
while True:
    try:
        cmd = input(
            f"({x.user}) ~ $ " if x.cwd == x.home else f"({x.user}) {x.cwd} ~ $ "
        )
        if cmd != "":
            tmp = cmd.split()
            if tmp[0] in commandLine.commands:
                commandLine.commands[tmp[0]](x, cmd[len(tmp[0]) + 1 :]) if tmp[
                    0
                ] not in commandLine.browsers else commandLine.commands[tmp[0]](
                    x, tmp[0]
                )
            else:
                print("\n\tCommand not recognized.\n")
    except KeyboardInterrupt:
        print("\x1bc\x1b[H")
        break
    except EOFError:
        print("\x1bc\x1b[H")
        break
