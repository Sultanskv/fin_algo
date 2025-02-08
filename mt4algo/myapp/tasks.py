# from celery import shared_task
# import subprocess

# @shared_task
# def place_order_task(mt5_path, login, server, password, symbol, lot, order_type_str, stop_loss, take_profit):
#     result = subprocess.check_output(["python", r"C:\Users\pc\Documents\sahil\algosms\myapp\execure_order.py", mt5_path, str(login), server, password, symbol, str(lot), order_type_str, str(stop_loss), str(take_profit)])
#     return result

# @shared_task
# def close_all_orders_task(mt5_path, login, server, password):
#     result = subprocess.check_output(["python", r"C:\Users\pc\Documents\sahil\algosms\myapp\close_all_orders.py", mt5_path, str(login), server, password])
#     return result

# from celery import shared_task
# import subprocess
# import pandas as pd
# import datetime
# from .models import ClientDetail, TradeHistory

# @shared_task
# def fetch_trade_data():
#     now = datetime.datetime.now()
#     start_time = now - datetime.timedelta(days=30)  # Adjust as needed

#     clients = ClientDetail.objects.exclude(mt5_login=None)
    
#     for client in clients:
#         # Fetch open trades
#         result = subprocess.check_output(["python", r"C:\Users\pc\Documents\sahil\algosms\myapp\get_open_trades.py", mt5_path, str(client.mt5_login), client.mt5_server, client.mt5_password])
#         with open(r"C:\Users\pc\Documents\sahil\algosms\myapp\open_trades.pkl", 'rb') as f:
#             open_trades = pickle.load(f)
        
#         for trade in open_trades:
#             TradeHistory.objects.update_or_create(
#                 client=client,
#                 ticket=trade['ticket'],
#                 defaults={
#                     'time': datetime.datetime.fromtimestamp(trade['time']),
#                     'symbol': trade['symbol'],
#                     'volume': trade['volume'],
#                     'trade_type': 'OPEN',
#                     'price': trade['price_open'],
#                     'sl': trade['sl'],
#                     'tp': trade['tp'],
#                     'profit': trade['profit']
#                 }
#             )

#         # Fetch trade history
#         result = subprocess.check_output(["python", r"C:\Users\pc\Documents\sahil\algosms\myapp\get_history.py", mt5_path, str(client.mt5_login), client.mt5_server, client.mt5_password])
#         with open(r"C:\Users\pc\Documents\sahil\algosms\myapp\history.pkl", 'rb') as f:
#             history = pickle.load(f)
        
#         for trade in history:
#             TradeHistory.objects.update_or_create(
#                 client=client,
#                 ticket=trade['ticket'],
#                 defaults={
#                     'time': datetime.datetime.fromtimestamp(trade['time']),
#                     'symbol': trade['symbol'],
#                     'volume': trade['volume'],
#                     'trade_type': trade['type'],
#                     'price': trade['price'],
#                     'sl': trade.get('sl'),
#                     'tp': trade.get('tp'),
#                     'profit': trade['profit'],
#                     'change': trade.get('change')
#                 }
#             )

            
# from celery import shared_task
# from .mt5_functions import monitor_and_update_closed_trades

# @shared_task
# def monitor_trades_real_time():
#     monitor_and_update_closed_trades()

# tasks.py



# tasks.py

from celery import shared_task
from .models import ClientDetail
from myapp.mt5_sync import update_closed_trades_for_client

@shared_task
def update_all_closed_trades():
    clients = ClientDetail.objects.filter(mt5_login__isnull=False)
    for client in clients:
        update_closed_trades_for_client(client)

