# ---------------------- Load libraries ----------------------
import os
import argparse
import os.path as op
import pandas as pd
import numpy as np
from  scipy import special, integrate, stats


# ---------------------- FUNCTIONS ----------------------

# This function is designed to estimate the reference ratio in the absence of any regulatory
# difference; that is, the reference bias due to alignment. This is done by obtaining the
# median ratio between eh1 and eh2 across the top 20% expressed loci in the library.
def get_r0(ASEdat, eh1 = "refCount", eh2 = "altCount"):
    eh1 = ASEdat[eh1]
    eh2 = ASEdat[eh2]
    totalCount = eh1 + eh2
    indices = totalCount >= np.quantile(totalCount, 0.8)
    return np.median(eh1[indices] / totalCount[indices])


# This function calculates Binomial coefficients for choosing 0:n out of n,
# in log scale. It is useful for precalculating the coefficients and
# providing them to "Binom_test_fast.R" or "pdf_binom_fast.R" when they
# are redone on the same N, over and over again. This function was
# designed by Pejman Mohammadi, 2018, Scripps Research, San Diego, CA.
def log_BinCoeffs(n):
    log_z = np.zeros(n + 1)
    lgamm = special.gammaln(list(range(1, n + 2)))
    m1 = int(np.floor(n / 2.0))
    m2 = int(np.ceil(n / 2.0))
    x = np.arange(1, m1 + 1)
    x = x.astype(int)
    xc = n - x
    xc = xc.astype(int)
    
    log_z[1:(m1+1)] = lgamm[n] - lgamm[x.tolist()] - lgamm[xc.tolist()]
    log_z[(n-1):(m2-1):-1] = log_z[1:(m1+1)]
    return log_z


# This function generates the binomial pdf, with the option to provide
# Binomial coefficients to it. It is useful when it is recalculated on
# the same N, over and over again.
# log_BinCoeffs can be precalculated using the function log_BinCoeffs(n)
# NEED TO INSERT WARNING IF p OUT OF DOMAIN [0,1]
def pdf_Binom_fast(n,p,log_BinCoeff):
    if (p == 0):
        Bin_p = np.zeros(n + 1)
        Bin_p[0] = 1
        return Bin_p
    elif (p == 1):
        Bin_p = np.zeros(n + 1)
        Bin_p[n] = 1
        return Bin_p
    else:
        log_p = np.log(p)
        log_pc = np.log(1-p)
        x = np.arange(0, n + 1)
        xc = n - x
        Bin_p = np.exp(log_p*x+log_pc*xc+log_BinCoeff)
        Bin_p = Bin_p / np.sum(Bin_p)
        return Bin_p


# For the following test we assume X and N are scalars while p is a vector
def Binom_test_ctm_dbl(X,N,p1,p2,log_BinCoeff,r0):
    m = np.round(r0 * N)
    p_value = np.zeros(len(pd.Series(p1)))
    for i in range(len(p_value)):
        if (X == m):
            p_value[i] = 1
        else:
            Bnp1 = pdf_Binom_fast(N, p1, log_BinCoeff)
            Bnp2 = pdf_Binom_fast(N, p2, log_BinCoeff)
            Bnp = (Bnp1+Bnp2) / 2
            Bnp  = Bnp / sum(Bnp)
            tpl = sum(Bnp[0:X])
            tpr = 0 if X==N else sum(Bnp[(X + 1): (N + 1)])
            
            p_value[i] = 2 * min(tpl,tpr)
            p_value[i] = p_value[i] + Bnp[X]
            
    return p_value


# Function generates the required integrand for the test.
def integrand(dE, eh1, eh2, Eg_std, r0, p0, log_BinCoeff):
    N = eh1 + eh2
    prob_dE = stats.norm.pdf(dE, loc = 0, scale = Eg_std)
    dE = np.log(0.5) if dE < np.log(0.5) else dE
    kr = 2 * np.exp(dE) - 1
    rr = kr / (kr + 1)
    rn = rr + p0 * (1 - 2 * rr)
    kn = rn / (1 - rn)
    k0 = r0 / (1 - r0)

    k = kn * k0 
    r_mR = k / (k+1)

    k = k0 / kn 
    r_mA = 1 if np.isinf(k) else k / (k + 1)
    
    return Binom_test_ctm_dbl(eh1,N,r_mR,r_mA,log_BinCoeff,r0) * prob_dE


# This is a black box function which performs the statistical test on a single SNP.
def Test_ASE_Outliers(Eg_std, eh1, eh2, r0, p0):
    Eg_std = max(Eg_std, np.finfo(np.float64).eps)
    rad = Eg_std * 4
    
    log_BinCoeff = log_BinCoeffs(eh1 + eh2)
    if (eh1 == eh2):
        p_val = 1
    else:
        (p_val, err) = integrate.quad(integrand, -rad, rad, args = (eh1, eh2, Eg_std, r0, p0, log_BinCoeff))
    
    return p_val


# Carry out Benjamini-Hochberg procedure to get adjusted p-values
def BH_adjust(p):
    nna = p.notnull()
    p0 = p
    p = p[nna]
    n = len(p)
    i = np.arange(n, 0, -1)
    ro = p.rank(ascending = False).astype(int) - 1
    p = p.sort_values(ascending = False)
    p = (n / i * p).cummin()
    p[p > 1] = 1
    p0[nna] = p.iloc[ro.tolist()]
    return p0


# This test is designed to detect if ASE data reveals sufficient allelic imbalance to induce
# an outlier in total gene expression.
def ANEVADOT_test(ASEdat, Eg_std, output_columns = ["refCount","altCount"], 
                  eh1 = "refCount", eh2 = "altCount", r0 = np.nan, p0 = np.nan, 
                  FDR = 0.05,coverage = 10, plot = True):
    output = ASEdat.loc[:, output_columns]
    if (np.isnan(r0).any()):
        r0 = get_r0(ASEdat, eh1, eh2)
    if (np.isnan(p0).any()):
        p0 = 0.000326
    if (len(r0) == 1):
        r0 = [r0] * len(ASEdat)
    if (len(pd.Series(p0))):
        p0 = [p0] * len(ASEdat)

    output["p_value"] = [np.nan] * len(ASEdat)
    output["p_adj"] = [np.nan] * len(ASEdat)
    output.index = np.arange(len(output))
    for i in range(len(output)):
        if (np.isnan(Eg_std[i])):
            output.loc[i, "p_value"] = np.nan
            next
        elif ((output.loc[i,eh1]+output.loc[i,eh2])>=coverage):
            output.loc[i, "p_value"] = Test_ASE_Outliers(Eg_std[i], output.loc[i, "REF_COUNT"], output.loc[i, "ALT_COUNT"], r0[i], p0[i])
        else:
            output.loc[i, "p_value"] = np.nan
    
    p = output.p_value.copy()
    output["p_adj"] = BH_adjust(p)
    return output

