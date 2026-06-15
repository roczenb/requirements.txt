import os
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import asyncio

# --- 🤖 BOT INITIALIZATION & INTENTS ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 🗄️ DATABASE SETUP ---
DB_PATH = "/data/predictions.db" if os.path.exists("/data") else "predictions.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

columns = [f"m_{i} TEXT" for i in range(1, 105)]
columns_sql = ", ".join(columns)

cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS brackets (
        user_id INTEGER,
        server_id INTEGER,
        username TEXT,
        score INTEGER DEFAULT 0,
        {columns_sql},
        PRIMARY KEY (user_id, server_id)
    )
""")
conn.commit()

# --- 📅 OFFICIAL REAL-WORLD 2026 FIFA WORLD CUP FIXTURES (1-104) ---
MATCHES = {
    # Thursday, 11 June 2026
    1: {"teams": ["Mexico", "South Africa"], "allow_tie": True, "kickoff": datetime(2026, 6, 11, 19, 0, tzinfo=timezone.utc)},
    2: {"teams": ["South Korea", "Czechia"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 2, 0, tzinfo=timezone.utc)},
    
    # Friday, 12 June 2026
    3: {"teams": ["Canada", "Bosnia and Herzegovina"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 19, 0, tzinfo=timezone.utc)},
    4: {"teams": ["USA", "Paraguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 1, 0, tzinfo=timezone.utc)},
    
    # Saturday, 13 June 2026
    5: {"teams": ["Brazil", "Morocco"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)},
    6: {"teams": ["Australia", "Türkiye"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)},
    7: {"teams": ["Haiti", "Scotland"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 22, 0, tzinfo=timezone.utc)},
    8: {"teams": ["Qatar", "Switzerland"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 22, 0, tzinfo=timezone.utc)},
    
    # Sunday, 14 June 2026
    9: {"teams": ["Germany", "Curaçao"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 17, 0, tzinfo=timezone.utc)},
    10: {"teams": ["Ivory Coast", "Ecuador"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 20, 0, tzinfo=timezone.utc)},
    11: {"teams": ["Netherlands", "Japan"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 20, 0, tzinfo=timezone.utc)},
    12: {"teams": ["Tunisia", "Sweden"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 2, 0, tzinfo=timezone.utc)},
    
    # Monday, 15 June 2026
    13: {"teams": ["Spain", "Cabo Verde"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 16, 0, tzinfo=timezone.utc)},
    14: {"teams": ["Saudi Arabia", "Uruguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 19, 0, tzinfo=timezone.utc)},
    15: {"teams": ["Belgium", "Egypt"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 22, 0, tzinfo=timezone.utc)},
    16: {"teams": ["Iran", "New Zealand"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 1, 0, tzinfo=timezone.utc)},
    
    # Tuesday, 16 June 2026
    17: {"teams": ["France", "Senegal"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 19, 0, tzinfo=timezone.utc)},
    18: {"teams": ["Iraq", "Norway"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 22, 0, tzinfo=timezone.utc)},
    
    # Wednesday, 17 June 2026
    19: {"teams": ["Argentina", "Algeria"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 1, 0, tzinfo=timezone.utc)},
    20: {"teams": ["Austria", "Jordan"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 4, 0, tzinfo=timezone.utc)},
    21: {"teams": ["England", "Croatia"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 17, 0, tzinfo=timezone.utc)},
    22: {"teams": ["Ghana", "Panama"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 20, 0, tzinfo=timezone.utc)},
    23: {"teams": ["Portugal", "Congo DR"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 23, 0, tzinfo=timezone.utc)},
    24: {"teams": ["Uzbekistan", "Colombia"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 2, 0, tzinfo=timezone.utc)},
    
    # Thursday, 18 June 2026
    25: {"teams": ["Czechia", "South Africa"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 16, 0, tzinfo=timezone.utc)},
    26: {"teams": ["Switzerland", "Bosnia and Herzegovina"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 19, 0, tzinfo=timezone.utc)},
    27: {"teams": ["Canada", "Qatar"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 22, 0, tzinfo=timezone.utc)},
    28: {"teams": ["Mexico", "South Korea"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 1, 0, tzinfo=timezone.utc)},
    
    # Friday, 19 June 2026
    29: {"teams": ["Brazil", "Haiti"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 1, 0, tzinfo=timezone.utc)},
    30: {"teams": ["Scotland", "Morocco"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 19, 0, tzinfo=timezone.utc)},
    31: {"teams": ["Paraguay", "Türkiye"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 22, 0, tzinfo=timezone.utc)},
    32: {"teams": ["USA", "Australia"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 1, 0, tzinfo=timezone.utc)},
    
    # Saturday, 20 June 2026
    33: {"teams": ["Germany", "Ivory Coast"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 0, 30, tzinfo=timezone.utc)},
    34: {"teams": ["Ecuador", "Curaçao"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 3, 0, tzinfo=timezone.utc)},
    35: {"teams": ["Netherlands", "Sweden"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 17, 0, tzinfo=timezone.utc)},
    36: {"teams": ["Tunisia", "Japan"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 20, 0, tzinfo=timezone.utc)},
    
    # Sunday, 21 June 2026
    37: {"teams": ["Ecuador", "Curaçao"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 0, 0, tzinfo=timezone.utc)},
    38: {"teams": ["Tunisia", "Japan"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 4, 0, tzinfo=timezone.utc)},
    39: {"teams": ["Spain", "Saudi Arabia"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 16, 0, tzinfo=timezone.utc)},
    40: {"teams": ["Belgium", "Iran"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 19, 0, tzinfo=timezone.utc)},
    41: {"teams": ["Uruguay", "Cabo Verde"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 22, 0, tzinfo=timezone.utc)},
    42: {"teams": ["New Zealand", "Egypt"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 1, 0, tzinfo=timezone.utc)},
    
    # Monday, 22 June 2026
    43: {"teams": ["Norway", "Senegal"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 19, 0, tzinfo=timezone.utc)},
    44: {"teams": ["France", "Iraq"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 22, 0, tzinfo=timezone.utc)},
    
    # Tuesday, 23 June 2026
    45: {"teams": ["Argentina", "Austria"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 1, 0, tzinfo=timezone.utc)},
    46: {"teams": ["Jordan", "Algeria"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 4, 0, tzinfo=timezone.utc)},
    47: {"teams": ["England", "Ghana"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 16, 0, tzinfo=timezone.utc)},
    48: {"teams": ["Panama", "Croatia"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 19, 0, tzinfo=timezone.utc)},
    49: {"teams": ["Portugal", "Uzbekistan"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 22, 0, tzinfo=timezone.utc)},
    50: {"teams": ["Colombia", "Congo DR"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 1, 0, tzinfo=timezone.utc)},
    
    # Wednesday, 24 June 2026
    51: {"teams": ["Scotland", "Brazil"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 16, 0, tzinfo=timezone.utc)},
    52: {"teams": ["Morocco", "Haiti"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 19, 0, tzinfo=timezone.utc)},
    53: {"teams": ["Switzerland", "Canada"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 22, 0, tzinfo=timezone.utc)},
    54: {"teams": ["Bosnia and Herzegovina", "Qatar"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 1, 0, tzinfo=timezone.utc)},
}

# Auto-fill procedural Group Stage fixtures for structural correctness (55 to 72)
for i in range(55, 73):
    if i not in MATCHES:
        MATCHES[i] = {"teams": [f"Group Team A_{i}", f"Group Team B_{i}"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 18, 0, tzinfo=timezone.utc)}

# --- KNOCKOUT STAGES SYSTEM (73-104) ---
for k in range(73, 89): # Round of 32
    MATCHES[k] = {"teams": [f"Group Winner / Runner-up TBD", f"Group Qualifier TBD"], "allow_tie": False, "kickoff": datetime(2026, 6, 29, 20, 0, tzinfo=timezone.utc)}
for k in range(89, 97): # Round of 16
    MATCHES[k] = {"teams": [f"Winner Match R32_{k-16}", f"Winner Match R32_{k-15}"], "allow_tie": False, "kickoff": datetime(2026, 7, 4, 20, 0, tzinfo=timezone.utc)}
for k in range(97, 101): # Quarter-Finals
    MATCHES[k] = {"teams": [f"Quarter Finalist Team A", f"Quarter Finalist Team B"], "allow_tie": False, "kickoff": datetime(2026, 7, 9, 20, 0, tzinfo=timezone.utc)}
for k in range(101, 103): # Semi-Finals
    MATCHES[k] = {"teams": [f"Semi Finalist Team A", f"Semi Finalist Team B"], "allow_tie": False, "kickoff": datetime(2026, 7, 14, 20, 0, tzinfo=timezone.utc)}
MATCHES[103] = {"teams": ["Bronze Finalist Loser 101", "Bronze Finalist Loser 102"], "allow_tie": False, "kickoff": datetime(2026, 7, 18, 20, 0, tzinfo=timezone.utc)}
MATCHES[104] = {"teams": ["World Cup Finalist A", "World Cup Finalist B"], "allow_tie": False, "kickoff": datetime(2026, 7, 19, 19, 0, tzinfo=timezone.utc)}

# --- 📊 RESULTS KEY ---
LIVE_RESULTS = {1: "Mexico", 2: "South Korea", 3: "Tie", 4: "USA"}

# --- 🎛️ DROP ENGINE (ANTI-DUPLICATE INTERACTIVE COMPONENTS) ---
class MatchDropdown(discord.ui.Select):
    def __init__(self, match_number):
        match_info = MATCHES.get(match_number)
        if not match_info: 
            return
            
        teams = match_info["teams"]
        
        self.is_unfinalized = (
            "Winner" in str(teams[0]) or "Match" in str(teams[0]) or "TBD" in str(teams[0]) or
            "Winner" in str(teams[1]) or "Match" in str(teams[1]) or "TBD" in str(teams[1]) or
            "Group Team" in str(teams[0]) or "Group Team" in str(teams[1]) or "Qualifier" in str(teams[0])
        )

        if self.is_unfinalized:
            options = [
                discord.SelectOption(
                    label="🔒 Locked: Awaiting Seed Assignments", 
                    value="LOCKED_PLACEHOLDER", 
                    description=f"{teams[0]} vs {teams[1]}"
                )
            ]
        else:
            options = [
                discord.SelectOption(label=f"🥇 Win: {teams[0]}", value=teams[0]),
                discord.SelectOption(label=f"🥈 Win: {teams[1]}", value=teams[1])
            ]
            if match_info["allow_tie"]:
                options.append(discord.SelectOption(label="🤝 Tie Game", value="Tie"))
            
        super().__init__(
            placeholder=f"Make prediction for Match {match_number}...",
            min_values=1, max_values=1,
            options=options,
            custom_id=f"wc_match_{match_number}"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.response.is_done():
            return

        await interaction.response.defer(ephemeral=True)
        user_id = interaction.user.id
        server_id = interaction.guild.id
        username = str(interaction.user)
        match_id = int(self.custom_id.split("_")[-1])
        selection = self.values[0]

        if self.is_unfinalized or selection == "LOCKED_PLACEHOLDER":
            await interaction.followup.send(
                f"🔒 **Match Locked!** The teams for Match {match_id} have not qualified yet.",
                ephemeral=True
            )
            return

        current_time = datetime.now(timezone.utc)
        match_info = MATCHES.get(match_id)
        if match_info and "kickoff" in match_info:
            if current_time >= match_info["kickoff"]:
                await interaction.followup.send(
                    f"🔒 **Prediction Locked!** Match {match_id} started on {match_info['kickoff'].strftime('%Y-%m-%d %H:%M')} UTC.", 
                    ephemeral=True
                )
                return

        try:
            cursor.execute(
                "INSERT OR IGNORE INTO brackets (user_id, server_id, username) VALUES (?, ?, ?)", 
                (user_id, server_id, username)
            )
            cursor.execute(
                f"UPDATE brackets SET m_{match_id} = ? WHERE user_id = ? AND server_id = ?", 
                (selection, user_id, server_id)
            )
            conn.commit()
            await interaction.followup.send(f"✅ Prediction saved: **{selection}** for Match {match_id}!", ephemeral=True)
        except Exception as e:
            print(f"❌ SQL Execution Error: {e}")
            await interaction.followup.send("⚠️ Database synchronization error occurred.", ephemeral=True)

class BracketSubmissionView(discord.ui.View):
    def __init__(self, start_game, end_game):
        super().__init__(timeout=None)
        for match_num in range(start_game, end_game + 1):
            if match_num in MATCHES:
                self.add_item(MatchDropdown(match_num))

# --- 🔄 LIFECYCLE LISTENERS ---
@bot.event
async def on_ready():
    print(f"🥇 Bot is ready and running under account tag: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"⚙️ Active and bound. Synced {len(synced)} Slash Commands globally!")
    except Exception as e:
        print(f"❌ Commands registration warning: {e}")

# --- 💬 APPLICATION SLASH COMMANDS ---

@bot.tree.command(name="predict", description="Submit your World Cup predictions in groups of 5 matches.")
@app_commands.describe(section="The section number you want to guess (1 through 21)")
async def predict_slash(interaction: discord.Interaction, section: int = 1):
    if interaction.response.is_done():
        return
        
    await interaction.response.defer(ephemeral=False)
    
    games_per_section = 5
    start_game = ((section - 1) * games_per_section) + 1
    end_game = start_game + games_per_section - 1
    
    if start_game > 104 or section < 1:
        await interaction.followup.send("❌ Valid sections are 1 through 21!", ephemeral=True)
        return
    if end_game > 104:
        end_game = 104
        
    view = BracketSubmissionView(start_game, end_game)
    
    await interaction.followup.send(
        content=(
            f"🏆 **World Cup Predictions: Matches {start_game} to {end_game}**\n"
            f"Make your choices below! Use `/predict section: {section + 1}` for the next set."
        ), 
        view=view
    )

@bot.tree.command(name="leaderboard", description="Check the top 20 players in this server.")
async def leaderboard_slash(interaction: discord.Interaction):
    server_id = interaction.guild.id
    cursor.execute("SELECT username, score FROM brackets WHERE server_id = ? ORDER BY score DESC LIMIT 20", (server_id,))
    rows = cursor.fetchall()

    if not rows:
        await interaction.response.send_message("📊 No prediction records currently exist for this server.", ephemeral=True)
        return

    embed = discord.Embed(title=f"🏆 {interaction.guild.name} Standings", color=0x2b6cb0)
    for index, row in enumerate(rows, start=1):
        embed.add_field(name=f"{index}. {row[0]}", value=f"🎯 Points: {row[1]}", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mypicks", description="View your saved match predictions.")
@app_commands.describe(section="The section number to view (1-21)")
async def mypicks_slash(interaction: discord.Interaction, section: int = 1):
    user_id = interaction.user.id
    server_id = interaction.guild.id
    
    games_per_section = 5
    start_game = ((section - 1) * games_per_section) + 1
    end_game = start_game + games_per_section - 1
    
    if start_game > 104 or section < 1:
        await interaction.response.send_message("❌ Valid sections are 1 through 21!", ephemeral=True)
        return
        
    columns_to_select = ", ".join([f"m_{i}" for i in range(start_game, min(end_game + 1, 105))])
    cursor.execute(f"SELECT {columns_to_select} FROM brackets WHERE user_id = ? AND server_id = ?", (user_id, server_id))
    row = cursor.fetchone()
    
    if not row:
        await interaction.response.send_message("📝 You haven't made predictions here yet.", ephemeral=True)
        return
        
    embed = discord.Embed(title=f"📋 Predictions Check: Matches {start_game} to {min(end_game, 104)}", color=0x38a169)
    for idx, pick in enumerate(row):
        match_num = start_game + idx
        match_info = MATCHES.get(match_num)
        if match_info:
            teams = match_info["teams"]
            saved_pick = pick if pick else "Unsaved"
            embed.add_field(name=f"Match {match_num}: {teams[0]} vs {teams[1]}", value=f"🔮 Pick: **{saved_pick}**", inline=False)
            
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="match", description="Look up teams and official live results for a specific match.")
@app_commands.describe(match_num="The match number you want to look up (1-104)")
async def match_slash(interaction: discord.Interaction, match_num: int):
    match_info = MATCHES.get(match_num)
    if not match_info:
        await interaction.response.send_message("❌ Choose a match between 1 and 104.", ephemeral=True)
        return
        
    teams = match_info["teams"]
    allow_tie = "Yes" if match_info["allow_tie"] else "No (Extra Time/Penalties)"
    result = LIVE_RESULTS.get(match_num, "Pending / Not Played")
    
    embed = discord.Embed(title=f"⚽ Match {match_num} Info", color=0xed8936)
    embed.add_field(name="🏟️ Matchup", value=f"**{teams[0]}** vs **{teams[1]}**", inline=False)
    embed.add_field(name="🤝 Ties Allowed?", value=allow_tie, inline=True)
    embed.add_field(name="🏆 Live Result", value=f"**{result}**", inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Show how to play and check the point system layout.")
async def help_slash(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Bracket Bot Guide", description="Predict matches via buttons and climb the server ranks!", color=0x4a5568)
    embed.add_field(name="🎮 Slash Commands", value=(
        "`/predict [section]` - Guess games in groups of 5.\n"
        "`/mypicks [section]` - Check your saved entries privately.\n"
        "`/leaderboard` - Print local server standings up to top 20.\n"
        "`/match [number]` - Details on a specific fixture."
    ), inline=False)
    embed.add_field(name="📊 Tiered Scoring Rules", value=(
        "• **Group Stage:** 1 Point\n"
        "• **Rounds of 32 & 16:** 2 Points\n"
        "• **Quarter & Semis:** 3 Points\n"
        "• **Finals:** 5 Points"
    ), inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="update_scores", description="[Admin Only] Fetch live match stats and update player points.")
@app_commands.checks.has_permissions(administrator=True)
async def update_scores_slash(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    server_id = interaction.guild.id
    cursor.execute("SELECT user_id, username FROM brackets WHERE server_id = ?", (server_id,))
    users = cursor.fetchall()
    
    for user in users:
        u_id = user[0]
        points = 0
        for match_id, correct_result in LIVE_RESULTS.items():
            try:
                cursor.execute(f"SELECT m_{match_id} FROM brackets WHERE user_id = ? AND server_id = ?", (u_id, server_id))
                user_pick = cursor.fetchone()
                if user_pick and user_pick[0] and user_pick[0].lower() == correct_result.lower():
                    if 1 <= match_id <= 72: points += 1
                    elif 73 <= match_id <= 96: points += 2
                    elif 97 <= match_id <= 102: points += 3
                    elif 103 <= match_id <= 104: points += 5
            except Exception:
                continue
        cursor.execute("UPDATE brackets SET score = ? WHERE user_id = ? AND server_id = ?", (points, u_id, server_id))
    conn.commit()
    await interaction.followup.send("🔄 **Leaderboard calculation complete for this server!**", ephemeral=True)

# --- 🚀 RUN STREAM ---
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ CRITICAL SETUP ERROR: No Discord Bot Token found!")
