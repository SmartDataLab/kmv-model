import akshare as ak
import pandas as pd


def get_real_hk_data(code):
    index_map_dict = {
        "资产": "total_assets",
        "负债": "total_liab",
        "股东权益": "total_hldr_eqy_inc_min_int",
        "流通股本": "outstanding_share",
        "总股本": "total_share",
        "净利润": "profit_to_op",
        "投资回报率": "roe_dt",
    }
    # df = pro.balancesheet(ts_code=code, start_date=start_date, end_date=end_date)
    df = pd.read_excel("data/上市城商行信息表.xlsx")

    df2 = ak.stock_hk_daily(symbol=code, adjust="qfq")
    start_date = "20180101"
    end_date = "20201231"
    start_date_t = pd.datetime(
        int(start_date[:4]), int(start_date[4:6]), int(start_date[6:8])
    )
    end_date_t = pd.datetime(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:8]))
    idxs = [
        x
        for x in df2.index
        if (x - start_date_t).days >= 0 and (x - end_date_t).days <= 0
    ]
    df2 = df2.loc[idxs, :]
    df.index = df["股票代码"]
    idx_dict = {}
    idx_2018 = [x for x in df2.index if x.strftime("%Y") == "2018"]
    idx_2019 = [x for x in df2.index if x.strftime("%Y") == "2019"]
    idx_2020 = [x for x in df2.index if x.strftime("%Y") == "2020"]
    idx_dict = {"2018": idx_2018, "2019": idx_2019, "2020": idx_2020}
    for year, idx in idx_dict.items():
        for zh_index, en_index in index_map_dict.items():
            df2.loc[idx, en_index] = df.loc[int(code), year + zh_index]
    return df2


# %%
if __name__ == "__main__":
    print(get_real_hk_data("01983"))
# %%
