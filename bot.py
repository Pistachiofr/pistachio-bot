import discord
from discord.ext import commands
import random
import json
import os
import time
import asyncio
from discord.ui import View
# =========================
# CONFIG
# =========================
TOKEN = os.getenv("TOKEN")
OWNER_ID = 1282006578777686066
# =========================
# DONNEES
# =========================
bot = commands.Bot(...)
xp = {}
argent = {}
inventaires = {}
last_daily = {}
boutique = {
   "ajout en ami de Pistachio": 1500,
   "rôle personnalisé": 2500,
   "rôle 🌑 Moon's chosen": 3000,
   "ajout en ami de Delta Tag" : 5000,
   "rôle 🌔Moonkeeper" : 10000
   "devenir admin" : 100000
}
blagues = [
     "Quelle est la différence entre un rappeur et un campeur ? Le rappeur te nique ta mère et le campeur te monte ta tente",
      "Je me demande si les touristes chinois savent que les souvenirs qu'ils achètent viennent de chez eux",
      "Tu préfères avoir des bites à la place des dents ou chier de la mayonnaise ?",
      "Tu préfères vomir des limaces ou chier des cafards qui te grattouillent l’anus ?",
      "Tu préfères avoir des doigts en forme de saucisses ou des oreilles en forme de crêpes ?",
      "Tu préfères manger une pizza au dentifrice ou une glace au goût de sardine ?",
      "Tu préfères de très mauvais préliminaires avec Jude Law ou de très bons préliminaires avec un frère Bogdanoff ?"
]
# =========================
# JSON
# =========================
def sauvegarder():
   data = {
       "xp": xp,
       "argent": argent,
       "inventaires": inventaires,
       "last_daily": last_daily
   }
   with open("data.json", "w", encoding="utf-8") as f:
       json.dump(data, f, indent=4, ensure_ascii=False)

def charger():
   global xp
   global argent
   global inventaires
   global last_daily
   if not os.path.exists("data.json"):
       return
   with open("data.json", "r", encoding="utf-8") as f:
       data = json.load(f)
   xp = data.get("xp", {})
   argent = data.get("argent", {})
   inventaires = data.get("inventaires", {})
   last_daily = data.get("last_daily", {})
# =========================
# UTILITAIRE
# =========================
def creer_compte(user_id):
   user_id = str(user_id)
   if user_id not in xp:
       xp[user_id] = 0
   if user_id not in argent:
       argent[user_id] = 0
   if user_id not in inventaires:
       inventaires[user_id] = []
# =========================
# BOT
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
   command_prefix="!",
   intents=intents
)
# =========================
# READY
# =========================
@bot.event
async def on_ready():
   charger()
   bot.add_view(TicketView())
   print(f"Connecté en tant que {bot.user}")
   await bot.change_presence(
       activity=discord.Game(
           name="Tape !aide pour tout problème rencontré 🍀"
       )
   )
# =========================
# BIENVENUE
# =========================
@bot.event
async def on_member_join(member):
   await member.guild.system_channel.send(
       f"Salut {member.mention} bienvenue. Pour toute question ou problème, n'hésite pas à ouvrir un ticket"
   )
# =========================
# MESSAGES
# =========================
@bot.event
async def on_message(message):
   if message.author.bot:
       return
   user_id = str(message.author.id)
   creer_compte(user_id)
   xp[user_id] += 1
   sauvegarder()
   texte = message.content.lower()
   if bot.user in message.mentions:
       if "salut" in texte or "bonjour" in texte:
           await message.channel.send("👋 Salut !")
       elif "merci" in texte:
           await message.channel.send(" Avec plaisir !")
       elif "ça va" in texte or "cv" in texte:
           await message.channel.send(" trql ett ?")
       else:
           await message.channel.send(
               "Je ne parle pas aux imbéciles"
           )
   await bot.process_commands(message)
# =========================
# COMMANDES
# =========================
@bot.command()
async def ping(ctx):
   await ctx.send("🏓 Pong !")
@bot.command()
async def avatar(ctx, membre: discord.Member = None):
   if membre is None:
       membre = ctx.author
   await ctx.send(membre.display_avatar.url)
@bot.command()
async def blague(ctx):
   await ctx.send(random.choice(blagues))
@bot.command()
async def dé(ctx):
   await ctx.send(
       f"🎲 {random.randint(1,6)}"
   )
@bot.command()
async def pf(ctx):
   await ctx.send(
       random.choice(["Pile 🪙","Face 🪙"])
   )
# =========================
# XP
# =========================
@bot.command()
async def niveau(ctx, membre: discord.Member = None):
   if membre is None:
       membre = ctx.author
   user_id = str(membre.id)
   creer_compte(user_id)
   await ctx.send(
       f"⭐ {membre.name} possède {xp[user_id]} XP"
   )
# =========================
# PROFIL
# =========================
@bot.command()
async def profil(ctx, membre: discord.Member = None):
   if membre is None:
       membre = ctx.author
   user_id = str(membre.id)
   creer_compte(user_id)
   await ctx.send(
       f"""
👤 {membre.name}
⭐ XP : {xp[user_id]}
💰 Argent : {argent[user_id]}
🎒 Objets : {len(inventaires[user_id])}
"""
   )
# =========================
# DAILY
# =========================
@bot.command()
async def daily(ctx):
   user_id = str(ctx.author.id)
   creer_compte(user_id)
   maintenant = time.time()
   dernier = last_daily.get(user_id, 0)
   restant = 86400 - (maintenant - dernier)
   if restant > 0:
       heures = int(restant // 3600)
       minutes = int((restant % 3600) // 60)
       await ctx.send(
           f"⏳ Reviens dans {heures}h {minutes}min."
       )
       return
   argent[user_id] += 100
   last_daily[user_id] = maintenant
   sauvegarder()
   await ctx.send(
       f"🎁 {ctx.author.mention} reçoit 100 pièces !"
   )
# =========================
# ARGENT
# =========================
@bot.command()
async def argentt(ctx):
   user_id = str(ctx.author.id)
   creer_compte(user_id)
   await ctx.send(
       f"💰 Tu possèdes {argent[user_id]} pièces."
   )
#--------------------------
@bot.command()
async def giveargent(ctx, membre: discord.Member, montant: int):
   if ctx.author.id != OWNER_ID:
       await ctx.send("❌ Commande réservée au propriétaire.")
       return
   if montant <= 0:
       await ctx.send("❌ Montant invalide.")
       return
   user_id = str(membre.id)
   creer_compte(user_id)
   argent[user_id] += montant
   sauvegarder()
   await ctx.send(
       f"💰 {membre.mention} reçoit {montant} pièces !"
   )
#------------------------
@bot.command()
async def removeargent(ctx, membre: discord.Member, montant: int):
   if ctx.author.id != OWNER_ID:
       return
   user_id = str(membre.id)
   creer_compte(user_id)
   argent[user_id] = max(
       0,
       argent[user_id] - montant
   )
   sauvegarder()
   await ctx.send(
       f"💸 {montant} pièces retirées à {membre.mention}"
   )
# =========================
# CASINO
# =========================
@bot.command()
async def casino(ctx, mise: int):
   user_id = str(ctx.author.id)
   creer_compte(user_id)
   if mise <= 0:
       await ctx.send("❌ Mise invalide.")
       return
   if argent[user_id] < mise:
       await ctx.send("❌ Pas assez d'argent.")
       return
   if random.randint(1,100) <= 40:
       argent[user_id] += mise
       resultat = (
           f"🎉 Tu gagnes {mise} pièces !\n"
           f"💰 Solde : {argent[user_id]}"
       )
   else:
       argent[user_id] -= mise
       resultat = (
           f"💀 Tu perds {mise} pièces.\n"
           f"💰 Solde : {argent[user_id]}"
       )
   sauvegarder()
   await ctx.send(resultat)
# =========================
# SHOP
# =========================
@bot.command()
async def shop(ctx):
   texte = "🛒 Boutique\n\n"
   for objet, prix in boutique.items():
       texte += f"{objet} - {prix} pièces\n"
   await ctx.send(texte)
@bot.command()
async def acheter(ctx, objet):
   user_id = str(ctx.author.id)
   creer_compte(user_id)
   objet = objet.lower()
   if objet not in boutique:
       await ctx.send("❌ Objet introuvable.")
       return
   prix = boutique[objet]
   if argent[user_id] < prix:
       await ctx.send("❌ Pas assez d'argent.")
       return
   argent[user_id] -= prix
   inventaires[user_id].append(objet)
   sauvegarder()
   await ctx.send(
       f"✅ Achat de {objet} effectué."
   )
# =========================
# INVENTAIRE
# =========================
@bot.command()
async def inventaire(ctx):
   user_id = str(ctx.author.id)
   creer_compte(user_id)
   if len(inventaires[user_id]) == 0:
       await ctx.send("🎒 Inventaire vide.")
       return
   await ctx.send(
       "🎒 " + ", ".join(inventaires[user_id])
   )
# =========================
# TICKET
# =========================
class TicketView(View):
   def init(self):
       super().init(timeout=None)
   @discord.ui.button(
       label="🎫 Créer un ticket",
       style=discord.ButtonStyle.green,
       custom_id="create_ticket_button"
   )
   async def create_ticket(
       self,
       interaction: discord.Interaction,
       button: discord.ui.Button
   ):
       nom_salon = f"ticket-{interaction.user.id}"
       for salon in interaction.guild.text_channels:
           if salon.name == nom_salon:
               await interaction.response.send_message(
                   "❌ Tu possèdes déjà un ticket ouvert.",
                   ephemeral=True
               )
               return
       categorie = discord.utils.get(
           interaction.guild.categories,
           name="Tickets"
       )
       if categorie is None:
           categorie = await interaction.guild.create_category(
               "Tickets"
           )
       overwrites = {
           interaction.guild.default_role:
           discord.PermissionOverwrite(
               view_channel=False
           ),
           interaction.user:
           discord.PermissionOverwrite(
               view_channel=True,
               send_messages=True,
               read_message_history=True
           ),
           interaction.guild.me:
           discord.PermissionOverwrite(
               view_channel=True,
               send_messages=True,
               manage_channels=True
           )
       }
       salon = await interaction.guild.create_text_channel(
           nom_salon,
           category=categorie,
           overwrites=overwrites
       )
       await salon.send(
           f"""
🎫 Bonjour {interaction.user.mention}
Merci d'avoir contacté le support.
Décris ton problème ici.
🔒 Pour fermer le ticket :
!fermer
"""
       )
       await interaction.response.send_message(
           f"✅ Ticket créé : {salon.mention}",
           ephemeral=True
       )
# =======================
@bot.command()
async def panelticket(ctx):
   if ctx.author.id != OWNER_ID:
       return
   embed = discord.Embed(
       title="🎫 Support",
       description="""
Besoin d'aide ?
Clique sur le bouton ci-dessous pour ouvrir un ticket.
""",
       color=discord.Color.green()
   )
   await ctx.send(
       embed=embed,
       view=TicketView()
   )
# ========================
@bot.command()
async def fermer(ctx):
   if not ctx.channel.name.startswith("ticket-"):
       await ctx.send(
           "❌ Cette commande doit être utilisée dans un ticket."
       )
       return
   await ctx.send(
       "🔒 Fermeture du ticket..."
   )
   await ctx.channel.delete()
# =========================
# MP
# =========================
@bot.command()
async def mp(ctx, membre: discord.Member, *, message):
   try:
       await membre.send(message)
       await ctx.send(
           "✅ Message envoyé."
       )
   except Exception as e:
       await ctx.send(
           f"❌ {e}"
       )
# =========================
# KICK
# =========================
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, membre: discord.Member):
   try:
       await membre.kick()
       await ctx.send(
           f" {membre} expulsé."
       )
   except:
       await ctx.send(
           "❌ Impossible."
       )
# =========================
# SECRET
# =========================
@bot.command()
async def secret(ctx):
   if ctx.author.id != OWNER_ID:
       return
   await ctx.send(
       " Bonjour patron"
   )
# =========================
# GIVEAWAY
# =========================
@bot.command()
async def giveaway(ctx, duree, *, lot):
   if ctx.author.id != OWNER_ID:
       return
   multiplicateurs = {
       "s": 1,
       "m": 60,
       "h": 3600,
       "j": 86400
   }
   try:
       unite = duree[-1]
       valeur = int(duree[:-1])
       secondes = valeur * multiplicateurs[unite]
   except:
       await ctx.send(
           "❌ Format invalide.\nExemple : !giveaway 1h Nitro"
       )
       return
   embed = discord.Embed(
       title="🎉 GIVEAWAY 🎉",
       description=f"""
🎁 Lot : {lot}
⏳ Durée : {duree}
Clique sur 🎉 pour participer !
""",
       color=discord.Color.gold()
   )
   message = await ctx.send(embed=embed)
   await message.add_reaction("🎉")
   await asyncio.sleep(secondes)
   message = await ctx.channel.fetch_message(
message.id
   )
   participants = []
   for reaction in message.reactions:
       if str(reaction.emoji) == "🎉":
           async for user in reaction.users():
               if not user.bot:
                   participants.append(user)
   if len(participants) == 0:
       await ctx.send(
           "❌ Aucun participant."
       )
       return
   gagnant = random.choice(
       participants
   )
   await ctx.send(
       f"🏆 Félicitations {gagnant.mention} !\nTu remportes {lot} !"
   )

# =========================
# AIDE
# =========================
@bot.command()
async def aide(ctx):
   await ctx.send("""
🤖 ===== PISTACHIO ===== 🤖
🎮 Commandes Fun
!ping → Vérifie si le bot répond
!blague → Affiche une blague ou un dilemne
!dé → Lance un dé
!pf → Pile ou Face
!avatar → Ton avatar
!avatar @username → Avatar d'un joueur
⭐ XP
!niveau → Voir ton XP
!niveau @username → Voir l'XP d'un joueur
👤 Profil
!profil → Voir ton profil
!profil @username → Voir le profil d'un joueur
💰 Économie
!daily → Récompense quotidienne
!argentt → Voir ton argent
!casino montant → Jouer au casino
🛒 Boutique
!shop → Voir la boutique
!acheter objet → Acheter un objet
!inventaire → Voir ton inventaire
📨 Messages Privés
!mp @username message
""")
# =========================
# FIN
# =========================
bot.run(TOKEN)
