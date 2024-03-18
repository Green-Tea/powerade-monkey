import logging
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from datetime import datetime, timedelta, timezone

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        logger.warning('Message was empty because intents were not enabled properly')
        return
    
    try:
        response: str = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        logger.error(f'Error: {e}')
        
@client.event
async def on_ready() -> None:
    logger.info(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = message.author.name
    user_message: str = message.content
    channel: str = message.channel.name

    if username == '_seaweed' and (channel == 'general' or channel == 'cunt-convos'):
        now_utc = datetime.now(timezone.utc)
        utc_plus_7 = now_utc + timedelta(hours=7)
        timestamp = utc_plus_7.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'Time of awakening: {timestamp}')
        await send_message(message, user_message)

    return

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
