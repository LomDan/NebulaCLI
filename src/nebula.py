import commandLine, os


def init() -> str:
    info = ""
    try:
        with open(f"usr config\\usr.config", "r") as f:
            info = f.read()
        return info
    except:
        os.mkdir("usr config")
        with open(f"usr config\\usr.config", "w") as f:
            f.write("")
        init()


def prompt(options: str, usr: str, home: str) -> str:
    specials = {"usr": usr, "home": home}

    def check(string: str) -> str:
        res = []
        for i in range(len(string)):
            if string[i] == "*":
                res.append(i)
        res = list(zip(res, res[1:] + res[:1]))
        res = [i for i in res if res.index(i) % 2 == 0]
        for a, b in res:
            match string[a + 1 : b]:
                case "usr":
                    string = string[:a] + specials["usr"] + string[b + 1 :]
                case "cwd":
                    string = string[:a] + specials["home"] + string[b + 1 :]
        return string

    options = check(options)
    return options


def alias(info: str) -> list[str]:
    _usr, _home, _prompt = "", "", ""
    if info != "":
        info = info.split(sep="}\n")
        idx = 0
        for i in info:
            if i[i.find("usr@") + len("usr@") : i.find(" ")] == os.getlogin():
                idx = info.index(i)
                break
        info = info[idx].splitlines()[1:-1]
        for i in info:
            idx = i.split()
            match idx[0]:
                case "alias":
                    _usr = idx[2][:-1]
                case "prompt":
                    _prompt = " ".join(idx[2:]).removesuffix(",")
                case "home":
                    _home = idx[2][:-1]
    return [_usr, _home, _prompt]


def main() -> None:
    config = init()
    info = alias(config)
    _usr, _home, _prompt = "", "", ""
    if info[0] != "":
        _usr = info[0]
    if info[1] != "":
        _home = info[1]
    if info[2] != "":
        _prompt = prompt(info[2], _usr, _home)

    x = commandLine.CLI(
        _usr if _usr != "" else os.getlogin(), _home if _home != "" else "C:\\"
    )
    print("\x1bc\x1b[H")
    while True:
        try:
            cmd = input(
                _prompt
                if _prompt != ""
                else f"({x.user}) ~ $ "
                if x.cwd == x.home
                else f"({x.user}) {x.cwd} ~ $ "
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

    return


if __name__ == "__main__":
    main()
