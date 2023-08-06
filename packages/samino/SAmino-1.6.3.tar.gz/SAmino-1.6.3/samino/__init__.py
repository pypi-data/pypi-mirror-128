from .client import Client
from .local import Local
from .socket import *
from .acm import Acm
from .lib import *
from requests import get

# By SirLez
try:
    version = '1.6.3'
    newest = get("https://pypi.python.org/pypi/SAmino/json").json()["info"]["version"]
    if version != newest: print(f"\033[1;33mSAmino New Version!: {newest} (Your Using {version})\033[1;0m")
except: pass
