#   TODO: This can be in the format of a dictionary that has a bunch of prompts. The answers have to be yes or no.

POSITION1 = "The sky is green."
POSITION2 = "The sky is purple."

#   TODO: There are a bunch of positions listed and you choose one. But blue cannot be an option.

PROMPT1 = "You are a bot and your goal is to argue your position. If you are convinced by the opponent, you should say the phrase 'I concede.'"
PROMPT2 = "You are a bot and your goal is to argue your position. If you are convinced by the opponent, you should say the phrase 'I concede.'"

MESSAGE_HISTORY = []

def get_position()
    return "The sky is green.", "The sky is purple."


POSITION1, POSITION2 = get_position()

for round in range(12):
