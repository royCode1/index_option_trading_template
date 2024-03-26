from urllib import response
from fyers_apiv3.FyersWebsocket import data_ws
from fyers_apiv3 import fyersModel
from pprint import pprint
from pprint import pprint
from flask import Flask, request
import threading
import json
import helper_fyers as helper

##############################################
#                   INPUT's                  #
##############################################
app_id = open("fyers_client_id.txt",'r').read()
access_token = open("fyers_access_token.txt",'r').read()
fyers = fyersModel.FyersModel(token=access_token,is_async=False,client_id=app_id)

ltpDict={}

instrumentList = [
                  "NSE:NIFTYBANK-INDEX"
                  ]

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/ltp')
def getLtp():
    print(ltpDict)
    ltp = -1
    instrument = request.args.get('instrument')
    try:
        ltp = ltpDict[instrument]
    except Exception as e :
        print("EXCEPTION occured while getting ltpDict()")
        print(e)
    return str(ltp)

def onmessage(message):
    global ltpDict
    ltpDict[message['symbol']] = message['ltp']
    print(ltpDict)

def onerror(message):
    print("")

def onclose(message):
    print("Connection closed:", message)

def onopen():
    print("Connection opened")

def startServer():
    print("Inside startServer()")
    app.run(host='0.0.0.0', port=4001)

# Replace the sample access token with your actual access token obtained from Fyers
access_token_websocket = app_id + ":" + access_token

def main():
    print("Inside main()")
    t1 = threading.Thread(target=startServer)
    t1.start()

    access_token_websocket = app_id + ":" + access_token

    fyers = data_ws.FyersDataSocket(access_token=access_token_websocket,
                                    write_to_file=False,
                                    reconnect=True,
                                    on_connect=onopen,
                                    on_close=onclose,
                                    on_error=onerror,
                                    on_message=onmessage,
                                    log_path="./")

    fyers.connect()

    # Specify the data type and symbols you want to subscribe to
    data_type = "SymbolUpdate"

    # Subscribe to the specified symbols and data type
    fyers.subscribe(symbols=instrumentList, data_type=data_type)

    # Keep the socket running to receive real-time data
    fyers.keep_running()

    t1.join()
    print("websocket started !!")

main()
