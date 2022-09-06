
import os
import requests

from dotenv import load_dotenv
load_dotenv()


class CMC(object):

    _session = None
    __DEFAULT_BASE_URL = 'https://api.coinmarketcap.com/'
    __PRO_BASE_URL = 'https://pro-api.coinmarketcap.com/'
    __DEFAULT_TIMEOUT = 30
    __API_KEY_ENV_KEY = "CMC_PRO_API_KEY"

    def __init__(self, api_key=None, base_url=None, request_timeout=__DEFAULT_TIMEOUT):
        self.api_key = api_key or os.getenv(self.__API_KEY_ENV_KEY)
        if (not base_url):
            base_url = self.__PRO_BASE_URL if self.api_key \
                else self.__DEFAULT_BASE_URL

        self.base_url = base_url
        self.request_timeout = request_timeout

    @property
    def session(self):
        if (self._session):
            return self._session
        self._session = requests.Session()
        self._session.headers.update({'Content-Type': 'application/json'})
        if (self.api_key):
            self._session.headers.update({"X-CMC_PRO_API_KEY": self.api_key})
        return self._session

    def __make_req(self, endpoint, params, v):
        if (self.api_key):
            params["CMC_PRO_API_KEY"] = self.api_key

        url = self.base_url + f"{v}/" + endpoint
        response_object = self.session.get(
            url, params=params, timeout=self.request_timeout)

        response_object.raise_for_status()

        return response_object.json()

    def ohlcv_historical(self, params):
        "https://coinmarketcap.com/api/documentation/v1/#operation/getV2CryptocurrencyOhlcvHistorical"
        return self.__make_req('cryptocurrency/ohlcv/historical', params, "v2")

    def quotes_historical(self, params):
        "https://coinmarketcap.com/api/documentation/v1/#operation/getV1ExchangeQuotesHistorical"
        return self.__make_req("exchange/quotes/historical", params, "v1")
