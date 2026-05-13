#slack-bot-wizardo

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
LLM_API_URL=http://localhost:11434/api/generate
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
