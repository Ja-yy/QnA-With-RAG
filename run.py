
from src.agents import MainAgent
from src.utils import parse_chunked_response

# def init():
#     bot = Bot(conversation_id="test")
#     for conv in bot.get_conv_hist():
#         print(conv)


# init()

while True:
    bot = MainAgent()
    user_input = input("User Input:")
    for i, token in enumerate(bot.ask(user_input)):
        # Print as a stream
        print(parse_chunked_response(token), end="", flush=True)
