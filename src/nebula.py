import commandLine, os


def main() -> None:
    x = commandLine.CLI(os.getlogin(), "C:\\")
    prmpt = commandLine.Prompt(x)
    x.cls()
    while True:
        try:
            cmd = input(prmpt._prompt())
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
            x.cls()
            break
        except EOFError:
            x.cls()
            break

    return


if __name__ == "__main__":
    main()
