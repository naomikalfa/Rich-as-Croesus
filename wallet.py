from termcolor import cprint
import json

import get_all_caches as caches


class Wallet:
    def __init__(self, coin='', amount='', fiat=''):
        self.coin = coin
        self.amount = amount
        self.fiat = fiat

    # can only have one fiat per portfolio to conform to API cache call standards
    def get_value_in_fiat(self):
        prices = caches.get_todays_price_cache(fiat=self.fiat)
        for i, v in enumerate(prices['data']):
            if v['symbol'] == self.coin:
                coin_in_fiat = v['quote'][self.fiat]['price']
                total_crypto_in_fiat = round(float(self.amount) * coin_in_fiat, 2)
                return total_crypto_in_fiat

    def output(self):
        return self.coin, self.amount, self.fiat

    def to_dict(self):
        return {'coin': self.coin, 'amount': self.amount, 'fiat': self.fiat}


def sum_portfolio_wallets():
    with open('portfolio.json', 'r+', newline='\n') as folio:
        portfolio = json.load(folio)
        cprint('   All wallets in your portfolio: \n', 'grey', 'on_yellow', attrs=['bold', 'dark'])
        for wallet in portfolio:
            cprint(wallet, 'yellow', 'on_grey', attrs=['bold'])

    wallets = [Wallet(w['coin'], w['amount'], w['fiat']) for w in portfolio]
    sum = 0
    for wallet in wallets:
        sum += wallet.get_value_in_fiat()

    cprint(f"\n   At today's prices, all wallets in your portfolio would be worth: {round(sum, 2):,.2f} "
           f"{portfolio[0]['fiat']}", 'yellow', 'on_grey', attrs=['bold', 'dark'])

    return portfolio, wallets
