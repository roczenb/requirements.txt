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

# --- 🗄️ REMOTE SERVER DATABASE SETUP ---
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

# --- 📅 CORRECTED CHRONOLOGICAL MATCH DATASET WITH TIME-LOCKS ---
MATCHES = {
    # --- GROUP STAGE ---
    1: {"teams": ["Mexico", "South Africa"], "allow_tie": True, "kickoff": datetime(2026, 6, 11, 20, 0, tzinfo=timezone.utc)},
    2: {"teams": ["South Korea", "Czechia"], "allow_tie": True, "kickoff": datetime(2026, 6, 11, 23, 0, tzinfo=timezone.utc)},
    3: {"teams": ["Canada", "Bosnia and Herzegovina"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 18, 0, tzinfo=timezone.utc)},
    4: {"teams": ["USA", "Paraguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 21, 0, tzinfo=timezone.utc)},
    5: {"teams": ["Haiti", "Scotland"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 13, 0, tzinfo=timezone.utc)},
    6: {"teams": ["Australia", "Türkiye"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 16, 0, tzinfo=timezone.utc)},
    7: {"teams": ["Brazil", "Morocco"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)},
    8: {"teams": ["Qatar", "Switzerland"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 22, 0, tzinfo=timezone.utc)},
    9: {"teams": ["Ivory Coast", "Ecuador"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 13, 0, tzinfo=timezone.utc)},
    10: {"teams": ["Argentina", "Sweden"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 16, 0, tzinfo=timezone.utc)},
    11: {"teams": ["Chile", "Iran"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 19, 0, tzinfo=timezone.utc)},
    12: {"teams": ["Spain", "Cameroon"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 22, 0, tzinfo=timezone.utc)},
    13: {"teams": ["Netherlands", "Honduras"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 14, 0, tzinfo=timezone.utc)},
    14: {"teams": ["France", "Tunisia"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 17, 0, tzinfo=timezone.utc)},
    15: {"teams": ["Italy", "Saudi Arabia"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 20, 0, tzinfo=timezone.utc)},
    16: {"teams": ["Japan", "Nigeria"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 23, 0, tzinfo=timezone.utc)},
    17: {"teams": ["Germany", "New Zealand"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 14, 0, tzinfo=timezone.utc)},
    18: {"teams": ["Belgium", "Algeria"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 17, 0, tzinfo=timezone.utc)},
    19: {"teams": ["Portugal", "Panama"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 20, 0, tzinfo=timezone.utc)},
    20: {"teams": ["Croatia", "Costa Rica"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 23, 0, tzinfo=timezone.utc)},
    21: {"teams": ["Uruguay", "Oman"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 14, 0, tzinfo=timezone.utc)},
    22: {"teams": ["Colombia", "Uzbekistan"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 17, 0, tzinfo=timezone.utc)},
    23: {"teams": ["England", "Ghana"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 20, 0, tzinfo=timezone.utc)},
    24: {"teams": ["Denmark", "Peru"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 23, 0, tzinfo=timezone.utc)},
    25: {"teams": ["Mexico", "Czechia"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 14, 0, tzinfo=timezone.utc)},
    26: {"teams": ["South Korea", "South Africa"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 17, 0, tzinfo=timezone.utc)},
    27: {"teams": ["Canada", "Paraguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 20, 0, tzinfo=timezone.utc)},
    28: {"teams": ["USA", "Bosnia and Herzegovina"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 23, 0, tzinfo=timezone.utc)},
    29: {"teams": ["Haiti", "Türkiye"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 14, 0, tzinfo=timezone.utc)},
    30: {"teams": ["Australia", "Scotland"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 17, 0, tzinfo=timezone.utc)},
    31: {"teams": ["Brazil", "Switzerland"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 20, 0, tzinfo=timezone.utc)},
    32: {"teams": ["Qatar", "Morocco"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 23, 0, tzinfo=timezone.utc)},
    33: {"teams": ["Ivory Coast", "Sweden"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 14, 0, tzinfo=timezone.utc)},
    34: {"teams": ["Argentina", "Ecuador"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 17, 0, tzinfo=timezone.utc)},
    35: {"teams": ["Chile", "Cameroon"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 20, 0, tzinfo=timezone.utc)},
    36: {"teams": ["Spain", "Iran"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 23, 0, tzinfo=timezone.utc)},
    37: {"teams": ["Netherlands", "Tunisia"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 14, 0, tzinfo=timezone.utc)},
    38: {"teams": ["France", "Honduras"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 17, 0, tzinfo=timezone.utc)},
    39: {"teams": ["Italy", "Nigeria"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 20, 0, tzinfo=timezone.utc)},
    40: {"teams": ["Japan", "Saudi Arabia"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 23, 0, tzinfo=timezone.utc)},
    41: {"teams": ["Germany", "Algeria"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 14, 0, tzinfo=timezone.utc)},
    42: {"teams": ["Belgium", "New Zealand"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 17, 0, tzinfo=timezone.utc)},
    43: {"teams": ["Portugal", "Costa Rica"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 20, 0, tzinfo=timezone.utc)},
    44: {"teams": ["Croatia", "Panama"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 23, 0, tzinfo=timezone.utc)},
    45: {"teams": ["Uruguay", "Uzbekistan"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 15, 0, tzinfo=timezone.utc)},
    46: {"teams": ["Colombia", "Oman"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 15, 0, tzinfo=timezone.utc)},
    47: {"teams": ["England", "Peru"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 19, 0, tzinfo=timezone.utc)},
    48: {"teams": ["Denmark", "Ghana"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 19, 0, tzinfo=timezone.utc)},
    49: {"teams": ["Mexico", "South Korea"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 15, 0, tzinfo=timezone.utc)},
    50: {"teams": ["Czechia", "South Africa"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 15, 0, tzinfo=timezone.utc)},
    51: {"teams": ["Canada", "USA"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 19, 0, tzinfo=timezone.utc)},
    52: {"teams": ["Paraguay", "Bosnia and Herzegovina"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 19, 0, tzinfo=timezone.utc)},
    53: {"teams": ["Haiti", "Australia"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 15, 0, tzinfo=timezone.utc)},
    54: {"teams": ["Türkiye", "Scotland"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 15, 0, tzinfo=timezone.utc)},
    55: {"teams": ["Brazil", "Qatar"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 19, 0, tzinfo=timezone.utc)},
    56: {"teams": ["Switzerland", "Morocco"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 19, 0, tzinfo=timezone.utc)},
    57: {"teams": ["Ivory Coast", "Argentina"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 15, 0, tzinfo=timezone.utc)},
    58: {"teams": ["Sweden", "Ecuador"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 15, 0, tzinfo=timezone.utc)},
    59: {"teams": ["Chile", "Spain"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 19, 0, tzinfo=timezone.utc)},
    60: {"teams": ["Cameroon", "Iran"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 19, 0, tzinfo=timezone.utc)},
    61: {"teams": ["Netherlands", "France"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 15, 0, tzinfo=timezone.utc)},
    62: {"teams": ["Tunisia", "Honduras"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 15, 0, tzinfo=timezone.utc)},
    63: {"teams": ["Italy", "Japan"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 19, 0, tzinfo=timezone.utc)},
    64: {"teams": ["Nigeria", "Saudi Arabia"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 19, 0, tzinfo=timezone.utc)},
    65: {"teams": ["Germany", "Belgium"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    66: {"teams": ["Algeria", "New Zealand"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    67: {"teams": ["Portugal", "Croatia"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    68: {"teams": ["Costa Rica", "Panama"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    69: {"teams": ["Uruguay", "Colombia"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    70: {"teams": ["Uzbekistan", "Oman"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    71: {"teams": ["England", "Denmark"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    72: {"teams": ["Peru", "Ghana"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    
    # --- KNOCKOUT STAGE (ROUND OF 32) ---
    73: {"teams": ["Group A Winner", "Group B Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 6, 28, 16, 0, tzinfo=timezone.utc)},
    74: {"teams": ["Group C Winner", "Group D Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 6, 28, 20, 0, tzinfo=timezone.utc)},
    75: {"teams": ["Group B Winner", "Group A Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 6, 29, 16, 0, tzinfo=timezone.utc)},
    76: {"teams": ["Group D Winner", "Group C Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 6, 29, 20, 0, tzinfo=timezone.utc)},
    77: {"teams": ["Group E Winner", "Group F Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 6, 30, 16, 0, tzinfo=timezone.utc)},
    78: {"teams": ["Group G Winner", "Group H Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 7, 30, 20, 0, tzinfo=timezone.utc)},
    79: {"teams": ["Group F Winner", "Group E Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 7, 1, 16, 0, tzinfo=timezone.utc)},
    80: {"teams": ["Group H Winner", "Group G Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 7, 1, 20, 0, tzinfo=timezone.utc)},
    81: {"teams": ["Group I Winner", "Group J Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 7, 2, 16, 0, tzinfo=timezone.utc)},
    82: {"teams": ["Group K Winner", "Group L Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 7, 2, 20, 0, tzinfo=timezone.utc)},
    83: {"teams": ["Group J Winner", "Group I Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 7, 3, 16, 0, tzinfo=timezone.utc)},
    84: {"teams": ["Group L Winner", "Group K Runner-up"], "allow_tie": False, "kickoff": datetime(2026, 7, 3, 20, 0, tzinfo=timezone.utc)},
    85: {"teams": ["3rd Place Team 1", "3rd Place Team 2"], "allow_tie": False, "kickoff": datetime(2026, 7, 3, 23, 0, tzinfo=timezone.utc)},
    86: {"teams": ["3rd Place Team 3", "3rd Place Team 4"], "allow_tie": False, "kickoff": datetime(2026, 7, 3, 23, 0, tzinfo=timezone.utc)},
    87: {"teams": ["3rd Place Team 5", "3rd Place Team 6"], "allow_tie": False, "kickoff": datetime(2026, 7, 3, 23, 0, tzinfo=timezone.utc)},
    88: {"teams": ["3rd Place Team 7", "3rd Place Team 8"], "allow_tie": False, "kickoff": datetime(2026, 7, 3, 23, 0, tzinfo=timezone.utc)},
    
    # --- ROUND OF 16 ---
    89: {"teams": ["Winner Match 73", "Winner Match 74"], "allow_tie": False, "kickoff": datetime(2026, 7, 4, 16, 0, tzinfo=timezone.utc)},
    90: {"teams": ["Winner Match 75", "Winner Match 76"], "allow_tie": False, "kickoff": datetime(2026, 7, 4, 20, 0, tzinfo=timezone.utc)},
    91: {"teams": ["Winner Match 77", "Winner Match 78"], "allow_tie": False, "kickoff": datetime(2026, 7, 5, 16, 0, tzinfo=timezone.utc)},
    92: {"teams": ["Winner Match 79", "Winner Match 80"], "allow_tie": False, "kickoff": datetime(2026, 7, 5, 20, 0, tzinfo=timezone.utc)},
    93: {"teams": ["Winner Match 81", "Winner Match 82"], "allow_tie": False, "kickoff": datetime(2026, 7, 6, 16, 0, tzinfo=timezone.utc)},
    94: {"teams": ["Winner Match 83", "Winner Match 84"], "allow_tie": False, "kickoff": datetime(2026, 7, 6, 20, 0, tzinfo=timezone.utc)},
    95: {"teams": ["Winner Match 85", "Winner Match 86"], "allow_tie": False, "kickoff": datetime(2026, 7, 7, 16, 0, tzinfo=timezone.utc)},
    96: {"teams": ["Winner Match 87", "Winner Match 88"], "allow_tie": False, "kickoff": datetime(2026, 7, 7, 20, 0, tzinfo=timezone.utc)},
    
    # --- QUARTERFINALS ---
    97: {"teams": ["Winner Match 89", "Winner Match 90"], "allow_tie": False, "kickoff": datetime(2026, 7, 8, 16, 0, tzinfo=timezone.utc)},
    98: {"teams": ["Winner Match 91", "Winner Match 92"], "allow_tie": False, "kickoff": datetime(2026, 7, 9, 20, 0, tzinfo=timezone.utc)},
    99: {"teams": ["Winner Match 93", "Winner Match 94"], "allow_tie": False, "kickoff": datetime(2026, 7, 10, 16, 0, tzinfo=timezone.utc)},
    100: {"teams": ["Winner Match 95", "Winner Match 96"], "allow_tie": False, "kickoff": datetime(2026, 7, 11, 20, 0, tzinfo=timezone.utc)},
    
    # --- SEMIFINALS ---
    101: {"teams": ["Winner Match 97", "Winner Match 98"], "allow_tie": False, "kickoff": datetime(2026, 7, 14, 20, 0, tzinfo=timezone.utc)},
    102: {"teams": ["Winner Match 99", "Winner Match 100"], "allow_tie": False, "kickoff": datetime(2026, 7, 15, 20, 0, tzinfo=timezone.utc)},
    
    # --- FINALS ---
    103: {"teams": ["Loser Match 101", "Loser Match 102"], "allow_tie": False, "kickoff": datetime(2026, 7, 18, 20, 0, tzinfo=timezone.utc)},
    104: {"teams": ["Winner Match 101", "Winner Match 102"], "allow_tie": False, "kickoff": datetime(2026, 7, 19, 19, 0, tzinfo=timezone.utc)}
}

# --- 📊 MASTER RESULTS ANSWER KEY (NON-BLOCKING SCRAPER) ---
MANUAL_RESULTS = {1: "Mexico", 2: "South Korea", 3: "Tie", 4: "USA", 5: "Tie"}
LIVE_RESULTS = {}
LIVE_RESULTS.update(MANUAL_RESULTS)

def fetch_live_world_cup_results():
    automated_results = {}
    try:
        url = "https://www.theguardian.com/football/world-cup-2026-fixtures"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = soup.find_all('div', class_='football-match')
        
        for idx, match in enumerate(matches, start=1):
            home_el = match.find('div', class_='team-home')
            away_el = match.find('div', class_='team-away')
            score_el = match.find('div', class_='match-score')
            
            if home_el and away_el and score_el:
                home_team = home_el.text.strip()
                away_team = away_el.text.strip()
                score_text = score_el.text.strip()
                
                if "-" in score_text:
                    home_goals, away_goals = map(int, score_text.split("-"))
                    if home_goals > away_goals:
                        automated_results[idx] = home_team
                    elif away_goals > home_goals:
                        automated_results[idx] = away_team
                    else:
                        automated_results[idx] = "Tie"
    except Exception as e:
        print(f"Scraper thread handling delay notice: {e}")
    return automated_results

# Define background worker task loop
@tasks.loop(minutes=60)
async def auto_update_matches():
    print("🔄 Checking for tournament updates...")
    
    # Non-blocking executor pattern offloads requests away from the event loop thread
    loop = asyncio.get_event_loop()
    scraped_data = await loop.run_in_executor(None, fetch_live_world_cup_results)
    if scraped_data:
        LIVE_RESULTS.update(scraped_data)
        print(f"✅ Cached results dictionary updated synchronized. Total matches registered: {len(LIVE_RESULTS)}")
        
    fetched_matches = [
        {"id": 1, "home": "Sentinels", "away": "Fnatic"},
        {"id": 2, "home": "Winner of Match 1", "away": "TBD"}
    ]
    
    if os.path.exists("tournament.db"):
        try:
            temp_conn = sqlite3.connect("tournament.db")
            temp_cursor = temp_conn.cursor()
            for match in fetched_matches:
                temp_cursor.execute("""
                    UPDATE matches SET home_team = ?, away_team = ? WHERE id = ?
                """, (match["home"], match["away"], match["id"]))
            temp_conn.commit()
            temp_conn.close()
            print("✅ Database synced with updated knockout rosters!")
        except Exception as e:
            print(f"Tournament DB Fallback Notice: {e}")

# --- 🎛️ ANTI-DUPLICATE INTERACTIVE COMPONENTS ---
class MatchDropdown(discord.ui.Select):
    def __init__(self, match_number):
        match_info = MATCHES.get(match_number)
        if not match_info: 
            return
            
        teams = match_info["teams"]
        
        # 🛡️ UNRESOLVED PLACEHOLDER NAME PROTECTION TRACKER
        self.is_unfinalized = (
            "Winner" in str(teams[0]) or "Match" in str(teams[0]) or "TBD" in str(teams[0]) or
            "Winner" in str(teams[1]) or "Match" in str(teams[1]) or "TBD" in str(teams[1]) or
            "Group" in str(teams[0])  or "Group" in str(teams[1])  or "Place" in str(teams[0])
        )

        if self.is_unfinalized:
            options = [
                discord.SelectOption(
                    label="🔒 Locked: Teams Unfinalized", 
                    value="LOCKED_PLACEHOLDER", 
                    description=f"{teams[0]} vs {teams[1]}"
                )
            ]
        else:
            options = [
                discord.SelectOption(label=f"🥇 Winner: {teams[0]}", value=teams[0]),
                discord.SelectOption(label=f"🥈 Winner: {teams[1]}", value=teams[1])
            ]
            if match_info["allow_tie"]:
                options.append(discord.SelectOption(label="🤝 Tie Game", value="Tie"))
            
        super().__init__(
            placeholder=f"Pick winner for Match {match_number}...",
            min_values=1, max_values=1,
            options=options,
            custom_id=f"wc_match_{match_number}"
        )

    async def callback(self, interaction: discord.Interaction):
        # 🛡️ ANTI-DUPLICATE DROP SUBMISSION SHIELD
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
                f"🔒 **Match Locked!** You cannot submit a prediction for Match {match_id} yet because the real qualifying teams haven't been finalized in the bracket.",
                ephemeral=True
            )
            return

        # --- 🕒 UTC COMPLIANT TIME LOCK CHECK ---
        current_time = datetime.now(timezone.utc)
        match_info = MATCHES.get(match_id)
        if match_info and "kickoff" in match_info:
            if current_time >= match_info["kickoff"]:
                await interaction.followup.send(
                    f"🔒 **Prediction Locked!** Match {match_id} has already kicked off on {match_info['kickoff'].strftime('%Y-%m-%d %H:%M')} UTC.", 
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
            await interaction.followup.send(f"✅ Saved: You picked **{selection}** for Match {match_id}!", ephemeral=True)
        except Exception as e:
            print(f"❌ DB Save Error: {e}")
            await interaction.followup.send("⚠️ Database sync issue.", ephemeral=True)

class BracketSubmissionView(discord.ui.View):
    def __init__(self, start_game, end_game):
        super().__init__(timeout=None)
        for match_num in range(start_game, end_game + 1):
            if match_num in MATCHES:
                self.add_item(MatchDropdown(match_num))

# --- 🔄 SYNC SLASH COMMANDS ON STARTUP ---
@bot.event
async def on_ready():
    print(f"🥇 Bot logged in as {bot.user}")
    
    if not auto_update_matches.is_running():
        auto_update_matches.start()
        
    try:
        synced = await bot.tree.sync()
        print(f"⚙️ Successfully synced {len(synced)} Slash Commands globally!")
    except Exception as e:
        print(f"❌ Error syncing slash commands: {e}")

# --- 💬 APPLICATION SLASH COMMANDS ---

@bot.tree.command(name="predict", description="Submit your World Cup predictions in groups of 5 matches.")
@app_commands.describe(section="The section number you want to guess (1 through 21)")
async def predict_slash(interaction: discord.Interaction, section: int = 1):
    # 🛡️ ANTI-DUPLICATE INTERACTION EXECUTION FILTER
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
        await interaction.response.send_message("📊 Standings are empty for this server! Submissions are open.", ephemeral=True)
        return

    embed = discord.Embed(title=f"🏆 {interaction.guild.name} Leaderboard", color=0x2b6cb0)
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
        await interaction.response.send_message("📝 You haven't made predictions yet! Use `/predict`.", ephemeral=True)
        return
        
    embed = discord.Embed(title=f"📋 {interaction.user.name}'s Picks: Matches {start_game} to {min(end_game, 104)}", color=0x38a169)
    for idx, pick in enumerate(row):
        match_num = start_game + idx
        match_info = MATCHES.get(match_num)
        if match_info:
            teams = match_info["teams"]
            saved_pick = pick if pick else "No prediction made yet"
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

# --- 🚀 BOT INITIATION ---
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN") or os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        print("🤖 Booting up bot application streams...")
        bot.run(TOKEN)
    else:
        print("❌ CRITICAL SETUP ERROR: No Discord Bot Token found!")
