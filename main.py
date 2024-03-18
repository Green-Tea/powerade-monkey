from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty because intents were not enabled properly')
        return
    
    try:
        response: str = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(f'Error: {e}')
        
@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = message.author.name
    user_message: str = message.content
    channel: str = message.channel.name

    if username == '_seaweed' and channel == 'general':
        await send_message(message, user_message)

    return

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()