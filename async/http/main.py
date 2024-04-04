import httpx
import asyncio
import time

async def get_url(url: str)->tuple:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return ( url, response.status_code, response.elapsed )

async def main():
    urls = [
        "https://app.stage.lokalise.cloud",
        "https://app.lokalise.com",
        "https://www.google.es",
        "https://duckduckgo.com",
        "https://as.com",
        "https://www.youtube.com"
    ]
    async with asyncio.TaskGroup() as tg:
        res = [tg.create_task(get_url(u)) for u in urls]
    return [r.result() for r in res]

if __name__ == "__main__":
    ini = time.perf_counter()
    res = asyncio.run(main())
    end = time.perf_counter()
    print(f"Elapsed time: {end - ini}")

    print(res)
