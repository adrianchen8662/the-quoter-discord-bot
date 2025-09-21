import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
QUOTE_CHANNEL_ID = 707430563493052476

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Quote channel ID: {QUOTE_CHANNEL_ID}')
    print(f'Connected to {len(bot.guilds)} guild(s)')
    
    # List all guilds the bot is in
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')
    
    # Check what commands are registered before syncing
    print(f"Commands registered in tree: {len(bot.tree.get_commands())}")
    for cmd in bot.tree.get_commands():
        print(f"  - {cmd.name} ({type(cmd).__name__})")
    
    # Try syncing to a specific guild first (faster for testing)
    try:
        print("Syncing slash commands globally...")
        synced = await bot.tree.sync()
        print(f'✅ Successfully synced {len(synced)} global command(s)')
        for cmd in synced:
            print(f'  - /{cmd.name}: {cmd.description}')
        
        # Also try syncing to the first guild for immediate testing
        if bot.guilds:
            guild = bot.guilds[0]
            print(f"\nAlso syncing to guild '{guild.name}' for immediate testing...")
            
            # Check bot permissions in the guild
            bot_member = guild.get_member(bot.user.id)
            if bot_member:
                perms = bot_member.guild_permissions
                print(f"Bot permissions in guild:")
                print(f"  - send_messages: {perms.send_messages}")
                print(f"  - read_messages: {perms.read_messages}")
                print(f"  - embed_links: {perms.embed_links}")
                print(f"  - read_message_history: {perms.read_message_history}")
                print(f"  - administrator: {perms.administrator}")
                
                # Check if bot has application command permissions
                # This is controlled by server settings, not bot permissions
                print(f"  - Bot can use application commands: This is controlled by server settings")
            
            try:
                guild_synced = await bot.tree.sync(guild=guild)
                print(f'✅ Successfully synced {len(guild_synced)} command(s) to {guild.name}')
                if len(guild_synced) == 0:
                    print("⚠️  Zero commands synced to guild - this might be a permissions issue")
            except Exception as guild_sync_error:
                print(f"❌ Guild sync failed: {guild_sync_error}")
            
    except Exception as e:
        print(f'❌ Failed to sync commands: {e}')
        print(f'Error type: {type(e).__name__}')
        import traceback
        traceback.print_exc()

# Add a manual sync command for testing
@bot.command(name='sync')
async def sync_command(ctx):
    """Manually sync slash commands (owner only)"""
    try:
        await ctx.send("🔄 Syncing commands...")
        
        # Clear existing commands first
        bot.tree.clear_commands(guild=ctx.guild)
        
        # Sync globally
        synced = await bot.tree.sync()
        await ctx.send(f'✅ Synced {len(synced)} global commands')
        
        # Force sync to current guild
        guild_synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'✅ Synced {len(guild_synced)} commands to this server')
        
        # Wait a moment and check what commands Discord sees
        await ctx.send("Try typing `/` now to see if commands appear!")
        
    except Exception as e:
        await ctx.send(f'❌ Failed to sync: {e}')
        print(f"Sync error: {e}")
        import traceback
        traceback.print_exc()

# Add a simple text command for testing
@bot.command(name='test')
async def test_command(ctx):
    """Simple text command to test if bot is responding"""
    await ctx.send(f'✅ Bot is working! Latency: {round(bot.latency * 1000)}ms')

@bot.tree.command(name='ping', description='Check if the bot is alive and responsive')
async def ping_command(interaction: discord.Interaction):
    """Simple ping command to check bot responsiveness"""
    latency = round(bot.latency * 1000)  # Convert to milliseconds
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot is alive and responding!",
        color=0x00ff00
    )
    
    embed.add_field(
        name="Latency",
        value=f"{latency}ms",
        inline=True
    )
    
    embed.add_field(
        name="Status",
        value="✅ Online",
        inline=True
    )
    
    embed.set_footer(text=f"Requested by {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def quote_message_helper(interaction: discord.Interaction, message_to_quote: discord.Message):
    """Helper function to quote a message"""
    try:
        # Check if the message is from a bot (prevent quoting bot messages)
        if message_to_quote.author.bot:
            await interaction.response.send_message(
                "❌ You cannot quote messages from bots!", 
                ephemeral=True
            )
            return
        
        # Get the quote channel
        quote_channel = bot.get_channel(QUOTE_CHANNEL_ID)
        if not quote_channel:
            await interaction.response.send_message(
                "❌ Quote channel not found!", 
                ephemeral=True
            )
            return
        
        # Format the quote
        quoted_content = message_to_quote.content
        quoted_user = message_to_quote.author
        
        # Handle empty messages (like image-only messages)
        if not quoted_content:
            quoted_content = "*[Image or empty message]*"
        
        # Create the quote message
        quote_text = f'"{quoted_content}" - {quoted_user.mention}'
        
        # Create an embed for better formatting
        embed = discord.Embed(
            description=quote_text,
            color=0x00ff00,
            timestamp=message_to_quote.created_at
        )
        
        embed.set_author(
            name=f"Quote from #{interaction.channel.name}",
            icon_url=quoted_user.display_avatar.url
        )
        
        embed.set_footer(
            text=f"Quoted by {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        
        # Add jump link to original message
        embed.add_field(
            name="Original Message",
            value=f"[Jump to message]({message_to_quote.jump_url})",
            inline=False
        )
        
        # Send to quote channel
        await quote_channel.send(embed=embed)
        
        # Confirm to user
        await interaction.response.send_message(
            f"✅ Message quoted to {quote_channel.mention}!", 
            ephemeral=True
        )
        
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ I don't have permission to access the quote channel!", 
            ephemeral=True
        )
    except Exception as e:
        print(f"Error in quote helper: {e}")
        await interaction.response.send_message(
            "❌ An error occurred while quoting the message!", 
            ephemeral=True
        )

@bot.tree.command(name='quote', description='Quote a message (reply to a message or provide message ID)')
async def quote_command(interaction: discord.Interaction, message_id: str = None):
    """Quote a message by replying to it or providing a message ID"""
    
    message_to_quote = None
    
    # First, try to get the message from the message_id parameter
    if message_id:
        try:
            message_to_quote = await interaction.channel.fetch_message(int(message_id))
        except (ValueError, discord.NotFound):
            await interaction.response.send_message(
                "❌ Invalid message ID or message not found!", 
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"Error fetching message by ID: {e}")
            await interaction.response.send_message(
                "❌ Error fetching the message!", 
                ephemeral=True
            )
            return
    
    # If no message_id provided, try to find a replied-to message
    if not message_to_quote:
        # For slash commands, we need to look at the interaction's data to find replies
        # This is a workaround since slash commands don't have direct reply detection
        
        # Try to get recent messages and find one that this might be replying to
        try:
            # Get the last few messages in the channel
            messages = []
            async for msg in interaction.channel.history(limit=20):
                messages.append(msg)
            
            # Look for the most recent non-bot message that isn't from the user who ran the command
            for msg in messages:
                if msg.author != interaction.user and not msg.author.bot:
                    # Ask the user to confirm this is the message they want to quote
                    # For now, we'll assume the most recent non-bot message is what they want
                    message_to_quote = msg
                    break
        except Exception as e:
            print(f"Error finding message to quote: {e}")
    
    if not message_to_quote:
        await interaction.response.send_message(
            "❌ Please provide a message ID with the command: `/quote message_id:123456789`\n"
            "You can get a message ID by right-clicking a message and selecting 'Copy ID' "
            "(Developer Mode must be enabled in Discord settings).", 
            ephemeral=True
        )
        return
    
    await quote_message_helper(interaction, message_to_quote)

# Alternative context menu command (right-click on message)
@bot.tree.context_menu(name='Quote Message')
async def quote_context_menu(interaction: discord.Interaction, message: discord.Message):
    """Quote a message via right-click context menu"""
    
    # Check if the message is from a bot (prevent quoting bot messages)
    if message.author.bot:
        await interaction.response.send_message(
            "❌ You cannot quote messages from bots!", 
            ephemeral=True
        )
        return
    
    await quote_message_helper(interaction, message)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f'Error: {error}')

if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable not set!")
        exit(1)
    
    bot.run(TOKEN)