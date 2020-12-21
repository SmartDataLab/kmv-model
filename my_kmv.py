
import numpy as np
from scipy.stats import norm
from scipy import integrate
from arch.univariate import ZeroMean, GARCH, Normal, ARX


R = 0.05
T = 250
INF = 1000

def get_fake_data(n):
    return {'p':3.0 * np.random.random(n),'e_':4.0 * np.random.random(n),'d_short':5.0 * np.random.random(n),'d_long':5.0 * np.random.random(n)}

def get_E(p : np.array, e : np.array, outstanding_shares : float, total_shares : float):
    return p * outstanding_shares + (1 - outstanding_shares/total_shares) * e

def get_sigmaE(E, method = 'GARCH'):
    # TODO(sujinhua): add specific method to calculate the ratio of the
    ar = ARX(E, lags=[1,5])
    ar.volatility = GARCH(p = 1, q = 1)
    res = ar.fit(update_freq = 0, disp = 'off')
    return res.conditional_volatility

def get_DP(d_short : np.array, d_long : np.array):
    return d_short + d_long / 2 

def get_d1(VA, sigmaA, DP):
    return (np.log(VA/DP) + (R + 0.5 * sigmaA ** 2) * T) / (sigmaA * np.sqrt(T))

def get_Nd1(d1):     
    return norm.cdf(d1)

def get_Nd2(d1, sigmaA):
    return norm.cdf(d1 - sigmaA * np.sqrt(T))

def get_VA(E, Nd1, DP, Nd2):
    return (E + DP * np.exp(-R * T) * Nd2) / Nd1

def intergration_fun(t, nd1):
    return t ** (1/(2.1073*nd1)) * np.exp(-1 * t)

def get_integration_factor(Nd1):
    factor_list = []
    for nd1 in Nd1:
        v,err = integrate.quad(lambda x: intergration_fun(x,nd1), 0, INF)
        factor_list.append(v)
    return np.array(factor_list)

def get_sigmaA(E, sigmaE, VA, VE, Nd1):
    return sigmaE * (VA / VE) ** (1/(2.1073 * Nd1)) * get_integration_factor(Nd1)

def get_iterated_result(p,e, d_short, d_long, outstanding_shares, total_shares, N, stop_diff):
    E = get_E(p, e, outstanding_shares, total_shares)
    DP = get_DP(d_short, d_long)
    sigmaE = get_sigmaE(E)

    sigmaE = np.nan_to_num(sigmaE, copy = True, nan = np.nanmean(sigmaE))

    sigmaA = np.random.random(len(p))
    VA = np.random.random(len(p))
    for i in range(N):
        d1 =  get_d1(VA, sigmaA, DP)
        Nd1 = get_Nd1(d1)
        Nd2 = get_Nd2(d1, sigmaA)
        VA_diff = get_VA(E, Nd1, DP, Nd2) - VA
        sigmaA_diff = get_sigmaA(E, sigmaE, VA, E, Nd1) - sigmaA
        VA += VA_diff
        sigmaA += sigmaA_diff
        if np.linalg.norm(VA_diff) + np.linalg.norm(sigmaA_diff) < 2 * stop_diff:
            break
    return VA, sigmaA, i+1

        
if __name__ == '__main__':
    data = get_fake_data(1000)
    p,e,d_short,d_long = list(data.values())
    print(get_iterated_result(p,e,d_short,d_long,1e7,2e7,100,1e-3))
        
