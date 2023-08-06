import requests

cache = {}


def loadTokenPrices(tokenName):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=euphoria-2%2Charmony&vs_currencies=USD&include_market_cap=true"
    res = requests.get(url).json()

    cache["WAGMI"] = res["euphoria-2"]
    cache["ONE"] = res["harmony"]

    return cache[tokenName]["usd"]
