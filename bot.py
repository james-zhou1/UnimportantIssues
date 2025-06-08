import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from terminal import AIDebateBot, Player, simulate_round

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Load environment variables
load_dotenv()

# Get the token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

TOPICS = {
    "the color of the sky": ("The color of the sky is green", "The color of the sky is purple")
}



async def send_challenge(ctx):
    # Create a button view for accepting the debate challenge
    class AcceptDebateButton(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @discord.ui.button(label='Accept Debate Challenge', style=discord.ButtonStyle.green)
        async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.value = interaction.user
            self.stop()

    # Create and send the button
    view = AcceptDebateButton()
    await ctx.send("Click the button to accept the debate challenge:", view=view)

    # Wait for someone to click the button
    timeout = 30.0
    try:
        await view.wait()
    except asyncio.TimeoutError:
        await ctx.send("No one accepted the debate challenge. Please try again.")
        return

    if view.value:
        await ctx.send(f"{view.value.mention} has accepted the challenge!")

    return view.value.id, ctx.author.id

@bot.command(name='debate')
async def debate(ctx):
    alice_id, bob_id = await send_challenge(ctx)


    import random
    
    # Randomly select a topic and its stances
    topic = random.choice(list(TOPICS.keys()))
    stances = TOPICS[topic]
    
    # Randomly assign stances to Alice and Bob
    if random.random() < 0.5:
        alice_stance, bob_stance = stances
    else:
        bob_stance, alice_stance = stances

    alice_player_obj = Player(0, alice_stance)
    bob_player_obj = Player(1, bob_stance)

    FIRST_PLAYER = random.randint(0, 1)

    NUM_ROUNDS = 3

    for round in range(1, NUM_ROUNDS + 1):
        # Send round 1 message as an embed
        embed = discord.Embed(
            title=f"Round {round}",
            description="Coaching phase! Both coaches should give instructions to their respective bots.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        # Get instructions from coaches


        def check_alice(m):
            return m.author.id == alice_id and m.channel == ctx.channel
        def check_bob(m):
            return m.author.id == bob_id and m.channel == ctx.channel
        try:
            await ctx.send(f"<@{alice_id}>, please give instructions to Alice (30 seconds):")
            alice_instructions = await bot.wait_for('message', check=check_alice, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Time's up! One of the coaches took too long to respond.")


        try:
            await ctx.send(f"<@{bob_id}>, please give instructions to Bob (30 seconds):")
            bob_instructions = await bot.wait_for('message', check=check_bob, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Time's up! One of the coaches took too long to respond.")
        
        
        embed = discord.Embed(
            title=f"Round {round + 1}",
            description="Debate phase! Alice and Bob will respond to each other.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        

        FIRST_PLAYER ^= 1
        # Get responses from Alice and Bob
        alice_response, bob_response = simulate_round(FIRST_PLAYER, round - 1, alice_player_obj, bob_player_obj, alice_instructions.content, bob_instructions.content)
        
        await asyncio.sleep(5)
        await ctx.send(f"Alice: {alice_response}")
        await asyncio.sleep(5)
        await ctx.send(f"Bob: {bob_response}")
        await asyncio.sleep(5)

        # Check for concessions
        if "i concede" in alice_response.lower() and "i concede" in bob_response.lower():
            embed = discord.Embed(
                title="Debate Ended in Draw",
                description="Both players have conceded! The debate ends in a draw.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
        elif "i concede" in alice_response.lower():
            embed = discord.Embed(
                title="Bob Wins!",
                description="Alice has conceded! Bob wins the debate!",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
        elif "I concede" in bob_response.lower():
            embed = discord.Embed(
                title="Alice Wins!",
                description="Bob has conceded! Alice wins the debate!",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return

# Start the bot
bot.run(TOKEN)
            