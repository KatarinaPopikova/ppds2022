""""Author: Katarína Stasová
    License: MIT
    The asynchronous program to find the capital city of a country.
"""
import aiohttp
import asyncio
import time


async def get_capital_city(country):
    """ The function is labeled `async`, so this is a native coroutine. It can be interrupted for lines marked with the
    await command. It uses async frameworks for creating HTTP requests asynchronously, so it performs a context switch
    back to the event loop. Code creates an aiohttp session context manager, then uses the session to get the text
    retrieved from the URL asynchronously.
    Coroutine select the capital city of country and find out the elapsed time.

    :param country: country to find data
    """
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
    """ This coroutine call another coroutine to get the capital cities of the countries from the list.
     The coroutine objects are created and run with the asyncio.gather () function. This feature schedules them and then
     runs them competitively.
    """
    start_time = time.perf_counter()

    await asyncio.gather(*[get_capital_city(country) for country in
                           ['Slovakia', 'Germany', 'China', 'India', 'Zimbabwe', 'Guinea', 'Nauru', 'Andorra', 'Tonga',
                            'Kiribati', 'Norway']])

    total_time = time.perf_counter() - start_time
    print(f"\nTotal time: {total_time:.1f}")


if __name__ == "__main__":
    """ This creates an event loop. This loop will run main()"""
    # Solve "RuntimeError: Event loop is closed" when ProactorEventLoop is used
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
