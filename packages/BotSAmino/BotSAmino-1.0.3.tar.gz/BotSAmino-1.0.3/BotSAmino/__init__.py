from .client import BotAminew
from .local import Local
from .socket import *
from .acm import Acm
from .lib import *
from requests import get
version = '1.0.3'

try:
    newest = get("https://pypi.python.org/pypi/BotAminew/json").json()["info"]["version"]
    if version != newest: print(f"\033[1;33mBotAminew New Version!: {newest} (Your Using {version})\033[1;0m")
except: pass

__version__ = version
