import numpy as np
from scipy.stats import norm
from scipy import integrate
from arch.univariate import ZeroMean, GARCH, Normal, ARX
from api_data import get_real_data
import pandas as pd
import math

R = 0.05
T = 250
INF = 1000
DDsumlist=np.zeros((25,3))


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
    # TODO(sujinhua): estimating the model parameters.
    # The scale of y is 3.747e+20.
    # Parameterestimation work better when this value is between 1 and 1000.
    # The recommendedrescaling is 1e-09 * y.
    rescale = 1e9
    ar = ARX(E / rescale, lags=[1, 5])
    ar.volatility = GARCH(p=1, q=1)
    res = ar.fit(update_freq=0, disp="off")
    return res.conditional_volatility * rescale


def get_DP(d_short: np.array, d_long: np.array):
    return d_short + d_long / 2


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
        p, e, d_short, d_long, outstanding_shares, total_shares, N, stop_diff, mode="v1"
):
    # 根据2020文章 对于金融业的关系函数 设计v2
    get_sigmaA_fun = {"v1": get_sigmaA, "v2": get_sigmaA_v2}[mode]
    E = check_and_interpolate(get_E(p, e, outstanding_shares, total_shares))
    # E = E.astype("double")
    DP = check_and_interpolate(get_DP(d_short, d_long))
    # print(E)
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
    DD = (VA - DP) / (sigmaA)



    return VA, sigmaA, i + 1, DD, np.linalg.norm(VA_diff) + np.linalg.norm(sigmaA_diff)


# %%
def check_and_interpolate(x):
    nan_array = np.isnan(x)
    if nan_array.sum() == 0:
        return x
    else:
        x[nan_array] = x.mean()
        return x


# %%

#def getD_EDF





if __name__ == "__main__":
    mode = "v2"
    codes = ["000001.SZ","002948.SZ","601860.SH","601658.SH","601998.SH","601077.SH",
             "601288.SH","601398.SH","600036.SH","601818.SH","601328.SH","600908.SH",
             "601988.SH","601939.SH","601916.SH","601577.SH","002936.SZ","600016.SH",
             "002966.SZ","600919.SH","600015.SH","600928.SH","601128.SH","603323.SH",
             "601229.SH","002142.SZ","002958.SZ","601997.SH","002839.SZ","601169.SH",
             "600000.SH","600926.SH","002807.SZ","601166.SH","601838.SH","601009.SH"]
    dates = [("20100101","20101201"),
             ("20110101","20111201"),
             ("20120101","20121201"),
             ("20130101","20131201"),
             ("20140101","20141201"),
             ("20150101","20151201"),
             ("20160101","20161201"),
             ("20170101","20171201"),
             ("20180101","20181201"),
             ("20190101","20191201"),
             ("20200101","20201201"),]
    AllDD=pd.DataFrame()

    for code in codes:

        df1 = get_real_data(code, "20100101","20201201")
        df2 = get_real_data(code, "20150101","20201201")
        df= df1.drop(df2.index)
        p, e, d_short, d_long, outstanding_shares, total_shares, profit = (
            df["close"],
            df["total_hldr_eqy_inc_min_int"],
            df["total_liab"] / 3,
            df["total_liab"] / 2,
            df["outstanding_share"],
            df["total_share"],
            df["profit_to_op"]
        )
        p = check_and_interpolate(p.astype("double"))
        e = check_and_interpolate(e.astype("double"))
        d_long = check_and_interpolate(d_long.astype("double"))
        d_short = check_and_interpolate(d_short.astype("double"))
        outstanding_shares = check_and_interpolate(outstanding_shares.astype("double"))
        total_shares = check_and_interpolate(total_shares.astype("double"))
        VA, sigmaA, iter_, DD, delta_ = get_iterated_result(
            p, e, d_short, d_long, outstanding_shares, total_shares, 100, 1e-3, mode=mode
            )
        print(profit)
        profit = profit.tolist()
        sp = 0
        for i in profit:
            sp += i
        sp /= len(profit)

        AllDD['%s' % code] = DD
        DD=DD.tolist()



            #以下是求经验EDF的代码，现在仍然需要利润率数据和规则
        for i in DD:

            for j in range(25):
            print(j*(-40),(j+1)*(-40))
            if(i<=j*(-40) and i>(j+1)*(-40)):

                if(sp<=31.2):
                    DDsumlist[j][0]+=1
                    DDsumlist[j][1]+=1
                else: DDsumlist[j][0]+=1


    AllDD.to_csv("alldd.csv" )
    for i in range(25):
        DDsumlist[i][2]=DDsumlist[i][1]/DDsumlist[i][0]

    print(DDsumlist)

