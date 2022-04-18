import requests
import time


def get_capital_city(country):
    url = 'https://restcountries.com/v3.1/name/' + country
    print(f"Get capital city of {country} from URL: {url}")
    time_start = time.perf_counter()
    request = requests.get(url).json()[0]
    capital = request["capital"][0]
    elapsed = time.perf_counter() - time_start
    print(f"The capital city of {country} is {capital}, elapsed time: {elapsed:.1f}")


def main():
    start_time = time.perf_counter()

    [get_capital_city(country) for country in
     ['Slovakia', 'Germany', 'China', 'India', 'Zimbabwe', 'Guinea', 'Nauru', 'Andorra', 'Tonga', 'Kiribati', 'Norway']]

    total_time = time.perf_counter() - start_time
    print(f"\nTotal time: {total_time:.1f}")


if __name__ == "__main__":
    main()
