from typing import Any
import discord
from discord.flags import Intents
from utils import load_config

class MyClient(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.tree = discord.app_commands.CommandTree(client=self)

config = load_config()






