from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.id_to_stock = {}
        self.stock_dict = {}

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

    def updatePortfolio(self, contract: Contract, position: int,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        super().updatePortfolio(contract, position, marketPrice, marketValue,
                                averageCost, unrealizedPNL, realizedPNL, accountName)
        print("Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:",
            contract.exchange, "Position:", position, "MarketPrice:", marketPrice,
            "MarketValue:", marketValue, "AverageCost:", averageCost)
        self.stock_dict[contract.symbol] = [marketPrice,position]
    
    def tickPrice(self, reqId, tickType, price, attrib):
        print('The current ask price is: ', price)
        self.stock_dict[self.id_to_stock[reqId]] = [price,0]
    
    def setStockId(self,i,tic):
        self.id_to_stock[i] = tic

    def getStockData(self):
        return self.stock_dict


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

def get_stock_info(app,ticker_list,accountid,demo=True):
    def run_loop():
	    app.run()

    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    # Check if the API is connected via
    while True:
        if isinstance(app.nextorderId, int):
            break
        else:
            print('waiting for connection')
            time.sleep(1)
    acc_type = 3 if demo else 1
    for i,tic in enumerate(ticker_list):
        contract = Stock_contract(str(tic))
        app.setStockId(i,tic)
        app.reqMarketDataType(acc_type)
        app.reqMktData(i, contract, '', demo, False, [])
        time.sleep(1)
    
    #get information for stocks currently in the portfolio
    app.reqAccountUpdates(True,accountid)
    time.sleep(2)

    return app.getStockData()