import json
import requests
import websocket
from threading import Thread

from .lib import CheckExceptions

try: from bot import Commands
except ImportError: from .bot import Commands


# By SirLez
# Solved By SirLez
# and Sloved By Bovonos ،_،
# and Reworked By SirLez ._.
# Note: socket2 is a socket to send & recv data ! ( Do Not load the data with json )
# upgraded by Phoenix :D

class Socket(Commands):
    def __init__(self):
        self.socket_url = "wss://ws1.narvii.com"
        websocket.enableTrace(False)
        Commands.__init__(self)

    def handle_message(self, data):
        try: data = json.loads(data)
        except Exception: data = data

        self.on_receive(data)
        # return self.methods.get(typ, self.classic)(data)

    def on_error(self, error): print(error)
    def on_close(self): print("__CLOSED__")
    def send(self, data): self.socket2.send(json.dumps(data))
    def recv(self): return json.loads(self.socket2.recv())

    def web_socket_url(self):
        req = requests.get("https://aminoapps.com/api/chat/web-socket-url", headers={'cookie': self.sid})
        if req.status_code != 200: return CheckExceptions(req.json())
        else:
            self.socket_url = req.json()["result"]["url"]
            return self.socket_url

    def launch(self, socket2: bool = False):
        self.headers = {'cookie': self.sid}

        if socket2:
            self.socket2 = websocket.WebSocket()
            self.socket2.connect(self.web_socket_url(), header=self.headers)

        self.socket = websocket.WebSocketApp(
            self.web_socket_url(),
            on_message=self.handle_message,
            on_error=self.on_error,
            on_close=self.on_close,
            header=self.headers
        )
        Thread(target=self.socket.run_forever, kwargs={"ping_interval": 60}).start()
