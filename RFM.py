import numpy
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# data = pd.read_excel('/Users/liumingxin/Downloads/ce.xls')
# data['DateDiff'] = (pd.to_datetime(data['today']) - pd.to_datetime(data['DealDateTime']))
# data['DateDiff'] = data['DateDiff'].dt.days
# R_Agg = data.groupby(by=['CustomerID'])['DateDiff'].agg(numpy.min).to_frame()
# R_Agg.columns = ['Recency']
# F_Agg = data.groupby(by=['CustomerID'])['OrderID'].agg(numpy.size).to_frame()
# F_Agg.columns = ['Frequency']
# M_Agg = data.groupby(by=['CustomerID'])['Sales'].agg(numpy.sum).to_frame()
# M_Agg.columns = ['Monetary']
# aggData = R_Agg.join(F_Agg).join(M_Agg)
# print(aggData)
aggData = pd.read_excel('user_RFM.xlsx',index_col="CustomerID")
scaler = MinMaxScaler()
aggData['rankR'] = 1-scaler.fit_transform(aggData['Recency'].values.reshape(-1, 1))
aggData['rankF'] = scaler.fit_transform(aggData['Frequency'].values.reshape(-1, 1))
aggData['rankM'] = scaler.fit_transform(aggData['Monetary'].values.reshape(-1, 1))
aggData['rankRFM'] = 0.5 * aggData['rankR'] .astype(int) + 0.3 * aggData['rankF'].astype(int) + 0.2 * aggData['rankM'].astype(int)
print(aggData.head())
binRs = [-0.1, aggData['rankR'].mean(), 1.1]
aggData['R_S'] = pd.cut(aggData.rankR, binRs, labels=[1, 2])
binFs = [-0.1, aggData['rankF'].mean(), 1.1]
aggData['F_S'] = pd.cut(aggData.rankF, binFs, labels=[1, 2])
binMs = [-0.1, aggData['rankM'].mean(), 1.1]
aggData['M_S'] = pd.cut(aggData.rankM, binMs, labels=[1, 2])
print(aggData.head())
def fun(a,b,c):
    if (a == 2) & (b == 2) & (c == 2):
            return '高价值用户'
    if (a == 1) & (b == 2) & (c == 2):
            return '重点保持客户'
    if (a == 2) & (b == 1) & (c == 2):
            return '重点发展客户'
    if (a == 1) & (b == 1) & (c == 2):
            return '重点挽留客户'
    if (a == 2) & (b == 2) & (c == 1):
            return '重点保护客户'
    if (a == 1) & (b == 2) & (c == 1):
            return '一般保护客户'
    if (a == 2) & (b == 1) & (c == 1):
            return '一般发展客户'
    if (a == 1) & (b == 1) & (c == 1):
            return '潜在客户'
aggData['RFM'] = aggData.apply(lambda x:fun(x.R_S, x.F_S,x.M_S), axis = 1)
aggData.reset_index(level=0, inplace=True)
aggData = aggData.astype({'CustomerID': 'str'})
print(aggData.head(10))
aggData.to_excel("RFM_result.xlsx")


