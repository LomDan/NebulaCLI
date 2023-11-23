import commandLine, os


def main() -> None:
    x = commandLine.CLI(os.getlogin(), os.path.expanduser("~"))
    x.cls()
    while True:
        try:
            cmd = input(x.prompt._prompt())
            if cmd != "":
                tmp = cmd.split()
                if tmp[0] in commandLine.commands:
                    commandLine.commands[tmp[0]](x, cmd[len(tmp[0]) + 1 :]) if tmp[
                        0
                    ] not in commandLine.browsers else commandLine.commands[tmp[0]](
                        x, tmp[0]
                    )
                else:
                    try:
                        x.handle(tmp)
                    except commandLine.CommandNotFoundError:
                        print("\n\tCommand not recognized.\n")
                    except Exception as e:
                        print(e)
        except KeyboardInterrupt:
            x.cls()
            break
        except EOFError:
            x.cls()
            break

    return


if __name__ == "__main__":
    main()
