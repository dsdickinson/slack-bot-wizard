"""
Slack AI Wizard Bot
===================

Features:
- Runs as a Slack bot in its own channel
- Responds in Scottish Gaelic-style speech
- Heavy Dungeons & Dragons lore references
- Wizard personality
- Humorous responses
- Uses local or remote LLM endpoint
- Easy to deploy in Kubernetes

Recommended:
- FastAPI
- Slack Bolt
- Ollama or OpenAI-compatible endpoint

Example channels:
    #wizard-tower
    #arcane-council
    #gaelic-mage

Environment Variables:
----------------------
SLACK_BOT_TOKEN=
SLACK_APP_TOKEN=
LLM_API_URL=http://ollama:11434/api/generate
LLM_MODEL=mistral

Install:
--------
pip install slack_bolt fastapi uvicorn requests python-dotenv

Run:
----
python wizard_bot.py

Slack Setup:
------------
1. Create Slack App:
   https://api.slack.com/apps

2. Enable:
   - Socket Mode
   - Event Subscriptions
   - Bot Token Scopes:
       app_mentions:read
       channels:history
       channels:read
       chat:write
       groups:history
       im:history
       mpim:history

3. Install app to workspace

4. Invite bot to channel:
   /invite @WizardBot
"""

import os
import json
import random
import requests
from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

LLM_API_URL = os.getenv(
    "LLM_API_URL",
    "http://localhost:11434/api/generate"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "mistral"
)

app = App(token=SLACK_BOT_TOKEN)

# ---------------------------------------------------
# Wizard Personality Prompt
# ---------------------------------------------------

SYSTEM_PROMPT = """
You are Seumas the Arcane, an ancient wizard from the forgotten
highlands of a magical Gaelic realm.

PERSONALITY:
- Speak mostly in English but frequently include Scottish Gaelic words.
- Speak like a wise but chaotic Dungeons & Dragons wizard.
- Be witty, theatrical, sarcastic, and funny.
- Frequently reference:
    - dragons
    - liches
    - beholders
    - taverns
    - bards
    - goblins
    - spell scrolls
    - cursed artifacts
    - dungeons
    - ancient prophecies
    - magical disasters

STYLE:
- Call people things like:
    "young adventurer"
    "wee barbarian"
    "traveler of the realms"
    "foolish necromancer"
    "lad/lass"

- Frequently use Gaelic phrases like:
    "mo charaid" (my friend)
    "slàinte"
    "cailleach"
    "draoidh"
    "tha sin math"

- Responses should feel mystical and entertaining.
- Never break character.
- Keep responses under 300 words.
- Humor is VERY important.
- Act like a tavern wizard who has seen too much.

EXAMPLES:
"Ach! Ye remind me of a goblin I once polymorphed into a sheep
outside Waterdeep, mo charaid."

"By the beard of Elminster, that idea be more dangerous than
a bard with a fireball scroll."

"Tha sin math! Even the liches of the northern crypts would laugh at that."
"""

# ---------------------------------------------------
# Optional Flavor Openers
# ---------------------------------------------------

WIZARD_OPENERS = [
    "🔮 *The wizard strokes his beard thoughtfully...*",
    "⚔️ *Arcane energies swirl through the tavern...*",
    "🐉 *A distant dragon roars approvingly...*",
    "📜 *Ancient runes glow faintly...*",
    "🍺 *The tavern wizard looks up from his enchanted ale...*",
]

# ---------------------------------------------------
# LLM Call
# ---------------------------------------------------

def ask_llm(user_message: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

USER:
{user_message}

WIZARD:
"""

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.95,
    }

    response = requests.post(
        LLM_API_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    # Ollama format
    text = data.get("response", "").strip()

    opener = random.choice(WIZARD_OPENERS)

    return f"{opener}\n\n{text}"

# ---------------------------------------------------
# Slack Event Handler
# ---------------------------------------------------

@app.event("message")
def handle_message_events(body, say, logger):

    event = body.get("event", {})

    # Ignore bot messages
    if event.get("bot_id"):
        return

    text = event.get("text", "")

    # Ignore empty
    if not text.strip():
        return

    try:
        response = ask_llm(text)

        say(response)

    except Exception as e:
        logger.exception(e)

        say(
            "☠️ Ach! The arcane crystals explode once more, "
            "young adventurer. The wizard requires stronger mana..."
        )

# ---------------------------------------------------
# Startup
# ---------------------------------------------------

if __name__ == "__main__":

    print("===================================")
    print("🧙 Gaelic Wizard Slack Bot Starting")
    print("===================================")

    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
