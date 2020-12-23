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

    code = code.split(".")[1].lower() + code.split(".")[0]
    # df2 = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    df2 = ak.stock_zh_a_daily(
        symbol=code, start_date=start_date, end_date=end_date, adjust="qfq"
    )

    df2["total_liab"] = None
    df2["total_share"] = None
    df2["total_hldr_eqy_inc_min_int"] = None

    for date_str in df2.index:
        (
            df2["total_liab"],
            df2["total_share"],
            df2["total_hldr_eqy_inc_min_int"],
        ) = find_total_liab(date_str.strftime("%y%m%d"), df)

    return df2


if __name__ == "__main__":
    code = "601398.SH"
    df = get_real_data(code, "20180101", "20201210")
    print(df)


# %%
