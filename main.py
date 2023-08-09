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

    def get_first_price_exist_date(self, token_id) -> str | None:
        endpoint = self.get_url(
            f'coins/{token_id}/market_chart?vs_currency=usd&days=max')
        data = utils.get(endpoint=endpoint)
        if 'prices' in data:
            first_price_date = data['prices'][0][0]
            if first_price_date != 0:
                return utils.timestamp_to_datestr(int(first_price_date) / 1000, _format='%d-%m-%Y')
            else:
                return None
        else:
            return None

    # date_str: DD-MM-YYYY
    def get_hist_token_price(self, token_id, date_str):
        endpoint = self.get_url(f'coins/{token_id}/history?date={date_str}')
        return utils.get(endpoint=endpoint)['market_data']['market_cap']['usd']


if __name__ == "__main__":
    gecko = Coingecko()
    print(gecko.get_first_price_exist_date('aave'))
    print(gecko.get_hist_token_price('aave', '2020-10-10'))
