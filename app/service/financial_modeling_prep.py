# financial_modiling_prep.py

## lib
import requests

## module


## definition
class FinancialModelingPrep:
    api_key = None
    forex_list = [
        "EURUSD", "CNYUSD", "INRUSD", "RUBUSD", "JPYUSD", "KRWUSD"
    ]

    @classmethod
    def activate(cls, config:dict):
        cls.api_key = config["api_key"]

    @classmethod
    def deactivate():
        pass


    @classmethod
    def get_index_by_name(cls, index:str):
        url = f"https://financialmodelingprep.com/api/v4/etf-holdings/portfolio-date?symbol=SPY"

        resp = requests.get( url )
        if resp.status_code == 200:
            return resp.json()
        else:
            print("error :",resp.status_code)
            return False
        

    @classmethod
    def get_forex_by_pair( cls, pair:str ):
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{pair}?apikey={cls.api_key}"

        resp = requests.get( url )
        if resp.status_code == 200:
            return resp.json()
        else:
            print("error :",resp.status_code)
            return False
        





