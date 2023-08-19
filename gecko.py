from datetime import datetime
import utils


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

