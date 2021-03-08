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
    "南京银行": "601009.SH",
    "北京银行": "601169.SH",
    "宁波银行": "002142.SZ"
}
tuple_list = get_tuple_list(code_dict.values(), "20100101", "20201231")
# %%
import matplotlib.pyplot as plt

figure = plt.figure()
plt.hist([x[0] for x in tuple_list], bins = 20)
plt.savefig("figure_chang/chang_DD_hist.png")
plt.close()

# %%
figure = plt.figure()
plt.hist([x[1] for x in tuple_list], bins = 20)
plt.savefig("figure_chang/chang_roe_hist.png")
plt.close()

# dd -> range
array_x = []
array_y = []
import numpy as np
for x in tuple_list:
    array_x.append(x[0])
    array_y.append(x[1])
#print(np.mean(array_x))
#print(np.std(array_x,ddof=1))
xiaxian1 = np.mean(array_x) - 2*np.std(array_x,ddof=1)
shangxian1 = np.mean(array_x) + 2*np.std(array_x,ddof=1)
per20 = np.nanpercentile(array_y,20)#
jiange1 = (shangxian1 - xiaxian1)/20
# %%
range_list = [(xiaxian1 + i * jiange1, xiaxian1 + (i+1) * jiange1) for i in range(20)]
count_dict = {i: [0, 0] for i in range(-1, 21)}

for x in tuple_list:
    if x[0] <= range_list[0][0]:
        count_dict[-1][0] += 1
        if x[1] < per20:
            count_dict[-1][1] += 1
        continue
    if x[0] > range_list[-1][1]:
        count_dict[20][0] += 1
        if x[1] < per20:
            count_dict[20][1] += 1
        continue
    for j, range_ in enumerate(range_list):
        if x[0]  > range_[0] and x[0]  <= range_[1]:
            count_dict[j][0] += 1
            if x[1] < per20:
                count_dict[j][1] += 1
                break
count_dict
# %%
for key, value in count_dict.items():
    if key == -1:
        print("(-inf,%s)"%xiaxian1, value[1] / value[0] if value[0] != 0 else 0)
    elif key == 20:
        print("(%s,inf)"%shangxian1, value[1] / value[0] if value[0] != 0 else 0)
    else:
        print(range_list[key], value[1] / value[0] if value[0] != 0 else 0)
# %%
import numpy as np

midx = [(range_list[i][0] + range_list[i][0]) / 2 for i in range(20)]
midy = [
    count_dict[i][1] / count_dict[i][0] if count_dict[i][0] != 0 else 0
    for i in range(20)
]

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
    

import pickle as pk

# %%
pk.dump(midx, open("data/midx.pk", "wb"))
pk.dump(midy, open("data/midy.pk", "wb"))
pk.dump(b, open("data/edf_fun.pk", "wb"))
# %%
#import matplotlib.pyplot as plt

#plot_x = [(-0.5 + i / 1000)  for i in range(1, 1000)]
#plot_y = [b(x) for x in plot_x]
#plt.plot(plot_x, plot_y)
#plt.savefig("figure_chang/zhexian.png")
# %%
