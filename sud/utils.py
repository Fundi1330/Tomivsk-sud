from os import path, pardir, getcwd
from json import loads
from functools import wraps
from db import get_user
from typing import Dict, Any

def load_config():
    with open(path.join(getcwd(), 'config.json'), 'r') as config:
        return loads(config.read())
    
def registration_required(f):
    async def wrapper(*args):
        if get_user(args[0].user.id) is None:
            await args[0].response.send_message('Ви не зареєстровані!')
            return
        await f(*args)
    
    return wrapper