import time
from configobj import ConfigObj
# from alive_progress import alive_bar
# from poloniex_api import Poloniex
from colorama import Fore, Style, Back, init
from termcolor import colored
import data
import datetime


init()  # для отображения цвета в windows cmd
cfg = ConfigObj('config.ini', encoding='utf8')
p = data.poloniex()
tk = data.ticker()
coin1 = cfg['PAIR']['coin1']  # первая монета пары
coin2 = cfg['CURRENCY']['coin2']  # вторая монета пары


def timer(tm):
    for i in range(tm + 1):
        print(f"{Fore.YELLOW}{Style.BRIGHT} -----  {tm - i}  ----- {Fore.RESET}", end='')
        print('\r', end='')
        time.sleep(1)
# def timer(tm):
#     print(f"{Fore.WHITE}{Style.BRIGHT} TIME THE PAUSE PROGRESS ")
#     with alive_bar(tm, bar='blocks') as bar:
#         for i in range(tm):
#             time.sleep(1)
#             bar()        


def cancel_sell_order():
    b, s = [], []  # списки открытых buy и sell ордеров
    all_open_orders = p.returnOpenOrders(currencyPair=tk)
    for order in all_open_orders:
        if order['type'] == 'buy':
            b.append(order['orderNumber'])
        elif order['type'] == 'sell':
            s.append(order['orderNumber'])
    # print(f'BUY: {b}')
    # print(f'SELL: {s}')
    if len(s) != 0:
        for order_number in s:
            p.cancelOrder(orderNumber=order_number)
            print(f'SELL ОРДЕР {order_number} ЗАКРЫТ')
    else:
        print('Нет SELL ордеров')


def buy_counting():
    end_time = int(time.time())  # время окончания - текущее
    start_time = int(end_time - 60 * 60 * 24 * 31)  # время начала минус месяц
    spent_coins, bought_coins = 0, 0  # spent_coins - потрачено монет, bought_coins - куплено
    t_history = p.returnTradeHistory(currencyPair=tk, start=start_time, end=end_time, limit=100)
    # trade_history (по умолчанию 500, "limit=100" - 100 последних ордеров)
    # print(f'!!!!: {t_history[0]}')
    if t_history[0]['type'] == "buy":
        for i in t_history:
            if i['type'] == "buy":
                bought_coins += float(i['amount'])  # i['amount']  # сколько купили
                spent_coins += float(i['total'])  # i['total']  # сколько потратили
            else:
                break
        print(f"Купили всего: {bought_coins} {coin2}")
        print(f"Потратили всего: {spent_coins} {coin1}")
    elif t_history[0]['type'] != "buy":
        print("ПОСЛЕДНИЙ ИСПОЛНЕННЫЙ ОРДЕР НЕ Buy")
    return spent_coins, bought_coins


# f"{Fore.GREEN} Sell cycle: {Fore.YELLOW}{Style.BRIGHT}{cycle}{Fore.RESET}"
def order_sell():
    print(f"{Fore.WHITE}{Style.BRIGHT}           ЗАПУСК МОДУЛЯ ПРОДАЖИ {Fore.RESET}")
    time_n = datetime.datetime.now()
    print(colored('            ' + time_n.strftime("%d-%m-%Y %H:%M:%S"), 'cyan', 'on_grey'))
    coin2_balance = float(p.returnBalances()[coin2])
    if coin2_balance > 0.000001:
        cancel_sell_order()
        sell_percent = cfg['percent-sell']['p4']  # Процент продажи
        volume_coin = buy_counting()  # Функция вернет кортеж из 2-x элементов
        spent = volume_coin[0]  # потраченные монеты
        bought = volume_coin[1]  # купленные монеты
        average = spent / bought  # усреднение
        # if coin2_balance != bought:
        #     print(f"{Fore.GREEN}{Style.BRIGHT}Баланс не соответсвует колличеству купленных монет !!! {Fore.RESET}")
        percent = float(average) / 100.0 * float(sell_percent)
        print(f"Процент продажи: {percent}")
        price_sell_order = round(float(average) + float(percent), 8)
        print(f"Цена ордера: {Fore.YELLOW}{Style.BRIGHT}{price_sell_order}{Fore.RESET}")
        current_price = float(p.returnOrderBook(currencyPair=tk)['bids'][0][0])
        time.sleep(1)
        # if current_price > price_sell_order:
        #     set_sell_order = p.sell(currencyPair=tk, rate=price_sell_order, amount=coin2_balance)
        #     print(f"{Fore.GREEN}{Style.BRIGHT}Добавлен SELL ордер: {str(set_sell_order)} {Fore.RESET}")
        if current_price > price_sell_order:
            p1 = float(p.returnOrderBook(currencyPair=tk)['bids'][0][0])
            p2 = 0
            while current_price > price_sell_order:
                timer(3)
                print(f"{Fore.RED}{Style.BRIGHT} => Price_UP => {Fore.RESET}")
                p2 = float(p.returnOrderBook(currencyPair=tk)['bids'][0][0])
                time.sleep(1)
                if p2 >= p1:
                    p1 = p2
                    current_price = p2
                elif p2 < p1 and p2 > price_sell_order:
                    set_sell_order = p.sell(currencyPair=tk, rate=p2, amount=coin2_balance)
                    print(f"{Fore.GREEN}{Style.BRIGHT}Добавлен SELL ордер: {str(set_sell_order)} {Fore.RESET}")
                    order_sell()
                else:
                     current_price = float(p.returnOrderBook(currencyPair=tk)['bids'][0][0])
                print(f"Current_price: {current_price}")
                print(" ")
        else:
            print(" ")
            timer(10)
            print(" ")
            order_sell()
    else:
        print(" ")
        timer(10)
        print(" ")
        order_sell()


def main():
    print(f"{Fore.GREEN} START {Fore.RESET}")
    order_sell()


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as err:
            print(err)
            time.sleep(5)
            continue
