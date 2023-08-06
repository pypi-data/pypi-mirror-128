import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy import stats
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest


def outlier_five(args, data):
    row,col = data.shape
    print('数据标准化...',end='')
    # Z标准化：实现中心化和正态分布
    scaler = StandardScaler()
    scaler.fit(data)
    data_stand = scaler.transform(data)
    data_stand = pd.DataFrame(data_stand)
    data_stand.index = data.index
    data_stand.columns = data.columns
    print(data_stand)
    print('完成.')

    # store results
    outlier_dict = {}
    outlier_dict["zscore"] = data_stand
    # get run method
    method_array = np.array([args.sigma, args.lof, args.svm, args.ee, args.isof])
    if any(method_array):
        run_all = False
    else:
        run_all = True

    if args.sigma or run_all:
        print('3sigma-箱线图离群点...',end='')
        row, col = data.shape
        colnames = data_stand.columns
        data_stand1 = np.array(data_stand)
        zuhe = []
        for i in range(row):
            if (stats.normaltest(data_stand1[i]).pvalue > 1e-3):
                zuhe.append(colnames[(data_stand1[i] > args.threshold) | (data_stand1[i] < -(args.threshold))])
            else:
                x1 = pd.Series(data_stand1[i])
                x = data_stand1[i]
                x_25 = x1.quantile(0.25)
                x_75 = x1.quantile(0.75)
                iqr = x_75 - x_25
                zuhe.append(colnames[(x < x_25 - 1.5 * iqr) | (x > x_75 + 1.5 * iqr)])

        zuhe = pd.DataFrame(zuhe, index=data.index)
        zuhe2 = zuhe.apply(lambda x: list(filter(None, x)), axis=1)
        sigma_box = zuhe2
        print("完成.")

        outlier_dict["sigma"] = sigma_box


    x,y = data_stand.shape
    
    if args.lof or run_all:
        print('LOF离群点...',end='')
        data_stand1 = np.array(data_stand)
        clf = LocalOutlierFactor(n_neighbors=20)
        brain_lof_outlier = []
        for i in range(x):
            brain_lof_outlier.append(clf.fit_predict(data_stand1[i].reshape(-1, 1)))

        brain_lof_outlier = pd.DataFrame(brain_lof_outlier,index=data_stand.index, columns=data_stand.columns)
        brain_lof_outlier[brain_lof_outlier==-1] = np.nan
        brain_col = data_stand.columns
        lof = brain_lof_outlier.apply(lambda x : (brain_col[np.where(np.isnan(x))]).tolist(),axis=1)
        print("已完成.")

        outlier_dict["lof"] = lof


    if args.svm or run_all:
        print('OneClassSVM离群点...',end='')
        data_stand1 = np.array(data_stand)
        clf = OneClassSVM(gamma='auto',nu=0.1)
        brain_svm_outlier = []
        for i in range(x):
            brain_svm_outlier.append(clf.fit_predict(data_stand1[i].reshape(-1, 1)))

        brain_svm_outlier = pd.DataFrame(brain_svm_outlier,index=data_stand.index, columns=data_stand.columns)
        brain_svm_outlier[brain_svm_outlier==-1] = np.nan
        brain_col = data_stand.columns
        svm = brain_svm_outlier.apply(lambda x : (brain_col[np.where(np.isnan(x))]).tolist(),axis=1)
        print("已完成.")

        outlier_dict["svm"] = svm

    if args.ee or run_all:
        print('EllipticEnvelope离群点...',end='')
        data_stand1 = np.array(data_stand)
        cov = EllipticEnvelope(random_state=0)
        brain_ee_outlier = []
        for i in range(x):
            brain_ee_outlier.append(cov.fit_predict(data_stand1[i].reshape(-1, 1)))

        brain_ee_outlier = pd.DataFrame(brain_ee_outlier, index=data_stand.index, columns=data_stand.columns)
        brain_ee_outlier[brain_ee_outlier == -1] = np.nan
        brain_col = data_stand.columns
        ee= brain_ee_outlier.apply(lambda x: (brain_col[np.where(np.isnan(x))]).tolist(), axis=1)
        print("已完成.")

        outlier_dict["ee"] = ee


    if args.isof or run_all:
        print('IsolateForest离群点...',end='')
        data_stand1 = np.array(data_stand)
        clf = IsolationForest(random_state=0)
        brain_isof_outlier = []
        for i in range(x):
            brain_isof_outlier.append(clf.fit_predict(data_stand1[i].reshape(-1, 1)))

        brain_isof_outlier = pd.DataFrame(brain_isof_outlier, index=data_stand.index, columns=data_stand.columns)
        brain_isof_outlier[brain_isof_outlier == -1] = np.nan
        brain_col = data_stand.columns
        isof = brain_isof_outlier.apply(lambda x: (brain_col[np.where(np.isnan(x))]).tolist(), axis=1)
        print("已完成.")
        outlier_dict["isof"] = isof


    '''
    x = pd.DataFrame(outlier_array).T
    print(x)

    outlier = []
    row, col = x.shape
    for i in range(row):
        s = x.iloc[i, :].tolist()
        s_str = ",".join('%s' % id for id in s)
        outlier.append([x.strip() for x in (s_str.translate({ord(i): None for i in '[]"\''})).split(",")])
    print("文件已合并完成.")
    outlier = pd.DataFrame(outlier, index=lof.index)

    outlier_five = []
    row, col = outlier.shape
    for j in range(row):
        five = pd.DataFrame(outlier.iloc[j, :].value_counts())
        outlier_five.append(np.array(five[five >= threshold].dropna().index))
    print("文件已筛选完成.")

    outlier_last = pd.DataFrame(outlier_five, index=lof.index)
    '''

    return outlier_dict
