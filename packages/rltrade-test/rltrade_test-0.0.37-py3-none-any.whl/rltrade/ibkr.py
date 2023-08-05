from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)

	def nextValidId(self, orderId: int):
		super().nextValidId(orderId)
		self.nextorderId = orderId
		print('The next valid order id is: ', self.nextorderId)

	def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
		print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
	def openOrder(self, orderId, contract, order, orderState):
		print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

	def execDetails(self, reqId, contract, execution):
		print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


def Stock_contract(symbol, secType='STK', exchange='SMART', currency='USD'):
	''' custom function to create stock contract '''
	contract = Contract()
	contract.symbol = symbol
	contract.secType = secType
	contract.exchange = exchange
	contract.currency = currency
	return contract

def api_connect(demo=True):
    app = IBapi()
    app.nextorderId = None
    if demo:
        app.connect('127.0.0.1', 7497, 123)
    else:
        app.connect('127.0.0.1', 7496, 123)
    return app


def buy_stock(app,ticker,quantity):
    
    def run_loop():
	    app.run()

    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    # Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
            break
        else:
            print('waiting for connection')
            time.sleep(1)

    #Create order object
    order = Order()
    order.action = 'BUY'
    order.totalQuantity = quantity
    order.orderType = 'MKT'

    #Place order
    app.placeOrder(app.nextorderId, Stock_contract(ticker), order)
    app.nextorderId += 1
    time.sleep(2)

def sell_stock(app,ticker,quantity):
    def run_loop():
	    app.run()

    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    # Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
            break
        else:
            print('waiting for connection')
            time.sleep(1)

    #Create order object
    order = Order()
    order.action = 'SELL'
    order.totalQuantity = quantity
    order.orderType = 'MKT'

    #Place order
    app.placeOrder(app.nextorderId, Stock_contract(ticker), order)
    app.nextorderId += 1
    time.sleep(2)