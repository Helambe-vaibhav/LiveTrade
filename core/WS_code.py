import time
from .utlis import Logger
from fyers_apiv3.FyersWebsocket import data_ws
from typing import List

class FyersWS():
    def __init__(self, acces_token:str, appid:str, respQueue, tokens :List[str] = [], logpath :str = ''):
        self.accessToken = appid + ":" + acces_token
        self.dataType = "SymbolUpdate"
        self.initTokens = tokens
        self.respQueue = respQueue
        self.logpath = logpath
        self.logger = Logger(logpath, 'FyersWS').logger

    def onMessage(self, message: dict):
        """
        This function is called when a message is received from the websocket

        Working:
        1. Check if the message type is 'if' or 'sf'
        2. Add the current timestamp to the message
        3. Remove the type from the message
        4. Put the message in the response queue

        :param message:
        :return:
        """
        try:
            if message.get("type") in ['if', "sf"] :
                message['current_timestamp'] = time.time()
                # remove type
                del message['type']
                self.respQueue.put({"Symbol": message['symbol'], "Data": message,'current_timestamp':message['current_timestamp']})
        except Exception as e :
            self.logger.exception(f"Error in on Message : {str(e)}" )

    def onError(self, message: str):
        """
        This function is called when an error is received from the websocket
        :param message:
        :return:
        """
        self.logger.debug(f"Error : {message}")

    def onClose(self, message: str):
        """
        This function is called when the connection is closed
        :param message:
        :return:
        """
        self.logger.debug(f"Close : {message}")

    def onOpen(self):
        """
        This function is called when the connection is opened
        :return:
        """
        self.Subscribe(self.initTokens)
        self.logger.info("Connection Opened")

    def disconnect(self):
        """
        This function is called to close the connection
        :return:
        """
        self.fyers.close_connection()
        self.logger.info("Connection Closed")

    def Subscribe(self, tokens: List[str]):
        """
        This function is called to subscribe to a list of tokens for the websocket
        :param tokens:
        :return:
        """
        try:
            self.fyers.subscribe(symbols=tokens, data_type=self.dataType)
            self.logger.info(f"Subscribed to {tokens}")
        except Exception as e :
            self.logger.exception(f"Error with Subscribe : {str(e)}")

    def Unsubscribe(self, tokens: List[str]):
        """
        This function is called to unsubscribe to a list of tokens for the websocket
        :param tokens:
        :return:
        """
        try:
            self.fyers.unsubscribe(symbols=tokens, data_type=self.dataType)
            self.logger.info(f"Unsubscribed to {tokens}")
        except Exception as e :
            self.logger.exception(f"Error with Unsubscribe : {str(e)}")

    def connect(self):
        """
        This function is called to establish the connection
        :return:
        """
        try:
            self.fyers = data_ws.FyersDataSocket(
                access_token=self.accessToken,
                log_path=self.logpath,
                litemode=False,
                write_to_file=False,
                reconnect=True,
                on_connect=self.onOpen,
                on_close=self.onClose,
                on_error=self.onError,
                on_message=self.onMessage,

            )
            self.fyers.connect()
            self.logger.info("Connection Established")
        except Exception as e :
            self.logger.exception(f"Error in connect : {str(e)}")