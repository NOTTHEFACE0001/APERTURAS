import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import os

# ==========================================
# 🖼️ ENLACES PROPORCIONADOS POR EL USUARIO
# ==========================================
URL_LOGO = "https://cdn.discordapp.com/attachments/1497999534759084032/1498004220131934268/WhatsApp_Image_2026-04-24_at_14.47.16-removebg-preview.png"
IMG_APERTURA  = "https://cdn.discordapp.com/attachments/1497999534759084032/1503081674538221568/Captura_de_pantalla_2026-05-10_125245.jpg"
IMG_CIERRE    = "https://cdn.discordapp.com/attachments/1497999534759084032/1503082415990636727/Captura_de_pantalla_2026-05-10_125631.jpg"
IMG_ENCUESTA  = "https://cdn.discordapp.com/attachments/1497999534759084032/1503084596177277080/Captura_de_pantalla_2026-05-07_211448.jpg"

# ==========================================
# 🌐 FLASK KEEP-ALIVE
# ==========================================
app = Flask('')
@app.route('/')
def home(): return "SISTEMA GCRPCM ONLINE"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# ==========================================
# 🤖 BOT
# ==========================================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'✅ Bot Gran Chile RP Actualizado: {bot.user}')


# ==========================================
# ✅ /abrir_servidor
# ==========================================
@bot.tree.command(name="abrir_servidor", description="Anuncio oficial de apertura del servidor")
@app_commands.describe(
    horario_cierre="¿A qué hora cierra el servidor? (ej: 22:00)",
    modo="Modo de roleplay de la sesión"
)
@app_commands.choices(modo=[
    app_commands.Choice(name="🟢 Modo Normal",     value="🟢 Normal"),
    app_commands.Choice(name="🟡 Modo Evento",     value="🟡 Evento Especial"),
    app_commands.Choice(name="🔴 Modo Emergencia", value="🔴 Emergencia Activa"),
])
async def abrir(interaction: discord.Interaction, horario_cierre: str, modo: str = "🟢 Normal"):
    embed = discord.Embed(
        title="✨ ¡SERVIDOR ABIERTO! ✨",
        description="La sesión de roleplay ha comenzado oficialmente.\n¡Bienvenidos a **Gran Chile RP**! 🇨🇱",
        color=0x2ecc71
    )
    embed.add_field(name="🆔 CÓDIGO",           value="`GCRPCM`",             inline=True)
    embed.add_field(name="🕒 CIERRE ESTIMADO",  value=f"**{horario_cierre}**", inline=True)
    embed.add_field(name="🎮 MODO DE SESIÓN",   value=modo,                   inline=True)
    embed.add_field(name="🎙️ HOST DE SESIÓN",  value=interaction.user.mention, inline=True)
    embed.add_field(name="📅 FECHA",            value=f"<t:{int(__import__('time').time())}:D>", inline=True)
    embed.add_field(name="⏱️ INICIO",           value=f"<t:{int(__import__('time').time())}:t>", inline=True)
    embed.add_field(
        name="📢 RECUERDA",
        value=(
            "▸ Sigue el reglamento en todo momento.\n"
            "▸ Respeta a los demás jugadores.\n"
            "▸ Mantén el rol activo y de calidad."
        ),
        inline=False
    )
    embed.set_image(url=IMG_APERTURA)
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System • Gran Chile RP", icon_url=URL_LOGO)

    view = discord.ui.View()
    view.add_item(discord.ui.Button(
        label="📋 Ver Reglamento",
        style=discord.ButtonStyle.link,
        url="https://discord.com/channels/@me"   # ← Cambia por el link real
    ))

    await interaction.response.send_message(
        content="@everyone <@&1234567890> <@&0987654321>\n> 🇨🇱 **Ciudadano/a** • 👥 **Ciudadano Chileno** — ¡La sesión ha comenzado!",
        # ☝️ Reemplaza los IDs de rol por los reales
        embed=embed,
        view=view
    )


# ==========================================
# ⛔ /cerrar_servidor
# ==========================================
@bot.tree.command(name="cerrar_servidor", description="Anuncio oficial de cierre del servidor")
@app_commands.describe(motivo="Motivo del cierre (opcional)")
async def cerrar(interaction: discord.Interaction, motivo: str = "Fin de sesión normal."):
    import time
    embed = discord.Embed(
        title="⛔ SERVIDOR CERRADO ⛔",
        description="La sesión de roleplay ha finalizado.\n¡Gracias por participar en **Gran Chile RP**! 🇨🇱",
        color=0xe74c3c
    )
    embed.add_field(name="🌐 ESTADO",        value="🔴 OFFLINE",              inline=True)
    embed.add_field(name="⚒️ CERRADO POR",   value=interaction.user.mention,  inline=True)
    embed.add_field(name="⏱️ HORA DE CIERRE",value=f"<t:{int(time.time())}:t>", inline=True)
    embed.add_field(name="📝 MOTIVO",        value=motivo,                    inline=False)
    embed.add_field(
        name="📌 INFO",
        value="▸ Guardamos tu progreso automáticamente.\n▸ ¡Vuelve pronto para la próxima sesión!",
        inline=False
    )
    embed.set_image(url=IMG_CIERRE)
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System • Gran Chile RP", icon_url=URL_LOGO)

    await interaction.response.send_message(content="@everyone", embed=embed)


# ==========================================
# ⏸️ /pausar_servidor
# ==========================================
@bot.tree.command(name="pausar_servidor", description="Pausa temporal la sesión")
@app_commands.describe(
    duracion="¿Cuánto dura la pausa? (ej: 15 minutos)",
    motivo="¿Por qué se pausa?"
)
async def pausar(interaction: discord.Interaction, duracion: str, motivo: str = "Descanso."):
    embed = discord.Embed(
        title="⏸️ SERVIDOR EN PAUSA",
        description="La sesión ha sido pausada temporalmente.\nEsperamos reanudar pronto.",
        color=0xf39c12
    )
    embed.add_field(name="⏱️ DURACIÓN ESTIMADA", value=f"**{duracion}**",        inline=True)
    embed.add_field(name="📝 MOTIVO",             value=motivo,                  inline=True)
    embed.add_field(name="🎙️ PAUSADO POR",        value=interaction.user.mention, inline=True)
    embed.add_field(
        name="💡 MIENTRAS TANTO",
        value="▸ Puedes usar los canales de OOC.\n▸ No abandones el servidor.\n▸ Espera el aviso de reanudación.",
        inline=False
    )
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System • Gran Chile RP", icon_url=URL_LOGO)

    await interaction.response.send_message(content="@everyone", embed=embed)


# ==========================================
# ▶️ /reanudar_servidor
# ==========================================
@bot.tree.command(name="reanudar_servidor", description="Reanuda la sesión tras una pausa")
async def reanudar(interaction: discord.Interaction):
    import time
    embed = discord.Embed(
        title="▶️ ¡SESIÓN REANUDADA!",
        description="La pausa ha terminado.\n¡Volvemos al roleplay en **Gran Chile RP**! 🇨🇱",
        color=0x1abc9c
    )
    embed.add_field(name="🕒 HORA DE REANUDACIÓN", value=f"<t:{int(time.time())}:t>", inline=True)
    embed.add_field(name="🎙️ REANUDADO POR",       value=interaction.user.mention,    inline=True)
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System • Gran Chile RP", icon_url=URL_LOGO)

    await interaction.response.send_message(content="@everyone", embed=embed)


# ==========================================
# 🚨 /emergencia
# ==========================================
@bot.tree.command(name="emergencia", description="Alerta de emergencia o situación crítica en el rol")
@app_commands.describe(
    tipo="Tipo de emergencia",
    descripcion="Descripción breve de la emergencia"
)
@app_commands.choices(tipo=[
    app_commands.Choice(name="🚒 Incendio",             value="🚒 Incendio"),
    app_commands.Choice(name="🚑 Emergencia Médica",    value="🚑 Emergencia Médica"),
    app_commands.Choice(name="🚔 Persecución Policial", value="🚔 Persecución Policial"),
    app_commands.Choice(name="💥 Desastre Natural",     value="💥 Desastre Natural"),
    app_commands.Choice(name="⚠️ Alerta General",       value="⚠️ Alerta General"),
])
async def emergencia(interaction: discord.Interaction, tipo: str, descripcion: str):
    import time
    embed = discord.Embed(
        title=f"🚨 EMERGENCIA ACTIVA — {tipo}",
        description=f"**{descripcion}**",
        color=0xff0000
    )
    embed.add_field(name="⏱️ HORA",          value=f"<t:{int(time.time())}:t>",  inline=True)
    embed.add_field(name="📣 REPORTADO POR", value=interaction.user.mention,     inline=True)
    embed.add_field(
        name="🆘 INSTRUCCIONES",
        value=(
            "▸ Todos los servicios de emergencia al lugar.\n"
            "▸ Ciudadanos: manténganse alejados de la zona.\n"
            "▸ Sigan las instrucciones de los oficiales."
        ),
        inline=False
    )
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System • Gran Chile RP", icon_url=URL_LOGO)

    await interaction.response.send_message(content="@everyone 🚨", embed=embed)


# ==========================================
# 🎉 /evento_especial
# ==========================================
@bot.tree.command(name="evento_especial", description="Anuncia un evento especial en el servidor")
@app_commands.describe(
    nombre="Nombre del evento",
    descripcion="Descripción del evento",
    hora="Hora del evento (ej: 20:00)",
    premio="Premio o recompensa del evento (opcional)"
)
async def evento(
    interaction: discord.Interaction,
    nombre: str,
    descripcion: str,
    hora: str,
    premio: str = "Sin premio definido."
):
    import time
    embed = discord.Embed(
        title=f"🎉 EVENTO ESPECIAL — {nombre}",
        description=descripcion,
        color=0x9b59b6
    )
    embed.add_field(name="🕒 HORA DEL EVENTO",  value=f"**{hora}**",           inline=True)
    embed.add_field(name="📅 FECHA",             value=f"<t:{int(time.time())}:D>", inline=True)
    embed.add_field(name="🎙️ ORGANIZADO POR",   value=interaction.user.mention, inline=True)
    embed.add_field(name="🏆 PREMIO / RECOMPENSA", value=premio,               inline=False)
    embed.add_field(
        name="📌 PARTICIPA",
        value="▸ Preséntate a tiempo.\n▸ Sigue las reglas del evento.\n▸ ¡Diviértete!",
        inline=False
    )
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System • Gran Chile RP", icon_url=URL_LOGO)

    view = discord.ui.View()
    view.add_item(discord.ui.Button(
        label="✅ ¡Me anoto!",
        style=discord.ButtonStyle.success,
        custom_id="evento_anotarse",
        disabled=True   # Decorativo; actívalo con un callback si quieres funcionalidad real
    ))

    await interaction.response.send_message(content="@everyone 🎉", embed=embed, view=view)


# ==========================================
# 🗳️ /votar_apertura
# ==========================================
@bot.tree.command(name="votar_apertura", description="Votación para abrir sesión")
@app_commands.describe(hora_propuesta="Hora propuesta para abrir (ej: 20:00)")
async def votar(interaction: discord.Interaction, hora_propuesta: str = "Por definir"):
    embed = discord.Embed(
        title="📊 ¿ABRIMOS SESIÓN?",
        description=(
            f"**Hora propuesta:** `{hora_propuesta}`\n\n"
            "Vota con las reacciones para que los hosts decidan.\n"
            "✅ Sí, quiero jugar · ❌ No puedo hoy"
        ),
        color=0x3498db
    )
    embed.add_field(name="🎙️ PROPUESTO POR", value=interaction.user.mention, inline=True)
    embed.add_field(name="🌐 SERVIDOR",       value="Gran Chile RP 🇨🇱",      inline=True)
    embed.set_image(url=IMG_ENCUESTA)
    embed.set_thumbnail(url=URL_LOGO)
    embed.set_footer(text="GCRPCM System • Gran Chile RP", icon_url=URL_LOGO)

    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")


# ==========================================
# 🚀 INICIO
# ==========================================
keep_alive()
bot.run(os.getenv('TOKEN_ANUNCIOS'))
