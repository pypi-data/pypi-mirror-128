import re
import requests
from bs4 import BeautifulSoup
from sharepp.Coin import Coin

LANG_UND_SCHWARZ_ETF_URL = "https://www.ls-tc.de/de/etf/"
COIN_GECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
EURO_CURRENCY = "eur"


def get_etf_price(isin: str) -> float:
    """
    Gets the current price in euro of a given ETF.

    :param isin: the ISIN of the ETF
    :return: the current price
    """
    if is_isin(isin):
        response = requests.get(LANG_UND_SCHWARZ_ETF_URL + isin)
        parsed_html = BeautifulSoup(response.text, "html.parser")
        price_span = parsed_html.find("div", class_="mono").find("span")
        price_string = price_span.text.replace(".", "").replace(",", ".")
        return float(price_string)
    else:
        raise ValueError(
            "You must provide a string object representing a valid ISIN!")


def get_coin_price(coin: Coin) -> float:
    """
    Gets the current price in euro of a given cryptocurrency.

    :param coin: the cryptocurrency
    :return: the current price of the cryptocurrency
    """
    response = requests.get(
        COIN_GECKO_URL.format(coin=coin.value, currency=EURO_CURRENCY)).json()
    return float(response[coin.value][EURO_CURRENCY])


def is_isin(isin: str) -> bool:
    """
    Checks whether a string is a valid ISIN or not.

    :param isin: the string to be checked
    :return: true if the given string is a valid ISIN, otherwise false
    """
    if re.match("^[A-Za-z]{2}[A-Za-z0-9]{10}", isin):
        return True
    else:
        return False
