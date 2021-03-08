import numpy as np
from scipy.stats import norm
from scipy import integrate
from arch.univariate import ZeroMean, GARCH, Normal, ARX
from api_data import get_real_data
from api_data2 import get_real_hk_data
import pandas as pd

R = 0.05
T = 250
INF = 1000


def get_fake_data(n):
    return {
        "p": 3.0 * np.random.random(n),
        "e_": 4.0 * np.random.random(n),
        "d_short": 5.0 * np.random.random(n),
        "d_long": 5.0 * np.random.random(n),
    }


def get_E(p: np.array, e: np.array, outstanding_shares: float, total_shares: float):
    return p * outstanding_shares + (1 - outstanding_shares / total_shares) * e


def get_sigmaE(E, method="GARCH"):
    # The scale of y is 3.747e+20.
    # Parameterestimation work better when this value is between 1 and 1000.
    # The recommendedrescaling is 1e-09 * y.
    rescale = 1e9
    ar = ARX(E / rescale, lags=[1, 5])
    ar.volatility = GARCH(p=1, q=1)
    res = ar.fit(update_freq=0, disp="off")
    return check_and_interpolate(res.conditional_volatility * rescale)


def get_DP(d_short: np.array, d_long: np.array, lever_ratio):
    return (d_short + d_long / 2) / (lever_ratio * 2)


def get_d1(VA, sigmaA, DP):
    return (np.log(VA / DP) + (R + 0.5 * sigmaA ** 2) * T) / (sigmaA * np.sqrt(T))


def get_Nd1(d1):
    return norm.cdf(d1)


def get_Nd2(d1, sigmaA):
    return norm.cdf(d1 - sigmaA * np.sqrt(T))


def get_VA(E, Nd1, DP, Nd2):
    return (E + DP * np.exp(-R * T) * Nd2) / Nd1


def intergration_fun(t, nd1):
    return t ** (1 / (2.1073 * nd1)) * np.exp(-1 * t)


def get_integration_factor(Nd1):
    factor_list = []
    for nd1 in Nd1:
        v, err = integrate.quad(lambda x: intergration_fun(x, nd1), 0, INF)
        factor_list.append(v)
    return np.array(factor_list)


def get_sigmaA(E, sigmaE, VA, VE, Nd1):
    return sigmaE * (VA / VE) ** (1 / (2.1073 * Nd1)) * get_integration_factor(Nd1)


def get_sigmaA_v2(E, sigmaE, VA, VE, Nd1):
    return sigmaE * VE / (VA * Nd1)


def get_iterated_result(
    p,
    e,
    d_short,
    d_long,
    lever_ratio,
    outstanding_shares,
    total_shares,
    N,
    stop_diff,
    mode="v1",
):
    # 根据2020文章 对于金融业的关系函数 设计v2
    get_sigmaA_fun = {"v1": get_sigmaA, "v2": get_sigmaA_v2}[mode]
    E = check_and_interpolate(get_E(p, e, outstanding_shares, total_shares))
    # E = E.astype("double")
    DP = check_and_interpolate(get_DP(d_short, d_long, lever_ratio))
    # print("E", E, "sigmaE", get_sigmaE(E))
    sigmaE = check_and_interpolate(get_sigmaE(E))
    # sigmaE = sigmaE.astype("double")
    # sigmaE = np.nan_to_num(sigmaE, copy=True, nan=np.nanmean(sigmaE))

    sigmaA = np.ones(len(p)) * DP.mean() / 10
    VA = np.ones(len(p)) * DP.mean()
    for i in range(N):
        d1 = check_and_interpolate(get_d1(VA, sigmaA, DP))
        Nd1 = check_and_interpolate(get_Nd1(d1))
        Nd2 = check_and_interpolate(get_Nd2(d1, sigmaA))
        VA_diff = check_and_interpolate(get_VA(E, Nd1, DP, Nd2)) - VA
        sigmaA_diff = (
            check_and_interpolate(get_sigmaA_fun(E, sigmaE, VA, E, Nd1)) - sigmaA
        )
        VA += VA_diff
        sigmaA += sigmaA_diff
        if np.linalg.norm(VA_diff) + np.linalg.norm(sigmaA_diff) < 2 * stop_diff:
            break
    DD = (VA - DP) / (VA * sigmaA)
    return VA, sigmaA, i + 1, DD, np.linalg.norm(VA_diff) + np.linalg.norm(sigmaA_diff)


#%%
def check_and_interpolate(x):
    nan_array = np.isnan(x)
    if nan_array.sum() == 0:
        return x
    else:
        x[nan_array] = x.mean()
        return x


def get_final_res_from_code(code, start_date, end_date, mode):
    if "." in code:
        df = get_real_data(code, start_date, end_date)
    else:
        df = get_real_hk_data(code)
    p, e, d_short, d_long, outstanding_shares, total_shares, lever_ratio = (
        df["close"],
        df["total_hldr_eqy_inc_min_int"],
        df["total_liab"] * 0.9,
        df["total_liab"] * 0.1,
        df["outstanding_share"],
        df["total_share"],
        df["total_liab"] / df["total_hldr_eqy_inc_min_int"],
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
    df["VA"] = VA
    df["sigmaA"] = sigmaA
    df["DD"] = DD
    return iter_, delta_, df


#%%
# hong kong data
# {'重庆银行': '01963',
#  '甘肃银行': '02139',
#  '徽商银行': '03698',
#  '晋商银行': '02558',
#  '威海银行': '09677',
#  '哈尔滨银行': '06138',
#  '贵州银行': '06199',
#  '江西银行': '01916',
#  '九江银行': '06190',
#  '盛京银行': '02066',
#  '中原银行': '01216',
#  '锦州银行': '00416',
#  '泸州银行': '01983',
#  '天津银行': '01578'}
if __name__ == "__main__":
    mode = "v2"
    code = "601187.SH"
    # code = "01578"
    iter_, delta_, df = get_final_res_from_code(code, "20100101", "20201201", mode)
    df_res = pd.DataFrame({"VA": df["VA"], "sigmaA": df["sigmaA"], "DD": df["DD"]})
    df_res.to_csv("%s_res_%s.csv" % (code, mode))
    print(iter_, delta_, df_res)
    print(df)
    print(df["total_liab"])
    print(df["total_hldr_eqy_inc_min_int"])
