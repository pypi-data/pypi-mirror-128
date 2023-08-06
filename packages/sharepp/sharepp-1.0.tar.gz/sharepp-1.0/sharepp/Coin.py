from enum import Enum


class Coin(Enum):
    """Enum representing all currently supported cryptocurrencies."""

    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    BINANCE_COIN = "binancecoin"
    TETHER = "tether"
    SOLANA = "solana"
    CARDANO = "cardano"
    RIPPLE = "ripple"
    USD_COIN = "usd-coin"
    POLKADOT = "polkadot"
    DOGECOIN = "dogecoin"
