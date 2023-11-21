import os, subprocess, platform, hashlib
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Colors:
    CLEAR = "\x1bc\x1b[H"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


class CLI:
    def __init__(self, user: str, home: str) -> None:
        self.user: str = user
        self.home: str = home
        os.chdir(self.home)
        self.cwd: str = home
        self.tree: list[str] = [self.home]
        self.cache: str = ""
        return

    def echo(self, string: str) -> None:
        if (string.__contains__("$")) and (string.count("$") == 2):
            match string[string.find("$") + 1 : string.rfind("$")]:
                case "user":
                    string = (
                        string[: string.find("$")]
                        + self.user
                        + string[string.rfind("$") + 1 :]
                    )
                case "home":
                    string = (
                        string[: string.find("$")]
                        + self.home
                        + string[string.rfind("$") + 1 :]
                    )
                case "cwd":
                    string = (
                        string[: string.find("$")]
                        + self.cwd
                        + string[string.rfind("$") + 1 :]
                    )
        print(string)
        return

    def ls(self, dir: str) -> None:
        try:
            if dir == "":
                print(f"\n----{self.cwd}----")
                for i in os.listdir(self.cwd):
                    if i.__contains__("."):
                        print(f"--f-  {i}")
                    else:
                        print(f"-d--  {i}")
            else:
                print(f"----{dir}----")
                for i in os.listdir(dir):
                    if i.__contains__("."):
                        print(f"--f-  {i}")
                    else:
                        print(f"-d--  {i}")
        except:
            print("Directory not found")
        return

    def cd(self, path: str) -> None:
        try:
            if (path != "\\") and (path != "/") and (path != ".."):
                self.cwd += path + "\\"
                for i in path.split(sep="\\"):
                    self.tree.append(i + "\\")
            elif (path == "\\") or (path == "/"):
                self.cwd = self.home
                self.tree = [self.home]
            elif path == "..":
                self.tree.pop()
                self.cwd = "".join(self.tree)
            os.chdir(self.cwd)
            self.cache = self.cwd
        except:
            self.cwd = self.cache
            print("Directory not found")
        return

    def browser(self, name: str) -> None:
        match name:
            case "brave":
                subprocess.Popen(
                    "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                )
            case "opera":
                subprocess.Popen(
                    "C:\\Users\\stacy\\AppData\\Local\\Programs\\Opera\\launcher.exe"
                )
        return

    def file_explorer(self, *args) -> None:
        # subprocess.Popen("C:\\Windows\\explorer.exe")
        try:
            if len(args[0]) == 0:
                subprocess.run(["explorer"])
            else:
                subprocess.run(["explorer"] + [a for a in args])
        except Exception as e:
            print(e)
        return
        return

    def python(self, args: str) -> None:
        try:
            if len(args[0]) == 0:
                subprocess.run(["python"], check=True)
            else:
                subprocess.run(["python"] + [a for a in args], check=True)
        except Exception as e:
            print(e)
        return

    def pip(self, *args) -> None:
        try:
            if len(args[0]) == 0:
                subprocess.run(["pip"], check=True)
            else:
                subprocess.run(["pip"] + [a for a in args], check=True)
        except Exception as e:
            print(e)
        return

    def git(self, *args) -> None:
        try:
            if len(args[0]) == 0:
                subprocess.run(["git"])
            else:
                subprocess.run(["git"] + [a for a in args], check=True)
        except Exception as e:
            print(e)
        return

    def node(self, *args) -> None:
        try:
            if len(args[0]) == 0:
                subprocess.run(["node"], check=True)
            else:
                subprocess.run(["node"] + [a for a in args], check=True)
        except Exception as e:
            print(e)
        return

    def display(self, *args) -> None:
        print(
            f"""
             {Colors.PURPLE}
              _   _   _____   ____    _     _   _        ____
             | \\ | | | ____| |  _ \\  | |   | | | |      / _  \\
             |  \\| | | |___  | |_| | | |   | | | |     | |_|  |
             | \\ \\ | | ____| |____/  | |   | | | |     |  __  | 
             | |\\  | | |___  |  _ \\  | |___| | | |___  | |  | | 
             | | \\_| |_____| | |_| | |_______| |_____| | |  |_| 
             |_|             |____/                    |_|
             {Colors.RESET}
            Nebula CLI
            Unleash the Power of Nebula: Where Command Lines Reach for the Stars!
            
             __________________________________________________________________
            |System info:                                                   
            |               OS:\t\t{Colors.BLUE}{platform.system()}{Colors.RESET}                         
            |               User:\t{Colors.BLUE}{os.getlogin()}{Colors.RESET}                         
            |               Time:\t{Colors.BLUE}{(x := str(datetime.now()))[:x.rfind('.')]}{Colors.RESET}
            |               Status:\t{Colors.BLUE}All good!{Colors.RESET}
            |__________________________________________________________________

            """
        )
        return

    def mkfile(self, filename: str) -> None:
        with open(filename, "w") as f:
            f.write("")
        return

    def rm(self, filename: str) -> None:
        os.remove(filename)
        return

    def cat(self, filename: str) -> None:
        with open(filename, "r") as f:
            print(f.read())
        return

    def cls(self, *args) -> None:
        print(Colors.CLEAR)
        return

    def nvim(self, *args) -> None:
        try:
            if len(args[0]) == 0:
                subprocess.run(["nvim"], check=True)
            else:
                subprocess.run(["nvim"] + [a for a in args], check=True)
        except Exception as e:
            print(e)
        return

    def code(self, *args) -> None:
        try:
            if len(args[0]) == 0:
                subprocess.run(["code"], check=True)
            else:
                subprocess.run(["code"] + [a for a in args], check=True)
        except Exception as e:
            print(e)
        return

    def subl(self, *args) -> None:
        try:
            if len(args[0]) == 0:
                subprocess.run(
                    ["C:\\Program Files\\Sublime Text\\subl.exe"], check=True
                )
            else:
                subprocess.run(
                    ["C:\\Program Files\\Sublime Text\\subl.exe"] + [a for a in args],
                    check=True,
                )
        except Exception as e:
            print(e)
        return

    def lapce(self, *args) -> None:
        try:
            if len(args[0]) == 0:
                subprocess.run(["lapce"], check=True)
            else:
                subprocess.run(["lapce"] + [a for a in args], check=True)
        except Exception as e:
            print(e)
        return

    def checksum(self, *args) -> None:
        def chksum(function: str, filename: str) -> str | ValueError:
            match function:
                case "sha256":
                    with open(filename, "r") as f:
                        return hashlib.sha256(f.read().encode()).hexdigest()
                case "sha512":
                    with open(filename, "r") as f:
                        return hashlib.sha512(f.read().encode()).hexdigest()
            return ValueError("unknown hash function")

        def check(function: str, filename: str, csum: str) -> bool | ValueError:
            match function:
                case "sha256":
                    with open(filename, "r") as f:
                        return csum == hashlib.sha256(f.read().encode()).hexdigest()
                case "sha512":
                    with open(filename, "r") as f:
                        return csum == hashlib.sha512(f.read().encode()).hexdigest()
            return ValueError("unknown hash function")

        try:
            args = args[0].split()
            match len(args):
                case 2:
                    print(chksum(args[0], args[1]))
                case 3:
                    print(check(args[0], args[1], args[2]))
        except ValueError as e:
            print(e)


class Prompt:
    def __init__(self, cli: CLI) -> None:
        self.usr: str = cli.user
        self.cwd: str = cli.cwd
        self.home: str = cli.home
        self.prompt: str = f"({self.usr}) \x01~ $ "
        self.change: bool = False
        self.cli: CLI = cli

        def read() -> str | None:
            try:
                with open(
                    "C:\\Software Development\\Game\\usr config\\usr.config", "r"
                ) as f:
                    return f.read()
            except:
                os.mkdir("C:\\Software Development\\Game\\usr config")
                with open(
                    "C:\\Software Development\\Game\\usr config\\usr.config", "w"
                ) as f:
                    f.write("")
                read()
            return

        if isinstance((x := read()), str):
            self.usr_config = x
        self.alias()
        self.config(self.prompt)
        return

    def alias(self) -> None:
        if len(self.usr_config) > 0:
            info = self.usr_config.split(sep="}\n")
            idx = -1
            for i in info:
                if i[i.find("usr@") + len("usr@") : i.find(" ")] == os.getlogin():
                    idx = info.index(i)
                    break
            if idx != -1:
                info = info[idx].splitlines()
                for i in info:
                    idx = i.split()
                    match idx[0]:
                        case "alias":
                            self.usr = idx[2]
                        case "prompt":
                            self.prompt = " ".join(idx[2:]) + " "
                            self.change = True
        return

    def config(self, config: str):
        specials = {"usr": self.usr, "cwd": "\x01"}

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
                        string = string[:a] + specials["cwd"] + string[b + 1 :]
            return string

        self.prompt = check(config)
        return

    def _prompt(self) -> str:
        if self.home != os.getcwd():
            return self.prompt.replace("\x01", f"{os.getcwd()} ")
        return self.prompt


commands = {
    "clear": CLI.cls,
    "echo": CLI.echo,
    "ls": CLI.ls,
    "cd": CLI.cd,
    "brave": CLI.browser,
    "opera": CLI.browser,
    "explorer": CLI.file_explorer,
    "display": CLI.display,
    "mkfile": CLI.mkfile,
    "rm": CLI.rm,
    "cat": CLI.cat,
    "nvim": CLI.nvim,
    "python": CLI.python,
    "pip": CLI.pip,
    "git": CLI.git,
    "node": CLI.node,
    "code": CLI.code,
    "subl": CLI.subl,
    "chksum": CLI.checksum,
}
browsers = ["brave", "opera"]
