# --- imports ---
import os, subprocess, platform, hashlib, usrconfig, shutil
from datetime import datetime
from dataclasses import dataclass


# --- custom errors ---
class PathRequiredError(BaseException):
    """
    Used for when a command might be a system command but is not listed in the system
    """

    ...


class CommandNotFoundError(BaseException):
    """
    Used to check if a command is not found
    """

    ...


# --- modified classes ---


class str(str):
    def find_all(self, char: str) -> list[tuple[int]]:
        index = []
        for i in range(len(self)):
            if self[i] == char:
                index.append(i)
        paired = list(zip(index, index[1:]))
        return [i for i in paired if paired.index(i) % 2 == 0]


# --- base classes ---
class CLI:
    """
    Base class for the nebula cli itself
    """

    def __init__(self) -> None:
        self.usr: str = os.getlogin()
        self.home: str = os.path.expanduser("~") + "\\"
        os.chdir(self.home)
        self.cwd: str = self.home
        self.tree: list[str] = [self.home]
        self.cache: str = self.cwd
        self.hot_reload()
        self.commands = {
            "clear": CLI.cls,
            "echo": CLI.echo,
            "ls": CLI.ls,
            "cd": CLI.cd,
            "display": CLI.display,
            "mkfile": CLI.mkfile,
            "rm": CLI.rm,
            "cat": CLI.cat,
            "catb": CLI.catb,
            "chksum": CLI.checksum,
            "config": CLI.config,
            "list": CLI.list_all,
            "rmdir": CLI.rmdir,
        }
        self.browsers = ["brave", "opera"]
        return

    def hot_reload(self) -> None:
        if os.path.exists(os.path.expanduser("~") + "\\NebulaCLI"):
            self.prompt = Prompt(self)
        else:
            os.mkdir(os.path.expanduser("~") + "\\NebulaCLI")
            self.prompt = Prompt(self)
        return

    def echo(self, string: str) -> None:
        """
        writes text to system.stdout, it can also write certain variables in with that text
        """
        print(string)
        return

    def ls(self, dir: str) -> None:
        """
        lists all files and sub-directories within a directory\n
        if you type ls, it will list the current dir\n
        however, if you specify a sub-directory (ls *sub-dir*), it will list the sub-directory you specified
        """
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
        """
        cd changes the current working directory
        """
        if path.__contains__("/"):
            path = path.replace("/", "\\", path.count("/"))
        if path.__contains__(self.cwd):
            path = path[path.index(self.cwd) + len(self.cwd) :]
        try:
            if len(path) > 2:
                self.cwd += path + "\\"
                [self.tree.append(i + "\\") for i in path.split(sep="\\")]
                os.chdir(self.cwd)
                self.cache = self.cwd
            elif path == "\\":
                os.chdir("\\")
                self.cwd = os.getcwd()
                self.tree = [self.cwd]
                self.cache = self.cwd
            elif path == "..":
                self.tree.pop()
                self.cwd = "".join(self.tree)
                os.chdir(self.cwd)
                self.cache = self.cwd
        except:
            self.cwd = self.cache
            os.chdir(self.cwd)
            print("\n\tDirectory not found\n")
        return

    def browser(self, name: str) -> None:
        """
        used to open up browser instances\n
        there is no browser command in nebula however,\n
        as to open a new instance, you should type the name of the browser
        """
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

    def display(self, *args) -> None:
        """
        displays some system info and some info about nebula itself
        """
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
        """
        creates a new file
        """
        with open(filename, "w") as f:
            f.write("")
        return

    def rm(self, filename: str) -> None:
        """
        removes or deletes a file
        """
        os.remove(filename)
        return

    def rmdir(self, dirname: str) -> None:
        """
        removes or deletes a directory
        """
        try:
            os.rmdir(dirname)
        except:
            try:
                shutil.rmtree(dirname)
            except Exception as e:
                print(e)
        return

    def cat(self, filename: str) -> None:
        """
        reads the contents of a file and writes it to system.stdout
        """
        if os.path.exists(filename):
            with open(filename, "r") as f:
                print(f.read())
            return
        else:
            print("\n\tFile not found\n")

    def catb(self, filename: str) -> None:
        """
        reads the contents of a file and writes the bytes to system.stdout
        """
        with open(filename, "r") as f:
            print(f.read().encode())
        return

    def cls(self, *args) -> None:
        """
        clears the console
        """
        print(Colors.CLEAR)
        return

    def subl(self, *args) -> None:
        """
        opens up a new Sublime Text instance\n
        takes command line arguments
        """
        path = ""
        match platform.system():
            case "Windows":
                if os.path.exists("C:\\Program Files\\Sublime Text"):
                    path = "C:\\Program Files\\Sublime Text\\subl.exe"
                elif os.path.exists("C:\\Program Files (x86)\\Sublime Text"):
                    path = "C:\\Program Files (x86)\\Sublime Text\\subl.exe"
            case "Linux":
                path = "subl"
        try:
            if len(args[0]) == 0:
                subprocess.run([path])
            else:
                subprocess.run([path] + [a for a in args])
        except Exception as e:
            raise e
        return

    def system_process(self, *args) -> None | PathRequiredError:
        """
        for all system processes
        """
        try:
            if len(args[0][1:]) == 0:
                subprocess.run([args[0][0]])
            else:
                subprocess.run([args[0][0]] + [a for a in args[0][1:]])
            return
        except Exception as e:
            raise PathRequiredError

    def system_process_path(self, *args) -> None | Exception:
        """
        for all commands that require a path
        """
        try:
            handled: bool = False
            match args[0][0]:
                case "subl":
                    self.subl(args[0][1:])
                    handled = True
                case "brave":
                    self.browser("brave")
                    handled = True
                case "opera":
                    self.browser("opera")
                    handled = True
            if not handled:
                raise CommandNotFoundError()
            return
        except Exception as e:
            return e

    def handle(self, *args) -> None:
        """
        handles all system process commands like nvim, etc.\n
        if they aren't system processes then it tries to check for a path
        """
        try:
            if args[0][0] in self.prompt.plugins:
                subprocess.run(self.prompt.plugins[args[0][0]])
            else:
                self.system_process(args[0])
            return
        except PathRequiredError:
            self.system_process_path(args[0])
            return

    def checksum(self, *args) -> None:
        """
        checksums a file\n
        currently only supports sha256 and sha512\n\n
        particularly useful for working with .iso files
        """

        def chksum(function: str, filename: str) -> str | ValueError:
            """
            used for when you simply want to see the checksum of a file
            """
            match function:
                case "sha256":
                    with open(filename, "r") as f:
                        return hashlib.sha256(f.read().encode()).hexdigest()
                case "sha512":
                    with open(filename, "r") as f:
                        return hashlib.sha512(f.read().encode()).hexdigest()
            return ValueError("unknown hash function")

        def check(function: str, filename: str, csum: str) -> bool | ValueError:
            """
            used for when you want to check if the checksum of a file matches an existing checksum
            """
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

    def config(self, *args) -> None:
        usrconfig.UsrConfig(self.usr).config()
        self.hot_reload()
        return

    def list_all(self, *args) -> None:
        [print(i) for i in list(self.commands.keys())]
        return

    def command(self, cmd: str) -> None:
        cmd = str(cmd)
        specials = {
            "usr": lambda: self.usr,
            "home": lambda: self.home,
            "cwd": lambda: self.cwd,
            "date": datetime.now,
        }
        if cmd.__contains__("$") and cmd.count("$") % 2 == 0:
            for a, b in cmd.find_all("$"):
                if cmd[a + 1 : b] in specials:
                    cmd = cmd[:a] + str(specials[cmd[a + 1 : b]]()) + cmd[b + 1 :]
        tmp = cmd.split()
        if tmp[0] in self.commands:
            self.commands[tmp[0]](self, cmd[len(tmp[0]) + 1 :]) if tmp[
                0
            ] not in self.browsers else self.commands[tmp[0]](self, tmp[0])
        else:
            try:
                self.handle(tmp)
            except CommandNotFoundError:
                print("\n\tCommand not recognized.\n")
            except Exception as e:
                print(e)
        return


class Prompt:
    """
    Base class for the prompt displayed inside of the nebula cli
    """

    def __init__(self, cli: CLI) -> None:
        self.usr: str = cli.usr
        self.cwd: str = cli.cwd
        self.home: str = cli.home
        self.prompt = lambda: f"({self.usr}) \u0091~ $ "
        self.change: bool = False
        self.plugins: dict[str, str] = {}
        self.cli: CLI = cli

        def read() -> str | None:
            """
            gets the contents of the usr.config file, if it exists\n
            if it doesn't exist creates the folder 'usr config' and creates the new usr.config file
            """
            if os.path.exists(
                (
                    x := os.path.expanduser("~")
                    + "\\NebulaCLI\\usr config\\usr.usrconfig"
                )
            ):
                with open(x, "r") as f:
                    return str(f.read())
            else:
                os.mkdir((x := os.path.expanduser("~") + "\\NebulaCLI\\usr config"))
                with open(x + "\\usr.usrconfig", "w") as f:
                    f.write("")
                with open(x + "\\configed.list", "w") as f:
                    f.write("")
                return

        if isinstance((x := read()), str):
            self.usr_config = x
        else:
            self.usr_config = ""
        self.alias()
        self.config(self.prompt())
        return

    def alias(self) -> None:
        """
        checks if the config file contains a config for the current user\n
        if so updates all the info that Prompt class needs
        """
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
                            self.usr = " ".join(idx[2:])
                        case "prompt":
                            self.prompt = " ".join(idx[2:]) + " "
                            self.change = True
                        case "plugin":
                            for i in range(
                                len([i for i in idx[2:] if idx[2:].index(i) % 2 == 0])
                            ):
                                self.plugins[
                                    (x := idx[2:][i])[x.find("'") + 1 : x.rfind("'")]
                                ] = (x := idx[2:][i + 1])[
                                    x.find("'") + 1 : x.rfind("'")
                                ].replace(
                                    "\\\\", "\\"
                                )
        return

    def config(self, config: str) -> None:
        """
        configures the prompt according to the info read from the config file
        """
        specials = {"usr": self.usr, "cwd": "\u0091"}

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
                        print("shot")
                    case "cwd":
                        string = string[:a] + specials["cwd"] + string[b + 1 :]
                    case "plugin":
                        print("stuff")
            return string

        self.prompt = lambda: check(config)
        return

    def _prompt(self) -> str:
        """
        returns the prompt\n
        if the current wokring directory is the same as the home directory\n
        otherwise it replaces the \\u9001 (unicode private use character) byte with the current wokring directory
        """
        if self.home != os.getcwd() + "\\":
            return self.prompt().replace("\u0091", f"{os.getcwd()} ")
        return self.prompt()


# --- resources ---
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
