from .meta import SingletonMeta


class Tinkoff(metaclass=SingletonMeta):
    urls = {"EURUSD": "https://api.tinkoff.ru/v1/currency_rates?from=EUR&to=USD",
            "GBPEUR": "https://api.tinkoff.ru/v1/currency_rates?from=GBP&to=EUR",
            "GBPUSD": "https://api.tinkoff.ru/v1/currency_rates?from=GBP&to=USD"
            }

    currencies_rates = {}

    chains = {
        "USD_EUR_GBP_USD": ("EURUSD_SELL", "GBPEUR_SELL", "GBPUSD_BUY", "GBPUSD_SELL", "GBPEUR_BUY", "EURUSD_BUY")
    }
