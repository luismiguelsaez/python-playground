import logging
import httpx
import asyncio
from time import sleep
from os.path import exists
from os import environ
from sys import stdout


bot_token = environ.get("BOT_TOKEN")

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(stream=stdout)
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


async def get_updates(token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.telegram.org/bot{token}/getUpdates")
    return response.json()


async def send_message(token: str, chat_id: int, text: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": text, "parse_mode": "MarkdownV2"},
        )
    return response.json()


async def send_photo(token: str, chat_id: int, file: str) -> tuple[int, str]:
    if not exists(file):
        return 1, "File not found"
    async with httpx.AsyncClient() as client:
        with open(file, "rb") as f:
            files = {"photo": ("pikachu.jpeg", f, "image/jpeg")}
            response = await client.post(
                url=f"https://api.telegram.org/bot{token}/sendPhoto",
                files=files,
                data={"caption": "Pikachu", "chat_id": chat_id},
            )

    return response.status_code, response.text


async def get_bot_ip() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.ipify.org")
    return response.text


async def main():
    update_id = 0
    while True:
        logger.debug("Checking for updates")
        updates = await get_updates(token=bot_token)
        for update in updates["result"]:
            if update["update_id"] > update_id:
                update_id = update["update_id"]
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message["text"]
                if text == "/ip":
                    logger.info("Handling /ip command")
                    res = await send_message(
                        token=bot_token, chat_id=chat_id, text=await get_bot_ip()
                    )
                    logger.debug(f"IP result: {res}")
                elif text == "/photo":
                    logger.info("Handling /photo command")
                    code, res = await send_photo(
                        token=bot_token,
                        chat_id=chat_id,
                        file="./pikachu.jpeg",
                    )
                    logger.debug(f"Photo result: {code} - {res}")

        sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
