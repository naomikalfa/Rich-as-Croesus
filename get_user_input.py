import json
from termcolor import colored, cprint

import core_calculations as calc
import get_all_caches as caches
import wallet as w


def choose_coinfiat_lists():
    lists = input(colored('   Let us begin!\n   Type yes to see available coins and currencies: \n', 'cyan', 'on_grey',
                          attrs=['bold', 'dark'])).lower().strip(' ')
    if lists == 'yes' or lists == 'yeah' or lists == 'yup' or lists == 'yeah':
        coin_list, fiat_list = caches.get_coins_currencies_list()
        cprint(coin_list, 'red', 'on_grey')
        cprint(fiat_list, 'yellow', 'on_grey')
    else:
        pass
    return lists


def choose_express_nuanced():
    version = input(colored('   Choose express, historical, or portfolio: \n ', 'cyan', 'on_grey',
                            attrs=['bold', 'dark'])).lower().strip(' ')
    return version


def express():
    express = w.Wallet()
    express.fiat = input(colored('   Enter the fiat currency to output to. Id est, Euro is EUR: \n  ', 'cyan',
                                 'on_grey', attrs=['bold', 'dark'])
                         ).upper().strip(' ')
    express.coin = input(colored('   Enter the cryptocoin of choice. Id est, Monero is XMR: \n  ', 'cyan', 'on_grey',
                                 attrs=['bold', 'dark'])
                         ).upper().strip(' ')
    express_fiat_amount = int(float(input(colored('   Enter amount of fiat to fictitiously spend: \n', 'cyan',
                                                  'on_grey', attrs=['bold', 'dark'])).strip(' ')))
    express_start = input(colored(f"   Enter the date you'd like to have purchased all that {express.coin} (please use"
                                  f" format dd-mm-yyy): \n", 'cyan', 'on_grey', attrs=['bold', 'dark'])).strip(' ')
    express_high_low = input(colored("   Enter 'high' to calculate value based on the coin's daily high, else enter "
                                     "'low': \n", 'cyan', 'on_grey', attrs=['bold', 'dark'])).lower().strip(' ')

    print(colored('. . . Calculating . . .', 'red', 'on_white', attrs=['bold', 'dark', 'underline', 'blink']))

    fiat_amount_spent, fiat, todays_coin_price, coin, coin_amount, new_fiat_amount_spent, start, current_coin_amount,\
        historical_coin_price = calc.calculate_all_prices(express.fiat, express.coin, express_start, express_high_low,
                                                          express_fiat_amount)

    calc.calculate_single_profit_loss(fiat_amount_spent, fiat, coin, coin_amount, new_fiat_amount_spent, start)

    return


def coin_data_span():
    which_span = input(colored("   Enter 'alltime' for the coin's entire history or 'specific' for a span between two "
                               "given dates: \n", 'cyan', 'on_grey', attrs=['bold', 'dark']))
    if which_span == 'alltime':
        alltime = w.Wallet()
        alltime.fiat = input(colored('   Enter the fiat currency to output to. Id est, Euro is EUR: '
                                            '\n  ', 'cyan', 'on_grey', attrs=['bold', 'dark'])).upper().strip(' ')
        alltime.coin = input(colored('   Enter the cryptocoin of choice. Id est, Monero is XMR: \n  ', 'cyan',
                                            'on_grey', attrs=['bold', 'dark'])).upper().strip(' ')
        alltime_high_or_low = input(colored("   Enter 'high' to calculate value based on the coin's daily high, else "
                                            "enter 'low': \n", 'cyan', 'on_grey', attrs=['bold', 'dark'])).lower().strip(' ')

        coin_historical_data, start_date, end_date = caches.get_historical_price_cache(alltime.fiat,
                                                                                       alltime.coin)
        calc.output_coin_histdata(coin_historical_data, alltime_high_or_low, alltime.coin, start_date, end_date,
                                  alltime.fiat)

    elif which_span == 'specific':
        specific = w.Wallet()
        specific.fiat = input(colored('   Enter the fiat currency to output to. Id est, Euro is EUR: \n ',
                                             'cyan', 'on_grey', attrs=['bold', 'dark'])).upper().strip(' ')
        specific.coin = input(colored('   Enter the cryptocoin of choice. Id est, Monero is XMR: \n  ',
                                             'cyan', 'on_grey', attrs=['bold', 'dark'])).upper().strip(' ')
        specific_start = input(colored(f"   Enter the date you'd like to have purchased all that {specific.coin} (please "
                                       f"use format dd-mm-yyy): \n", 'cyan', 'on_grey', attrs=['bold', 'dark'])).strip(' ')
        specific_end = input(colored("   Enter the end date for your historical coin span in the format dd-mm-yyy: \n",
                                     'cyan', 'on_grey', attrs=['bold', 'dark'])).strip(' ')
        specific_high_or_low = input(colored("   Enter 'high' to calculate value based on the coin's daily high, else "
                                             "enter 'low': \n", 'cyan', 'on_grey', attrs=['bold', 'dark'])).lower().strip(' ')

        coin_historical_data, start_date, end_date = caches.get_historical_price_cache(specific.fiat,
                                                                                       specific.coin,
                                                                                       specific_start, specific_end)
        calc.output_coin_histdata(coin_historical_data, specific_high_or_low, specific.coin, start_date,
                                  end_date, specific.fiat)


def create_portfolio():
    num_wallets = input(colored('   How many wallets would you like to create in this portfolio?', 'cyan', 'on_grey',
                                attrs=['bold', 'dark'])).strip(' ')
    fiat = input(colored('   Enter the fiat currency to output to. Id est, Euro is EUR. Only one per portfolio: \n',
                         'cyan', 'on_grey', attrs=['bold', 'dark'])).upper().strip(' ')
    portfolio_start = input(colored("   Enter the date on which you'd like to have purchased all them cryptocoins (please "
                                    f"use format dd-mm-yyy): \n", 'cyan', 'on_grey', attrs=['bold', 'dark'])).upper().strip(' ')
    high_or_low = input(colored("   Enter 'high' to calculate value based on the coin's daily high, else enter 'low': "
                                "\n", 'cyan', 'on_grey', attrs=['bold', 'dark']))

    with open('portfolio.json', 'w+', newline='\n') as f:

        # to format it for proper .json
        new_portfolio = []
        for i in range(int(num_wallets)):
            print(colored(f'   Wallet {i + 1}:', 'red', 'on_white'))
            coin = input(colored('   Enter the cryptocoin of choice. Id est, Monero is XMR: \n', 'cyan',
                                 'on_grey', attrs=['bold', 'dark'])).upper().strip(' ')
            amount = input(colored('   Enter number of coins to fictitiously purchase: \n', 'cyan', 'on_grey',
                                   attrs=['bold', 'dark']))
            wallet = w.Wallet(coin, amount, fiat)
            new_portfolio.append(wallet.to_dict())

        json.dump(new_portfolio, f, indent=2, separators=(',', ': '))

        return new_portfolio, portfolio_start, high_or_low


def load_portfolio(start_date='', high_low=''):
    # Ensure we're not doubling up on logic if we've landed here directly after creating a new portfolio
    if start_date == '' and high_low == '':

        start_date = input(colored("   Enter the date on which you'd like to have purchased all them cryptocoins (please"
                              f" use format dd-mm-yyy): \n", 'cyan', 'on_grey', attrs=['bold', 'dark'])).strip()
        high_low = input(colored("   Enter 'high' to calculate value based on the coin's daily high, else enter 'low': \n",
                             'cyan', 'on_grey', attrs=['bold', 'dark'])).lower().strip()

    with open('portfolio.json', 'r+', newline='\n') as folio:
        portfolio = json.load(folio)
        print(colored('   A detailed report for each wallet in your portfolio!', 'grey', 'on_yellow',
                      attrs=['blink', 'dark', 'bold']))
        sum_fiat_loss_amount = 0
        sum_fiat_profit_amount = 0
        total_fiat_amount_spent = 0
        for wallet in portfolio:
            print(colored(f"   {wallet}", 'yellow', 'on_grey'))

            fiat_amount_spent, fiat, todays_coin_price, coin, coin_amount, new_fiat_amount, start, current_coin_amount,\
                historical_coin_price = calc.calculate_all_prices(wallet['fiat'], wallet['coin'], start_date, high_low,
                                                                  wallet['amount'])

            total_fiat_amount_spent += fiat_amount_spent
            profit_loss_stasis, state = calc.calculate_single_profit_loss(fiat_amount_spent, fiat, coin, coin_amount,
                                                                          new_fiat_amount, start)

            if state == 'loss':
                sum_fiat_loss_amount += profit_loss_stasis
            if state == 'profit':
                sum_fiat_profit_amount += profit_loss_stasis

        calc.calculate_multiple_profit_loss(total_fiat_amount_spent, portfolio, start, fiat_amount_spent, fiat,
                                            sum_fiat_profit_amount,
                                            sum_fiat_loss_amount, new_fiat_amount)

    return


# Let the action begin!

cprint("   Welcome! \n   You are about to discover whether, with that keen 20/20 hindsight, you could have made "
       "yourself rich as Croesus. \n   Here are your options:\n", 'white', 'on_cyan', attrs=['bold'])
cprint("   1. Express: Input some data to find out how much a coveted cryptocurrency would be worth in today's fiat had you pulled"
       " the gun all those moons ago.\n", 'cyan', 'on_blue', attrs=['bold'])
cprint("   2. Historical: Print out all or some of the historical data of a chosen coin.\n",  'cyan', 'on_blue', attrs=['bold'])
cprint("   3. Portfolio: Create or load a portfolio with as many wallets as you'd like to find out what your theoretical portfolio"
       " would have been worth today and what your profits or losses might have looked like.\n",  'cyan', 'on_blue', attrs=['bold'])
choose_coinfiat_lists()
version = choose_express_nuanced()

if version == 'express':
    express()
elif version == 'historical':
        coin_data_span()
elif version == 'portfolio':
        which_portfolio = input(colored("   Type 'new' to create a new portfolio or 'old' to load an existing one: \n",
                                        'cyan', 'on_grey', attrs=['bold', 'dark'])).lower().strip(' ')

        if which_portfolio == 'new':
            new_portfolio, new_portfolio_start, new_high_low = create_portfolio()
            w.sum_portfolio_wallets()
            load_portfolio(new_portfolio_start, new_high_low)
        elif which_portfolio == 'old':
            load_portfolio()
else:
    cprint('   Hmmm seems like you have chosen to input an incorrect value. Perhaps you ought to venture another '
           'attempt at trying your hand at this speculative game? ', 'red', 'on_white', attrs=['bold'])
