from gecko import Coingecko

if __name__ == "__main__":
    gecko_ = Coingecko()
    gecko_.get_top_coins_by_mcap(200)
