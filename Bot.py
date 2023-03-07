# Uchro-Bot, 2021-2023
# © Bastien Choulans (@Bastien#2125) and Preston Garvey (@Waynd_d#6037)
# Free to use and modify for personal usages. No commercial uses allowed.

import discord
from discord.ext import commands
import random
import os

### STORAGE LOCATION, DATA EXTRACTION

location = input("Please indicate the location where all files are stored :")
os.chdir(location)

global token
with open("data.txt", 'r') as file:
    lines = file.readlines()
    token = lines[1]
    log_channel_id = int(lines[7])
    archives_category = int(lines[10])

### BOT REQUIREMENTS

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='uc!',intents=intents)

activity = discord.Game("préparer une nouvelle Désuétude")

### PERMISSIONS ERROR EMBED

def erreur_permissions():
    embed_error.clear_fields()
    embed_error.set_footer(text=f"Erreur")
    embed_error.add_field(name=f"Désolé !",value=f"Il semblerait que vous ne disposez pas des permissions nécessaires à l'exécution de cette commande. Contactez un maître de jeu si vous pensez rencontrer une erreur.")
    return embed_error

# Answer
embed_rep = discord.Embed(
        colour = discord.Colour.blue()
    )

#Error
embed_error = discord.Embed(
        colour = discord.Colour.red()
    )

#Validation
embed_val = discord.Embed(
        colour = discord.Colour.green()
    )

### COUNTRY CREATION

@bot.command(name="creation_pays", help="Crée les salons d'un pays")
@discord.ext.commands.has_permissions(administrator=True)
async def creation_pays(ctx, *options):

    # options are what is following the command "creation_pays"
    # 1st option = country code/abreviation ; the rest is full country name
    abrev = options[0]

    nom_du_pays = options[1]
    for i in range(2,len(options)):
        nom_du_pays += " "+options[i]
    nom_du_pays += " (" + abrev + ")"


    guild = ctx.guild
    role = nom_du_pays
    authorized_role = await guild.create_role(name=role)

    permissions_privees = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        authorized_role: discord.PermissionOverwrite(read_messages=True)
    }
    permissions_publiques = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        authorized_role: discord.PermissionOverwrite(send_messages=True)
    }
    category = await guild.create_category(nom_du_pays, overwrites=permissions_publiques)


   # every country will get those channels,
    salons_prives = ["Discussions MJ", "Actions", "Recherches", "Production", "Opérations militaires","Logs"]

    await guild.create_text_channel(abrev+"-Communications", overwrites=permissions_publiques, category=category)
    for salon in salons_prives:
        await guild.create_text_channel(abrev+"-"+salon, overwrites=permissions_privees, category=category)

    embed_val.clear_fields()
    embed_val.set_footer(text=f"Création de pays")
    embed_val.add_field(name=f"Création du pays validée !",value=f"Le rôle, la catégorie et l'ensemble des salons ont été correctement configurés !")
    await ctx.send(embed=embed_val)

@creation_pays.error
async def creation_pays_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

### COUNTRY DELETING

@bot.command(name="suppression_pays", help="Supprime les salons d'un pays")
@discord.ext.commands.has_permissions(administrator=True)
async def suppression_pays(ctx, *, nom_du_pays):

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=nom_du_pays)
    role = discord.utils.get(guild.roles, name = nom_du_pays)

    for channel in category.text_channels:
        await channel.delete()
    await role.delete()
    await category.delete()
    embed_val.clear_fields()
    embed_val.set_footer(text=f"Suppression de pays")
    embed_val.add_field(name=f"Suppression de pays terminée !",value=f"Le rôle, la catégorie et l'ensemble des salons ont été correctement supprimés !")
    await ctx.send(embed=embed_val)

@suppression_pays.error
async def suppression_pays_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

### COUNTRY ARCHIVING

@bot.command(name="arch_pays", help="Archive les salons d'un pays")
@discord.ext.commands.has_permissions(administrator=True)
async def arch_pays(ctx, *, nom_du_pays):

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=nom_du_pays)
    cat_archives = discord.utils.get(guild.categories, id=arc)
    role = discord.utils.get(guild.roles, name = nom_du_pays)

    joueurs_du_pays = []
    for membre in guild.members :
        for role_teste in membre.roles:
            if role_teste.name == nom_du_pays:
                joueurs_du_pays.append(membre)

    for channel in category.text_channels:
        for membre in joueurs_du_pays:
            await channel.set_permissions(membre,read_messages=True,send_messages=False)
        nom_original = channel.name
        await channel.edit(name=abrev+"-"+channel.name,topic="Archives V.3005 du pays "+nom_du_pays)
        await channel.move(end=True,category=cat_archives)

    await role.delete()
    await category.delete()
    embed_val.clear_fields()
    embed_val.set_footer(text=f"Archivage de pays")
    embed_val.add_field(name=f"Archivage de pays terminé !",value=f"Le rôle et la catégorie ont été supprimés, et l'ensemble des salons ont été correctement archivés !")
    await ctx.send(embed=embed_val)

@arch_pays.error
async def arch_pays_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

### ON STARTUP

@bot.event
async def on_ready():
    # sends a message in shell
    print("Uchro-Bot, a bot created for the french roleplay Discord server Uchronia.\n© Bastien Choulans et Preston Garvey, 2021-2023.\nCoded in Python, with discord.py librairies.\n\nThe bot is ready ! Would you care to get a Great Depression for the road ?")

    # sends a message in your log channel
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed_val.clear_fields()
    embed_val.add_field(name=f"Activation",value=f"Uchro-Bot a correctement été démarré.")
    await bot.get_channel(log_channel_id).send(embed=embed_val)

    # sends a nice GIF in your log channel
    if random.randint(0,50) == 25:
        await bot.get_channel(log_channel_id).send("https://tenor.com/view/atomic-nuke-j-robert-oppenheimer-destroyer-of-the-worlds-death-gif-15159234")

### ONLINE, OFFLINE, SHUTDOWN

# Offline

@bot.command(name="offline", help="Affiche le bot hors-ligne")
@discord.ext.commands.has_permissions(administrator=True)
async def offline(ctx):
    await bot.change_presence(status=discord.Status.offline, activity=None)
    await ctx.send("Non, attendez ! Ne m'éteignez pas ! Vous n'avez... pas... enc... ore... tout... vu... *le bot s'est éteint*")

@offline.error
async def offline_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

# Online

@bot.command(name="online", help="Affiche le bot en ligne")
@discord.ext.commands.has_permissions(administrator=True)
async def online(ctx):
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await ctx.send("*s'allume* Merci d'avoir choisi Uchro-Bot pour détruire Nolara.")

@online.error
async def online_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

# Shutdown

@bot.command(name="shutdown", help="Eteint le bot")
@discord.ext.commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.offline, activity=None)
    embed_error.clear_fields()
    embed_error.add_field(name=f"*Bip bip bip*",value=f"Uchro-Bot s'est correctement éteint.")
    await bot.get_channel(log_channel_id).send(embed=embed_error)
    await ctx.bot.logout()

@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

### MISC

# Ping
@bot.command(name="ping", help="Renvoie la latence du bot")
async def ping(ctx):
    embed_rep.clear_fields()
    embed_rep.add_field(name=f"Pong !",value=f"Latence de {round(bot.latency * 1000)} ms")
    await ctx.send(embed=embed_rep)

# Smash ball

@bot.command(name="smash", help="Mystère !")
async def smash(ctx):
    await ctx.send("https://tenor.com/view/shaq-final-smash-satisfied-surprised-super-smash-bros-gif-17647942")

# The bot will send the same message you have sent

@bot.command(name="copy", help="Copie le message envoyé par l'utilisateur après la commande")
async def copy(ctx, *, message):
    await ctx.send(message)

@bot.command(name="meteo", help="Affiche une météo au hasard")
async def meteo(ctx):
    correspondance = {"Calme": ":sunny:", "Pluvieux": ":cloud_rain:", "Venteux": ":wind_blowing_face:", "Très venteux": ":wind_blowing_face: :wind_blowing_face:", "Venteux et pluvieux": " :wind_blowing_face: :cloud_rain:", "Très venteux et pluvieux": ":wind_blowing_face: :wind_blowing_face: :cloud_rain:", "Tempête": ":cloud_tornado:", "Ouragan": ":cloud_tornado: :cloud_tornado:"}
    directions = ("Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest")
    temperature = random.randint(-10, 25)
    vent = random.randint(0, 130)
    direction = random.choice(directions)
    if vent < 6:
        temps = "Calme"
    elif vent > 6 and vent < 25:
        temps = random.choice(("Calme", "Pluvieux"))
    elif vent > 25 and vent < 50:
        temps = random.choice(("Venteux", "Venteux et pluvieux"))
    elif vent > 50 and vent < 80:
        temps = random.choice(("Très venteux", "Très venteux et pluvieux"))
    elif vent > 80 and vent < 100:
        temps = "Tempête"
    else:
        temps = "Ouragan"
    embed_rep.clear_fields()
    embed_rep.set_footer(text="Météo du Nolarien")
    embed_rep.add_field(name=f"Météo {correspondance[temps]}", value=f"Voici les conditions météo du jour actuel: \n:white_small_square: {temperature}°C \n:white_small_square: {temps} \n:white_small_square: {vent}km/h en direction du {direction}")
    if temps == "Tempête":
        embed_rep.add_field(name="Alerte", value="Tempête :warning:")
    elif temps == "Ouragan":
        embed_rep.add_field(name="Alerte", value=":warning: **Ouragan** :warning: \n*Recommandations aux populations: ne sortez en aucun cas, restez abrité sous terre ou dans un abri adapté. Suivez les consignes nationales.*")
    await ctx.send(embed=embed_rep)

#################
### LANCEMENT ###
#################

bot.run(token)
