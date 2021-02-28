#%%
from my_kmv import get_final_res_from_code
from tqdm import tqdm


def get_average_data(codes, start_date, end_date):
    mode = "v2"
    big_df = None
    for i, code in tqdm(enumerate(codes)):
        if i == 0:
            _, _, big_df = get_final_res_from_code(
                code, start_date, end_date, mode=mode
            )
        else:
            try:
                _, _, df = get_final_res_from_code(
                    code, start_date, end_date, mode=mode
                )
            except:
                print(code, "have no data")
                continue
            index = [
                x.strftime("%Y-%m-%d")
                for x in set(list(big_df.index)).intersection(set(list(df.index)))
            ]
            big_df.loc[index, :] = (i + 1) / (i + 2) * big_df.loc[index, :] + 1 / (
                i + 2
            ) * df.loc[index, :]
            # big_df = big_df.loc[index, :]
            # df = df.loc[big_df.index, :]
            # for column in big_df.columns:
            # big_df[column] += df[column]
    # for column in big_df.columns:
    # big_df[column] /= i + 1
    return big_df


#%%

code_dict = {
    "宁波银行": "002142.SZ",
    "郑州银行": "002936.SZ",
    "青岛银行": "002948.SZ",
    "苏州银行": "002966.SZ",
    "无锡银行": "600908.SH",
    "江苏银行": "600919.SH",
    "杭州银行": "600926.SH",
    "西安银行": "600928.SH",
    "南京银行": "601009.SH",
    "北京银行": "601169.SH",
    # "厦门银行": "601187.SH", api没有数据
    "上海银行": "601229.SH",
    "长沙银行": "601577.SH",
    "成都银行": "601860.SH",
    # "重庆银行": "601963.SH", api没有数据
    "贵阳银行": "601997.SH",
}
mean_df = get_average_data(code_dict.values(), "20100101", "20191231")
#%%


def get_baoshang_data(mean_df):
    df = mean_df.copy()
    average_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "outstanding_share",
        "turnover",
    ]
    data_dict = {
        2010: {
            "total_liab": 94077126000,
            "total_share": 6817532000 / 2.65,
            "total_hldr_eqy_inc_min_int": 6817532000,
            "profit_to_op": 68175332000 * 0.3,
            "total_assets": 114752653000,
            "roe_dt": 28.92,
        },
        2011: {
            "total_liab": 110393512000,
            "total_share": 15830247000 / 3.93,
            "total_hldr_eqy_inc_min_int": 15830247000,
            "profit_to_op": 15830247000 * 0.25,
            "total_assets": 175123593000,
            "roe_dt": 21.57,
        },
        2012: {
            "total_liab": 122974239000,
            "total_share": 17990182000 / 4.47,
            "total_hldr_eqy_inc_min_int": 17990182000,
            "profit_to_op": 2845104000,
            "total_assets": 207618288000,
            "roe_dt": 13.22,
        },
        2013: {
            "total_liab": 148561814000,
            "total_share": 19330421000 / 4.82,
            "total_hldr_eqy_inc_min_int": 19330421000,
            "profit_to_op": 3046402000,
            "total_assets": 242556366000,
            "roe_dt": 12.44,
        },
        2014: {
            "total_liab": 169525744000,
            "total_share": 22457143000 / 5.58,
            "total_hldr_eqy_inc_min_int": 22457143000,
            "profit_to_op": 3744630000,
            "total_assets": 312864725000,
            "roe_dt": 13.81,
        },
        2015: {
            "total_liab": 177612954000,
            "total_share": 26235096000 / 5.93,
            "total_hldr_eqy_inc_min_int": 26235096000,
            "profit_to_op": 4470966000,
            "total_assets": 352595340000,
            "roe_dt": 14.05,
        },
        2016: {
            "total_liab": 193643281000,
            "total_share": 29799986000 / 6.11,
            "total_hldr_eqy_inc_min_int": 29799986000,
            "profit_to_op": 5507085000,
            "total_assets": 431582520000,
            "roe_dt": 15.11,
        },
        2017: {
            "total_liab": 540100000000 * 0.5,
            "total_share": 6817532000 / 2.65,
            "total_hldr_eqy_inc_min_int": 29799986000 + 5507085000 * 0.79,
            "profit_to_op": 5507085000 * 0.79,
            "total_assets": 540100000000,
            "roe_dt": 15.11 * 0.79,
        },
        2018: {
            "total_liab": 553400000000 * 0.7,
            "total_share": 6817532000 / 2.65,
            "total_hldr_eqy_inc_min_int": 29799986000
            + 5507085000 * 0.79
            + 5507085000 * 0.5,
            "profit_to_op": 5507085000 * 0.5,
            "total_assets": 550800000000,
            "roe_dt": 15.11 * 0.5,
        },
        2019: {
            "total_liab": 493200000000 * 0.8,
            "total_share": 6817532000 / 2.65,
            "total_hldr_eqy_inc_min_int": 29799986000
            + 5507085000 * 0.79
            + 5507085000 * 0.5
            + 5507085000 * 0.2,
            "profit_to_op": 5507085000 * 0.2,
            "total_assets": 523100000000,
            "roe_dt": 15.11 * 0.2,
        },
    }
    index = [x.strftime("%Y-%m-%d") for x in df.index]
    for year, data in data_dict.items():
        for column in data.keys():
            df.loc[[x for x in index if str(year) in x], column] = data[column]
    return df


# %%
baoshang_df = get_baoshang_data(mean_df)
# %%
from my_kmv import check_and_interpolate, get_iterated_result

mode = "v2"
p, e, d_short, d_long, outstanding_shares, total_shares, lever_ratio = (
    baoshang_df["close"],
    baoshang_df["total_hldr_eqy_inc_min_int"],
    baoshang_df["total_liab"] * 0.9,
    baoshang_df["total_liab"] * 0.1,
    baoshang_df["outstanding_share"]
    / mean_df["total_assets"]
    * baoshang_df["total_assets"],
    baoshang_df["total_share"],
    baoshang_df["total_liab"] / baoshang_df["total_hldr_eqy_inc_min_int"],
)
p = check_and_interpolate(p.astype("double"))
e = check_and_interpolate(e.astype("double"))
d_long = check_and_interpolate(d_long.astype("double"))
d_short = check_and_interpolate(d_short.astype("double"))
outstanding_shares = check_and_interpolate(outstanding_shares.astype("double"))
total_shares = check_and_interpolate(total_shares.astype("double"))
lever_ratio = check_and_interpolate(lever_ratio.astype("double"))
VA, sigmaA, iter_, DD, delta_ = get_iterated_result(
    p,
    e,
    d_short,
    d_long,
    lever_ratio,
    outstanding_shares,
    total_shares,
    100,
    1e-3,
    mode=mode,
)
baoshang_df["VA"] = VA
baoshang_df["sigmaA"] = sigmaA
baoshang_df["DD"] = DD
# %%
baoshang_df["sigmaA"].plot()
# %%
baoshang_df.to_csv("data/baoshang_res.csv")
# %%
import pickle as pk

b = pk.load(open("data/edf_fun.pk", "rb"))

mean_df["EDF"] = mean_df["DD"].apply(lambda x: b(x))
mean_df.to_csv("data/mean_EDF.csv")
# %%
