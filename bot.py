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
    view.timeout = 30.0
    await ctx.send("Click the button to accept the debate challenge:", view=view)

    # Wait for someone to click the button
    try:
        await view.wait()
    except asyncio.TimeoutError:
        await ctx.send("No one accepted the debate challenge. Please try again.")
        return None

    if not view.value:
        await ctx.send("No one accepted the debate challenge. Please try again.")
        return None

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
        # Get instructions from first player
        if FIRST_PLAYER == 0:
            try:
                await ctx.send(f"<@{alice_id}>, please give instructions to Alice (30 seconds):")
                # Create tasks for both the timeout warning and waiting for message
                warning_task = asyncio.create_task(asyncio.sleep(25))  # 25 seconds for warning
                message_task = asyncio.create_task(bot.wait_for('message', check=check_alice))
                
                # Wait for either task to complete
                done, pending = await asyncio.wait(
                    [warning_task, message_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # If warning completed first, send warning and continue waiting
                if warning_task in done:
                    await ctx.send(f"<@{alice_id}>, 5 seconds remaining!")
                    alice_instructions = await asyncio.wait_for(message_task, timeout=5.0)
                else:
                    alice_instructions = message_task.result()
                    
                # Cancel any pending tasks
                for task in pending:
                    task.cancel()
                    
            except asyncio.TimeoutError:
                await ctx.send("Time's up! One of the coaches took too long to respond.")
                return

            try:
                await ctx.send(f"<@{bob_id}>, please give instructions to Bob (30 seconds):")
                # Create tasks for both the timeout warning and waiting for message
                warning_task = asyncio.create_task(asyncio.sleep(25))  # 25 seconds for warning
                message_task = asyncio.create_task(bot.wait_for('message', check=check_bob))
                
                # Wait for either task to complete
                done, pending = await asyncio.wait(
                    [warning_task, message_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # If warning completed first, send warning and continue waiting
                if warning_task in done:
                    await ctx.send(f"<@{bob_id}>, 5 seconds remaining!")
                    bob_instructions = await asyncio.wait_for(message_task, timeout=5.0)
                else:
                    bob_instructions = message_task.result()
                    
                # Cancel any pending tasks
                for task in pending:
                    task.cancel()
                    
            except asyncio.TimeoutError:
                await ctx.send("Time's up! One of the coaches took too long to respond.")
                return
        else:
            try:
                await ctx.send(f"<@{bob_id}>, please give instructions to Bob (30 seconds):")
                # Create tasks for both the timeout warning and waiting for message
                warning_task = asyncio.create_task(asyncio.sleep(25))  # 25 seconds for warning
                message_task = asyncio.create_task(bot.wait_for('message', check=check_bob))
                
                # Wait for either task to complete
                done, pending = await asyncio.wait(
                    [warning_task, message_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # If warning completed first, send warning and continue waiting
                if warning_task in done:
                    await ctx.send(f"<@{bob_id}>, 5 seconds remaining!")
                    bob_instructions = await asyncio.wait_for(message_task, timeout=5.0)
                else:
                    bob_instructions = message_task.result()
                    
                # Cancel any pending tasks
                for task in pending:
                    task.cancel()
                    
            except asyncio.TimeoutError:
                await ctx.send("Time's up! One of the coaches took too long to respond.")
                return

            try:
                await ctx.send(f"<@{alice_id}>, please give instructions to Alice (30 seconds):")
                # Create tasks for both the timeout warning and waiting for message
                warning_task = asyncio.create_task(asyncio.sleep(25))  # 25 seconds for warning
                message_task = asyncio.create_task(bot.wait_for('message', check=check_alice))
                
                # Wait for either task to complete
                done, pending = await asyncio.wait(
                    [warning_task, message_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # If warning completed first, send warning and continue waiting
                if warning_task in done:
                    await ctx.send(f"<@{alice_id}>, 5 seconds remaining!")
                    alice_instructions = await asyncio.wait_for(message_task, timeout=5.0)
                else:
                    alice_instructions = message_task.result()
                    
                # Cancel any pending tasks
                for task in pending:
                    task.cancel()
                    
            except asyncio.TimeoutError:
                await ctx.send("Time's up! One of the coaches took too long to respond.")
                return
        
        
        embed = discord.Embed(
            title=f"Round {round}",
            description="Debate phase! Alice and Bob will respond to each other.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        

        
        # Get responses from Alice and Bob
        alice_response, bob_response = simulate_round(FIRST_PLAYER, round - 1, alice_player_obj, bob_player_obj, alice_instructions.content, bob_instructions.content)
        
        if FIRST_PLAYER == 0:
            typing_embed = discord.Embed(description="Alice is typing...", color=discord.Color.blue())
            typing_msg = await ctx.send(embed=typing_embed)
            await asyncio.sleep(2)
            await typing_msg.delete()
            await ctx.send(f"Alice: {alice_response}")
            
            typing_embed = discord.Embed(description="Bob is typing...", color=discord.Color.blue()) 
            typing_msg = await ctx.send(embed=typing_embed)
            await asyncio.sleep(2)
            await typing_msg.delete()
            await ctx.send(f"Bob: {bob_response}")
        else:
            typing_embed = discord.Embed(description="Bob is typing...", color=discord.Color.blue())
            typing_msg = await ctx.send(embed=typing_embed)
            await asyncio.sleep(2) 
            await typing_msg.delete()
            await ctx.send(f"Bob: {bob_response}")
            
            typing_embed = discord.Embed(description="Alice is typing...", color=discord.Color.blue())
            typing_msg = await ctx.send(embed=typing_embed)
            await asyncio.sleep(2)
            await typing_msg.delete()
            await ctx.send(f"Alice: {alice_response}")
        await asyncio.sleep(2)

        FIRST_PLAYER ^= 1
        
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
            