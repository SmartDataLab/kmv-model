from my_kmv import *

if __name__ == "__main__":
    mode = "v2"
    codes = [
        "000001.SZ",
        "002948.SZ",
        "601860.SH",
        "601658.SH",
        "601998.SH",
        "601077.SH",
        "601288.SH",
        "601398.SH",
        "600036.SH",
        "601818.SH",
        "601328.SH",
        "600908.SH",
        "601988.SH",
        "601939.SH",
        "601916.SH",
        "601577.SH",
        "002936.SZ",
        "600016.SH",
        "002966.SZ",
        "600919.SH",
        "600015.SH",
        "600928.SH",
        "601128.SH",
        "603323.SH",
        "601229.SH",
        "002142.SZ",
        "002958.SZ",
        "601997.SH",
        "002839.SZ",
        "601169.SH",
        "600000.SH",
        "600926.SH",
        "002807.SZ",
        "601166.SH",
        "601838.SH",
        "601009.SH",
    ]
    dates = [
        ("20100101", "20101201"),
        ("20110101", "20111201"),
        ("20120101", "20121201"),
        ("20130101", "20131201"),
        ("20140101", "20141201"),
        ("20150101", "20151201"),
        ("20160101", "20161201"),
        ("20170101", "20171201"),
        ("20180101", "20181201"),
        ("20190101", "20191201"),
        ("20200101", "20201201"),
    ]
AllDD = pd.DataFrame()

for code in codes:
    print(code)
    # df1 = get_real_data(code, "20100101", "20201201")
    # df2 = get_real_data(code, "20150101", "20201201")
    df = get_real_data(code, "20100101", "20151201")  # df1.drop(df2.index)
    print(df)
    p, e, d_short, d_long, outstanding_shares, total_shares, profit = (
        df["close"],
        df["total_hldr_eqy_inc_min_int"],
        df["total_liab"] / 3,
        df["total_liab"] / 2,
        df["outstanding_share"],
        df["total_share"],
        df["profit_to_op"],
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

    AllDD["%s" % code] = DD
    DD = DD.tolist()
