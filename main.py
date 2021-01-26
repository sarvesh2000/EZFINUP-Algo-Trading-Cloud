from flask import Flask, request
import pandas as pd
import numpy as np
import pandas_datareader as pdr
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    stock = pdr.get_data_yahoo(request.args.get('stockname'))
    print("DF")
    print(stock)
    stock.reset_index(inplace=True, drop=False)
    # stock = df.reset_index()['Close']
    # print(stock)
    Sma30 = pd.DataFrame()
    Sma30['Prev Close Price'] = stock['Close'].rolling(window=10).mean()
    # Creating Simple Moving Average with 100-day Window
    Sma100 = pd.DataFrame()
    Sma100['Prev Close Price'] = stock['Close'].rolling(window=60).mean()
    data = pd.DataFrame()
    data['stock'] = stock['Close']
    data['Sma30'] = Sma30['Prev Close Price']
    data['Sma100'] = Sma100['Prev Close Price']

    def buy_sell(data):
        sigPriceBuy = []
        sigPriceSell = []
        flag = -1

        for i in range(len(data)):
            if data['Sma30'][i] > data['Sma100'][i]:
                if flag != 1:
                    sigPriceBuy.append(data['stock'][i])
                    sigPriceSell.append(np.nan)
                    flag = 1
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            elif data['Sma30'][i] < data['Sma100'][i]:
                if flag != 0:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(data['stock'][i])
                    flag = 0
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)

        return (sigPriceBuy, sigPriceSell)

    buy_sell = buy_sell(data)
    data['Buy_Signal_Price'] = buy_sell[0]
    data['Sell_Signal_Price'] = buy_sell[1]

    print("Stock")
    print(stock['Date'])


    # End Result in JSON
    result = {"dates": stock['Date'].dt.date.values.tolist(), "price": stock['Close'].values.tolist(), "SMA30": Sma30['Prev Close Price'].values.tolist(), "SMA100": Sma100['Prev Close Price'].values.tolist(), "buy_point": data['Buy_Signal_Price'].values.tolist(), "sell_point": data['Sell_Signal_Price'].values.tolist()}
    # print("Result\n")
    # print(result)
    return result

if __name__ == '__main__':
    app.run(debug=True)




