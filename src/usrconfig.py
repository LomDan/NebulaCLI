import os


class UsrConfig:
    def __init__(self, usr: str) -> None:
        self.usr: str = usr
        self.changes = {}
        self.usr_commands = {
            "alias": UsrConfig.alias,
            "prompt": UsrConfig.prompt,
            "plugin": UsrConfig.plugin,
            "--list": UsrConfig.list_all,
        }

    def config(self) -> None:
        """
        allows the user to edit specifc variables within Nebula's configuration
        """
        print("User configuration: (type --list to list all commands)")
        while True:
            try:
                cmd = input(">>> ")
                if cmd != "":
                    tmp = cmd.split()
                    if tmp[0] in self.usr_commands:
                        self.usr_commands[tmp[0]](self, cmd[len(tmp[0]) + 1 :])
            except KeyboardInterrupt:
                print("\n")
                self.write()
                break
            except EOFError:
                print("\n")
                self.write()
                break

    def alias(self, *args) -> None:
        """
        allows the user to change the display name in the prompt
        """
        self.changes["alias"] = input(f"Enter alias for user {self.usr}:\t")
        return

    def prompt(self, *args) -> None:
        """
        allows the user to configure the prompt
        """
        self.changes["prompt"] = input(f"Enter prompt:\t")
        return

    def plugin(self, *args) -> None:
        """
        allows the user to add plugins to Nebula or run custom scripts through commands in Nebula
        """
        self.changes["plugin"] = {}
        self.changes["plugin"][input("Enter plugin name:\t")] = input(
            "Enter path to source file:\t"
        )
        return

    def list_all(self, *args) -> None:
        """
        lists all the available commands within the config console
        """
        for i in list(self.usr_commands.keys()):
            print(i)
        return

    def write(self) -> None:
        """
        writes the changes the user made to the .usrconfig file in the usr config folder
        """
        configed: bool = False
        with open(
            os.path.expanduser("~") + "\\NebulaCLI\\usr config\\configed.list", "r"
        ) as f:
            if self.usr in f.read().splitlines():
                configed = True
        if not configed:
            with open(
                os.path.expanduser("~") + "\\NebulaCLI\\usr config\\configed.list", "a"
            ) as f:
                f.write(f"{self.usr}\n")
            with open(
                os.path.expanduser("~") + "\\NebulaCLI\\usr config\\usr.usrconfig", "a"
            ) as f:
                header = f"usr@{self.usr}"
                info = ""
                for i in self.changes:
                    info += f"\t{i} = {self.changes[i]}\n"
                f.write(header + " (\n" + f"{info}" + ")")
        else:
            config = ""
            with open(
                os.path.expanduser("~") + "\\NebulaCLI\\usr config\\usr.usrconfig", "r"
            ) as f:
                info = f.read().splitlines()
                start, end = 0, 0
                for i in info:
                    if i == "usr@" + os.getlogin() + " (":
                        start = info.index(i)
                        break
                for i in info[start + 1 :]:
                    if i == ")":
                        end = info.index(i)
                        break

                header = f"usr@{self.usr}"
                _info = ""
                for i in self.changes:
                    _info += f"\t{i} = {self.changes[i]}\n"
                config = (
                    "".join(info[:start])
                    + header
                    + " (\n"
                    + f"{_info}"
                    + ")"
                    + "".join(info[end + 1 :])
                )
            with open(
                os.path.expanduser("~") + "\\NebulaCLI\\usr config\\usr.usrconfig", "w"
            ) as f:
                f.write(config)
        return
