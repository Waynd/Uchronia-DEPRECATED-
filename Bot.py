import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='uc!')
activite = discord.Game("vérifier que tout marche. Ce n'est pas le cas.")
global token
with open("token.txt", 'r') as fichier:
    lignes = fichier.readlines()
    token = lignes[0]

def erreur_permissions():
    embed_error.clear_fields()
    embed_error.set_footer(text=f"Erreur")
    embed_error.add_field(name=f"Désolé !",value=f"Il semblerait que vous ne disposez pas des permissions nécessaires à l'exécution de cette commande. Contactez un maître de jeu si vous pensez rencontrer une erreur.")
    return embed_error

#######################
### COMMANDES ADMIN ###
#######################

@bot.event
async def on_ready():
    print("Uchro-Bot, robot créé pour le serveur Uchronia.\n© Bastien Choulans et Preston Garvey, 2021.\nProgrammé en Python, utilise les librairies discord.py.\n\nLe bot est enfin prêt ! Allez, une petite Désuétude pour la route.")

    await bot.change_presence(status=discord.Status.online, activity=activite)
    embed_val.clear_fields()
    embed_val.add_field(name=f"Activation",value=f"Uchro-Bot a correctement été démarré.")
    await bot.get_channel(959516597867929721).send(embed=embed_val)
    if random.randint(0,50) == 25:
        await bot.get_channel(959516597867929721).send("https://tenor.com/view/atomic-nuke-j-robert-oppenheimer-destroyer-of-the-worlds-death-gif-15159234")

@bot.command(name="offline", help="Affiche le bot hors-ligne")
async def offline(ctx):
    await bot.change_presence(status=discord.Status.offline, activity=None)
    await ctx.send("Non, attendez ! Ne m'éteignez pas ! Vous n'avez... pas... enc... ore... tout... vu... *le bot s'est éteint*")

@bot.command(name="online", help="Affiche le bot en ligne")
async def online(ctx):
    await bot.change_presence(status=discord.Status.online, activity=activite)
    await ctx.send("*s'allume* Merci d'avoir choisi Uchro-Bot pour détruire Nolara.")

##########################
### COMMANDES LUDIQUES ###
##########################

@bot.command(name="ping", help="Renvoie la latence du bot")
async def ping(ctx):
    embed_rep.clear_fields()
    embed_rep.add_field(name=f"Pong !",value=f"Latence de {round(bot.latency * 1000)} ms")
    await ctx.send(embed=embed_rep)

@bot.command(name="smash", help="Mystère !")
async def smash(ctx):
    await ctx.send("https://tenor.com/view/shaq-final-smash-satisfied-surprised-super-smash-bros-gif-17647942")

@bot.command(name="copy", help="Copie le message envoyé par l'utilisateur après la commande")
async def copy(ctx, *, message):
    await ctx.send(message)

#######################
### GESTION DE PAYS ###
#######################

#Réponse
embed_rep = discord.Embed(
        colour = discord.Colour.blue()
    )

#Erreur
embed_error = discord.Embed(
        colour = discord.Colour.red()
    )

#Validation
embed_val = discord.Embed(
        colour = discord.Colour.green()
    )


@bot.command(name="creation_pays", help="Crée les salons d'un pays")
@discord.ext.commands.has_permissions(administrator=True)
async def creation_pays(ctx, *, nom_du_pays):
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
    category = await guild.create_category(nom_du_pays, overwrites=None)
    await guild.create_text_channel("Informations publiques", overwrites=permissions_publiques, category=category)
    await guild.create_text_channel("Annonces extérieures", overwrites=permissions_publiques, category=category)
    salons_prives = ["Discussions MJ", "Actions économiques", "Autres actions", "Constructions", "Recherches", "Opérations militaires"]
    for salon in salons_prives:
        await guild.create_text_channel(salon, overwrites=permissions_privees, category=category)
    embed_val.clear_fields()
    embed_val.set_footer(text=f"Création de pays")
    embed_val.add_field(name=f"Création du pays validée !",value=f"Le rôle, la catégorie et l'ensemble des salons ont été correctement configurés !")
    await ctx.send(embed=embed_val)

@creation_pays.error
async def creation_pays_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

########################
### AUTRES COMMANDES ###
########################

@bot.command(name="shutdown", help="Eteint le bot")
@discord.ext.commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.offline, activity=None)
    embed_error.clear_fields()
    embed_error.add_field(name=f"*Bip bip bip*",value=f"Uchro-Bot s'est correctement éteint.")
    await bot.get_channel(959516597867929721).send(embed=embed_error)
    await ctx.bot.logout()
    
@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

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
