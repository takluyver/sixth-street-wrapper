import requests

TIME_SERIES_DAILY = "Time Series (Daily)"
LOW_PRICE_KEY = "3. low"
HIGH_PRICE_KEY = "2. high"


class Stocker:
    """
    A wrapper class for retrieving and analyzing stock data using the Alpha Vantage API.
    """

    # note: improvement, if we set a symbol at the top level when initializing the library
    # we can assume we are going to be working with the same data and can cache it
    # this will save us from making the same api call over and over again, but we will need a way to invalidate the cache
    # if the user wants to work with a different symbol
    # or if the data is stale because the program has been running for some time and new data has been added
    def __init__(self, key, symbol=None):
        """
        Initializes a new instance of the Stocker class with the specified API key and symbol.

        :param key: The Alpha Vantage API key to use for retrieving stock data.
        :param symbol: The stock symbol to retrieve data for. If not specified, the symbol must be provided in each method call.
        """
        self.symbol = symbol
        self.key = key

    def _get_url(self, key, symbol):
        """
        Helper function that returns the URL for retrieving daily stock data for the specified symbol.

        :param symbol: The stock symbol to retrieve data for.
        :return: The URL for retrieving daily stock data for the specified symbol.
        """
        if symbol is None:
            symbol = self.symbol
            print(symbol)
        return f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}"

    def lookup(self, date, symbol=None):
        """
        Retrieves the open, high, low, close, and volume for the specified stock symbol on the specified date.

        :param date: The date to retrieve data for, in the format "YYYY-MM-DD".
        :param symbol: The optional stock symbol to retrieve data for. If not specified, the symbol must be provided in the constructor.
        :return: A dictionary containing the open, high, low, close, and volume for the specified stock symbol on the specified date.
        """
        url = self._get_url(self.key, symbol)
        response = requests.get(url)
        data = response.json()[TIME_SERIES_DAILY]

        if date not in data:
            return None
        return data[date]

    def min(self, n, symbol=None):
        """
        Retrieves the lowest price that the specified stock symbol traded at over the last 'n' data points (lowest low).

        :param n: The number of data points to retrieve.
        :param symbol: The optional stock symbol to retrieve data for. If not specified, the symbol must be provided in the constructor.
        :return: The lowest price that the specified stock symbol traded at over the last 'n' data points (lowest low).
        """
        url = self._get_url(self.key, symbol)
        response = requests.get(url)
        data = response.json()[TIME_SERIES_DAILY]

        lowest_price = float("inf")
        for date in sorted(data.keys())[:n]:
            low_price = float(data[date][LOW_PRICE_KEY])
            if low_price < lowest_price:
                lowest_price = low_price
        if lowest_price == float("inf"):
            return None
        return lowest_price

    def max(self, n, symbol=None):
        """
        Retrieves the highest price that the specified stock symbol traded at over the last 'n' data points (highest high).

        :param n: The number of data points to retrieve.
        :param symbol: The stock symbol to retrieve data for. If not specified, the symbol must be provided in the constructor.
        :return: The highest price that the specified stock symbol traded at over the last 'n' data points (highest high).
        """
        url = self._get_url(self.key, symbol)
        response = requests.get(url)
        data = response.json()[TIME_SERIES_DAILY]

        highest_price = 0
        for date in sorted(data.keys(), reverse=True)[:n]:
            high_price = float(data[date][HIGH_PRICE_KEY])
            if high_price > highest_price:
                highest_price = high_price
        if highest_price == 0:
            return None
        return highest_price
