import tushare as ts
import numpy as np

with open('token.txt') as f:
    token = f.readline()

pro = ts.pro_api(token)

code = '601398.SH'
df = pro.balancesheet(ts_code=code, start_date = '20180101', end_date = '20180730')

print(df)

for column in df.columns:
    if not df[column][0] == None:
        print(column)

print(df['deriv_liab'])
print(df['oth_liab'])
print(df['total_liab'])

df2 = pro.daily(ts_code=code, start_date='20180101', end_date='20180730')
print(df2)