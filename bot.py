import discord
from discord.ext import commands
from discord.ui import Button, View
from flask import Flask
from threading import Thread
import os

# ------------------ WEB SERVER PARA UPTIME ROBOT ------------------
app = Flask("")

@app.route("/")
def home():
    return "Bot activo"

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()
# -------------------------------------------------------------------

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------ CONFIG ------------------
ROLES_CHANNEL_ID = 123456789012345678    # Canal de roles

# Roles de ping
PING_ROLES = {
    "live ping": 1460125747489538089,
    "lol ping": 1460126037693431809,
    "valorant ping": 1460126178303152292,
    "esports ping": 1460126245152096418
}

# Roles cosméticos
GAME_ROLES = {
    "league of legends": 1460290957663535320,
    "valorant": 1460291045832003829,
    "2xko": 1460291230108880976
}

# Archivo para guardar ID del mensaje de roles
MESSAGE_ID_FILE = "roles_msg_id.txt"

# ------------------ FUNCIONES ------------------

async def send_roles_embed():
    channel = bot.get_channel(ROLES_CHANNEL_ID)
    if channel is None:
        return

    # Revisar si ya existe el mensaje
    message_id = None
    if os.path.exists(MESSAGE_ID_FILE):
        with open(MESSAGE_ID_FILE, "r") as f:
            message_id = f.read().strip()

    if message_id:
        try:
            msg = await channel.fetch_message(int(message_id))
            return  # Ya existe, no enviar
        except:
            pass  # Se borró, enviar de nuevo

    # Crear embed
    embed = discord.Embed(
        title="Roles de Ping y Juegos",
        description="Reacciona con los botones para asignarte roles 💜",
        color=0x6A0DAD
    )

    # Crear botones
    view = View(timeout=None)  # timeout=None hace que el view sea persistente
    for role_name in list(PING_ROLES.keys()) + list(GAME_ROLES.keys()):
        button = Button(label=role_name, style=discord.ButtonStyle.primary, custom_id=role_name)
        async def button_callback(interaction, role_name=role_name):
            role_id = PING_ROLES.get(role_name) or GAME_ROLES.get(role_name)
            role = interaction.guild.get_role(role_id)
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f"Se te quitó el rol {role_name}", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"Se te asignó el rol {role_name}", ephemeral=True)
        button.callback = button_callback
        view.add_item(button)

    msg = await channel.send(embed=embed, view=view)

    # Guardar ID para no duplicar
    with open(MESSAGE_ID_FILE, "w") as f:
        f.write(str(msg.id))

# ------------------ EVENTOS ------------------

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    await send_roles_embed()

# ------------------ TOKEN ------------------
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
