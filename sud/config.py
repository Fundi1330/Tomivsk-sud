import discord
from bot import MyClient
from os import environ
from dotenv import load_dotenv, find_dotenv
from db import init_db, get_user, add_user, get_zayavas_by_user, get_object_by_val, create_object
from utils import registration_required

intents = discord.Intents.default()
intents.message_content = True

load_dotenv(find_dotenv())

guild = discord.Object(id=1173668238635307018)

client = MyClient(intents=intents)
tree = client.tree

@client.event
async def on_ready():
    # tree.clear_commands(guild=guild)
    await tree.sync(guild=guild)
    print('Logged on!')

init_db()

@tree.command(name='register', description='Зареєструватися у системі судочинства. ОБОВ\'ЯЗКОВО перед використанням інших команд', guild=guild)
async def register_command(int):
    if get_user(int.user.id) is not None:
        await int.response.send_message('Ви вже зареєстровані!')
        return
    add_user(int.user.id)
    await int.response.send_message('Ви успішно зареєструвалися!')

@tree.command(name='get_pozivs', description='Отримати всі ваші заяви до суду', guild=guild)
@registration_required
async def get_zayavas_command(int):
    message = 'Ваші позови до суду:\n'
    for i in get_zayavas_by_user(int.user.id):
        message += f'Справа {i[1]} #{i[0]}\n'
    await int.response.send_message(message)

@tree.command(name='get_poziv', description='Отримати інформацію про певну заяву за її айді', guild=guild)
@registration_required
async def get_zayava_command(int, id: int):
    zayava = get_object_by_val('id', id, 'zayava')
    message = f'Інформація про справу #{zayava[0]}:\nСтатус: {"Активна" if zayava[3] else "Не активна"}\nДетальніше про справу: {zayava[1]}\nНазва справи: {zayava[1]}'
    await int.response.send_message(message)

@tree.command(name='post_poziv', description='Подати заяву до суду', guild=guild)
@registration_required
async def post_zayava_command(int, name: str, description: str):
    if not get_object_by_val('title', name, 'zayava'):
        create_object(('title', 'description', 'active', 'user_id'), (name, description, 1, get_user(int.user.id)[0]), 'zayava')
        await int.response.send_message('Заяву успішно створено')
    await int.response.send_message('Заява із такою назвою вже існує!')

client.run(environ.get('token'))
