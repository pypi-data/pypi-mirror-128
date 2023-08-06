import numpy as np
import pandas as pd
from aislab.gnrl.bf import *
from aislab.gnrl.sf import *
from aislab.gnrl.measr import *

##############################################################################
##############################################################################
def f_cs(X, args):
    import copy
    from aislab.gnrl.sf import sort
    from aislab.dp_feng.binenc import cut
    from aislab.gnrl.measr import confm
    # Objective function for credit risk strategy optimization
    # needed for old GA
    if isinstance(X, list):
        X = np.array(X)
    # needed for old GA

    data = args['data']  # data set
    BRA = args['BRA']  # Desired Bad Rate in AA (less risky) risk zone
    BRR = args['BRR']  # Desired Bad Rate in RR (most risky) risk zone
    TA = args['TA']  # Desired Total number of applications in AA risk zone
    TR = args['TR']  # Desired Total number of applications in RR risk zone
    minNb = args['minNb']  # minimum number of Bad applications in each risk zone
    minNgb = args['minNgb']  # minimum number of Good & Bad applications in each risk zone
    mindBR = args['mindBR']  # minimum change in the Bad Rate moving from one risk zone to a neighbour zone
    w = args['w']  # vector containing the weights of all business requirements included in the objective function
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. second (GBR) scorecard
    lb1 = args['lb1']  # lower bound for cut-offs of the first scorecard
    lb2 = args['lb2']  # lower bound for cut-offs of the second scorecard
    ub1 = args['ub1']  # upper bound for cut-offs of the first scorecard
    ub2 = args['ub2']  # upper bound for cut-offs of the second scorecard
    if X.ndim == 1: X = np.array([X])
    N = len(X)
    F = np.full((N,), np.nan)
    i = 0
    for x in X:
        # !!!!!
        x1, ss = sort(c_(x[:nc1, ]))
        x2, ss = sort(c_(x[nc1:, ]))
        minx = np.min([args['minx'], np.min(x)])  # upper bound for cut-offs of the first scorecard
        maxx = np.max([args['maxx'], np.max(x)])  # upper bound for cut-offs of the second scorecard
        x1 = (x1 - minx) / (maxx - minx) * (ub1 - lb1) + lb1
        x2 = (x2 - minx) / (maxx - minx) * (ub2 - lb2) + lb2
        x1 = np.round(x1.flatten())
        x2 = np.round(x2.flatten())
        # !!!!!

        if len(set(x1)) != len(x1) or len(set(x2)) != len(x2):
            F[i] = np.inf
            i += 1
            continue # if there are 2 or more the same GB cut-offs: F = inf
        try:
            GB_zones = cut(data['Score_GB'].values, x1).flatten()
            GBR_zones = cut(data['Score_GBR'].values, x2).flatten()
        except:
            print("In fobj(): Wrong cut-offs...")
        good = confm(-GB_zones, -GBR_zones, w=data['Good'].values).astype(int)  # confusion matrix
        bad = confm(-GB_zones, -GBR_zones, w=data['Bad'].values).astype(int)  # confusion matrix
        reject = confm(-GB_zones, -GBR_zones, w=data['Reject'].values).astype(int)  # confusion matrix
        import warnings
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        bad_rate = bad / (good + bad) * 100
        total_gb = good + bad
        total = good + bad + reject
        drBR = bad_rate[:, 1:] - bad_rate[:, :-1]  # rowwise delta BR
        dcBR = bad_rate[1:, :] - bad_rate[:-1, :]  # colwise delta BR

        mr, nr = np.shape(drBR)
        mc, nc = np.shape(dcBR)
        drBR1 = copy.deepcopy(drBR)
        for k in range(nr-1, 0, -1):
            for j in range(mr-1, 0, -1):
                if k-1 >= 0 and not np.isnan(drBR1[j, k]) and np.isnan(drBR1[j, k-1]): drBR1[j, k-1] = drBR1[j, k]
                if j-1 >= 0 and not np.isnan(drBR1[j, k]) and np.isnan(drBR1[j-1, k]): drBR1[j-1, k] = drBR1[j, k]
        dcBR1 = copy.deepcopy(dcBR)
        for k in range(nc-1, 0, -1):
            for j in range(mc-1, 0, -1):
                if k-1 >= 0 and not np.isnan(dcBR1[j, k]) and np.isnan(dcBR1[j, k-1]): dcBR1[j, k-1] = dcBR1[j, k]
                if j-1 >= 0 and not np.isnan(dcBR1[j, k]) and np.isnan(dcBR1[j-1, k]): dcBR1[j-1, k] = dcBR1[j, k]
        negdrBR = drBR1[drBR1 < mindBR]  # negative trend or not enough change in rowwise delta BR
        negdcBR = dcBR1[dcBR1 < mindBR]  # negative trend or not enough change in colwise delta BR

        # discriminatory power of the strategy  #  min(F1) = 0
        F1 = (((BRA - bad_rate[0, 0]) / max(1e-6, 100 - BRA)) ** 2 + ((TA - total[0, 0]) / max(1e-6, TA)) ** 2) / 2
        F2 = (((BRR - bad_rate[-1, -1]) / max(1e-6, BRR - 0)) ** 2 + ((TR - total[-1, -1]) / max(1e-6, TR)) ** 2) / 2
        # monotonicity of BR  #  min(F2) = 0
        F3 = ((np.sum(mindBR - negdrBR) + np.sum(mindBR - negdcBR)) / (nc1 * nc2)) ** 2
        # mininmum number of Bad and Good & Bad applications per segment  #  min(F4) = min(F5) = 0
        F4 = (np.sum((minNb - bad) * (minNb - bad > 0) * (total_gb > 0)) / max(1e-6,
                                                                               (nc1 + 1) * (nc2 + 1) * minNb)) ** 2
        F5 = (np.sum((minNgb - total_gb)*(minNgb - total_gb > 0)*(total_gb > 0))/max(1e-6, (nc1 + 1)*(nc2 + 1)*minNgb))**2
        # minimum number of NaN cells: min(F6) = 0
        F6 = (np.sum(np.sum(np.isnan(bad_rate))) / ((nc1 + 1) * (nc2 + 1))) ** 2
        # minimum number of records in most populated cell  # min(F7) = 0
        F7 = np.max(np.max(total)) / max(1e-6, sum(sum(total)))
        F[i] = w[0] * F1 + w[1] * F2 + w[2] * F3 + w[3] * F4 + w[4] * F5 + w[5] * F6 + w[6] * F7

        if np.isnan(F[i]):
            F[i] = np.inf
            if i == len(F):
                return F
        i += 1
    #     # needed for old GA
    #     if len(F) == 1: F = -F[0]
    #     if isinstance(F, float) and np.isinf(F): F = -np.inf
    # if len(X) > 1: F = -F
    #     # needed for old GA
#     if isinstance(X, list): F = F[0]

    return F
##############################################################################
def bprob(Strat, data, w, args_new, args_old):
    if Strat == 'NewClients_Product1':
        data = data[['APP_AccountID', 'NewClient', 'ProductType', 'Score_GB_N1', 'Score_GBR_N1', 'Good', 'Bad', 'Reject']]
        data.columns = ['APP_AccountID', 'NewClient', 'ProductType', 'Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']
        data = data[data['NewClient'] == True]
        data = data[data['ProductType'] == 1]
        args = args_new
        args['lb1'] = np.min(data['Score_GB'])
        args['ub1'] = np.max(data['Score_GB'])
        args['lb2'] = np.min(data['Score_GBR'])
        args['ub2'] = np.max(data['Score_GBR'])
        args['minx'] = np.min(np.min(data[['Score_GB', 'Score_GBR']]))
        args['maxx'] = np.max(np.max(data[['Score_GB', 'Score_GBR']]))
    elif Strat == 'NewClients_Product2':
        data = data[['APP_AccountID', 'NewClient', 'ProductType', 'Score_GB_N2', 'Score_GBR_N2', 'Good', 'Bad', 'Reject']]
        data.columns = ['APP_AccountID', 'NewClient', 'ProductType', 'Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']
        data = data[data['NewClient'] == True]
        data = data[data['ProductType'] == 2]
        args = args_new
        args['lb1'] = np.min(data['Score_GB'])
        args['ub1'] = np.max(data['Score_GB'])
        args['lb2'] = np.min(data['Score_GBR'])
        args['ub2'] = np.max(data['Score_GBR'])
        args['minx'] = np.min(np.min(data[['Score_GB', 'Score_GBR']]))
        args['maxx'] = np.max(np.max(data[['Score_GB', 'Score_GBR']]))
    elif Strat == 'OldClients_Product1':
        data = data[['APP_AccountID', 'NewClient', 'ProductType', 'Score_GB_O1', 'Score_GBR_O1', 'Good', 'Bad', 'Reject']]
        data.columns = ['APP_AccountID', 'NewClient', 'ProductType', 'Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']
        data = data[data['NewClient'] == False]
        data = data[data['ProductType'] == 1]
        data['Bad'][data['Reject'] == 1] = 0
        args = args_old
        args['lb1'] = np.min(data['Score_GB'])
        args['ub1'] = np.max(data['Score_GB'])
        args['lb2'] = np.min(data['Score_GBR'])
        args['ub2'] = np.max(data['Score_GBR'])
        args['minx'] = np.min(np.min(data[['Score_GB', 'Score_GBR']]))
        args['maxx'] = np.max(np.max(data[['Score_GB', 'Score_GBR']]))
    elif Strat == 'OldClients_Product2':
        data = data[['APP_AccountID', 'NewClient', 'ProductType', 'Score_GB_O2', 'Score_GBR_O2', 'Good', 'Bad', 'Reject']]
        data.columns = ['APP_AccountID', 'NewClient', 'ProductType', 'Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']
        data = data[data['NewClient'] == False]
        data = data[data['ProductType'] == 2]
        data['Bad'][data['Reject'] == 1] = 0
        args = args_old
        args['lb1'] = np.min(data['Score_GB'])
        args['ub1'] = np.max(data['Score_GB'])
        args['lb2'] = np.min(data['Score_GBR'])
        args['ub2'] = np.max(data['Score_GBR'])
        args['minx'] = np.min(np.min(data[['Score_GB', 'Score_GBR']]))
        args['maxx'] = np.max(np.max(data[['Score_GB', 'Score_GBR']]))
    elif Strat == 'NewClients':
        data = data[['APP_AccountID', 'NewClient', 'Score_GB_New', 'Score_GBR_New', 'Good', 'Bad', 'Reject']]
        data.columns = ['APP_AccountID', 'NewClient', 'Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']
        data = data[data['NewClient'] == True]
        args = args_new
        args['lb1'] = np.min(data['Score_GB'])
        args['ub1'] = np.max(data['Score_GB'])
        args['lb2'] = np.min(data['Score_GBR'])
        args['ub2'] = np.max(data['Score_GBR'])
        args['minx'] = np.min(np.min(data[['Score_GB', 'Score_GBR']]))
        args['maxx'] = np.max(np.max(data[['Score_GB', 'Score_GBR']]))
    elif Strat == 'OldClients':
        data = data[['APP_AccountID', 'NewClient', 'Score_GB_Old', 'Score_GBR_Old', 'Good', 'Bad', 'Reject']]
        data.columns = ['APP_AccountID', 'NewClient', 'Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']
        data = data[data['NewClient'] == False]
        data['Bad'][data['Reject'] == 1] = 0
        args = args_old
        args['lb1'] = np.min(data['Score_GB'])
        args['ub1'] = np.max(data['Score_GB'])
        args['lb2'] = np.min(data['Score_GBR'])
        args['ub2'] = np.max(data['Score_GBR'])
        args['minx'] = np.min(np.min(data[['Score_GB', 'Score_GBR']]))
        args['maxx'] = np.max(np.max(data[['Score_GB', 'Score_GBR']]))
    args['w'] = w
    args['data'] = data
    return data, args

###############################################################################
def tables(x, args):
    from aislab.gnrl.sf import sort
    from aislab.dp_feng.binenc import cut

    data = args['data']  # data set
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. second (GBR) scorecard

    lb1 = args['lb1']  # lower bound for cut-offs of the first scorecard
    lb2 = args['lb2']  # lower bound for cut-offs of the second scorecard
    ub1 = args['ub1']  # upper bound for cut-offs of the first scorecard
    ub2 = args['ub2']  # upper bound for cut-offs of the second scorecard
    minx = np.min([args['minx'], np.min(x)])  # upper bound for cut-offs of the first scorecard
    maxx = np.max([args['maxx'], np.max(x)])  # upper bound for cut-offs of the second scorecard


    x1, ss = sort(c_(x[:nc1, ]))
    x2, ss = sort(c_(x[nc1:, ]))
    minx = np.min([minx, np.min(x)])  # upper bound for cut-offs of the first scorecard
    maxx = np.max([maxx, np.max(x)])  # upper bound for cut-offs of the second scorecard
    x1 = (x1 - minx)/(maxx - minx)*(ub1 - lb1) + lb1
    x2 = (x2 - minx)/(maxx - minx)*(ub2 - lb2) + lb2
    x1 = np.round(x1.flatten())
    x2 = np.round(x2.flatten())

    cs = np.hstack((x1, x2))

    GB_zones = cut(data['Score_GB'].values, x1).flatten()
    GBR_zones = cut(data['Score_GBR'].values, x2).flatten()

    names1 = ['GB_A']
    for i in range(nc1 - 1): names1.append('GB_G' + str(i+1))
    names1.append('GB_R')
    names2 = ['GBR_A']
    for i in range(nc2 - 1): names2.append('GBR_G' + str(i+1))
    names2.append('GBR_R')
    # confusion matrix
    good = confm(-GB_zones, -GBR_zones, w=data['Good'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)
    bad = confm(-GB_zones, -GBR_zones, w=data['Bad'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)
    reject = confm(-GB_zones, -GBR_zones, w=data['Reject'].values, ux1=range(1-len(names1), 1), ux2=range(1-len(names2), 1)).astype(int)

    # n1 = len(names1)
    # for i in range(n1):
    #     if i not in np.unique(GB_zones):
    #         good = np.hstack((good[:, :i], nans((n1, 1)), good[:, (i+1):]))
    # n2 = len(names2)
    # for i in range(n2):
    #     if i not in np.unique(GBR_zones):
    #         good = np.vstack((good[:i, :], nans((1, n2)), good[(i+1):, :]))


    good = pd.DataFrame(good, index=names1, columns=names2)
    bad = pd.DataFrame(bad, index=names1, columns=names2)
    reject = pd.DataFrame(reject, index=names1, columns=names2)

    bad_rate = bad/(good + bad)*100
    total_gb = good + bad
    total = total_gb + reject
    return good, bad, reject, total_gb, total, bad_rate, cs

##############################################################################
def tables2(G, B, R, TGB, TGBR, BR, args):
    # GB Scorecard
    nc1 = args['nc1']  # number of cut-offs w.r.t. first (GB) scorecard
    nc2 = args['nc2']  # number of cut-offs w.r.t. first (GB) scorecard
    names1 = ['Accept']
    for i in range(nc1 - 1): names1.append('GB_G' + str(i+1))
    names1.append('Reject')
    names1.append('Total')
    names2 = ['Accept']
    for i in range(nc2 - 1): names2.append('GB_G' + str(i+1))
    names2.append('Reject')
    names2.append('Total')
    G1 = np.sum(G, axis=1)
    B1 = np.sum(B, axis=1)
    R1 = np.sum(R, axis=1)
    BadRej = B1 + R1
    TGBR1 = np.sum(TGBR, axis=1)
    TotalPrc = TGBR1/np.sum(TGBR1)*100
    BR = B1/(G1 + B1)*100
    BadAndRejectRate = BadRej/(G1 + BadRej)*100
    T1 = np.vstack((G1, B1, R1, BadRej, TGBR1, np.round(TotalPrc, 1), np.round(BR, 1), np.round(BadAndRejectRate, 1)))
    BR1 = np.sum(B1)/np.sum(G1 + B1)
    BadAndRejectRate1 = np.sum(B1 + R1)/np.sum(G1 + B1 + R1)
    Tot1 = [np.sum(np.sum(G1)), np.sum(np.sum(B1)), np.sum(np.sum(R1)), np.sum(np.sum(BadRej)), np.sum(np.sum(TGBR1)),
            np.sum(np.sum(TotalPrc)), BR1, BadAndRejectRate1]
    Tot = np.round(np.array([Tot1]).T, 1)
    T1 = np.hstack((T1, Tot))
    T1 = pd.DataFrame(T1, index=['Good', 'Bad', 'Reject', 'BadAndReject', 'Total', 'TotalPrc', 'BadRate', 'BadAndRejectRate'], columns=names1)
    # GBR Scorecard
    G2 = np.sum(G, axis=0)
    B2 = np.sum(B, axis=0)
    R2 = np.sum(R, axis=0)
    BadRej = B2 + R2
    TGBR2 = np.sum(TGBR, axis=0)
    TotalPrc = TGBR2/np.sum(TGBR2)*100
    BR = B2/(G2 + B2)*100
    BadAndRejectRate = BadRej/(G2 + BadRej)*100
    T2 = np.vstack((G2, B2, R2, BadRej, TGBR2, np.round(TotalPrc, 1), np.round(BR, 1), np.round(BadAndRejectRate, 1)))
    BR1 = np.sum(B2)/np.sum(G2 + B2)
    BadAndRejectRate1 = np.sum(B2 + R2)/np.sum(G2 + B2 + R2)
    Tot1 = [np.sum(np.sum(G2)), np.sum(np.sum(B2)), np.sum(np.sum(R2)), np.sum(np.sum(BadRej)), np.sum(np.sum(TGBR2)),
            np.sum(np.sum(TotalPrc)), BR1, BadAndRejectRate1]
    Tot = np.round(np.array([Tot1]).T, 2)
    T2 = np.hstack((T2, Tot))
    T2 = pd.DataFrame(T2, index=['Good', 'Bad', 'Reject', 'BadAndReject', 'Total', 'TotalPrc', 'BadRate', 'BadAndRejectRate'], columns=names2)
    return T1, T2
###############################################################################
def visualz(cs, F_opt, args, s, w, Strat, mut_rate, mut_met, mut_stdev, stop_itrConstF):
    G, B, R, TGB, TGBR, BR, cs = tables(cs, args)
    T1, T2 = tables2(G, B, R, TGB, TGBR, BR, args)  # if ~np.isinf(G):...

    print('============================================')
    print(Strat, ' - Report')
    print('============================================')
    T = {'': ['constraint', 'weight'],
         'BRA': [args['BRA'], w[0]],
         'TA': [args['TA'], w[0]],
         'BRR': [args['BRR'], w[1]],
         'TR': [args['TR'], w[1]],
         'mindBR': [args['mindBR'], w[2]],
         'minNb': [args['minNb'], w[3]],
         'minNgb': [args['minNgb'], w[4]],
         'NaN': [None, w[5]],
         'min_max_cell': [None, w[6]],
         'mutatRate': [mut_rate, None],
         'mutMethod': [mut_met, 'NaN'],
         'mutStdev': [mut_stdev, None],
         'stop_itrConstF': [stop_itrConstF, None]
        }
    print(pd.DataFrame(T).set_index(''))
    print('objF: ', F_opt)

    lus = int(np.max(np.max(s)))
    GG = np.full((lus, 1), np.nan)
    BB = np.full((lus, 1), np.nan)
    RR = np.full((lus, 1), np.nan)
    TT = np.full((lus, 1), np.nan)
    BRi = np.full((lus, 1), np.nan)

    for i in range(1, lus + 1):
        ind = s == i
        GG[i-1] = sum(G.values[ind])
        BB[i-1] = sum(B.values[ind])
        RR[i-1] = sum(R.values[ind])
        TT[i-1] = sum(TGBR.values[ind])

    BRi = BB/(GG + BB)*100
    TT = TT/sum(TT)*100
    CumGG1 = np.cumsum(GG)
    CumBB1 = np.cumsum(BB)
    CumGG2 = np.cumsum(GG[::-1])[::-1]
    CumBB2 = np.cumsum(BB[::-1])[::-1]

    CumTT1 = c_(np.cumsum(TT))
    CumTT2 = c_(np.cumsum(TT[::-1])[::-1])
    CumBR1 = c_(CumBB1/(CumGG1 + CumBB1))
    CumBR2 = c_(CumBB2/(CumGG2 + CumBB2))

    nn = range(int(np.min(s)), int(np.max(s) + 1))
    print('\n')
    #print(np.hstack((np.array([nn]).T, BRi, CumBR1, CumBR2, TT, CumTT)))
    Stats = pd.DataFrame(np.hstack((np.round(BRi, 2), np.round(TT, 2), np.round(CumBR1*100, 2), np.round(CumTT1, 2), np.round(CumBR2*100, 2), np.round(CumTT2, 2))))/100
    Stats = Stats.dropna()
    Stats.columns = ['BadRate', 'TotalPrc', 'CumBR', 'CumTotPrc', 'RevCumBR', 'RevCumTotPrc']
    print(Stats.to_string(index=False))
    print('\nCut-offsGB: ', cs[:args['nc1']])
    print('Cut-offsGBR: ', cs[args['nc1']:])


    print('\nBadRate: ')
    np.set_printoptions(suppress=True)
    print(np.round(BR, 2))

    print('\nTotal: ')
    print(TGBR)
    print('\nGood: ')
    print(G)
    print('\nBad: ')
    print(B)
    print('\nGood&Bad: ')
    print(TGB)
    print('\nReject: ')
    print(R)

    # names = {1: 'Accept', 2: 'LowRisk', 3: 'MidRisk', 4:'HighRisk', 5: 'Reject'}
    # m, n = s.shape
    # Segment = np.full((m*n, 1), 'xxxxxxxxxx')
    # Scorecard_GB = np.full((m*n, 1), 'xxxxxxxxx')
    # Scorecard_GBR = np.full((m*n, 1), 'xxxxxxxxx')
    # Colour = np.full((m*n, 1), 'xxxxxxxxx')
    # Code = nans((m*n, 1))
    # segment = 'OldClients'; s = s_old; colour = {1: 'green', 2: 'green', 3: 'green', 4: 'green', 5:'green', 6:'green', 7:'gray', 8:'gray', 9:'gray', 10:'red', 11:'red'}
    # segment = 'NewClients'; s = s_new; colour = {1: 'green', 2: 'green', 3: 'green', 4: 'green', 5:'green', 6:'green', 7:'green', 8:'gray', 9:'gray', 10:'red', 11:'red', 12:'red'}
    #
    # k = 0
    # for i in range(m):      # SC_GB
    #     for j in range(n):  # SC_GBR
    #         Segment[k, 0] = segment
    #         Scorecard_GB[k, 0] = names[i+1]
    #         Scorecard_GBR[k, 0] = names[j+1]
    #         Colour[k, 0] = colour[s[i, j]]
    #         Code[k, 0] = s[i, j]
    #         k += 1
    #
    # df = pd.DataFrame({    'Segment': Segment.flatten(),
    #      'Scorecard_GB': Scorecard_GB.flatten(),
    #     'Scorecard_GBR': Scorecard_GBR.flatten(),
    #            'Colour': Colour.flatten(),
    #              'Code': Code.flatten()})
    # df.to_csv('/home/user/Desktop/Saso/AutoSCDev/data/sc_Stik_07/python/'+'RiskZones'+segment+'.csv')
    return cs, G, B, R, TGB, TGBR, BR, T1, T2

###############################################################################
###############################################################################

# exp1:                                                 # y = a + b*e^x
# exp2:                                                 # y = a + b*e^(x + c)
# exp3:   ym = pm[0] + pm[1]*np.exp(x*pm[2])            # y = a + b*e^(x*c)

# log:    ym = pm[0] + pm[1]*np.log(abs(x) + 1)         # ym = a + b*ln(x)
# log1:   ym = pm[0] + pm[1]*np.log(pm[2]*abs(x) + 1)   # y = a + b*ln(c*|x| + 1)
# logW:   ym = pm[0] + pm[1]*np.log(abs(pm[2]*x + 1))   # y = a + b*ln(|c*x + 1|)

# lgr:    ym = 1/(1 + np.exp(-x@pm))                    # y = 1/(1 + e^-(x*pm))

# exp model
# args['b'] = 1e-8
# args['c'] = 1e3
# log model
# args['b'] = 0.01
# args['c'] = 1e3

def f_exp1(args):
    # F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp1_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_exp2(args):
    # F for model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp2_apl(x, pm)
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_exp3(args):
   # F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    if x.shape[1] == 0: x = c_(x)
    ym = exp3_apl(x, pm)
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    # print(np.hstack((e, w)))

    b = args['b']
    c = args['c']
    d1 = pm.flatten()
    d2 = (1 - (pm[0, 0] + pm[1, 0]))**2*c
    A = np.diag((d1 < b))*c
    F = F + pm.T@A@pm + d2

    return F, args
###################################################################################
def f_lgr(args):
    # F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    pm = args['x']
    ym = lgr_apl(x, pm)
    ym[ym > 1 - 1e-10] = 1 - 1e-10
    ym[ym < 1e-10] = 1e-10
    m = pm.shape[1]
    yy = np.matlib.repmat(y, 1, m)
    ww = np.matlib.repmat(w, 1, m)
    F = -sum(yy*np.log(ym)*ww + (1 - yy)*np.log(1 - ym)*ww)
    args['data'][:, -1] = ym.flatten()
    return F, args
###################################################################################
def f_log1(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log1_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_log2(args):
    # F for exponential model: ym = a + b*ln(x)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log2_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    F = F + pm.T@A@pm

    return F, args
###################################################################################
def f_log3(args):
    # F for exponential model: ym = a + b*ln(c*x + 1)
    pm = args['x']
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    if x.shape[1] == 0: x = c_(x)
    ym = log3_apl(x, args['x'])
    e = y - ym
    F = e.T@(e*w)
    args['data'][:, -1] = ym.flatten()

    b = args['b']
    c = args['c']
    d1 = pm.flatten()
    d2 = (pm[0, 0] - 1)**2*c

    A = np.diag((d1 < b))*c
    F = F + pm.T@A@pm + d2

    return F, args
###################################################################################
def g_exp1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    e = y - ym
    g = np.zeros((2, 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.exp(x))[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_exp2(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    tmp = np.exp(x + pm[2])
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@tmp)[0]
    g[2] = (-2*pm[1]*(w*e).T@tmp)[0]

    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_exp3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    tmp = np.exp(x*pm[2])
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@tmp)[0]
    g[2] = (-2*pm[1]*(w*e*x).T@tmp)[0]

    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    g = g + 2*A@pm + np.array([[-2*(1 - (pm[0,0] + pm[1,0]))*c], [-2*(1 - (pm[0,0] + pm[1,0]))*c], [0]])
    return g
###################################################################################
def g_lgr(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    g = -x.T@((y - ym)*w)
    return g
###################################################################################
def g_log1(args=None):
    # gradient of F for log model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    e = y - ym
    g = np.zeros((2, 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.log(abs(x) + 1))[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    g = g + 2*A@pm

    return g
###################################################################################
def g_log3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # gradient of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    y = c_(args['data'][:, -3])
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    g = np.zeros((len(pm), 1))
    g[0] = (-2*w.T@e)[0, 0]
    g[1] = (-2*(w*e).T@np.log(abs(pm[2]*x) + 1))[0]
    g[2] = ((-2*pm[1]*(w*e/(abs(pm[2]*x) + 1)).T@x)*np.sign(pm[2]*x + 1))[0]  # !!!: np.sign(0) = 0

    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    d2 = (pm[0, 0] - 1)**2*c
    g = g + 2*A@pm + np.array([[2*(pm[0,0] - 1)*c], [0], [0]])
    return g
###################################################################################
def h_exp1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^x
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    H = np.zeros(shape = (2,2))
    tmp = np.exp(x)
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    H = H + 2*A

    return H
###################################################################################
def h_exp2(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^(x + c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.exp(x + pm[2])
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = 2*pm[1]*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = 2*pm[1]*((w*tmp).T@tmp)[0] - 2*((w*e).T@tmp)[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w*tmp).T@tmp)[0] - 2*pm[1]*((w*e).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = np.hstack((pm.flatten()[:2], zeros((1,))))
    A = np.diag((dd < b))*c
    H = H + 2*A
    return H
    dd = pm.flatten()
    A = np.diag((dd < b))*c
###################################################################################
def h_exp3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for model: y = a + b*e^(x*c)
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.exp(x*pm[2])
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = 2*pm[1]*((w*x).T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = 2*pm[1]*((w*tmp*x).T@tmp)[0] - 2*((w*e*x).T@tmp)[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w*tmp*x**2).T@tmp)[0] - 2*pm[1]*((w*e*x**2).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    H = H + 2*A + np.array([[2*c, 2*c, 0], [2*c, 2*c, 0], [0, 0, 0]])
    return H
###################################################################################
def h_lgr(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    n = x.shape[1]
    H = (x*np.matlib.repmat(ym*(1 - ym)*w, 1, n)).T@x
    return H
###################################################################################
def h_log1(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    ym = c_(args['data'][:, -1])
    H = np.zeros(shape = (2,2))
    tmp = np.log(abs(x) + 1)
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    A = np.diag((pm.flatten() < b))*c
    H = H + 2*A
    return H
###################################################################################
def h_log3(args=None):
    # ---------------------------------------------
    # Author: Alexander Efemov
    # Date:   20.12.2009
    # Course: Modelling and Processes Optimization
    # ---------------------------------------------
    # Hessian of F for logistic regression model: ym = 1/(1 + exp(-x*pm))
    h = args['data'].shape[1]
    x = args['data'][:, np.arange(0, h - 3)]
    w = c_(args['data'][:, -2])
    y = c_(args['data'][:, -3])
    ym = c_(args['data'][:, -1])
    pm = args['x']
    e = y - ym
    H = np.zeros(shape=(3, 3))
    tmp = np.log(abs(pm[2]*x + 1))
    H[0, 0] = 2*np.sum(w)
    H[0, 1] = 2*(w.T@tmp)[0]
    H[0, 2] = (2*pm[1]*((w/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1))[0]
    H[1, 0] = H[0, 1]
    H[1, 1] = 2*((w*tmp).T@tmp)[0]
    H[1, 2] = (2*pm[1]*((w*tmp/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1) - 2*((w*e/abs(pm[2]*x + 1)).T@x)*np.sign(pm[1]*x + 1))[0]
    H[2, 0] = H[0, 2]
    H[2, 1] = H[1, 2]
    H[2, 2] = 2*pm[1]**2*((w/abs(pm[2]*x + 1)*x).T@x)[0] - 2*pm[1]*((w*e*x/abs(pm[2]*x + 1)).T@x)[0]

    pm = args['x']
    b = args['b']
    c = args['c']
    dd = pm.flatten()
    A = np.diag((dd < b))*c
    H = H + 2*A + np.array([[2*c, 0, 0], [0, 0, 0], [0, 0, 0]])
    return H
###################################################################################
def exp1_apl(x, pm):
    # model: y = a + b*e^x
    ym = pm[0] + pm[1]*np.exp(x)
    return ym
###################################################################################
def exp2_apl(x, pm):

    ym = pm[0] + pm[1]*np.exp(x + pm[2])
    return ym
###################################################################################
def exp3_apl(x, pm):
    # model: y = a + b*e^(x*c)
    ym = pm[0] + pm[1]*np.exp(x*pm[2])
    return ym
###################################################################################
def lgr_apl(x, pm):
    # logistic regression function
    if not isinstance(x, np.ndarray): x = np.array([[x]])
    if not isinstance(pm, np.ndarray): pm = np.array([[pm]])
    ym = 1/(1 + np.exp(-x@pm))
    return ym
###################################################################################
def log1_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(abs(x) + 1)
    return ym
###################################################################################
def log2_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(pm[2]*abs(x) + 1)
    return ym
###################################################################################
def log3_apl(x, pm):
    ym = pm[0] + pm[1]*np.log(abs(pm[2]*x + 1))
    return ym
###################################################################################
