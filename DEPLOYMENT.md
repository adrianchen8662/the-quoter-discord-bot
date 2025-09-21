# Deploy Discord Quote Bot to Portainer

There are two main ways to deploy this bot to Portainer: using Docker Compose (recommended) or creating a custom container.

## Method 1: Docker Compose (Recommended)

### Step 1: Prepare Your Files
1. Create a folder on your Portainer host with all the bot files:
   ```
   discord-quote-bot/
   ├── bot.py
   ├── requirements.txt
   ├── Dockerfile
   ├── docker-compose.yml
   └── .env
   ```

2. Create your `.env` file:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

### Step 2: Deploy via Portainer
1. **Log into Portainer**
2. **Go to "Stacks"** in the left sidebar
3. **Click "Add Stack"**
4. **Choose deployment method:**

#### Option A: Upload docker-compose.yml
1. Name your stack: `discord-quote-bot`
2. Upload your `docker-compose.yml` file
3. In **Environment Variables**, add:
   - Name: `DISCORD_TOKEN`
   - Value: `your_actual_discord_token`
4. Click **Deploy the stack**

#### Option B: Git Repository (if your code is on GitHub)
1. Name your stack: `discord-quote-bot`
2. Repository URL: `https://github.com/yourusername/discord-quote-bot`
3. Repository reference: `refs/heads/main`
4. Compose path: `docker-compose.yml`
5. In **Environment Variables**, add your Discord token
6. Click **Deploy the stack**

#### Option C: Web Editor
1. Name your stack: `discord-quote-bot`
2. Copy and paste your `docker-compose.yml` content
3. Add environment variables
4. Click **Deploy the stack**

### Step 3: Upload Files (if using upload method)
If Portainer needs the source files:
1. Go to **Volumes** → Create volume named `discord-bot-source`
2. Browse volume and upload your files (bot.py, requirements.txt, etc.)

---

## Method 2: Custom Container

### Step 1: Build and Push to Registry (Optional)
If you want to use a registry instead of building locally:

```bash
# Build the image
docker build -t your-registry.com/discord-quote-bot:latest .

# Push to registry
docker push your-registry.com/discord-quote-bot:latest
```

### Step 2: Create Container in Portainer
1. **Go to "Containers"**
2. **Click "Add Container"**
3. **Configure the container:**
   - **Name**: `discord-quote-bot`
   - **Image**: `your-registry.com/discord-quote-bot:latest` (or build from source)
   - **Environment Variables**:
     - `DISCORD_TOKEN`: `your_discord_bot_token`
   - **Restart Policy**: `Unless Stopped`
   - **Volumes** (optional):
     - Container: `/app/logs`
     - Host: `/var/lib/docker/volumes/discord-bot-logs`

4. **Click "Deploy the container"**

---

## Method 3: Build from Source in Portainer

### Step 1: Upload Source Code
1. **Create a volume** for your source code:
   - Go to **Volumes** → **Add Volume**
   - Name: `discord-bot-source`
   
2. **Upload your files**:
   - Browse the volume
   - Upload: `bot.py`, `requirements.txt`, `Dockerfile`, etc.

### Step 2: Create Build Stack
Create a stack with this compose file:

```yaml
version: '3.8'

services:
  discord-bot:
    build:
      context: /var/lib/docker/volumes/discord-bot-source/_data
      dockerfile: Dockerfile
    container_name: discord-quote-bot
    restart: unless-stopped
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
    volumes:
      - discord-bot-logs:/app/logs

volumes:
  discord-bot-logs:
```

---

## Monitoring and Management

### View Logs
1. Go to **Containers** or **Stacks**
2. Click on your container/stack
3. Click **Logs** to see output
4. Look for: "Successfully synced X command(s)"

### Update the Bot
1. **For Stacks**: 
   - Update your source code
   - Go to Stacks → Your Stack → **Editor**
   - Click **Update the Stack**

2. **For Containers**:
   - Stop the container
   - Remove it
   - Recreate with new image

### Environment Variables in Portainer
- `DISCORD_TOKEN`: Your Discord bot token
- `PYTHONUNBUFFERED`: `1` (for better logging)
- `TZ`: `America/New_York` (optional, for correct timestamps)

---

## Troubleshooting

### Bot Not Starting
1. Check logs for errors
2. Verify Discord token is correct
3. Ensure all files are uploaded correctly

### Commands Not Working
1. Check logs for "Successfully synced" messages
2. Verify bot has proper Discord permissions
3. Try the `!test` command first

### Resource Issues
The bot uses minimal resources:
- **Memory**: ~50-100MB
- **CPU**: Very low
- **Network**: Minimal

### File Permissions
If you get permission errors:
```bash
# On the Portainer host:
sudo chown -R 1000:1000 /var/lib/docker/volumes/discord-bot-source/_data
```

---

## Security Best Practices

1. **Never commit your Discord token** to version control
2. **Use environment variables** for sensitive data
3. **Limit container resources** if needed
4. **Use non-root user** (already configured in Dockerfile)
5. **Keep the bot token secure** in Portainer's environment variables

---

## Quick Start Summary

1. **Upload files** to Portainer host or create a volume
2. **Go to Stacks** → **Add Stack**
3. **Upload docker-compose.yml**
4. **Add DISCORD_TOKEN** environment variable
5. **Deploy stack**
6. **Check logs** for successful startup
7. **Test with `/ping`** in Discord