# MyPoloniex
# 03.01.21
import time
from configobj import ConfigObj
from poloniex_api import Poloniex
from termcolor import colored
from colorama import Fore, Style, Back, init
import datetime
# import logging
# import logging.config


init()  # для отображения цвета в windows cmd
cfg = ConfigObj('config.ini', encoding='utf8')
# config_file = "C:\ Users\............/config.ini"
api_key = cfg['API']['key']
api_secret = cfg['API']['secret']
p = Poloniex(
    API_KEY=api_key,
    API_SECRET=api_secret
)
interval_info = cfg['interval-info']['f']
interval_info2 = cfg['interval-info2']['f2']
coin1 = cfg['PAIR']['coin1']  # первая монета пары (BTC, ETH, USDT)
coin2 = cfg['CURRENCY']['coin2']  # вторая монета пары
balance = p.returnCompleteBalances()
cc1 = float(balance[coin1]['available'])
cc2 = float(balance[coin2]['available'])

TICKER = "coin1_coin2"
if coin1 == "BTC":
    TICKER = 'BTC_{currency}'.format(currency=coin2)
elif coin1 == "USDT":
    TICKER = 'USDT_{currency}'.format(currency=coin2)
elif coin1 == "USDC":
    TICKER = 'USDC_{currency}'.format(currency=coin2)
elif coin1 == "ETH":
    TICKER = 'ETH_{currency}'.format(currency=coin2)
elif coin1 == "XMR":
    TICKER = 'XMR_{currency}'.format(currency=coin2)

onOrders = float(str(balance[coin1]['onOrders']))
MyList = p.returnOpenOrders(currencyPair=TICKER)  # Список открытых ордеров
SumOrders = len(MyList)

# end_time = int(time.time())  # время окончания - текущее
# start_time = int(end_time - 60 * 60 * 24 * 31)  # время начала минус месяц

print(colored('Пара: ' + str(coin1) + ' - ' + str(coin2), 'blue', attrs=['bold']))
print(colored('Баланс ' + str(coin1) + ': ' + str(cc1), 'blue', attrs=['bold']))
print(colored('Баланс ' + str(coin2) + ': ' + str(cc2), 'blue', attrs=['bold']))
print('In orders:', onOrders, coin1)
print('К-во ордеров:', SumOrders)
print('')
print(colored('$         $          $         $          $          $', 'green', attrs=['bold']))
print('')


def timer(tm):
    for i in range(tm + 1):
        print(f"{Fore.YELLOW}{Style.BRIGHT} -----  {tm - i}  ----- {Fore.RESET}", end='')
        print('\r', end='')
        time.sleep(1)


# def buycoin_counting():
#     endtime = int(time.time())  # время окончания - текущее
#     starttime = int(endtime - 60 * 60 * 24 * 31)  # время начала минус месяц
#     spent_coins, bought_coins = 0, 0  # spent_coins - потрачено монет, bought_coins - куплено
#     t_history = p.returnTradeHistory(currencyPair=TICKER, start=starttime, end=endtime, limit=100)
#     # trade_history (по умолчанию 500, "limit=100" - 100 последних ордеров)
#     # print(f'!!!!: {t_history[0]}')
#     if t_history[0]['type'] == "buy":
#         for i in t_history:
#             if i['type'] == "buy":
#                 bought_coins += float(i['amount'])  # i['amount']  # сколько купили
#                 spent_coins += float(i['total'])  # i['total']  # сколько потратили
#             else:
#                 break
#         print(f"Купили всего: {bought_coins} {coin2}")
#         print(f"Потратили всего: {spent_coins} {coin1}")
#     elif t_history[0]['type'] != "buy":
#         print("ПОСЛЕДНИЙ ИСПОЛНЕННЫЙ ОРДЕР НЕ Buy")
#     return spent_coins, bought_coins


# def cancel_sell_order():
#     b, s = [], []  # списки открытых buy и sell ордеров
#     all_open_orders = p.returnOpenOrders(currencyPair=TICKER)
#     for order in all_open_orders:
#         if order['type'] == 'buy':
#             b.append(order['orderNumber'])
#         elif order['type'] == 'sell':
#             s.append(order['orderNumber'])
#     print(f'BUY: {b}')
#     print(f'SELL: {s}')
#     if len(s) != 0:
#         for order_number in s:
#             p.cancelOrder(orderNumber=order_number)
#             print(f'SELL ОРДЕР {order_number} ЗАКРЫТ')
#     else:
#         print('Нет SELL ордеров')


def func_sell():
    print(colored('ЗАПУСК МОДУЛЯ ПРОДАЖИ', 'green', attrs=['bold']))
    timer(3)
    # cancel_sell_order()
    # cfg1 = ConfigObj('config.ini', encoding='utf8')
    # # print('sell p1')
    # average = 0.0
    # volume_coin = buycoin_counting()  # Функция вернет кортеж из 2-x элементов
    # spent = volume_coin[0]  # потраченные монеты
    # bought = volume_coin[1]  # купленные монеты
    # average = spent / bought  # усреднение
    # sell_percent = cfg1['percent-sell']['p4']  # Процент продажи
    # coin2_balance = float(p.returnBalances()[coin2])
    # # print('sell p3')
    # if coin2_balance != bought:
    #     print(colored("Баланс не соответсвует колличеству купленных монет !!!", 'red', attrs=['bold']))
    # # print('sell p4')
    # percent = float(average) / 100.0 * float(sell_percent)
    # print(f"Процент продажи: {percent}")
    # price_sell_order = round(float(average) + float(percent), 8)
    # print(f"цена ордера: {price_sell_order}")
    # set_sell_order = p.sell(currencyPair=TICKER, rate=price_sell_order, amount=coin2_balance)
    # print(colored('Добавлен SELL ордер: ' + str(set_sell_order) + 'blue', attrs=['bold']))
    # # print('sell p5')


def func_buy1():
    print("START func BUY1")
    cfg2 = ConfigObj('config.ini', encoding='utf8')
    cfg2['last_step'] = {'ls': str(0.0)}  # Обнуляем параметр в конфиге
    cfg2.write()
    order_vol = cfg2['order_rate']['or']
    current_price = p.returnOrderBook(currencyPair=TICKER)['bids'][0][0]
    increment = cfg2['increment']['i']
    increment_step = cfg2['increment_step']['is']
    print(increment, increment_step)
    step_away_from_bids = cfg2['step-1']['p1']  # Отступ первого ордера в % от bids
    step_away_from_orders = cfg2['step-2']['p2']  # Первый отступ между ордерами
    percent = float(current_price) / 100 * float(step_away_from_bids)
    order_price = round(float(current_price) - float(percent), 5)
    volume = float(order_vol) / float(order_price)
    print(f"order_price: {order_price} oreder_vol: {order_vol} volume: {volume}")
    set_order = p.buy(currencyPair=TICKER, rate=order_price, amount=volume)  # выставляем ордер с параметрами
    print('Создан первый ордер:', set_order)

    cfg_buy_orders = cfg2['amount_orders']['am']
    mtg = cfg2['martingale']['mr']
    i = 0
    last_order_price = p.returnOpenOrders(currencyPair=TICKER)[0]['rate']
    temp_order_price = last_order_price
    coin_order = p.returnOpenOrders(currencyPair=TICKER)[0]['total']
    coin1_volume = coin_order
    temp_step = float(step_away_from_orders)
    print('1TempOrderPrice: ', temp_order_price, '1TempVolume: ', coin1_volume)
    while i < (int(cfg_buy_orders) - 1):
        if int(increment) == 1:  # Расчет с увеличением отступа между ордерами
            second_order_price1 = float(temp_order_price) - float(temp_order_price) / 100 * float(temp_step)
            print('second_order_price: ', second_order_price1)
            temp_order_price = second_order_price1
            temp_step = round(float(temp_step) + float(increment_step), 3)
            print('temp step: ', temp_step)
            second_volume = (float(coin1_volume) + float(coin1_volume) / 100 * float(mtg)) / float(
                second_order_price1)
            # Считаем размер следующего ордера
            print('second_volume: ', str(second_volume))
            coin1_volume = float(second_volume) * float(temp_order_price)
            set_second_order = p.buy(currencyPair=TICKER, rate=second_order_price1, amount=second_volume)
            print('СОЗДАН ОРДЕР: ', set_second_order)
            i += 1
            time.sleep(0.1)
            cfg2['last_step'] = {'ls': str(temp_step)}  # Меняем параметр в крнфиге
            cfg2.write()

        elif int(increment) == 0:  # Расчет с одинаковым отступом между ордерами
            second_order_price2 = float(temp_order_price) - float(temp_order_price) / 100 * float(
                step_away_from_orders)
            # Ситаем цену следующего ордера
            print('second_order_price: ', second_order_price2)
            temp_order_price = second_order_price2
            second_volume = (float(coin1_volume) + float(coin1_volume) / 100 * float(mtg)) / float(
                second_order_price2)
            # Считаем размер следующего ордера
            print('second_volume: ', str(second_volume))
            coin1_volume = float(second_volume) * float(temp_order_price)
            print('coin1_volume: ', str(coin1_volume))  # Для проверки (после отладки можно удалить)
            set_second_order = p.buy(currencyPair=TICKER, rate=second_order_price2, amount=second_volume)
            # выставляем следующий ордер с параметрами: цена, размер
            print('СОЗДАН ОРДЕР: ', set_second_order)
            i += 1
            time.sleep(0.1)
        else:
            print('НЕВЕРНЫЙ ПАРАМЕТР increment_step')
            break
    time.sleep(float(interval_info))


def func_buy2():
    print('Start BUY2')
    cfg3 = ConfigObj('config.ini', encoding='utf8')
    open_orders = p.returnOpenOrders(currencyPair=TICKER)
    # sum_orders = len(open_orders)
    # if sum_orders == 0:
    #     print('Нет bay ордеров, переход к модулю установки первых ордеров')
    #     func_buy1()

    amount_orders = cfg3['amount_orders']['am']
    step_away_from_orders = cfg3['step-2']['p2']
    order_vol = float(cfg3['order_rate']['or'])
    mtg = cfg3['martingale']['mr']
    increment = cfg3['increment']['i']
    increment_step = cfg3['increment_step']['is']
    buy_count = 0
    sell_count = 0

    for order in open_orders:  # Счетаем открытые ордера
        type_order = order['type']
        if type_order == 'buy':
            buy_count += 1
        elif type_order == 'sell':
            sell_count += 1
            print('')

    print('Колличесвто открытых Buy ордеров: ', buy_count)
    print('Колличесвто открытых Sell ордеров: ', sell_count)
    trade_history_type = p.returnTradeHistory(currencyPair=TICKER)[0]['type']
    if int(buy_count) < int(amount_orders) and trade_history_type == 'buy':
        print(colored('ОРДЕР НА ПОКУПКУ БЫЛ ИСПЛНЕН', 'green', attrs=['bold']))
        print(colored('ДОБАВЛЯЕМ ОРДЕРА', 'green', attrs=['bold']))
        time.sleep(2)
        order_rate = 0.0
        # if sell_count > 0 and buy_count == 0 and trade_history_type == 'buy':
        if buy_count == 0 and trade_history_type == 'buy':
            current_price = p.returnOrderBook(currencyPair=TICKER)['bids'][0][0]
            price_last_buy = p.returnTradeHistory(currencyPair=TICKER)[0]['rate']
            if current_price < price_last_buy:
                order_rate = current_price
            elif price_last_buy < current_price:
                order_rate = price_last_buy
        else:
            order_rate = p.returnOpenOrders(currencyPair=TICKER)[0]['rate']

        temp_order_rate = order_rate
        coin_order_sum = 0
        if temp_order_rate == 0.0:
            print(colored("ERROR order_rate = 0 !!!", 'red', attrs=['bold']))
            main()

        if buy_count < 1 and trade_history_type == 'buy':
            coin_order_sum = float(p.returnTradeHistory(currencyPair=TICKER)[0]['total'])
            print(f"coin_order_sum1: {coin_order_sum}")
            if coin_order_sum < order_vol - 0.5:
                # бывает покупается на чуть меньший обьем чем заданно, что бы сработало условие отнисаем от заданного 0.5
                coin_order_sum = p.returnTradeHistory(currencyPair=TICKER)[1]['total']
        elif buy_count > 0:
            coin_order_sum = p.returnOpenOrders(currencyPair=TICKER)[0]['total']

        print(f"coin_order_sum2: {coin_order_sum}")
        total_coin = coin_order_sum
        temp_step_up = cfg3['last_step']['ls']
        j = buy_count
        while j < int(amount_orders):
            if int(increment) == 1:
                order_price2 = float(temp_order_rate) - float(temp_order_rate) / 100 * float(temp_step_up)
                # Считаем цену нового ордера
                print('order_price ', order_price2)
                order_vol = (float(total_coin) + float(total_coin) / 100 * float(mtg)) / float(
                    order_price2)
                # Считаем обьем ордера
                print('order_vol ', order_vol)
                coin1_vol = float(order_vol) * float(order_price2)
                print('coin1_vol объем для след ордера: ', coin1_vol)
                cash_c2 = float(p.returnBalances()[coin1])
                print('cash coin1 ', cash_c2)
                if float(cash_c2) >= float(coin1_vol):
                    set_order = p.buy(currencyPair=TICKER, rate=order_price2, amount=order_vol)
                    # Выставляем ордер
                    print('Добавленый ордер: ' + str(set_order))
                    time.sleep(1)
                else:
                    print(colored('НЕДОСТАТОЧНО СРЕДСТВ ДЛЯ ДОБАВЛЕНИЯ ОРДЕРА' + ' !!!', 'red', attrs=['bold']))
                    time.sleep(10)
                    break
                temp_order_rate = p.returnOpenOrders(currencyPair=TICKER)[0]['rate']
                total_coin = p.returnOpenOrders(currencyPair=TICKER)[0]['total']
                temp_step_up = round(float(temp_step_up) + float(increment_step), 3)
                j += 1
                time.sleep(1)
                cfg3['last_step'] = {'ls': str(temp_step_up)}  # Меняем параметр в конфиге
                cfg3.write()

            elif increment == 0:  # Расчет с одинаковым отступом между ордерами
                order_price1 = float(temp_order_rate) - float(temp_order_rate) / 100 * float(
                    step_away_from_orders)
                # Считаем цену нового ордера
                print('order_price ', order_price1)
                order_vol = (float(total_coin) + float(total_coin) / 100 * float(mtg)) / float(
                    order_price1)
                # Считаем обьем ордера
                print('order_vol ', order_vol)
                coin1_vol = float(order_vol) * float(order_price1)
                print('coin1_vol объем btc для след ордера: ', coin1_vol)
                cash_c2 = float(p.returnBalances()[coin1])
                print('cash coin1 ', cash_c2)
                if float(cash_c2) > float(coin1_vol):
                    set_order = p.buy(currencyPair=TICKER, rate=order_price1,
                                      amount=order_vol)  # Выставляем ордер
                    print('Добавленый ордер: ' + str(set_order))
                    time.sleep(1)
                else:
                    print(
                        colored('НЕДОСТАТОЧНО СРЕДСТВ ДЛЯ ДОБАВЛЕНИЯ ОРДЕРА' + ' !!!', 'red', attrs=['bold']))
                    break
                temp_order_rate = p.returnOpenOrders(currencyPair=TICKER)[0]['rate']
                total_coin = p.returnOpenOrders(currencyPair=TICKER)[0]['total']
                j += 1
                time.sleep(5)

            else:
                print('НЕВЕРНЫЙ ПАРАМЕТР RISE-STEP')
                break
        print("BUY2 END")


def func_bids():
    print("BIDS START")
    open_orders = p.returnOpenOrders(currencyPair=TICKER)  # Получаем список открытых ордеров
    sum_open_orders = len(open_orders)
    cfg4 = ConfigObj('config.ini', encoding='utf8')
    step1 = cfg4['step-0']['p']
    type_open_orders = p.returnOpenOrders(currencyPair=TICKER)[-1]['type']
    print('Установленно ' + str(sum_open_orders) + ' ордера')
    current_price = p.returnOrderBook(currencyPair=TICKER)['bids'][0][0]
    percent = float(current_price) / 100 * float(step1)
    order_price = float(current_price) - float(percent)
    print('order_price ', order_price)
    order1 = p.returnOpenOrders(currencyPair=TICKER)[-1]['rate']
    print('order1 ', order1)
    if sum_open_orders > 0 and type_open_orders == 'buy' and float(order_price) > float(order1):
        print(colored('ПОДТЯГИВАЕМ ОРДЕРА К BIDS', 'blue', attrs=['bold']))
        j = 0
        while j < sum_open_orders:
            try:
                order_n = p.returnOpenOrders(currencyPair=TICKER)[0]['orderNumber']
                close = p.cancelOrder(orderNumber=order_n)  # удаляем нулевой ордер в списке по его номеру на бирже
                print('Удален ордер N: ' + str(order_n))
                print(close)
            except Exception:
                print('')
            j += 1
            time.sleep(0.2)

        print(colored('ЗАПУСК МОДУЛЯ УСТАНОВКИ BUY ОРДЕРОВ', 'green', attrs=['bold']))
        func_buy1()
        time.sleep(0.2)
    else:
        print(colored('ПОДНЯТИЕ ОРДЕРОВ К BIDS НЕ ТРЕБУЕТСЯ', 'green', attrs=['bold']))
        print("BIDS STOP")
        time.sleep(0.2)


def main():
    print(colored('Блок проверки сосотояния и вызова функций', 'yellow', attrs=['bold']))
    time_n = datetime.datetime.now()
    print(colored('            ' + time_n.strftime("%d-%m-%Y %H:%M:%S"), 'cyan', 'on_grey'))

    bb1 = p.returnBalances()[coin1]
    bb2 = p.returnBalances()[coin2]

    print(colored('Пара: ' + str(coin1) + ' - ' + str(coin2), 'blue', attrs=['bold']))
    print('')
    print(colored('Баланс ' + str(coin1) + ': ' + str(bb1), 'green', attrs=['bold']))
    print(colored('Баланс ' + str(coin2) + ': ' + str(bb2), 'yellow', attrs=['bold']))
    print('')
    print('Block 3')

    config = ConfigObj('config.ini', encoding='utf8')
    interval_info = config['interval-info']['f']
    TradeHistory = p.returnTradeHistory(currencyPair=TICKER)
    th_len = len(TradeHistory)
    print('th_len: ' + str(th_len))
    OpenOrders = p.returnOpenOrders(currencyPair=TICKER)
    open_orders_len = len(OpenOrders)
    cash_1 = float(p.returnBalances()[coin1])
    OrderRate = config['order_rate']['or']
    print('Block 4')

    if th_len > 0:  # P1
        print('P1 start')
        cash_2 = float(p.returnBalances()[coin2])
        th_type = p.returnTradeHistory(currencyPair=TICKER)[0]['type']
        print("Тип последнего ордера ", str(th_type))
        print('P1 stop')
        if th_type == 'buy':  # P2
            print('P2 start')
            if cash_2 > 0:
                func_buy2()
        #     cash_2 = float(p.returnBalances()[coin2])
        #     CurrentPrice = p.returnOrderBook(currencyPair=TICKER)['bids'][0][0]
        #     print('cash2 ', cash_2)
        #     j = float(cash_2) * float(CurrentPrice)
        #     print(f"j = {j}, P2 stop")
        #     if float(cash_2) > 0 and j >= 0.00001:  # P3
        #         print('P3 start')
        #         print('есть монеты продаем')
        #         func_sell()
        #         print('Функция Sell отработала')
        #         print('P3 stop')
        #     else:  # P4
        #         print('P4 start')
        #         func_buy2()
        #         print('P4 stop')
        elif th_type == 'sell' and open_orders_len > 0:  # P5
            print('P5 start')
            print(colored('ОРДЕР SELL ИСПОЛНЕН', 'green', attrs=['bold']))
            print('')
            print(colored('ЗАПУСКАЕМ МОДУЛЬ ПЕРЕСТРОЕНИЯ ОРДЕРОВ', 'green', attrs=['bold']))
            print('Проверка отступа от BIDS')
            func_bids()
            print('P5 stop')
        elif th_type == 'sell' and open_orders_len == 0:  # P6
            print('P6 start')
            print(colored('ОРДЕР SELL ИСПОЛНЕН', 'green', attrs=['bold']))
            print('')
            if cash_2 <= 0.00001:
                print(colored('ОТКРЫТЫХ BUY ОРДЕРОВ НЕТ, ЗАПУСК МОДУЛЯ УСТАНОВКИ ПЕРВЫХ ОРДЕРОВ', 'green', attrs=['bold']))
                func_buy1()
                print('P6 stop')
    
    elif open_orders_len < 1 and float(cash_1) >= float(OrderRate):  # P7
        print('P7 start')
        func_buy1()
        print('P7 stop')

    elif th_len == 0:
        print('ВЫПОЛНЯЕМ ПРОВЕРКУ УРОВНЯ ОРДЕРОВ К BIDS')
        func_bids()

    else:
        print(colored('МОНИТОРИНГ', 'green', attrs=['bold']))
        print('')
        print(colored('Пара: ' + str(coin1) + ' - ' + str(coin2), 'blue', attrs=['bold']))
        print(' ')
    config = ConfigObj('config.ini', encoding='utf8')
    print(colored('LAST_STEP: ' + config['last_step']['ls'], 'blue', attrs=['bold']))
    print('Конец цикла')
    # log_start()
    print(' ')


if __name__ == '__main__':
    cycle = 0
    while True:
        print("main START")
        try:
            main()
            print(colored('----------------- Цикл: ' + str(cycle) + ' ---------------------', 'red', 'on_grey',
                          attrs=['bold']))
            cycle += 1
            count = 7
            print(" ")
            timer(10)
        except Exception:
            time.sleep(5)
            continue
