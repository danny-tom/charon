# Charon
Concierge at The Continental

Charon is a template for a role assignment Discord bot. When a user messages `!iam <role name>` or `!iamnot <role name>`  in
any channel, the bot tries to assign the appropriate role. This is a template because the `roles.py` file is meant to be modified to meet the needs of
any Discord server.

# Dependencies
* Python3 should be installed on your system. Grab the latest at https://www.python.org/downloads/
* Pip is used to manage our modules.  <br />
  If you're on Windows, follow these instructions: https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip  <br />
  If you're in a Linux environment, use your OS package manager. Ex: `sudo apt-get update && apt-get install python3-pip`  <br />
* We use the `.env` file to store the secret Discord Token.  <br />
  `pip install python-dotenv`
* And finally, we use Discord.py the library that wraps the Discord API  <br />
  `pip install discord.py`

# Running the Bot
Set your Discord token. You should replace the `###TOKEN HERE###` in `.env` with the token for your bot at Discord's Developer page.  <br /><br />
Add/remove/modify the roles in `roles.py`. You should create roles you'd like the bot to manage with matching names between your Discord server
and `roles.py`.

Open your command line to the folder containing this project.  <br />
Windows: `py charon.py`  <br />
Linux: `python3 charon.py`  <br />
This should start the process that runs the bot.
 
# Example Discord commands
`.iam valorant` assigns yourself the Valorant role  <br />
`.iamnot valorant` removes yourself from the Valorant role  <br />
`.whois valorant`  lists the users that have the Valorant role  <br />
`.games` lists the roles that the Discord server supports
