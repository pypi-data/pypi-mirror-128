from inspect import getfullargspec
from sys import _getframe as getframe
from .lib.objects import Event, CommandMessage
from contextlib import suppress
# from ast import literal_eval
from .local import Local
from .acm import Acm


class SubClients:
    def __init__(self):
        self.comIds = []
        self.subclients = {}

    def add_subclient(self, comId):
        if comId in self.comIds: return
        self.comIds.append(comId)
        self.subclients[comId] = SubClient(comId)

    def get_subclient(self, comId):
        return self.subclients.get(comId, None)


class SubClient(Acm, Local):
    def __init__(self, comId):
        self.comId = comId
        Acm.__init__(self, comId)
        Local.__init__(self, comId)

    def accept_role(self, rid: str = None):
        with suppress(Exception):
            self.accept_organizer(rid)
            return True
        with suppress(Exception):
            self.promotion(noticeId=rid)
            return True

        return False

    def get_chat_id(self, chat: str = None):
        chats = self.get_public_chats()
        name = []
        for title, chat_id in zip(chats.title, chats.chatId):
            if chat.lower() in title.lower() or chat == chat_id: name = (title, chat_id)

            if chat == title: return chat_id

        if name: return name[1]

    def join_chatroom(self, chat: str = None, chatId: str = None):
        chats = self.get_public_chats()
        name = []
        for title, chat_id in zip(chats.title, chats.chatId):
            if chat.lower() in title.lower() or chat == chat_id: name = (title, chat_id)

            if chat == title:
                self.join_chat(chat_id)
                return title

        if name:
            self.join_chat(name[1])
            return name[0]

        return False


class Recall:
    def __init__(self):
        self.handlers = {}
        self.chat_methods = {
            "0:0": self.on_message,
            "3:113": self.on_sticker,
            "101:0": self.on_member_join,
            "102:0": self.on_member_left,
            "103:0": self.on_start_chat,
            "105:0": self.on_title_changed,
            "113:0": self.on_content_changed,
            "114:0": self.on_live_mode_started,
            "115:0": self.on_live_mode_ended,
            "116:0": self.on_host_changed,
            "118:0": self.on_left_chat,
            "120:0": self.on_chat_donate,
            "125:0": self.on_view_mode_enabled,
            "126:0": self.on_view_mode_disabled
        }
        self.notif_methods = {
            "53": self.on_set_you_host,
            "67": self.on_set_you_cohost,
            "68": self.on_remove_you_cohost
        }
        self.methods = {
            1000: self.chat_messages,
            10: self.payload,
        }

    def payload(self, data):
        value = f"{data['o']['payload']['notifType']}"
        return self.notif_methods.get(value, self.classic)(data)

    def chat_messages(self, data):
        value = f"{data['o']['chatMessage']['type']}:{data['o']['chatMessage'].get('mediaType', 0)}"
        return self.chat_methods.get(value, self.classic)(data)

    def roll(self, func, data):
        if func in self.handlers:
            for handler in self.handlers[func]: handler(data)

    def event(self, func):
        def regHandler(handler):
            if func in self.handlers: self.handlers[func].append(handler)
            else: self.handlers[func] = [handler]
            return handler
        return regHandler

    def on_content_changed(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_view_mode_disabled(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_view_mode_enabled(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_live_mode_ended(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_live_mode_started(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_sticker(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_set_you_host(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_remove_you_cohost(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_host_changed(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_set_you_cohost(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_title_changed(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_left_chat(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_start_chat(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_chat_donate(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_member_join(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_member_left(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def on_message(self, data): self.roll(getframe(0).f_code.co_name, Event(data["o"]))
    def classic(self, data): self.roll(getframe(0).f_code.co_name, data)


class Decorator(Recall):
    def __init__(self):
        self.commands = {}
        self.callbacks = {}
        Recall.__init__(self)

    def command_exist(self, name: str):
        return name in self.commands.keys()

    def get_commands(self):
        return self.commands.keys()

    def command(self, condition=None, aliases=None):
        if isinstance(aliases, str):
            aliases = [aliases]
        elif not aliases:
            aliases = []

        if not callable(condition):
            condition = None

        def add_command(command_funct):
            aliases.append(command_funct.__name__)
            for command in aliases:
                self.commands[command.lower()] = {"command": command_funct, "condition": condition}
            return command_funct

        return add_command


class Commands(Decorator, SubClients):
    def __init__(self, prefix: str = "!"):
        Decorator.__init__(self)
        self.prefix = prefix
        SubClients.__init__(self)

    def execute(self, command: str, type: str, data: CommandMessage):
        dico = {}

        if type == "command":
            dico = self.commands
        elif type == "callback":
            dico = self.callbacks

        com = dico[command]["command"]
        con = dico[command]["condition"]
        arg = getfullargspec(com).args
        arg.pop(0)
        s = len(arg)

        if not data._parameter and s: data._parameter = [value for value in data.message.split()[:s]]
        if data._parameter and not s: data._parameter = []
        if len(data._parameter) > s: data._parameter = data._parameter[:s]
        if (con and con(data)) or not con: com(data, *data._parameter)

    def on_receive(self, data):
        typ = data["t"]
        self.methods.get(typ, self.classic)(data)

        value = f"{data['o']['chatMessage']['type']}:{data['o']['chatMessage'].get('mediaType', 0)}"

        if value != "0:0":
            return

        self.add_subclient(data["o"]["ndcId"])
        args = CommandMessage(data["o"])
        args.subClient = self.get_subclient(args.comId)

        if isinstance(self.prefix, str): check = str(args.message).startswith(self.prefix)
        elif isinstance(self.prefix, list): check = [True for pre in self.prefix if str(args.message).startswith(pre)]

        if check and self.prefix:
            args.command = args.message.lower().split()[0][1:]
            args.message = ' '.join(args.message.split()[1:])

        elif check:
            args.command = args.content.lower().split()[0]
            args.message = ' '.join(args.content.split()[1:])

        if self.command_exist(args.command): self.execute(args.command, "command", args)
