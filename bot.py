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
        print("🚀 Slash commands synced successfully with Discord!")

bot = WorldCupBot()

# ==========================================
# 2. DATABASE HELPER FUNCTIONS
# ==========================================
def init_db():
    """Initializes the database tables if they do not exist."""
    # Connecting to world_cup_pool.db as specified in your repository
    conn = sqlite3.connect("world_cup_pool.db")
    cursor = conn.cursor()
    
    # Table to track user predictions safely
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
    Fetches match details based on an ID.
    This internal tracker matches the structure of your schedule.
    """
    mock_matches = {
        "1": {"teams": ["Argentina", "France"]},
        "2": {"teams": ["Winner of Match 49", "TBD"]},
        "3": {"teams": ["Brazil", "Match 50 Winner"]},
        "4": {"teams": ["England", "USA"]}
    }
    return mock_matches.get(match_id, None)

# Initialize database tables right away
init_db()

# ==========================================
# 3. BOT EVENT MONITOR
# ==========================================
@bot.event
async def on_ready():
    print(f"✅ Bot successfully logged into Discord!")
    print(f"Logged in as: {bot.user.name} (ID: {bot.user.id})")
    print("--------------------------------------------------")

# ==========================================
# 4. DISCORD SLASH COMMANDS (PERFECT INDENTATION)
# ==========================================
@bot.tree.command(name="predict", description="Predict the winner of a World Cup match!")
@app_commands.describe(match_id="The ID number of the match you want to predict")
async def predict(interaction: discord.Interaction, match_id: str):
    # Fetch the match info using the provided ID
    match_info = get_match_info(match_id)
    if not match_info:
        await interaction.response.send_message("❌ Match not found in the tournament schedule.", ephemeral=True)
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
        
        # Save prediction to sqlite3 database
        save_prediction(select_interaction.user.id, match_id, prediction)
        
        await select_interaction.response.send_message(
            f"✅ Your prediction for **{prediction}** has been securely locked in!", 
            ephemeral=True
        )

    select.callback = select_callback
    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message(
        f"Make your prediction for **{teams[0]} vs {teams[1]}**:", 
        view=view, 
        ephemeral=True
    )

# ==========================================
# 5. SAFE EXECUTION ENGINE
# ==========================================
# Checks for all possible naming configurations of your Discord Token
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN") or os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        print("🤖 Initializing Bot Connection...")
        bot.run(TOKEN)
    else:
        print("❌ CRITICAL ERROR: No bot token found in your Railway environment variables!")
        print("Please ensure you have a variable named DISCORD_TOKEN or TOKEN set.")
