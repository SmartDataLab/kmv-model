from my_kmv import get_final_res_from_code
import matplotlib.pyplot as plt
import pickle as pk

mode = "v2"
code = "601398.SH"

b = pk.load(open("data/edf_fun.pk", "rb"))

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
    "厦门银行": "601187.SH",
    "上海银行": "601229.SH",
    "长沙银行": "601577.SH",
    "成都银行": "601860.SH",
    # "重庆银行": "601963.SH", api没有数据
    "贵阳银行": "601997.SH",
}

# TODO(sujinhua):

for name, code in code_dict.items():
    iter_, delta_, df = get_final_res_from_code(code, "20100101", "20201201", mode)
    df["EDF"] = df["DD"].apply(lambda x: b(x))
    df.to_csv("data/{name}_{code}_kmv_raw_res.csv".format(name=name, code=code))
    df.describe().to_csv("data/{name}_{code}_describe.csv".format(name=name, code=code))
    df
    figure = plt.figure()
    df["VA"].hist()
    plt.savefig("figure/{name}_{code}_VA_hist.png".format(name=name, code=code))
    plt.close()
    figure = plt.figure()
    df["DD"].hist()
    plt.savefig("figure/{name}_{code}_DD_hist.png".format(name=name, code=code))
    plt.close()
    figure = plt.figure()
    df["EDF"].hist()
    plt.savefig("figure/{name}_{code}_EDF_hist.png".format(name=name, code=code))
    plt.close()
    figure = plt.figure()
    df["VA(1e11)"] = df["VA"] / 1e11
    df["EDF(%)"] = df["EDF"] * 100
    df[["VA(1e11)", "close", "EDF(%)"]].plot()
    plt.savefig("figure/{name}_{code}_price_VA.png".format(name=name, code=code))
    plt.close()
