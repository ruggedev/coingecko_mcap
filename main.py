import json
import logging
import os
import pandas as pd
from utils import get_days_diff
from datetime import datetime
from gecko import Coingecko
from typing import TypedDict, List


class Token(TypedDict):
    symbol: str
    gecko_id: str
    first_mcap_date: str


def update_tokens():
    # Load token configs from json
    with open('tokens.json', 'r+') as f:
        tokens: List[Token] = json.load(f)

    _tokens = tokens.copy()
    for i in _tokens:
        file_path = f'data/{i["symbol"]}.csv'
        if not os.path.exists(file_path):
            mcap_df = pd.DataFrame(columns=['symbol', 'date', 'mcap_usd'])
        else:
            mcap_df = pd.read_csv(file_path)
        if not i['first_mcap_date']:
            i['first_mcap_date'] = '-'.join((str(gecko_.get_first_price_exist_date(i['gecko_id'])[1])[0:10].split('-'))
                                            [::-1])

        start_ = mcap_df.iloc[-1]['date'] if len(mcap_df) > 0 else i['first_mcap_date']
        end_ = datetime.strftime((datetime.today()), '%d-%m-%Y')
        missing_days = get_days_diff(start_, end_)

        for d in missing_days:
            mc = gecko_.get_hist_token_price(i['gecko_id'], d)
            new_row = pd.DataFrame([{"symbol": i['symbol'], 'date': d, "mcap_usd": mc}])
            mcap_df = pd.concat([mcap_df, new_row], ignore_index=True)

            mcap_df = mcap_df[['symbol', 'date', 'mcap_usd']]
            mcap_df.to_csv(file_path)
            logging.info(f'Updating: {i["symbol"]}, date: {d}',
                         extra={'status_code': '', 'tag': '', 'method': ""})

    with open("tokens.json", "w") as outfile:
        json.dump(_tokens, outfile, indent=4)


if __name__ == "__main__":
    gecko_ = Coingecko()
    update_tokens()
