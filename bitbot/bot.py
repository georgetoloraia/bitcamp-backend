import discord, os, re

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1173683645878386729))
    print(f"[bitcamper] logged in as {client.user.name}")

@tree.command(name="ping", description="Ping", guild=discord.Object(id=1173683645878386729))
async def ping_command(interaction):
    await interaction.response.send_message(
        f"**{int(client.latency*1000)}**ms"
    )

@tree.command(name="mkchannels", description="Create private channels for members with a specified role.", guild=discord.Object(id=1173683645878386729))
async def create_channels(interaction, role: discord.Role):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            f"Only administrators can use this command.", ephemeral=True
        )
        return
    
    guild = interaction.guild

    members_with_role = [member for member in guild.members if role in member.roles]
    
    creating, skipping = [], []
    for member in members_with_role:
        if re.sub(r"[^\w]", "", member.name.lower()) in [channel.name for channel in member.guild.channels]:
            skipping.append(member.name)
        else:
            creating.append(member.name)
    
    message = f"Creating channels for {', '.join(creating)}."
    
    if len(creating) <= 0:
        message = "Creating channels for nobody."
    if len(skipping) > 0:
        message += f" Skipping creating channels for {', '.join(skipping)}. (Channels already exist)"
        
    await interaction.response.send_message(
        message, ephemeral=True
    )

    for member in members_with_role:
        channel_name = re.sub(r"[^\w]", "", member.name.lower())
        
        if channel_name in [channel.name for channel in member.guild.channels]:
            continue
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True),
            client.user: discord.PermissionOverwrite(read_messages=True)
        }

        new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        
        await new_channel.send(f"გამარჯობა, {member.mention}! ეს არის თქვენი პირადი არხი.")
    
@client.event
async def on_member_join(member):
    channel_name = f"{member.name}"
    guild = member.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
        client.user: discord.PermissionOverwrite(read_messages=True)
    }

    new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
    
    await new_channel.send(f"გამარჯობა, {member.mention}! ეს არის თქვენი პირადი არხი.")

if __name__ == "__main__":
    client.run(os.environ["DISCORD_BOT_TOKEN"])
