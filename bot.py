import os
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

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

# Define a loop that runs every 60 minutes
@tasks.loop(minutes=60)
async def auto_update_matches():
    print("🔄 Checking for tournament updates...")
    
    url = "YOUR_TOURNAMENT_URL_HERE"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Update Loop Notice: {e}")
    
    fetched_matches = [
        {"id": 1, "home": "Sentinels", "away": "Fnatic"},
        {"id": 2, "home": "Winner of Match 1", "away": "TBD"}
    ]
    
    # Note: Using your local tournament.db configuration context
    try:
        temp_conn = sqlite3.connect("tournament.db")
        temp_cursor = temp_conn.cursor()
        
        for match in fetched_matches:
            temp_cursor.execute("""
                UPDATE matches 
                SET home_team = ?, away_team = ? 
                WHERE id = ?
            """, (match["home"], match["away"], match["id"]))
            
        temp_conn.commit()
        temp_conn.close()
        print("✅ Database updated with latest bracket names!")
    except Exception as e:
        print(f"Tournament DB Update Notice: {e}")

# --- 📅 OFFICIAL 104-MATCH DATASET WITH TIME-LOCK TIMESTAMPS ---
MATCHES = {
    # --- GROUP STAGE ---
    1: {"teams": ["Mexico", "South Africa"], "allow_tie": True, "kickoff": datetime(2026, 6, 11, 20, 0, tzinfo=timezone.utc)},
    2: {"teams": ["South Korea", "Czechia"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 15, 0, tzinfo=timezone.utc)},
    3: {"teams": ["Canada", "Bosnia and Herzegovina"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 18, 0, tzinfo=timezone.utc)},
    4: {"teams": ["USA", "Paraguay"], "allow_tie": True, "kickoff": datetime(2026, 6, 12, 21, 0, tzinfo=timezone.utc)},
    5: {"teams": ["Haiti", "Scotland"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 13, 0, tzinfo=timezone.utc)},
    6: {"teams": ["Australia", "Türkiye"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 16, 0, tzinfo=timezone.utc)},
    7: {"teams": ["Brazil", "Morocco"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 19, 0, tzinfo=timezone.utc)},
    8: {"teams": ["Qatar", "Switzerland"], "allow_tie": True, "kickoff": datetime(2026, 6, 13, 22, 0, tzinfo=timezone.utc)},
    9: {"teams": ["Ivory Coast", "Ecuador"], "allow_tie": True, "kickoff": datetime(2026, 6, 14, 13, 0, tzinfo=timezone.utc)},
    10: {"teams": ["Argentina", "Sweden"], "allow_tie": True, "kickoff": datetime(2026, 6, 1
