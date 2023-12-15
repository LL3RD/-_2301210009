# 代码说明

## 回测代码 `mysystem/backtest.py`

@classmethod
## def signal(cls,indicate,buy_sig=1,sell_sig=-1):
从指标indicate生成买卖信号：
如果未持仓，则当信号大于buy_sig时候买入。
如果持仓，则当信号小于sell_sig卖出

@classmethod
## def crosssection(cls,signal,price,fee=False):
计算的signal信号，生成P&L，fee可以设定为0.0002即为双边万二的手续费


@classmethod
## def evaluate(cls,P_L,r_f=0.0267,index='sh000300'):
分析P_L，可以设置无风险利率r_f，可以设置不同的指数index，或者输入价格即可
计算P_L需要联网，因为要使用ak库导入index数据，若未联网，需要index=index_price

注意：：所有的数据都需要完整数据。

## 生成指标代码 `mysystem/indicate.py`
生成不同的指标

## 示例 `test.ipynb`
提供代码例子
