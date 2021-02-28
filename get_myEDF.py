#%%
from my_kmv import get_final_res_from_code


def get_tuple_list(codes, start_date, end_date):
    tuple_list = []
    mode = "v2"
    for code in codes:
        try:
            _, _, df = get_final_res_from_code(code, start_date, end_date, mode)
            tuple_list += list(zip(df["DD"], df["roe_dt"]))
        except:
            print(df["DD"], df["roe_dt"])
            print(code, "have failed")
    return tuple_list


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

tuple_list = get_tuple_list(code_dict.values(), "20100101", "20201231")
# %%
import matplotlib.pyplot as plt

plt.hist([x[0] for x in tuple_list])

# %%
plt.hist([x[1] for x in tuple_list])

# %%
range_list = [(-1 + i * 0.1, -0.9 + i * 0.1) for i in range(20)]
count_dict = {i: [0, 0] for i in range(-1, 21)}

for x in tuple_list:
    if x[0] * 1e8 <= range_list[0][0]:
        count_dict[-1][0] += 1
        if x[1] < 7.5:
            count_dict[-1][1] += 1
        continue
    if x[0] * 1e8 > range_list[-1][1]:
        count_dict[20][0] += 1
        if x[1] < 7.5:
            count_dict[20][1] += 1
        continue
    for j, range_ in enumerate(range_list):
        if x[0] * 1e8 > range_[0] and x[0] * 1e8 <= range_[1]:
            count_dict[j][0] += 1
            if x[1] < 7.5:
                count_dict[j][1] += 1
                break
count_dict
# %%
for key, value in count_dict.items():
    if key == -1:
        print("(-inf,-1e-8)", value[1] / value[0] if value[0] != 0 else 0)
    elif key == 20:
        print("(1e-8,inf)", value[1] / value[0] if value[0] != 0 else 0)
    else:
        print(range_list[key], value[1] / value[0] if value[0] != 0 else 0)
# %%
import numpy as np

samplex = [(range_list[i][0] + range_list[i][0]) / 2 * 1e-8 for i in range(20)]
sampley = [
    count_dict[i][1] / count_dict[i][0] if count_dict[i][0] != 0 else 0
    for i in range(20)
]

a = np.polyfit(samplex, sampley, 3)
b = np.poly1d(a)

import pickle as pk

# %%
pk.dump(b, open("data/edf_fun.pk", "wb"))
# %%
import matplotlib.pyplot as plt

plot_x = [(-0.5 + i / 1000) * 1e8 for i in range(1, 1000)]
plot_y = [b(x) for x in plot_x]
plt.plot(plot_x, plot_y)
# %%
