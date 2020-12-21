from arch.univariate import ZeroMean, GARCH, Normal
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

rs = np.random.RandomState(123)
dist = Normal(random_state=rs)
vol = GARCH(p=1, o=0, q=1)
sim_mod = ZeroMean(volatility=vol, distribution=dist)

params = [0.1, 0.05, 0.9]

sim_data = sim_mod.simulate(params, 1000)
print(sim_data.head())

'''
       data  volatility    errors
0 -1.033154    1.379696 -1.033154
1  0.775463    1.366226  0.775463
2  0.966169    1.345357  0.966169
3 -1.331714    1.332539 -1.331714
4  0.634797    1.336700  0.634797
'''

sim_data[['data', 'volatility']].plot()
plt.savefig('haha.png')
plt.show()