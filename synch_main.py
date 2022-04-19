""""Author: Katarína Stasová
    License: MIT
    The synchronous program to find the capital city of a country.
"""
import requests
import time


def get_capital_city(country):
    """ Synchronously retrieve data from API about countries.
    Select the capital city and find out the elapsed time.

    :param country: country to find data
    """
    url = 'https://restcountries.com/v3.1/name/' + country
    print(f"Get capital city of {country} from URL: {url}")
    time_start = time.perf_counter()
    request = requests.get(url).json()[0]
    capital = request["capital"][0]
    elapsed = time.perf_counter() - time_start
    print(f"The capital city of {country} is {capital}, elapsed time: {elapsed:.1f}")


def main():
    """
    The main function that calls another function to find the capitals of the countries in the list.
    It also measures the total duration of the finding capitals for all countries.
    """
    start_time = time.perf_counter()

    [get_capital_city(country) for country in
     ['Slovakia', 'Germany', 'China', 'India', 'Zimbabwe', 'Guinea', 'Nauru', 'Andorra', 'Tonga', 'Kiribati', 'Norway']]

    total_time = time.perf_counter() - start_time
    print(f"\nTotal time: {total_time:.1f}")


if __name__ == "__main__":
    main()
