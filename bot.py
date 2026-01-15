# -*- coding: utf-8 -*-
import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

GUILD_ID = 1460123308673601793
CHANNEL_ID = 1460129647022051379

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

PING_ROLES = {
    "live ping": "live ping",
    "lol ping": "lol ping",
    "valorant ping": "valorant ping",
    "esports ping": "esports ping"
}

class PingRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="live ping", style=discord.ButtonStyle.primary, custom_id="ping_live")
    async def live(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "live ping")

    @discord.ui.button(label="lol ping", style=discord.ButtonStyle.secondary, custom_id="ping_lol")
    async def lol(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "lol ping")

    @discord.ui.button(label="valorant ping", style=discord.ButtonStyle.secondary, custom_id="ping_valorant")
    async def valorant(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "valorant ping")

    @discord.ui.button(label="esports ping", style=discord.ButtonStyle.secondary, custom_id="ping_esports")
    async def esports(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "esports ping")

    async def toggle_role(self, interaction, role_name):
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role:
            await interaction.response.send_message("El rol no existe.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Rol **{role_name}** removido.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Rol **{role_name}** agregado.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    bot.add_view(PingRoles())

    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    await channel.send(
        "**Roles de notificaciones**\n"
        "Usa los botones para activar o quitar los pings que quieras.\n"
        "Puedes tener varios o ninguno, tú decides",
        view=PingRoles()
    )

bot.run(TOKEN)
