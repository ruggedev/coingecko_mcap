from datetime import datetime
import utils
import json

class Coingecko:
    free_url = 'https://api.coingecko.com/api/v3'
    pro_url = 'https://pro-api.coingecko.com/api/v3'

    def __init__(self, gecko_api_key=None):
        self.key = gecko_api_key

    def get_url(self, endpoint):
        if self.key:
            return f'{self.pro_url}/{endpoint}&x_cg_pro_api_key={self.key}'
        else:
            return f'{self.free_url}/{endpoint}'

    def get_top_coins_by_mcap(self, n):
        endpoint = self.get_url("coins/markets?vs_currency=usd&order="
                                f"market_cap_desc&per_page={n}&page=1&sparkline=false&locale=en")
        data = utils.get(endpoint=endpoint, tag='coingecko:coins')

        ks = ['id', 'symbol', 'current_price', 'market_cap', 'market_cap_rank']  # The keys you want
        filtered_arr = [{k: v for k, v in c.items() if k in ks} for c in data]
        yyyymmdd = datetime.today().strftime('%Y%m%d')
        with open(f"tokens_{yyyymmdd}.json", "w") as outfile:
            json.dump(filtered_arr, outfile, indent=4, sort_keys=False)

    def get_first_price_exist_date(self, token_id) -> tuple[int, datetime] | None:
        endpoint = self.get_url(
            f'coins/{token_id}/market_chart?vs_currency=usd&days=max')
        data = utils.get(endpoint=endpoint, tag='coingecko')
        if 'prices' in data:
            first_price_date = data['prices'][0][0]
            if first_price_date != 0:
                return int(first_price_date), utils.timestamp_to_datestr(int(first_price_date) / 1000, _format='%d-%m'
                                                                                                               '-%Y')
            else:
                return None
        else:
            return None

    # date_str: DD-MM-YYYY
    def get_hist_token_price(self, token_id, date_str) -> float:
        endpoint = self.get_url(f'coins/{token_id}/history?date={date_str}')

        res = utils.get(endpoint=endpoint, tag='coingecko')
        return float(res['market_data']['market_cap']['usd'] or 0.0) if 'market_data' in res else 0.0
