import os
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

# --- 🤖 BOT INITIALIZATION & INTENTS ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 🗄️ DATABASE SETUP ---
DB_PATH = "/data/predictions.db" if os.path.exists("/data") else "predictions.db"

def init_db():
    local_conn = sqlite3.connect(DB_PATH)
    local_cursor = local_conn.cursor()
    columns = [f"m_{i} TEXT" for i in range(1, 105)]
    columns_sql = ", ".join(columns)
    local_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS brackets (
            user_id INTEGER,
            server_id INTEGER,
            username TEXT,
            score INTEGER DEFAULT 0,
            {columns_sql},
            PRIMARY KEY (user_id, server_id)
        )
    """)
    local_conn.commit()
    local_conn.close()

init_db()

# --- 📅 OFFICIAL REAL-WORLD 2026 FIFA WORLD CUP FIXTURES (1-104) ---
MATCHES = {
    # --- GROUP STAGE: ROUND 1 ---
    1: {"teams": ["Mexico", "South Africa"], "allow_tie": True, "kickoff": datetime(2026, 6, 11, 19, 0, tzinfo=timezone.utc)},
    2: {"teams": ["South Korea", "Czechia"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 2, 0, tzinfo=timezone.utc)},
    3: {"teams": ["Canada", "Bosnia and Herzegovina"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 19, 0, tzinfo=timezone.utc)},
    4: {"teams": ["USA", "Paraguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 1, 0, tzinfo=timezone.utc)},
    5: {"teams": ["Haiti", "Scotland"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)},
    6: {"teams": ["Australia", "Türkiye"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)},
    7: {"teams": ["Brazil", "Morocco"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 22, 0, tzinfo=timezone.utc)},
    8: {"teams": ["Qatar", "Switzerland"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 22, 0, tzinfo=timezone.utc)},
    9: {"teams": ["Germany", "Curaçao"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 17, 0, tzinfo=timezone.utc)},
    10: {"teams": ["Netherlands", "Japan"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 20, 0, tzinfo=timezone.utc)},
    11: {"teams": ["Ivory Coast", "Ecuador"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 20, 0, tzinfo=timezone.utc)},
    12: {"teams": ["Sweden", "Tunisia"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 2, 0, tzinfo=timezone.utc)},
    13: {"teams": ["Spain", "Cabo Verde"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 16, 0, tzinfo=timezone.utc)},
    14: {"teams": ["Belgium", "Egypt"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 19, 0, tzinfo=timezone.utc)},
    15: {"teams": ["Saudi Arabia", "Uruguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 15, 22, 0, tzinfo=timezone.utc)},
    16: {"teams": ["Iran", "New Zealand"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 1, 0, tzinfo=timezone.utc)},
    17: {"teams": ["France", "Senegal"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 19, 0, tzinfo=timezone.utc)},
    18: {"teams": ["Iraq", "Norway"], "allow_tie": True, "kickoff": datetime(2026, 6, 16, 22, 0, tzinfo=timezone.utc)},
    19: {"teams": ["Argentina", "Algeria"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 1, 0, tzinfo=timezone.utc)},
    20: {"teams": ["Austria", "Jordan"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 4, 0, tzinfo=timezone.utc)},
    21: {"teams": ["Portugal", "Congo DR"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 17, 0, tzinfo=timezone.utc)},
    22: {"teams": ["England", "Croatia"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 20, 0, tzinfo=timezone.utc)},
    23: {"teams": ["Ghana", "Panama"], "allow_tie": True, "kickoff": datetime(2026, 6, 17, 23, 0, tzinfo=timezone.utc)},
    24: {"teams": ["Uzbekistan", "Colombia"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 2, 0, tzinfo=timezone.utc)},

    # --- GROUP STAGE: ROUND 2 ---
    25: {"teams": ["Czechia", "South Africa"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 16, 0, tzinfo=timezone.utc)},
    26: {"teams": ["Switzerland", "Bosnia and Herzegovina"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 19, 0, tzinfo=timezone.utc)},
    27: {"teams": ["Canada", "Qatar"], "allow_tie": True, "kickoff": datetime(2026, 6, 18, 22, 0, tzinfo=timezone.utc)},
    28: {"teams": ["Mexico", "South Korea"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 1, 0, tzinfo=timezone.utc)},
    29: {"teams": ["Brazil", "Haiti"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 16, 0, tzinfo=timezone.utc)},
    30: {"teams": ["Scotland", "Morocco"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 19, 0, tzinfo=timezone.utc)},
    31: {"teams": ["Türkiye", "Paraguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 19, 22, 0, tzinfo=timezone.utc)},
    32: {"teams": ["USA", "Australia"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 1, 0, tzinfo=timezone.utc)},
    33: {"teams": ["Germany", "Ivory Coast"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 17, 0, tzinfo=timezone.utc)},
    34: {"teams": ["Ecuador", "Curaçao"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 20, 0, tzinfo=timezone.utc)},
    35: {"teams": ["Netherlands", "Sweden"], "allow_tie": True, "kickoff": datetime(2026, 6, 20, 23, 0, tzinfo=timezone.utc)},
    36: {"teams": ["Tunisia", "Japan"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 2, 0, tzinfo=timezone.utc)},
    37: {"teams": ["Uruguay", "Cabo Verde"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 16, 0, tzinfo=timezone.utc)},
    38: {"teams": ["Spain", "Saudi Arabia"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 19, 0, tzinfo=timezone.utc)},
    39: {"teams": ["Belgium", "Iran"], "allow_tie": True, "kickoff": datetime(2026, 6, 21, 22, 0, tzinfo=timezone.utc)},
    40: {"teams": ["New Zealand", "Egypt"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 1, 0, tzinfo=timezone.utc)},
    41: {"teams": ["Norway", "Senegal"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 19, 0, tzinfo=timezone.utc)},
    42: {"teams": ["France", "Iraq"], "allow_tie": True, "kickoff": datetime(2026, 6, 22, 22, 0, tzinfo=timezone.utc)},
    43: {"teams": ["Argentina", "Austria"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 1, 0, tzinfo=timezone.utc)},
    44: {"teams": ["Jordan", "Algeria"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 4, 0, tzinfo=timezone.utc)},
    45: {"teams": ["England", "Ghana"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 17, 0, tzinfo=timezone.utc)},
    46: {"teams": ["Panama", "Croatia"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 20, 0, tzinfo=timezone.utc)},
    47: {"teams": ["Portugal", "Uzbekistan"], "allow_tie": True, "kickoff": datetime(2026, 6, 23, 23, 0, tzinfo=timezone.utc)},
    48: {"teams": ["Colombia", "Congo DR"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 2, 0, tzinfo=timezone.utc)},

    # --- GROUP STAGE: ROUND 3 ---
    49: {"teams": ["Scotland", "Brazil"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 16, 0, tzinfo=timezone.utc)},
    50: {"teams": ["Morocco", "Haiti"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 16, 0, tzinfo=timezone.utc)},
    51: {"teams": ["Switzerland", "Canada"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 20, 0, tzinfo=timezone.utc)},
    52: {"teams": ["Bosnia and Herzegovina", "Qatar"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 20, 0, tzinfo=timezone.utc)},
    53: {"teams": ["Czechia", "Mexico"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 23, 0, tzinfo=timezone.utc)},
    54: {"teams": ["South Africa", "South Korea"], "allow_tie": True, "kickoff": datetime(2026, 6, 24, 23, 0, tzinfo=timezone.utc)},
    55: {"teams": ["Curaçao", "Ivory Coast"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 16, 0, tzinfo=timezone.utc)},
    56: {"teams": ["Ecuador", "Germany"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 16, 0, tzinfo=timezone.utc)},
    57: {"teams": ["Japan", "Sweden"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 20, 0, tzinfo=timezone.utc)},
    58: {"teams": ["Tunisia", "Netherlands"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 20, 0, tzinfo=timezone.utc)},
    59: {"teams": ["Türkiye", "USA"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 23, 0, tzinfo=timezone.utc)},
    60: {"teams": ["Paraguay", "Australia"], "allow_tie": True, "kickoff": datetime(2026, 6, 25, 23, 0, tzinfo=timezone.utc)},
    61: {"teams": ["New Zealand", "Belgium"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 16, 0, tzinfo=timezone.utc)},
    62: {"teams": ["Egypt", "Iran"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 16, 0, tzinfo=timezone.utc)},
    63: {"teams": ["Cabo Verde", "Spain"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 20, 0, tzinfo=timezone.utc)},
    64: {"teams": ["Saudi Arabia", "Uruguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 20, 0, tzinfo=timezone.utc)},
    65: {"teams": ["Iraq", "Senegal"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 23, 0, tzinfo=timezone.utc)},
    66: {"teams": ["France", "Norway"], "allow_tie": True, "kickoff": datetime(2026, 6, 26, 23, 0, tzinfo=timezone.utc)},
    67: {"teams": ["Jordan", "Argentina"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 16, 0, tzinfo=timezone.utc)},
    68: {"teams": ["Algeria", "Austria"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 16, 0, tzinfo=timezone.utc)},
    69: {"teams": ["Croatia", "Ghana"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 20, 0, tzinfo=timezone.utc)},
    70: {"teams": ["Panama", "England"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 20, 0, tzinfo=timezone.utc)},
    71: {"teams": ["Congo DR", "Uzbekistan"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
    72: {"teams": ["Colombia", "Portugal"], "allow_tie": True, "kickoff": datetime(2026, 6, 27, 23, 0, tzinfo=timezone.utc)},
}

# --- 🏆 KNOCKOUT SEEDINGS BLOCK ---
r32_slots = [
    (73, "Group A Runner-up", "Group B Runner-up", datetime(2026, 6, 28, 21, 0, tzinfo=timezone.utc)),
    (74, "Group E Winner", "Group A/B/C/D/F Third Place", datetime(2026, 6, 29, 18, 0, tzinfo=timezone.utc)),
    (75, "Group F Winner", "Group C Runner-up", datetime(2026, 6, 29, 21, 0, tzinfo=timezone.utc)),
    (76, "Group C Winner", "Group F Runner-up", datetime(2026, 6, 29, 23, 0, tzinfo=timezone.utc)),
    (77, "Group I Winner", "Group C/D/F/G/H Third Place", datetime(2026, 6, 30, 16, 0, tzinfo=timezone.utc)),
    (78, "Group E Runner-up", "Group I Runner-up", datetime(2026, 6, 30, 19, 0, tzinfo=timezone.utc)),
    (79, "Group A Winner", "Group C/E/F/H/I Third Place", datetime(2026, 6, 30, 22, 0, tzinfo=timezone.utc)),
    (80, "Group L Winner", "Group E/H/I/J/K Third Place", datetime(2026, 7, 1, 16, 0, tzinfo=timezone.utc)),
    (81, "Group D Winner", "Group B/E/F/I/J Third Place", datetime(2026, 7, 1, 19, 0, tzinfo=timezone.utc)),
    (82, "Group G Winner", "Group A/E/H/I/J Third Place", datetime(2026, 7, 1, 22, 0, tzinfo=timezone.utc)),
    (83, "Group K Runner-up", "Group L Runner-up", datetime(2026, 7, 2, 16, 0, tzinfo=timezone.utc)),
    (84, "Group H Winner", "Group J Runner-up", datetime(2026, 7, 2, 19, 0, tzinfo=timezone.utc)),
    (85, "Group B Winner", "Group E/F/G/I/J Third Place", datetime(2026, 7, 2, 22, 0, tzinfo=timezone.utc)),
    (86, "Group J Winner", "Group H Runner-up", datetime(2026, 7, 3, 16, 0, tzinfo=timezone.utc)),
    (87, "Group K Winner", "Group D/E/I/J/L Third Place", datetime(2026, 7, 3, 19, 0, tzinfo=timezone.utc)),
    (88, "Group D Runner-up", "Group G Runner-up", datetime(2026, 7, 3, 22, 0, tzinfo=timezone.utc))
]
for m_id, t1, t2, dt in r32_slots:
    MATCHES[m_id] = {"teams": [t1, t2], "allow_tie": False, "kickoff": dt}

r16_slots = [
    (89, 74, 77, datetime(2026, 7, 4, 18, 0, tzinfo=timezone.utc)),
    (90, 73, 75, datetime(2026, 7, 4, 21, 0, tzinfo=timezone.utc)),
    (91, 76, 78, datetime(2026, 7, 5, 18, 0, tzinfo=timezone.utc)),
    (92, 79, 80, datetime(2026, 7, 5, 21, 0, tzinfo=timezone.utc)),
    (93, 83, 84, datetime(2026, 7, 6, 18, 0, tzinfo=timezone.utc)),
    (94, 81, 82, datetime(2026, 7, 6, 21, 0, tzinfo=timezone.utc)),
    (95, 86, 88, datetime(2026, 7, 7, 18, 0, tzinfo=timezone.utc)),
    (96, 85, 87, datetime(2026, 7, 7, 21, 0, tzinfo=timezone.utc))
]
for m_id, src1, src2, dt in r16_slots:
    MATCHES[m_id] = {"teams": [f"Winner Match {src1}", f"Winner Match {src2}"], "allow_tie": False, "kickoff": dt}

qf_slots = [
    (97, 89, 90, datetime(2026, 7, 9, 21, 0, tzinfo=timezone.utc)),
    (98, 93, 94, datetime(2026, 7, 10, 21, 0, tzinfo=timezone.utc)),
    (99, 91, 92, datetime(2026, 7, 11, 18, 0, tzinfo=timezone.utc)),
    (100, 95, 96, datetime(2026, 7, 11, 21, 0, tzinfo=timezone.utc))
]
for m_id, src1, src2, dt in qf_slots:
    MATCHES[m_id] = {"teams": [f"Winner Match {src1}", f"Winner Match {src2}"], "allow_tie": False, "kickoff": dt}

MATCHES[101] = {"teams": ["Winner Match 97", "Winner Match 98"], "allow_tie": False, "kickoff": datetime(2026, 7, 14, 21, 0, tzinfo=timezone.utc)}
MATCHES[102] = {"teams": ["Winner Match 99", "Winner Match 100"], "allow_tie": False, "kickoff": datetime(2026, 7, 15, 21, 0, tzinfo=timezone.utc)}
MATCHES[103] = {"teams": ["Loser Match 101", "Loser Match 102"], "allow_tie": False, "kickoff": datetime(2026, 7, 18, 21, 0, tzinfo=timezone.utc)}
MATCHES[104] = {"teams": ["Winner Match 101", "Winner Match 102"], "allow_tie": False, "kickoff": datetime(2026, 7, 19, 19, 0, tzinfo=timezone.utc)}

# --- 📊 WORLD CUP REAL-TIME RESULTS INDEX ---
LIVE_RESULTS = {
    1: "Mexico", 2: "South Korea", 3: "Tie", 4: "USA", 5: "Tie",
    6: "Australia", 7: "Scotland", 8: "Tie", 9: "Germany",
    10: "Ivory Coast", 11: "Tie", 12: "Sweden", 13: "Tie"
}

# --- 🎛️ DROPDOWN ENGINE ---
class MatchDropdown(discord.ui.Select):
    def __init__(self, match_number):
        match_info = MATCHES.get(match_number)
        if not match_info: 
            return
            
        teams = match_info["teams"]
        self.is_unfinalized = (
            "Winner" in str(teams[0]) or "Match" in str(teams[0]) or "TBD" in str(teams[0]) or
            "Winner" in str(teams[1]) or "Match" in str(teams[1]) or "TBD" in str(teams[1]) or
            "Group Team" in str(teams[0]) or "Group Team" in str(teams[1]) or "Qualifier" in str(teams[0]) or
            "Runner-up" in str(teams[0]) or "Runner-up" in str(teams[1]) or "Third Place" in str(teams[0]) or "Third Place" in str(teams[1])
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
        try:
            await interaction.response.defer(ephemeral=True)
            used_followup = True
        except discord.errors.NotFound:
            used_followup = False
            
        user_id = interaction.user.id
        server_id = interaction.guild.id
        username = str(interaction.user)
        match_id = int(self.custom_id.split("_")[-1])
        selection = self.values[0]

        if self.is_unfinalized or selection == "LOCKED_PLACEHOLDER":
            msg = f"🔒 **Match Locked!** The teams for Match {match_id} haven't qualified yet."
            if used_followup: await interaction.followup.send(msg, ephemeral=True)
            else:
                try: await interaction.user.send(msg)
                except discord.Forbidden: print(f"❌ DM fail on locked match.")
            return

        current_time = datetime.now(timezone.utc)
        match_info = MATCHES.get(match_id)
        if match_info and "kickoff" in match_info:
            if current_time >= match_info["kickoff"]:
                msg = f"🔒 **Prediction Locked!** Match {match_id} started on {match_info['kickoff'].strftime('%Y-%m-%d %H:%M')} UTC."
                if used_followup: await interaction.followup.send(msg, ephemeral=True)
                else:
                    try: await interaction.user.send(msg)
                    except discord.Forbidden: pass
                return

        try:
            local_conn = sqlite3.connect(DB_PATH)
            local_cursor = local_conn.cursor()
            local_cursor.execute(
                "INSERT OR IGNORE INTO brackets (user_id, server_id, username) VALUES (?, ?, ?)", 
                (user_id, server_id, username)
            )
            local_cursor.execute(
                f"UPDATE brackets SET m_{match_id} = ? WHERE user_id = ? AND server_id = ?", 
                (selection, user_id, server_id)
            )
            local_conn.commit()
            local_conn.close()
            
            msg = f"✅ Prediction saved: **{selection}** for Match {match_id}!"
            if used_followup: await interaction.followup.send(msg, ephemeral=True)
            else:
                try: await interaction.user.send(msg)
                except discord.Forbidden: pass
        except Exception as e:
            print(f"❌ SQL Execution Error: {e}")
            msg = "⚠️ Database synchronization error occurred."
            if used_followup: await interaction.followup.send(msg, ephemeral=True)
            else:
                try: await interaction.user.send(msg)
                except discord.Forbidden: pass

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
    try:
        await interaction.response.defer(ephemeral=False)
        used_followup = True
    except discord.errors.NotFound:
        used_followup = False

    games_per_section = 5
    start_game = ((section - 1) * games_per_section) + 1
    end_game = start_game + games_per_section - 1
    
    if start_game > 104 or section < 1:
        msg = "❌ Valid sections are 1 through 21!"
        if used_followup: await interaction.followup.send(msg, ephemeral=True)
        else:
            try: await interaction.user.send(msg)
            except discord.Forbidden: pass
        return
    if end_game > 104:
        end_game = 104
        
    view = BracketSubmissionView(start_game, end_game)
    content = f"🏆 **World Cup Predictions: Matches {start_game} to {end_game}**\nMake your choices below! Use `/predict section: {section + 1}` for the next set."
    
    if used_followup:
        await interaction.followup.send(content=content, view=view)
    else:
        try:
            await interaction.channel.send(content=f"{interaction.user.mention}\n{content}", view=view)
        except discord.Forbidden:
            try: await interaction.user.send(content=f"⚠️ Channel access forbidden. Sending submission interface directly:\n{content}", view=view)
            except discord.Forbidden: print("❌ Fatal: Total channel blackout and DMs closed.")

@bot.tree.command(name="leaderboard", description="Check the top 20 players in this server.")
async def leaderboard_slash(interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral=False)
        used_followup = True
    except discord.errors.NotFound:
        used_followup = False
    
    local_conn = sqlite3.connect(DB_PATH)
    local_cursor = local_conn.cursor()
    local_cursor.execute("SELECT username, score FROM brackets WHERE server_id = ? ORDER BY score DESC LIMIT 20", (interaction.guild.id,))
    rows = local_cursor.fetchall()
    local_conn.close()

    if not rows:
        msg = "📊 No prediction records currently exist for this server."
        if used_followup: await interaction.followup.send(msg)
        else:
            try: await interaction.user.send(msg)
            except discord.Forbidden: pass
        return

    embed = discord.Embed(title=f"🏆 {interaction.guild.name} Standings", color=0x2b6cb0)
    for index, row in enumerate(rows, start=1):
        embed.add_field(name=f"{index}. {row[0]}", value=f"🎯 Points: {row[1]}", inline=False)
    
    if used_followup: 
        await interaction.followup.send(embed=embed)
    else:
        try:
            await interaction.channel.send(embed=embed)
        except discord.Forbidden:
            try: await interaction.user.send(content=f"📊 Here is the leaderboard for **{interaction.guild.name}** (Channel message permissions are missing):", embed=embed)
            except discord.Forbidden: pass

@bot.tree.command(name="mypicks", description="View your saved match predictions.")
@app_commands.describe(section="The section number to view (1-21)")
async def mypicks_slash(interaction: discord.Interaction, section: int = 1):
    try:
        await interaction.response.defer(ephemeral=True)
        used_followup = True
    except discord.errors.NotFound:
        used_followup = False
        print(f"⚠️ Warning: Interaction for /mypicks expired before deferral due to gateway latency.")
    
    user_id = interaction.user.id
    server_id = interaction.guild.id
    
    games_per_section = 5
    start_game = ((section - 1) * games_per_section) + 1
    end_game = start_game + games_per_section - 1
    
    if start_game > 104 or section < 1:
        msg = "❌ Valid sections are 1 through 21!"
        if used_followup: await interaction.followup.send(msg, ephemeral=True)
        else:
            try: await interaction.user.send(msg)
            except discord.Forbidden: pass
        return
        
    columns_to_select = ", ".join([f"m_{i}" for i in range(start_game, min(end_game + 1, 105))])
    
    local_conn = sqlite3.connect(DB_PATH)
    local_cursor = local_conn.cursor()
    local_cursor.execute(f"SELECT {columns_to_select} FROM brackets WHERE user_id = ? AND server_id = ?", (user_id, server_id))
    row = local_cursor.fetchone()
    local_conn.close()
    
    if not row or all(pick is None for pick in row):
        msg = "📝 You haven't made predictions for this section yet."
        if used_followup: await interaction.followup.send(msg, ephemeral=True)
        else:
            try: await interaction.user.send(msg)
            except discord.Forbidden: pass
        return
        
    embed = discord.Embed(title=f"📋 Predictions Check: Matches {start_game} to {min(end_game, 104)}", color=0x38a169)
    for idx, pick in enumerate(row):
        match_num = start_game + idx
        match_info = MATCHES.get(match_num)
        if match_info:
            teams = match_info["teams"]
            saved_pick = pick if pick else "Unsaved ❌"
            embed.add_field(name=f"Match {match_num}: {teams[0]} vs {teams[1]}", value=f"🔮 Pick: **{saved_pick}**", inline=False)
            
    if used_followup:
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        try:
            await interaction.channel.send(content=f"{interaction.user.mention} Here are your picks:", embed=embed, delete_after=30)
        except discord.Forbidden:
            try:
                await interaction.user.send(content="⚠️ Gateway lag/channel permission restriction encountered. Delivering your picks here via DM:", embed=embed)
            except discord.Forbidden:
                print(f"❌ Total blackout: Bot has no channel permissions and user has DMs closed.")

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
    
    try:
        await interaction.response.send_message(embed=embed)
    except discord.errors.NotFound:
        try: await interaction.channel.send(embed=embed)
        except discord.Forbidden:
            try: await interaction.user.send(embed=embed)
            except discord.Forbidden: pass

@bot.tree.command(name="help", description="Show how to play and check the point system layout.")
async def help_slash(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Bracket Bot Guide", description="Predict matches via dropdowns and climb server ranks!", color=0x4a5568)
    embed.add_field(name="🎮 Slash Commands", value=(
        "`/predict [section]` - Guess games in blocks of 5.\n"
        "`/mypicks [section]` - Check your saved choices.\n"
        "`/leaderboard` - Print top 20 player standings.\n"
        "`/match [number]` - Live info regarding a fixture."
    ), inline=False)
    embed.add_field(name="📊 Tiered Scoring Rules", value=(
        "• **Group Stage:** 1 Point\n"
        "• **Rounds of 32 & 16:** 2 Points\n"
        "• **Quarter & Semis:** 3 Points\n"
        "• **Finals:** 5 Points"
    ), inline=False)
    
    try:
        await interaction.response.send_message(embed=embed)
    except discord.errors.NotFound:
        try: await interaction.channel.send(embed=embed)
        except discord.Forbidden:
            try: await interaction.user.send(embed=embed)
            except discord.Forbidden: pass

@bot.tree.command(name="update_scores", description="[Admin Only] Fetch live match stats and update player points.")
@app_commands.checks.has_permissions(administrator=True)
async def update_scores_slash(interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)
        used_followup = True
    except discord.errors.NotFound:
        used_followup = False
        
    server_id = interaction.guild.id
    local_conn = sqlite3.connect(DB_PATH)
    local_cursor = local_conn.cursor()
    local_cursor.execute("SELECT user_id, username FROM brackets WHERE server_id = ?", (server_id,))
    users = local_cursor.fetchall()
    
    updated_count = 0
    for user in users:
        u_id = user[0]
        points = 0
        for match_id, correct_result in LIVE_RESULTS.items():
            try:
                local_cursor.execute(f"SELECT m_{match_id} FROM brackets WHERE user_id = ? AND server_id = ?", (u_id, server_id))
                user_pick_row = local_cursor.fetchone()
                
                if user_pick_row and user_pick_row[0]:
                    user_pick = str(user_pick_row[0]).strip().lower()
                    actual_result = str(correct_result).strip().lower()
                    
                    if user_pick == actual_result:
                        if 1 <= match_id <= 72: points += 1
                        elif 73 <= match_id <= 96: points += 2
                        elif 97 <= match_id <= 102: points += 3
                        elif 103 <= match_id <= 104: points += 5
            except Exception as match_err:
                print(f"⚠️ Error parsing match {match_id} calculations: {match_err}")
                continue
                
        local_cursor.execute("UPDATE brackets SET score = ? WHERE user_id = ? AND server_id = ?", (points, u_id, server_id))
        updated_count += 1
        
    local_conn.commit()
    local_conn.close()
    
    msg = f"🔄 **Scores recalculated successfully!** Processed {updated_count} player brackets."
    if used_followup: await interaction.followup.send(msg, ephemeral=True)
    else:
        try: await interaction.channel.send(msg, delete_after=15)
        except discord.Forbidden:
            try: await interaction.user.send(msg)
            except discord.Forbidden: pass

# --- 🚀 RUN BOT CONTAINER ---
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ CRITICAL SETUP ERROR: No Discord Bot Token found inside environment variables!")
