import logging
import pandas as pd
from fyers_apiv3 import fyersModel
from core import FyersWS
from core.utlis import Logger
from multiprocessing import Queue
from ta.momentum import RSIIndicator
from threading import Thread
from datetime import datetime , timedelta
import time
import json



class Strategy():
    def __init__(self, appid, accesstoken):
        self.appid = appid
        self.accesstoken = accesstoken

        self.StrategyName = 'RsiGmrInfra'
        self.TradeBookPath = f'TradeBooks/{self.StrategyName}.csv'
        self.respQueue = Queue()
        self.logpath = 'LogFiles'
        self.token = 'NSE:GMRINFRA-EQ'
        self.TimeFrame = 1
        self.qty = 1

        self.Trade = False
        self.TradeInfo = {
            "symbol":self.token,
            "qty":self.qty,
            "EntryTime":None,
            "EntryPrice":0,
            "ExitTime":None,
            "ExitPrice":0,
            "PnL":0
        }
        self.currentTradeInfo = self.TradeInfo.copy()
        self.TradeBook = pd.DataFrame(columns=['Symbol','Qty','EntryTime', 'ExitTime', 'EntryPrice', 'ExitPrice', 'PnL'])

        self.Target = 0.5
        self.StopLoss = 0.5

        self.fyersWS = FyersWS(self.accesstoken, self.appid, self.respQueue,tokens=[self.token], logpath = self.logpath)
        self.fyersAPI = fyersModel.FyersModel(client_id=self.appid, token=self.accesstoken, log_path=self.logpath)
        self.fyersThread = None

        self.logger = Logger(self.logpath, self.StrategyName).logger


    def start(self):
        """
        Start the Fyers Websocket
        :return:
        """
        self.fyersThread = Thread(target = self.fyersWS.connect)
        self.fyersThread.start()
        self.logger.info("FyersWS Started")

    def stop(self):
        """
        Stop the Fyers Websocket
        :return:
        """
        self.fyersWS.disconnect()
        self.fyersThread.join()
        self.fyersThread = None
        self.logger.info("FyersWS Stopped")

    def adjustments(self):
        """
        Adjust the trade based on the current market conditions

        :return:
        """
        while True:
            message = self.respQueue.get()
            if (message['Symbol'] == self.token) & (self.Trade):
                current_profit = (message['Data']['ltp'] - self.currentTradeInfo['EntryPrice'])
                self.logger.info(f"Current Profit: {current_profit}")
                current_time = datetime.now()
                if (current_profit >= self.Target):
                    self.order_execution(data = self.order_format('SELL'), side='SELL')
                    self.logger.info(f"Trade Closed at {current_profit} Reason: Target Hit")
                if (current_profit <= -self.StopLoss):
                    self.order_execution(data = self.order_format('SELL'), side='SELL')
                    self.logger.info(f"Trade Closed at {current_profit} Reason: StopLoss Hit")
                if (current_time - self.currentTradeInfo['EntryTime']).seconds > 180:
                    self.order_execution(data = self.order_format('SELL'), side='SELL')
                    self.logger.info(f"Trade Closed at {current_profit} Reason: Time Limit Reached")

    def EntryConditions(self):
        """
        Entry Conditions for the trade
        :return:
        """
        data = {
            "symbol":self.token,
            "resolution":self.TimeFrame,
            "date_format":"0",
            "range_from":int((datetime.now() - timedelta(days=3)).timestamp()),
            "range_to":int(datetime.now().timestamp()),
            "cont_flag":"0"
        }
        response = self.fyersAPI.history(data=data)
        if response['code'] == 200:
            candles = pd.DataFrame(response['candles'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            candles['RSI'] = RSIIndicator(candles['close'], window=14).rsi()
            if candles['RSI'].iloc[-1] < 50:
                self.order_execution(data = self.order_format('BUY'), side='BUY')
                self.logger.info(f"Trade Opened for {self.token} Reason: RSI < 50")

    def ExitConditions(self):
        """
        Exit Conditions for the trade
        :return:
        """
        data = {
            "symbol":self.token,
            "resolution":self.TimeFrame,
            "date_format":"0",
            "range_from":int((datetime.now() - timedelta(days=3)).timestamp()),
            "range_to":int(datetime.now().timestamp()),
            "cont_flag":"0"
        }
        response = self.fyersAPI.history(data=data)
        if response['code'] == 200:
            candles = pd.DataFrame(response['candles'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            candles['RSI'] = RSIIndicator(candles['close'], window=14).rsi()
            if candles['RSI'].iloc[-1] > 50:
                self.order_execution(data = self.order_format('SELL'), side='SELL')
                self.logger.info(f"Trade Closed for {self.token} Reason: RSI > 50")

    def order_format(self,side='BUY'):
        """
        Format the order data
        :param side:
        :return:
        """
        side = 1 if side == 'BUY' else -1
        return {
            "symbol": self.token,
            "qty": self.qty,
            "type": 2,
            "side": side,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "stopLoss": 0,
            "takeProfit": 0,
            "offlineOrder": False,
            "disclosedQty": 0 }

    def order_execution(self, data, side='BUY'):
        """
        Execute the order
        :param data: order data
        :param side:  BUY/SELL
        :return:
        """
        order_ex = self.fyersAPI.place_order(data)
        order_id = order_ex['id']
        self.logger.info(f"Order Placed side: {side} with order id {order_id}")
        while True:
            data = {"id":order_id}
            response = self.fyersAPI.orderbook(data=data)
            if response['code'] == 200:
                order_status =  response['orderBook'][0]['status']
                if order_status == 2:
                    self.logger.info(f"Order executed {side} for {self.token} with order id {order_id} at {response['orderBook'][0]['tradedPrice']}")
                    if side == 'BUY':
                        self.currentTradeInfo['EntryTime'] = datetime.now()
                        self.currentTradeInfo['EntryPrice'] = response['orderBook'][0]['tradedPrice']
                        self.logger.info(f"Entry : {self.currentTradeInfo}")
                        self.Trade = True
                    else:
                        self.currentTradeInfo['ExitTime'] = datetime.now()
                        self.currentTradeInfo['ExitPrice'] = response['orderBook'][0]['tradedPrice']
                        self.currentTradeInfo['PnL'] = self.currentTradeInfo['ExitPrice'] - self.currentTradeInfo['EntryPrice']
                        self.logger.info(f"Exit : {self.currentTradeInfo}")
                        self.Trade = False
                    break
                elif order_status == 5:
                    print(f"Order rejected for {self.token} with order id {order_id}")
                    self.logger.info(f"Order rejected for {self.token} with order id {order_id}")
                    break
                time.sleep(1)

    def run(self):
        """
        Run the strategy
        :return:
        """
        self.start()
        # run adjustments in parallel
        adjustments_thread = Thread(target=self.adjustments)
        adjustments_thread.start()

        # Main Loop
        current_time = datetime.now()
        start_time = current_time.replace(hour=9, minute=15, second=0, microsecond=0)
        end_time = current_time.replace(hour=15, minute=30, second=0, microsecond=0)

        while (current_time < end_time and current_time > start_time):
            if int(time.time()) % 60 == 0:
                print(current_time)
                if not self.Trade:
                    self.EntryConditions()
                else:
                    self.ExitConditions()
                    self.TradeBook.loc[len(self.TradeBook)] = [self.self.currentTradeInfo['EntryTime'], self.currentTradeInfo['ExitTime'], self.currentTradeInfo['EntryPrice'], self.currentTradeInfo['ExitPrice'], self.currentTradeInfo['PnL']]
                    self.TradeBook.to_csv(self.TradeBookPath, index=False)
                    self.currentTradeInfo = self.TradeInfo.copy()
                time.sleep(3)
            current_time = datetime.now()

if __name__ == "__main__":
    config = json.load(open('user.json'))
    appid = config['user']['app_id']
    accesstoken = config['user']['access_token']
    strategy = Strategy(appid, accesstoken)
    strategy.run()