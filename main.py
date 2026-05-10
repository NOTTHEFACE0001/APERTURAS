import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import os

# ==========================================
# 🖼️ VARIABLES DE IMÁGENES (TOTALMENTE FIJAS)
# ==========================================
URL_LOGO = "https://cdn.discordapp.com/attachments/1497999534759084032/1498004220131934268/WhatsApp_Image_2026-04-24_at_14.47.16-removebg-preview.png"
IMG_CARABINEROS = "https://cdn.discordapp.com/attachments/1497999534759084032/1503084596177277080/Captura_de_pantalla_2026-05-07_211448.jpg"
IMG_BOMBEROS = "https://cdn.discordapp.com/attachments/1497999534759084032/1503081674538221568/Captura_de_pantalla_2026-05-10_125245.jpg"
IMG_PDI = "https://cdn.discordapp.com/attachments/1497999534759084032/1503082415990636727/Captura_de_pantalla_2026-05-10_125631.jpg"

app = Flask('')
@app.route('/')
def home(): return "SISTEMA GRAN CHILE RP ONLINE"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'✅ Bot Gran Chile RP Activado: {bot.user}')

# --- 🟢 COMANDO: ABRIR SERVIDOR ---
@bot.tree.command(name="abrir_servidor", description="Anuncio oficial con foto de Carabineros")
async def abrir(interaction: discord.Interaction, horario_cierre: str):
    embed = discord.Embed(title="✨ ¡SERVIDOR ABIERTO! ✨", color=0x2ecc71)
    embed.add_field(name="🆔 CÓDIGO", value="`GCRPCM` Concordancia", inline=False)
    embed.add_field(name="🕒 CIERRE ESTIMADO", value=f"**{horario_cierre}**", inline=True)
    embed.add_field(name="🎙️ HOST", value=interaction.user.mention, inline=True)
    embed.set_image(url=IMG_CARABINEROS) # Foto de Carabineros
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System", icon_url=URL_LOGO)
    await interaction.response.send_message("@everyone", embed=embed)

# --- ❌ COMANDO: CERRAR SERVIDOR ---
@bot.tree.command(name="cerrar_servidor", description="Anuncio de cierre con foto de la PDI")
async def cerrar(interaction: discord.Interaction):
    embed = discord.Embed(title="⛔ ¡SERVIDOR CERRADO! ⛔", color=0xe74c3c)
    embed.add_field(name="🌐 ESTADO", value="OFFLINE", inline=True)
    embed.add_field(name="⚒️ FINALIZADO POR", value=interaction.user.mention, inline=True)
    embed.set_image(url=IMG_PDI) # Foto de la PDI
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System", icon_url=URL_LOGO)
    await interaction.response.send_message("@everyone", embed=embed)

# --- 🗳️ COMANDO: VOTACIÓN ---
@bot.tree.command(name="votar_apertura", description="Votación con foto de Bomberos")
async def votar(interaction: discord.Interaction):
    embed = discord.Embed(title="📊 ¿ABRIMOS SESIÓN?", color=0x3498db)
    embed.description = "Vota con las reacciones si quieres abrir el servidor."
    embed.set_image(url=IMG_BOMBEROS) # Foto de Bomberos
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

keep_alive()
bot.run(os.getenv('TOKEN_ANUNCIOS'))
