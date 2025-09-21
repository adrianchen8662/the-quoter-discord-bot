# Discord Quote Bot

A Discord bot that allows users to quote messages to a designated channel using the `/quote` slash command or a right-click context menu.

## Features

- **Slash Command**: Use `/quote` when replying to a message to quote it
- **Context Menu**: Right-click on any message and select "Quote Message"
- **Rich Embeds**: Quotes are formatted with attractive embeds including timestamps and jump links
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Setup Instructions

### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token (you'll need this later)
5. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
   - Server Members Intent (optional)

### 2. Invite the Bot to Your Server

1. In the Discord Developer Portal, go to the "OAuth2" > "URL Generator" section
2. Select scopes: `bot` and `applications.commands`
3. Select bot permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
   - Embed Links
4. Use the generated URL to invite the bot to your server

### 3. Set Up the Environment

1. Clone or download this project
2. Copy `.env.example` to `.env`
3. Edit `.env` and replace `your_discord_bot_token_here` with your actual bot token

### 4. Deploy with Docker

#### Option A: Docker Compose (Recommended)

```bash
# Build and run the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

#### Option B: Docker directly

```bash
# Build the image
docker build -t discord-quote-bot .

# Run the container
docker run -d --name discord-quote-bot --env-file .env discord-quote-bot

# View logs
docker logs -f discord-quote-bot
```

### 5. Local Development

If you want to run locally without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

## Usage

### Method 1: Slash Command
1. Reply to any message you want to quote
2. Use the `/quote` slash command
3. The message will be quoted to the designated channel

### Method 2: Context Menu
1. Right-click on any message
2. Select "Quote Message" from the context menu
3. The message will be quoted to the designated channel

## Configuration

The quote channel ID is hardcoded in the bot (`707430563493052476`). To change it:

1. Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
2. Right-click on your desired channel and select "Copy ID"
3. Update the `QUOTE_CHANNEL_ID` variable in `bot.py`

## Bot Permissions Required

- Send Messages
- Use Slash Commands
- Read Message History
- Embed Links
- View Channel (for the quote channel)

## Troubleshooting

- **Bot not responding**: Check that the bot token is correct and the bot is online
- **Commands not appearing**: Make sure the bot has the "Use Slash Commands" permission
- **Can't quote to channel**: Ensure the bot has permission to view and send messages in the quote channel
- **"Referenced message not found"**: The original message may have been deleted

## File Structure

```
.
├── bot.py                 # Main bot code
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Environment variables template
└── README.md            # This file
```