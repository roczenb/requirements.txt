import os
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands

# ==========================================
# 1. BOT SETUP & INITIALIZATION
# ==========================================
intents = discord.Intents.default()
intents.message_content = True

class WorldCupBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Syncs your slash commands with Discord globally
        await self.tree.sync()
        print("Slash commands synced successfully!")

bot = WorldCupBot()

# ==========================================
# 2. DATABASE HELPER FUNCTIONS
# ==========================================
def init_db():
    """Initializes the database tables if they do not exist."""
    conn = sqlite3.connect("world_cup_pool.db")
    cursor = conn.cursor()
    # Table to track user predictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            user_id TEXT,
            match_id TEXT,
            prediction TEXT,
            PRIMARY KEY (user_id, match_id)
        )
    """)
    conn.commit()
    conn.close()

def save_prediction(user_id: int, match_id: str, prediction: str):
    """Saves or updates a user's prediction in the database."""
    conn = sqlite3.connect("world_cup_pool.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (user_id, match_id, prediction)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, match_id) 
        DO UPDATE SET prediction = excluded.prediction
    """, (str(user_id), match_id, prediction))
    conn.commit()
    conn.close()

def get_match_info(match_id: str):
    """
    Mock function to simulate fetching match details.
    Replace this internal logic with your API or scraper logic if needed!
    """
    # Example simulated Match Database
    mock_matches = {
        "1": {"teams": ["Argentina", "France"]},
        "2": {"teams": ["Winner of Match 49", "TBD"]},
        "3": {"teams": ["Brazil", "Match 50 Winner"]},
        "4": {"teams": ["England", "USA"]}
    }
    return mock_matches.get(match_id, None)

# Initialize database tables on startup
init_db()

# ==========================================
# 3. BOT EVENTS
# ==========================================
@bot.event
async def on_ready():
    print(f"Logged in safely as {bot.user.name} (ID: {bot.user.id})")
    print("------")

# ==========================================
# 4. DISCORD SLASH COMMANDS (THE MAIN CHAIN)
# ==========================================
@bot.tree.command(name="predict", description="Predict the winner of a World Cup match!")
@app_commands.describe(match_id="The ID number of the match you want to predict")
async def predict(interaction: discord.Interaction, match_id: str):
    # Fetch the match info using the provided ID
    match_info = get_match_info(match_id)
    if not match_info:
        await interaction.response.send_message("❌ Match not found in the schedule.", ephemeral=True)
        return

    # Extract the teams
    teams = match_info["teams"]

    # Check if the match contains undecided placeholder text
    is_undecided = (
        "Winner" in str(teams[0]) or 
        "Match" in str(teams[0]) or 
        "TBD" in str(teams[0]) or
        "Winner" in str(teams[1]) or 
        "Match" in str(teams[1]) or 
        "TBD" in str(teams[1])
    )

    # Lock the match if teams aren't finalized yet
    if is_undecided:
        await interaction.response.send_message(
            "🔒 This match is currently locked! The specific teams haven't been decided yet.", 
            ephemeral=True
        )
        return

    # Create the selection options for the user dropdown menu
    options = [
        discord.SelectOption(label=teams[0], value=teams[0], description=f"Predict {teams[0]} to win!"),
        discord.SelectOption(label=teams[1], value=teams[1], description=f"Predict {teams[1]} to win!"),
        discord.SelectOption(label="Draw", value="Draw", description="Predict a tie game!")
    ]

    # Present the prediction dropdown menu to the user
    select = discord.ui.Select(placeholder="Choose the winner...", options=options)

    async def select_callback(select_interaction: discord.Interaction):
        prediction = select.values[0]
