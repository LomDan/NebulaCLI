import os, subprocess, platform, hashlib
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Colors:
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
            if (path != "\\") and (path != ".."):
                self.cwd += path + "\\"
                for i in path.split(sep="\\"):
                    self.tree.append(i + "\\")
            elif path == "\\":
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
        subprocess.Popen("C:\\Windows\\explorer.exe")
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
             | \ | | | ____| |  _ \  | |   | | | |      / _  \\
             |  \| | | |___  | |_| | | |   | | | |     | |_|  |
             | \ \ | | ____| |____/  | |   | | | |     |  __  | 
             | |\  | | |___  |  _ \  | |___| | | |___  | |  | | 
             | | \_| |_____| | |_| | |_______| |_____| | |  |_| 
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
        print("\x1bc\x1b[H")
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
        def chksum(function: str, filename: str) -> str:
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
