# %%
import tushare as ts
import numpy as np
import pandas as pd
import akshare as ak


with open("token.txt") as f:
    token = f.readline()


pro = ts.pro_api(token)


def get_real_data(code, start_date, end_date):
    global pro
    df = pro.balancesheet(ts_code=code, start_date=start_date, end_date=end_date)
    # profit_to_op
    df3 = pro.fina_indicator(ts_code=code, start_date=start_date, end_date=end_date)

    def find_total_liab(date_str, df):
        date_month = int(date_str[:6])
        for i in range(len(df)):
            end_date = df.loc[i, "end_date"]
            months_delta = int(end_date[:6]) - date_month
            if months_delta < 3 and months_delta >= 0:
                break
        return (
            df.loc[i, "total_liab"],
            df.loc[i, "total_share"],
            df.loc[i, "total_hldr_eqy_inc_min_int"],
        )

    def find_profit_to_op(date_str, df):
        date_month = int(date_str[:6])
        for i in range(len(df)):
            end_date = df.loc[i, "end_date"]
            months_delta = int(end_date[:6]) - date_month
            # print(int(end_date[:6]), date_month, months_delta)
            if months_delta < 3 and months_delta >= 0:
                break
        return df.loc[i, "profit_to_op"]

    code = code.split(".")[1].lower() + code.split(".")[0]
    # df2 = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    df2 = ak.stock_zh_a_daily(
        symbol=code, start_date=start_date, end_date=end_date, adjust="qfq"
    )

    df2["total_liab"] = None
    df2["total_share"] = None
    df2["total_hldr_eqy_inc_min_int"] = None
    df2["profit_to_op"] = None

    for i, date_str in enumerate(df2.index):
        input_str = "20" + date_str.strftime("%y%m%d")
        # print(input_str)
        (
            df2.loc[date_str, "total_liab"],
            df2.loc[date_str, "total_share"],
            df2.loc[date_str, "total_hldr_eqy_inc_min_int"],
        ) = find_total_liab(input_str, df)
        df2.loc[date_str, "profit_to_op"] = find_profit_to_op(input_str, df3)
    return df2


if __name__ == "__main__":
    code = "600519.SH"
    df = get_real_data(code, "20200601", "20201210")
    df.to_csv("%s.csv" % code)
    print(df)


# %%
