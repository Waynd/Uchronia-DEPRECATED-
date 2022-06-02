import discord
from discord.ext import commands
from fonctions import *
from random import randint

bot = commands.Bot(command_prefix='uc!')
activite = discord.Game("vérifier que tout marche. Ce n'est pas le cas.")                           # Trouver une meilleure solution pour ça (BC)
token = 'ODk2NTA2MTQ3NDQyNDAxMzIw.YWIGaQ.oQ86vRjIylbqyfbQlTImEs3oPfc'

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
    if randint(0,50) == 25:
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
    autorized_role = await guild.create_role(name=role)
    permissions_privees = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        autorized_role: discord.PermissionOverwrite(read_messages=True)
    }
    permissions_publiques = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        autorized_role: discord.PermissionOverwrite(send_messages=True)
    }
    category = await guild.create_category(nom_du_pays, overwrites=None)
    await guild.create_text_channel("Informations publiques", overwrites=permissions_publiques, category=category)
    await guild.create_text_channel("Annonces extérieures", overwrites=permissions_publiques, category=category)
    await guild.create_text_channel("Discussions MJ", overwrites=permissions_privees, category=category)
    await guild.create_text_channel("Actions économiques", overwrites=permissions_privees, category=category)
    await guild.create_text_channel("Autres actions", overwrites=permissions_privees, category=category)
    await guild.create_text_channel("Constructions", overwrites=permissions_privees, category=category)
    await guild.create_text_channel("Recherches", overwrites=permissions_privees, category=category)
    await guild.create_text_channel("Opérations militaires", overwrites=permissions_privees, category=category)
    embed_val.clear_fields()
    embed_val.set_footer(text=f"Création de pays")
    embed_val.add_field(name=f"Création du pays validée !",value=f"Le rôle, la catégorie et l'ensemble des salons ont été correctement configurés !")
    await ctx.send(embed=embed_val)

@creation_pays.error
async def creation_pays_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        embed_error.clear_fields()
        embed_error.set_footer(text=f"Erreur")
        embed_error.add_field(name=f"Désolé !",value=f"Il semblerait que vous ne disposez pas des permissions nécessaires à l'exécution de cette commande. Contactez un maître de jeu si vous pensez rencontrer une erreur.")
        await ctx.send(embed=embed_error)

########################
### AUTRES COMMANDES ###
########################

@bot.command(name="shutdown", help="Eteint le bot")
@discord.ext.commands.has_permissions(administrator=True)
async def shutdown(ctx):
    embed_error.clear_fields()
    embed_error.add_field(name=f"*Bip bip bip*",value=f"Uchro-Bot s'est correctement éteint.")
    await bot.get_channel(959516597867929721).send(embed=embed_error)
    await ctx.bot.logout()
    
@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        embed_error.clear_fields()
        embed_error.set_footer(text=f"Erreur")
        embed_error.add_field(name=f"Désolé !",value=f"Il semblerait que vous ne disposez pas des permissions nécessaires à l'exécution de cette commande. Contactez un maître de jeu si vous pensez rencontrer une erreur.")
        await ctx.send(embed=embed_error)

    
################
### OBSOLETE ###
################

"""@bot.command()
async def creation_pays(ctx):
    nom = await bot.wait_for("message")
    nom1 = nom.content
    membre = nom.author
    await discord.Guild.create_role(name=nom1,reason="Création de pays")
    await discord.membre.add_roles(nom1)"""

"""@bot.group()
async def pays(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"La commande *pays* contient quatre sous-commandes :\n- creation\n- suppression\n- info\n- edition")

@pays.command()
async def creation(ctx):
    etape = 0   # Initialisation
    embed_cpq = discord.Embed(
        title = "Création de pays",
        colour = discord.Colour.blue()
    )
    embed_cpa = discord.Embed(
        title = "Création de pays",
        colour = discord.Colour.green()
    )

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Lancement de la phase de création de pays",value=f"Bonjour à vous, {ctx.author} ! Nous allons suivre pas à pas, avec vous, la création de votre pays. Rassurez-vous, tout est clairement indiqué ! ") ## Ajouter explications réactions.

    await ctx.send(embed=embed_cpa)
    print(f"\nPhase de création de pays exécutée par {ctx.author}.")

    ### Insérer une fonction qui retient le nom du joueur ayant exécuté la commande (éviter de se faire marcher dessus mais normalement un ticket sera ouvert)
    ### Insérer trois réactions (revenir en arrière, sauter une étape, annuler la commande de création)
    ### Revoir le stockage pour éviter les variables de merde + créer un token pour chaque pays dans phase initialisation

    etape = 1   # Nom du pays + drapeau
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Nom de pays et drapeau",value=f"Donnez-nous un nom à ce nouveau pays. Ensuite, dans un nouveau message, joignez-en pièce jointe ou en lien votre drapeau.")
    await ctx.send(embed=embed_cpq)

    nom_pays = await bot.wait_for("message")
    nom_pays = nom_pays.content
    drapeau = await bot.wait_for("message")
    drapeau = drapeau.content

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"Votre pays s'appelle désormais **{nom_pays}**.")
    embed_cpa.set_thumbnail(url=drapeau)
    await ctx.send(embed=embed_cpa)
    print(f"Le pays créé par {ctx.author} s'appelle {nom_pays}.")

    etape = 2   # Nom du dirigeant initial
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.set_thumbnail(url=drapeau)
    embed_cpq.add_field(name=f"Dirigeant de {nom_pays}",value=f"Passons à la personne que vous incarnerez : le dirigeant. Indiquez-nous dans deux messages successifs :\n:small_blue_diamond: le titre de sa fonction,\n:small_blue_diamond: son nom personnel.")
    await ctx.send(embed=embed_cpq)

    fonction_dirigeant = await bot.wait_for("message")
    fonction_dirigeant = fonction_dirigeant.content
    nom_dirigeant = await bot.wait_for("message")
    nom_dirigeant = nom_dirigeant.content

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"**{nom_dirigeant}** sera donc {fonction_dirigeant} de {nom_pays}.")
    await ctx.send(embed=embed_cpa)

    etape = 3   # Forme politique
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Structure de {nom_pays}",value=f"Question plus précise : quel régime politique sera adopté par votre pays ?\n\n*Fédération, république, monarchie, démocratie, aristocratie... Soyez le plus précis possible !*\n**/!\ L'idéologie adoptée par votre gouvernement se précisera dans deux étapes !**")
    await ctx.send(embed=embed_cpq)

    regime_politique = await bot.wait_for("message")
    regime_politique = regime_politique.content

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"On sait désormais que {nom_pays} a choisi de s'organiser en **{regime_politique}**.")
    await ctx.send(embed=embed_cpa)

    etape = 4   # Découpage administratif
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Découpage administratif de {nom_pays}",value=f"En sautant une ligne à chaque nouvel échelon, vous pouvez indiquer les niveaux de subvisions territoriales que vous avez prévu.\n**Pour terminer la liste, renseignez « Villes ».**\n*Régions-départements-villes, ou duchés/comtés/villes...*")
    await ctx.send(embed=embed_cpq)

    nv_echelon = await bot.wait_for("message")
    nv_echelon = nv_echelon.content
    liste_echelon = [nv_echelon]
    while nv_echelon != "Villes":
        nv_echelon = await bot.wait_for("message")
        nv_echelon = nv_echelon.content
        liste_echelon.append(nv_echelon)

    echelons = liste_var(liste_echelon)

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"Les subvisions administratives de {nom_pays} seront donc : {echelons}")
    await ctx.send(embed=embed_cpa)

    etape = 5   # Idéologie
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Idéologie politique {nom_pays}",value=f"Dans la continuité de la question précédente, quelles idéologies politiques seront adoptées par votre gouvernement ?\n*Anarchisme, communisme, socialisme, libéralisme, conservatisme, nationalisme...* ")
    await ctx.send(embed=embed_cpq)

    ideologie = await bot.wait_for("message")
    ideologie = ideologie.content

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"{nom_pays} a choisi d'adopter les idéologies suivantes : **{ideologie}**.")
    await ctx.send(embed=embed_cpa)

    etape = 6   # Villes principales
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Villes importantes de {nom_pays}",value=f"Nous allons désormais lister toutes les villes que vous considérez importantes. Sautez une ligne pour chaque nouvelle ville, et une fois que vous aurez fini, tapez le message « Fini ».\n\n*La première ville que vous aurez saisi sera votre capitale.*")
    await ctx.send(embed=embed_cpq)

    capitale = await bot.wait_for("message")
    capitale = capitale.content
    nv_ville = await bot.wait_for("message")
    nv_ville = nv_ville.content
    liste_villes = [nv_ville]
    while nv_ville != "Fini":
        nv_ville = await bot.wait_for("message")
        nv_ville = nv_ville.content
        liste_villes.append(nv_ville)
    liste_villes.pop()

    villes = liste_var(liste_villes)

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"La capitale de {nom_pays} est **{capitale}**. Les autres villes majeures du pays sont : {villes}")
    await ctx.send(embed=embed_cpa)

    etape = 7   # Religions présentes
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Religions présentes dans {nom_pays}",value=f"Maintenant, vous pouvez indiquer toutes les religions pratiquées dans votre pays, ainsi que le pourcentage de fidèles. \nSautez une ligne à chaque nouvelle religion, puis écrivez « Fini » après le dernier élément.")
    await ctx.send(embed=embed_cpq)

    nv_religion = await bot.wait_for("message")
    nv_religion = nv_religion.content
    liste_religions = [nv_religion]
    while nv_religion != "Fini":
        nv_religion = await bot.wait_for("message")
        nv_religion = nv_religion.content
        liste_religions.append(nv_religion)
    liste_religions.pop()

    religions = liste_var(liste_religions)

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"Les religions pratiquées dans {nom_pays} seront donc : {religions}")
    await ctx.send(embed=embed_cpa)


    etape = 8   # Répartition urbaine/rurale + populationb
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Répartition urbaine et rurale de {nom_pays}",value=f"Indiquez-nous le pourcentage de votre population habitant dans un milieu urbain. La proportion de ruraux en sera automatiquement déduite.\n\nEnsuite, indiquez dans l'ordre :\n:small_blue_diamond: Proportion d'étudiants,\n:small_blue_diamond: Proportion de retraités,\n:small_blue_diamond: Proportion d'agriculteurs,\n:small_blue_diamond: Proportion d'ouvriers,\n:small_blue_diamond: Pourcentage de conscription. \n\n*N'indiquez pas le « % » à côté des nombres.*")
    await ctx.send(embed=embed_cpq)

    pop_urbaine = await bot.wait_for("message")
    pop_urbaine = pop_urbaine.content
    pop_rurale = 100-pop_urbaine
    pop_etudiant = await bot.wait_for("message")
    pop_etudiant = pop_etudiant.content
    pop_retraite = await bot.wait_for("message")
    pop_retraite = pop_retraite.content
    pop_agri = await bot.wait_for("message")
    pop_agri = pop_agri.content
    pop_ouvrier = await bot.wait_for("message")
    pop_ouvrier = pop_ouvrier.content
    pop_conscrite = await bot.wait_for("message")
    pop_conscrite = pop_conscrite.content

    liste_pop = [pop_urbaine + " %", pop_rurale + " %", pop_etudiant + " %", pop_retraite + " %", pop_agri + " %", pop_ouvrier + " %", pop_conscrite + " %"]
    pop = liste_var(liste_pop)

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"Voici les répartitions de la population de {nom_pays} :\n:small_blue_diamond: Proportion d'urbains : {pop_urbaine} %,\n:small_blue_diamond: Proportion d'étudiants : {pop_etudiant} %,\n:small_blue_diamond: Proportion de retraités : {pop_retraite} %,\n:small_blue_diamond: Proportion d'agriculteurs : {pop_agri} %,\n:small_blue_diamond: Proportion d'ouvriers : {pop_ouvrier} %,\n:small_blue_diamond: Pourcentage de conscription : {pop_conscrite} %.")
    await ctx.send(embed=embed_cpa)


    etape = 9  # Histoire RP
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Contexte historique de {nom_pays}",value=f"Essayez d'expliquer de manière concise l'histoire de votre pays. Vous pouvez ajouter à la fin de votre texte un lien vers un document contenant l'histoire complète.")
    await ctx.send(embed=embed_cpq)

    histoire = await bot.wait_for("message")
    histoire = histoire.content

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"{nom_pays} a pour histoire : >{histoire}.")
    await ctx.send(embed=embed_cpa)


    etape = 10  # Remarques additionnelles
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Remarques additionnelles",value=f"Si vous avez des remarques particulières à ajouter, faites-le ici.")
    await ctx.send(embed=embed_cpq)

    remarques = await bot.wait_for("message")
    remarques = remarques.content

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"{remarques}")
    await ctx.send(embed=embed_cpa)


    etape = 11  # Répartition des points de base


    etape = 12  # État des infrastructures


    etape = 13  # Esprits nationaux initiaux
    embed_cpq.clear_fields()
    embed_cpq.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpq.add_field(name=f"Religions présentes dans {nom_pays}",value=f"Bientôt la fin !\n\nDans cette étape, vous allez lister tous vos esprits nationaux de départ, qui peuvent ajouter des bonus ou des malus spécifiques. Listez leurs noms en ajoutant à chaque fois un nouveau message.")
    await ctx.send(embed=embed_cpq)

    nv_esprit_nat = await bot.wait_for("message")
    nv_esprit_nat = nv_esprit_nat.content
    liste_esprits_nats = [nv_esprit_nat]
    while nv_esprit_nat != "Fini":
        nv_esprit_nat = await bot.wait_for("message")
        nv_esprit_nat = nv_esprit_nat.content
        liste_esprits_nats.append(nv_esprit_nat)
    liste_esprits_nats.pop()

    esprits_nats = ""
    for i in range(len(liste_esprits_nats)):
        esprits_nats = esprits_nats + "\n :small_blue_diamond: " + liste_esprits_nats[i]

    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"Vous en êtes à l'étape {etape} / 13.")
    embed_cpa.add_field(name=f"Parfait !",value=f"Les esprits nationaux dans {nom_pays} seront donc : {esprits_nats}")
    await ctx.send(embed=embed_cpa)

    etape = "Fin"
    embed_cpa.clear_fields()
    embed_cpa.set_footer(text=f"La phase de création du pays est terminée.")
    embed_cpa.add_field(name=f"Nom",value=f"{nom_pays}")
    embed_cpa.add_field(name=f"Dirigeant",value=f"{fonction_dirigeant} {nom_dirigeant}")
    embed_cpa.add_field(name=f"Nom",value=f"{nom_pays}")
    await ctx.send(embed=embed_cpa)"""



#################
### LANCEMENT ###
#################

bot.run(token)
