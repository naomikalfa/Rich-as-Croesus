import datetime
from termcolor import cprint

import get_all_caches as caches


def calculate_all_prices(fiat='EUR', coin='XMR', start='04-02-2020', high_low='high', coin_amount=int(42), fiat_amount_spent=int(0)):
    coin_amount = int(coin_amount)  # double casting to int here prevents crashes later on
    historical_prices = caches.get_historical_price_cache(fiat, coin, start)

    # to mitigate a ZeroDivisionError when the start date requested precedes the earliest data for coin in API database:
    if len(historical_prices[0]['data']['quotes']) == 0:
        historical_coin_price = 0
        cprint(f"   No coin data found for this date for {coin}, try a later date.", 'red', 'on_white', attrs=['bold'])

    else:
        historical_coin_price = float(historical_prices[0]['data']['quotes'][0]['quote'][fiat][high_low])
        fiat_amount_spent = int(coin_amount) * historical_coin_price

        cprint(
            f"   On {start}, at its {high_low}est price, 1 {coin} would have cost {historical_coin_price:,.2f} {fiat} &"
            f" to buy your desired amount of {coin_amount:,} {coin} would have cost {fiat_amount_spent:,.2f} {fiat}.",
            'yellow', 'on_grey', attrs=['bold', 'dark'])

    todays_prices = caches.get_todays_price_cache(fiat=fiat)

    for k, v in enumerate(todays_prices['data']):
        if todays_prices['data'][k]['symbol'] == coin:
            todays_coin_price = todays_prices['data'][k]['quote'][fiat]['price']

    new_fiat_amount_spent = f"{round(coin_amount * todays_coin_price)}"
    new_fiat_amount_spent = float(new_fiat_amount_spent)

    current_coin_amount = fiat_amount_spent / todays_coin_price
    cprint(f"   Whereas today, {fiat_amount_spent:,.2f} {fiat} would buy you {current_coin_amount:,} {coin}.", 'yellow',
           'on_grey', attrs=['bold', 'dark'])

    return fiat_amount_spent, fiat, todays_coin_price, coin, coin_amount, new_fiat_amount_spent, start, \
           current_coin_amount, historical_coin_price


def calculate_single_profit_loss(fiat_amount_spent, fiat, coin, coin_amount, new_fiat_amount, start):

    cprint(f"   Had you bought {coin_amount} {coin} for {fiat_amount_spent:,.2f} {fiat} on {start} and held on to "
           f"it, today {coin_amount} {coin} would be worth {new_fiat_amount:,.2f} {fiat}.\n", 'yellow', 'on_grey',
           attrs=['bold', 'dark'])

    cprint(f"   Pulling the trigger on {start} would have caused your fiat holdings to:", 'yellow', 'on_grey',
           attrs=['bold', 'dark'])

    if fiat_amount_spent > new_fiat_amount:
        loss = fiat_amount_spent - new_fiat_amount
        state = 'loss'
        cprint(f'   Decrease by {loss:,.2f} {fiat}, so sad, quelle dommage!\n', 'yellow', 'on_grey', attrs=['bold',
                                                                                                            'dark'])
        return loss, state

    elif fiat_amount_spent < new_fiat_amount:
        profit = new_fiat_amount - fiat_amount_spent
        state = 'profit'
        cprint(f'   Increase by {profit:,.2f} {fiat}, what joy, rich as Croesus you could have been!\n', 'yellow',
               'on_grey', attrs=['bold', 'dark'])
        return profit, state

    elif fiat_amount_spent == new_fiat_amount:
        stasis = fiat_amount_spent == new_fiat_amount
        state = 'stasis'
        cprint(f"   My my, how curious, your new and old {fiat} holdings remain identical - welcome to stasis!\n",
               'yellow', 'on_grey', attrs=['bold', 'dark'])
        return stasis, state


def calculate_multiple_profit_loss(total_fiat_amount_spent, portfolio, start, fiat_amount_spent, fiat,
                                   sum_fiat_profit_amount, sum_fiat_loss_amount, new_fiat_amount):

    cprint('   Total of all wallets combined:', 'grey', 'on_yellow', attrs=['dark', 'bold'])
    cprint(f"   All of your wallets purchased on {start} would have cost {total_fiat_amount_spent:,.2f} {fiat}.",
           'yellow', 'on_grey', attrs=['dark', 'bold'])

    total_profits_losses = sum_fiat_profit_amount - sum_fiat_loss_amount
    cprint(f"   Had you held onto all them coins, today the total profits of your portfolio would have been"
           f" {total_profits_losses:,.2f} {fiat}.\n", 'yellow', 'on_grey',  attrs=['dark', 'bold'])

    cprint(f"   Pulling the trigger on {start} would have caused your fiat holdings to:", 'yellow', 'on_grey',
           attrs=['bold', 'dark'])

    if total_fiat_amount_spent > total_profits_losses:
        loss = total_fiat_amount_spent - total_profits_losses
        state = 'loss'
        cprint(f'   Decrease by {loss:,.2f} {fiat}, so sad, quelle dommage!\n', 'yellow', 'on_grey', attrs=['bold',
                                                                                                            'dark'])
        return loss, state

    elif total_fiat_amount_spent < total_profits_losses:
        profit = total_profits_losses - total_fiat_amount_spent
        state = 'profit'
        cprint(f'   Increase by {profit:,.2f} {fiat}, what joy, rich as Croesus you could have been!\n', 'yellow',
               'on_grey', attrs=['bold', 'dark'])
        return profit, state

    elif fiat_amount_spent == new_fiat_amount:
        stasis = fiat_amount_spent - new_fiat_amount
        state = 'stasis'
        cprint(f"   My my, how curious, your new and old {fiat} holdings remain identical - welcome to stasis! \n",
               'yellow', 'on_grey', attrs=['bold', 'dark'])
        return stasis, state


def output_coin_histdata(coin_cache, high_or_low, coin, start_date, end_date, fiat):

    # coin price at start date based on user's high/low request
    cprint(f"   This was the {high_or_low}est price point for 1 {coin} on "
           f"{datetime.datetime.utcfromtimestamp(start_date).strftime('%d-%m-%Y')} in {fiat}: "
           f"{coin_cache['data']['quotes'][0]['quote'][fiat][high_or_low]:,.2f}", 'red', 'on_grey', attrs=['bold',
                                                                                                           'dark'])

    # coin price at end date based on user's high/low request
    length = range(len(coin_cache['data']['quotes']))
    cprint(f"   This was the {high_or_low}est price point for 1 {coin} on "
           f"{datetime.datetime.utcfromtimestamp(end_date).strftime('%d-%m-%Y')} in {fiat}: "
           f"{coin_cache['data']['quotes'][length[-1]]['quote'][fiat][high_or_low]:,.2f}", 'red', 'on_grey',
           attrs=['bold', 'dark'])

    cprint(f"   Here is your requested output for {coin_cache['data']['name']}'s historical data from "
           f"{datetime.datetime.utcfromtimestamp(start_date).strftime('%d-%m-%Y')} to "
           f"{datetime.datetime.utcfromtimestamp(end_date).strftime('%d-%m-%Y')}\ncoin id: {coin_cache['data']['id']}"
           f" // coin name: {coin_cache['data']['name']} // coin symbol: {coin_cache['data']['symbol']}", 'red',
           'on_grey', attrs=['bold', 'dark'])
    for k, v in enumerate(coin_cache['data']['quotes']):
        cprint(v, 'yellow', 'on_grey', attrs=['bold', 'dark'])

    return
