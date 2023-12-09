import asyncio

async def print_delay(msg: str, delay: int)->None:
    print(msg)
    await asyncio.sleep(delay)
    return

async def main():
    asyncio.gather(
        print_delay("Instance 1 - 1 sec", 1),
    )

if __name__ == '__main__':
    asyncio.run(main())
