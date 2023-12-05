import commandLine


def main() -> None:
    x = commandLine.CLI()
    x.cls()
    while True:
        try:
            cmd = input(x.prompt._prompt())
            if cmd != "":
                x.command(cmd)
        except KeyboardInterrupt:
            x.cls()
            break
        except EOFError:
            x.cls()
            break

    return


if __name__ == "__main__":
    main()
