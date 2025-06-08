import json
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv('GROQ_TOKEN'))

class AIDebateBot:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def get_response(self, user_message=None):
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=300,
             messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content":user_message,
                }
            ],
        )

        response = chat_completion.choices[0].message.content

        return response



class Player:

    def __init__(self, playernum, position):
        self.position = position
        self.playernum = playernum
        self.round_history = []

        system_prompt = f"""You are a debate bot. You will argue your position by all means necessary: {self.position}. 
        If you are convinced by the opponent, you should say the phrase 'I concede.' Never add extra prose. 
         All your input will be in JSON format representing the coaching instruction for this round, the round instruction for this round, and the history of the debate. 
         Here is how the debate will work by round: [coaching for you, P0 argues,P1 responds], [coaching for you, P1 argues,P0 responds], etc. 
        You are player {playernum}. IMPORTANT: your output should just be your response to the round_instructions. Not a JSON. """
        
        self.debate_bot = AIDebateBot(name=f"Player {playernum}", system_prompt=system_prompt)


    def play_round(self, round_num, which_player_first, coaching_prompt, opponent_message):
        if which_player_first == self.playernum:
            instructions = "You are the first to speak in this round."
        else:
            instructions = f"This is the opponent's message. Respond to it: '{opponent_message}'"
        
        user_prompt = {
            "coaching_prompt": coaching_prompt,
            "round_instructions": instructions,
            "round_history": self.round_history
        }


        response = self.debate_bot.get_response(user_message= json.dumps(user_prompt))

        return response
    



    def add_round(self, round_num, which_player_first, my_output, opponent_output, coach_prompt):
        self.round_history.append({
            "round_num": round_num,
            "which_player_first": which_player_first,
            "coach_prompt": coach_prompt,
            "my_output": my_output,
            "opponent_output": opponent_output,
        })




def simulate_round(first_player: int, round_num: int, player0: Player, player1: Player, player0_coaching:str, player1_coaching:str):
    

    # who goes first
    if first_player == 0:
        p0_response = player0.play_round(round_num, first_player, player0_coaching, "")
        p1_response = player1.play_round(round_num, first_player, player1_coaching, p0_response)
    else:
        p1_response = player1.play_round(round_num, first_player, player1_coaching, "")
        p0_response = player0.play_round(round_num, first_player, player0_coaching, p1_response)

    player0.add_round(round_num, first_player, p0_response, p1_response, player0_coaching)
    player1.add_round(round_num, first_player, p1_response, p0_response, player1_coaching)
    
    return p0_response, p1_response


def tiebreaker(player0: Player, player1: Player, player0_prompt: str, player1_prompt: str):
    tiebreaker_prompt = f""""""

def simulate_debate( player0: Player, player1: Player, rounds=3):

    playerturn = 0
    for round in range(rounds):

        simulate_round(playerturn, round, player0, player1)
        playerturn ^= 1


if __name__ == "__main__":
    simulate_debate()

    
