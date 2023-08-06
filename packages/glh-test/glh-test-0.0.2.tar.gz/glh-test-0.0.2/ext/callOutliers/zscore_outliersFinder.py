
# ---------------------- Load libraries ----------------------
import os
import sys
import time
import argparse
import os.path as op
import pandas as pd
import numpy as np


# ---------------------- FUNCTIONS ----------------------

# if extremeCase is False
# For each gene we took all zscores meet the cutoff as outliers, therefore, a gene might has multiple outliers
# here the medz is already processed (remove genes with less than 5 tissues),therefore we don't need input counts

# if extremeCase is True
# For each gene we took the maximal zscore among individuals for further outlier test, this can be used for further disease gene enrichment
# here we don't specify threshold, since we will output all tested genes and their maximal zscores
def pick_z_outliers(matz, threshold = None, indis = None, extremeCase = False):
    gene_column = matz.columns[0]
    if not extremeCase:
        matz = matz.melt(id_vars = [gene_column])
        if threshold == None: threshold = 3
        matz = matz[matz["value"].abs() > threshold]
        matz.columns = [gene_column, "INDS", "Z_score"]
        return matz
    else:
        matz.index = matz.iloc[:, 0]
        matz = matz.iloc[:, 1:]
        
        max_ind = matz.abs().idxmax(axis = 1)
        sample_id = pd.Categorical(max_ind.values, categories = indis, ordered = False)
        max_ind = max_ind[sample_id.notna()]
        sample_id = sample_id[sample_id.notna()]
        gene_id = max_ind.index
        max_ind = list(zip(gene_id, sample_id))
        
        z_extreme = matz.stack()[max_ind]
        matz = pd.DataFrame({gene_column : gene_id,
                            "INDS" : sample_id,
                            "Z_score" : z_extreme
                            })
        matz = matz.loc[matz.Z_score.abs() > threshold]
        return matz


# if extremeCase is False: For each gene we took all p_value meet the cutoff as outliers
# if extremeCase is True: For each gene we took the minimum p_value among individuals for further outlier test
def pick_p_outliers(matp, threshold = None, indis = None, extremeCase = False):
    gene_column = matp.columns[0]
    if not extremeCase:
        matp = matp.melt(id_vars = [gene_column])
        if threshold == None: threshold = 0.0027
        matp = matp[matp["value"] < threshold]
        matp.columns = [gene_column, "INDS", "P_value"]
        return matp
    else:
        matp.index = matp.iloc[:, 0]
        matp = matp.iloc[:, 1:]
        
        min_ind = matp.idxmin(axis = 1)
        sample_id = pd.Categorical(min_ind.values, categories = indis, ordered = False)
        min_ind = min_ind[sample_id.notna()]
        sample_id = sample_id[sample_id.notna()]
        gene_id = min_ind.index
        min_ind = list(zip(gene_id, sample_id))
        
        p_extreme = matp.stack()[min_ind]
        matp = pd.DataFrame({gene_column : gene_id,
                            "INDS" : sample_id,
                            "P_value" : p_extreme
                            })
        matp = matp.loc[matp.P_value < threshold]
        return matp

# call outlier for expression
def call_outliers_z(file, threshold):
    data = pd.read_csv(file, sep="\t", header=0)
    indis = data.columns[1:]

    outlier_picked = pick_z_outliers(matz = data, threshold = threshold)
    zscore_extreme = pick_z_outliers(matz = data, threshold = threshold, indis = indis, extremeCase = True)
    
    return (outlier_picked, zscore_extreme)

# call outliers for splice
def call_outliers_p(file,  threshold):
    data = pd.read_csv(file, sep = "\t", header = 0)
    indis = data.columns[1:]

    outlier_picked = pick_p_outliers(matp = data, threshold = threshold)
    pvalue_extreme = pick_p_outliers(matp = data, threshold = threshold, indis = indis, extremeCase = True)

    return (outlier_picked, pvalue_extreme)
