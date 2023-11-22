class UsrConfig:
    def __init__(self, usr: str) -> None:
        self.usr: str = usr
        self.changes = {}

    def config(self) -> None:
        print("User configuration: (type --list to list all commands)")
        while True:
            try:
                cmd = input(">>> ")
                if cmd != "":
                    tmp = cmd.split()
                    if tmp[0] in usr_commands:
                        usr_commands[tmp[0]](self, cmd[len(tmp[0]) + 1 :])
            except KeyboardInterrupt:
                print("\n")
                self.write()
                break
            except EOFError:
                print("\n")
                self.write()
                break

    def alias(self, *args) -> None:
        self.changes["alias"] = input(f"Enter alias for user {self.usr}: ")
        return

    def prompt(self, *args) -> None:
        self.changes["prompt"] = input(f"Enter prompt: ")
        return

    def list_all(self, *args) -> None:
        for i in list(usr_commands.keys()):
            print(i)
        return

    def write(self) -> None:
        configed: bool = False
        with open(
            "C:\\Software development\\Game\\usr config\\configed.list", "r"
        ) as f:
            if self.usr in f.read().splitlines():
                configed = True
        if not configed:
            with open(
                "C:\\Software development\\Game\\usr config\\configed.list", "a"
            ) as f:
                f.write(f"{self.usr}\n")
            with open(
                "C:\\Software development\\Game\\usr config\\usr.config", "a"
            ) as f:
                header = f"usr@{self.usr}"
                info = ""
                for i in self.changes:
                    info += f"\t{i} = {self.changes[i]}\n"
                f.write(header + " {\n" + f"{info}" + "}")
        else:
            pass
        return


usr_commands = {
    "alias": UsrConfig.alias,
    "prompt": UsrConfig.prompt,
    "--list": UsrConfig.list_all,
}
