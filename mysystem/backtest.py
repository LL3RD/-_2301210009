import pandas as pd
import numpy as np
import akshare as ak
from matplotlib import pyplot as plt

class backtest(object):
    def __init__(self):
        pass

    @classmethod
    def signal(cls,indicate,buy_sig=1,sell_sig=-1):
        signal=pd.DataFrame(np.zeros(len(indicate)),columns=['signal'],index=indicate.index)

        for i in range(len(signal)-1):
            if signal.iloc[i,0]==0:
                if indicate.iloc[i+1]>buy_sig:
                    signal.iloc[i+1,0]=1
                else:
                    signal.iloc[i+1,0]=0

            if signal.iloc[i,0]==1:
                if indicate.iloc[i+1]<sell_sig:
                    signal.iloc[i+1,0]=0
                else:
                    signal.iloc[i+1,0]=1

        return signal['signal']

    @classmethod
    def crosssection(cls,signal,price,fee=False):
        P_L=pd.DataFrame(columns=['P_L'],index=signal.index)
        P_L.iloc[0,0]=1
        for i in range(len(P_L)-1):
            if signal.iloc[i+1]==0:
                P_L.iloc[i+1,0]=P_L.iloc[i,0]
            if signal.iloc[i+1]==1:
                P_L.iloc[i+1,0]=P_L.iloc[i,0]*price.iloc[i+1]/price.iloc[i]
            if fee:
                if signal.iloc[i+1]!=signal.iloc[i]:
                    P_L.iloc[i+1,0]=P_L.iloc[i+1,0]*(1-fee)

        return P_L['P_L']

    @classmethod
    def evaluate(cls,P_L,r_f=0.0267,index='sh000300'):
        
        DD=[0]
        for i in range(len(P_L)-1):
            DD.append(P_L.iloc[:i+1].max()-P_L.iloc[i+1])
        DD=np.max(DD)

        if type(index) is str:
            stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=index)
            stock_zh_index_daily_df['date']=pd.to_datetime(stock_zh_index_daily_df['date'])
            stock_zh_index_daily_df.set_index('date',inplace=True)
            index_price=stock_zh_index_daily_df['close'].loc[P_L.index]
        else:
            index_price=index.copy()
            index='index'

        index_P_L=pd.DataFrame(columns=['index_P_L'],index=index_price.index)
        index_P_L.iloc[0,0]=P_L.iloc[0]

        for i in range(len(index_price)-1):
            index_P_L.iloc[i+1,0]=index_P_L.iloc[i,0]*index_price.iloc[i+1]/index_price.iloc[i]
    
        index_P_L=index_P_L['index_P_L']

        plt.figure(figsize=[10,5])
        plt.plot(P_L)
        plt.plot(index_P_L)
        plt.legend(['P_L',index])
        plt.ylabel('return')
        plt.xlabel('time')
        plt.title('P_L')
        plt.show()
        
        excess_P_L=P_L-index_P_L
        plt.figure(figsize=[10,5])
        plt.plot(excess_P_L)
        plt.legend(['excess_P_L'])
        plt.ylabel('return')
        plt.xlabel('time')
        plt.title('excess_P_L')
        plt.show()


        return_rate=P_L.pct_change()

        indicator={}

        indicator['return_rate_year']=np.round(252*return_rate.mean(),4)
        indicator['volatility_year']=np.round(np.sqrt(252)*return_rate.std(),4)
        indicator['sharp_ratio']=np.round((252*return_rate.mean()-r_f)/(np.sqrt(252)*return_rate.std()),4)
        indicator['max_drawdown']=np.round(DD,4)

        for key, value in indicator.items():
            print(f'{key}: {value}')

        return
    


