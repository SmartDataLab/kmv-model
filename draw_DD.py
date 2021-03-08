from my_kmv import get_final_res_from_code
import matplotlib.pyplot as plt
import pickle as pk

mode = "v2"
code = "601398.SH"


midx = pk.load(open("data/midx.pk","rb"))
midy = pk.load(open("data/midy.pk","rb"))
import random
#a = np.polyfit(samplex, sampley, 3)
#b = np.poly1d(a)
def b(dd,midx,midy):
    epsilon = random.random() * 0.05
    if dd >= midx[0] and dd < midx[19]:
        for i in range(0,18):
            if dd >= midx[i] and dd < midx[i+1]: 
                y = midy[i] + (dd - midx[i]) * (midy[i+1] - midy[i]) / (midx[i+1] - midx[i])
                return y + epsilon if y == 0.0 else y
    else: return epsilon

#短
code_dict = {"重庆银行": "01963",
    "甘肃银行": "02139",
    "徽商银行": "03698",
    "晋商银行": "02558",
    "威海银行": "09677",
    "哈尔滨银行": "06138",
    "贵州银行": "06199",
    "江西银行": "01916",
    "九江银行": "06190",
    "盛京银行": "02066",
    "中原银行": "01216",
    "锦州银行": "00416",
    "泸州银行": "01983",
    "天津银行": "01578",
    "上海银行": "601229.SH",
    "无锡银行": "600908.SH",
    "江苏银行": "600919.SH",
    "杭州银行": "600926.SH",
    "贵阳银行": "601997.SH",
    "南京银行": "601009.SH",
    "北京银行": "601169.SH",
    "宁波银行": "002142.SZ",
    "郑州银行": "002936.SZ",
    "青岛银行": "002948.SZ",
    "苏州银行": "002966.SZ",
    "西安银行": "600928.SH",
    "厦门银行": "601187.SH",  # api没有数据
    "长沙银行": "601577.SH",
    "成都银行": "601860.SH"
}
# TODO(sujinhua):

for name, code in code_dict.items():
    iter_, delta_, df = get_final_res_from_code(code, "20100101", "20201201", mode)
    df["EDF"] = df["DD"].apply(lambda x: b(x,midx,midy))
    df["date"] = df.index
    df.to_csv("data_chang/{name}_{code}_kmv_raw_res.csv".format(name=name, code=code))
    df.describe().to_csv("data_chang/{name}_{code}_describe.csv".format(name=name, code=code))
    figure = plt.figure()
    df["VA"].hist()
    plt.savefig("figure_chang/{name}_{code}_VA_hist.png".format(name=name, code=code))
    plt.close()
    figure = plt.figure()
    df["DD"].hist()
    plt.savefig("figure_chang/{name}_{code}_DD_hist.png".format(name=name, code=code))
    plt.close()
    figure = plt.figure()
    df["EDF"].hist()
    plt.savefig("figure_chang/{name}_{code}_EDF_hist.png".format(name=name, code=code))
    plt.close()
    figure = plt.figure()
    df["VA(1e11)"] = df["VA"] / 1e11
    df["EDF(%)"] = df["EDF"] * 100
    df[["VA(1e11)", "close", "EDF(%)"]].plot()
    plt.savefig("figure_chang/{name}_{code}_price_VA.png".format(name=name, code=code))
    plt.close()
