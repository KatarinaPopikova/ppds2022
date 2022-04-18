""""Author: Katarína Stasová
    License: MIT
    The asynchronous program to find the capital city of a country.
"""
import aiohttp
import asyncio
import time


async def get_capital_city(country):
    url = 'https://restcountries.com/v3.1/name/' + country
    print(f"Get capital city of {country} from URL: {url}")
    time_start = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            request = await resp.json()
            capital = request[0]["capital"][0]

    elapsed = time.perf_counter() - time_start
    print(f"The capital city of {country} is {capital}, elapsed time: {elapsed:.1f}")


async def main():
    start_time = time.perf_counter()

    await asyncio.gather(*[get_capital_city(country) for country in
                           ['Slovakia', 'Germany', 'China', 'India', 'Zimbabwe', 'Guinea', 'Nauru', 'Andorra', 'Tonga',
                            'Kiribati', 'Norway']])

    total_time = time.perf_counter() - start_time
    print(f"\nTotal time: {total_time:.1f}")


if __name__ == "__main__":
    # Solve "RuntimeError: Event loop is closed" when ProactorEventLoop is used
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
