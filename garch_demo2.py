#%%
import arch.data.core_cpi
core_cpi = arch.data.core_cpi.load()
ann_inflation = 100 * core_cpi.CPILFESL.pct_change(12).dropna()
fig = ann_inflation.plot()
# %%
ann_inflation

# %%
from arch.univariate import ARX

ar = ARX(ann_inflation, lags=[1, 3, 12])
print(ar.fit().summary())

# %%
from arch.univariate import ARCH, GARCH

ar.volatility = ARCH(p=5)
res = ar.fit(update_freq=0, disp='off')
print(res.summary())
# %%
fig = res.plot()
# %%
res.conditional_volatility
# %%
