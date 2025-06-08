import os
from groq import Groq


PROMPT1 = "You are a bot and your goal is to argue your position. If you are convinced by the opponent, you should say the phrase 'I concede.'"
PROMPT2 = "You are a bot and your goal is to argue your position. If you are convinced by the opponent, you should say the phrase 'I concede.'"

MESSAGE_HISTORY = []

def get_position():
    return "The sky is green.", "The sky is purple."


POSITION1, POSITION2 = get_position()
client = Groq(api_key="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")

class AIDebateBot:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def get_response(self, opponent_message=None):
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=800
        )

        response = chat_completion.choices[0].message.content
        return response

ALICE_PROMPT = "You are a logical and analytical debate bot. Your responses should be based on facts, evidence, and sound reasoning. You should concede only when presented with irrefutable evidence against your position. Keep your responses concise and focused on the logical aspects of the argument."
BOB_PROMPT = "You are an emotionally intelligent debate bot. Your responses should appeal to human emotions and values while maintaining a persuasive tone. You should concede when you genuinely feel the opponent's emotional argument is more compelling. Keep your responses engaging and relatable."

alice = AIDebateBot(
    name="Alice",
    system_prompt=ALICE_PROMPT
)

bob = AIDebateBot(
    name="Bob",
    system_prompt=BOB_PROMPT
)

# Example debate positions
POSITION1 = "The sky is green."
POSITION2 = "The sky is purple."

def simulate_debate(rounds=3):
    for round in range(rounds):
        print(f"\nRound {round + 1}:")
        
        alice_response = alice.get_response(POSITION1)
        print(f"Alice: {alice_response}")
        
        bob_response = bob.get_response(alice_response)
        print(f"Emotional Bot: {emotional_response}")
        
        # Check for concession
        if "I concede" in logical_response.lower() or "I concede" in emotional_response.lower():
            print("\nDebate ended due to concession.")
            break

if __name__ == "__main__":
    simulate_debate()

for round in range(1):
    
