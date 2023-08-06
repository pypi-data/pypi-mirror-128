# ---------------------- load libraries ----------------------
import os
import sys
import subprocess
import time
import os.path as op
import pandas as pd
import numpy as np
import scipy.stats as st
from ext.callOutliers import zscore_outliersFinder

# ---------------------- function ----------------------  

def print_info(info_type, info_str, log_file):
    time_str = time.strftime("[%H:%M:%S %Y]: ", time.localtime())

    if info_type == "START":
        log_handle = open(log_file, "w")
    else:
        log_handle = open(log_file, "a")

    if info_type == "MAIN":
        print(time_str + "---------- {prog_info} ----------".format(prog_info = info_str))
        print(time_str + "---------- {prog_info} ----------".format(prog_info = info_str), file = log_handle)
    elif info_type == "CMD":
        print(time_str + "{info_type}\t{cmd}".format(info_type = info_type, cmd = info_str))
        print(time_str + "{info_type}\t{cmd}".format(info_type = info_type, cmd = info_str), file = log_handle)
    else:
        print(time_str + "{info_type}\t{info_str}".format(info_type = info_type, info_str = info_str))
        print(time_str + "{info_type}\t{info_str}".format(info_type = info_type, info_str = info_str), file = log_handle)
    if info_type == "ERROR":
        print(time_str + "\t########## RUN mOutlierPipe FAILED ##########")
        print(time_str + "\t########## RUN mOutlierPipe FAILED ##########", file = log_handle)
        log_handle.close()
        exit(1)
    log_handle.close()


########## eOutlier module1 ##########
def collapse_gtf(args, main_path, res_dir, log_file):
    prog = op.join(main_path, "ext", "callOutliers", "collapse_annotation.py")
    if not op.exists(op.join(res_dir, "rnaseqc_res")):
        os.mkdir(op.join(res_dir, "rnaseqc_res"))

    gtf_file = op.join(res_dir, "rnaseqc_res", op.basename(args.gtf))
    mop_gtf_file = op.join(res_dir, "rnaseqc_res", "mop."+op.basename(args.gtf))
    cmd = "python {prog} {gtf} {res_gtf}".format(prog=prog, gtf=args.gtf, res_gtf=gtf_file)
    print_info("INFO", "COLLAPSE GTF ANNOTATION", log_file)
    pid = subprocess.Popen(cmd, shell = True)
    pid.wait()

    if pid.returncode == 0:
        print_info("INFO", "run collapse_gtf.py successful !!!", log_file)
        os.rename(gtf_file, mop_gtf_file)
    else:
        print_info("ERROR", "run collapse_gtf.py failed !!!", log_file)


# parse arguments for RNA-SeQC
def parse_rnaseqc(args, main_path, sample, bam_file, res_dir):
    prog = op.join(main_path, "ext", "rnaseqc")
    rnaseqc_dir = op.join(res_dir, "rnaseqc_res")

    gtf_file = op.join(res_dir, "rnaseqc_res", "mop."+op.basename(args.gtf))
    cmd = [prog, 
            gtf_file,
            bam_file,
            rnaseqc_dir, 
            "-s", sample]

    if args.bed:
        cmd.extend(["--bed", args.bed])
    if args.fasta:
        cmd.extend(["--fasta", args.fasta])
    if args.chimeric_distance:
        cmd.extend(["--chimeric-distance", args.chimeric_distance])
    if args.fragment_samples:
        cmd.extend(["--fragment-samples", args.fragment_samples])
    if args.mapping_quality:
        cmd.extend(["--mapping-quality", args.mapping_quality])
    if args.base_mismatch:
        cmd.extend(["--base-mismatch", args.base_mismatch])
    if args.offset:
        cmd.extend(["--offset", args.offset])
    if args.window_size:
        cmd.extend(["--window-size", args.window_size])
    if args.gene_length:
        cmd.extend(["--gene-length", args.gene_length])
    if args.legacy:
        cmd.extend(["--legacy"])
    if args.stranded:
        cmd.extend(["--stranded"])
    if args.chimeric_tag:
        cmd.extend(["--chimeric-tag", args.chimeric_tag])
    if args.exclude_chimeric:
        cmd.extend(["--exclude-chimeric"])
    if args.single_end:
        cmd.extend(["--unpaired"])
    if args.rpkm:
        cmd.extend(["--rpkm"])
    if args.coverage:
        cmd.extend(["--coverage"])
    if args.coverage_mask:
        cmd.extend(["--coverage-mask", args.coverage_mask])
    if args.detection_threshold:
        cmd.extend(["--detection-threshold", args.detection_threshold])
    
    return " ".join(cmd)

def run_rnaseqc(args, main_path, meta_info, parallel_number, res_dir, log_file):
    task_pids = {}
    task_info = {}
    task_num = len(meta_info)
    
    for data in meta_info:
        task_info[data[0]] = data[1]
        cmd = parse_rnaseqc(args, main_path, data[0], data[1], res_dir)
        print_info("INFO", "Running RNA-SeQC for (sample: {sample})".format(sample=data[0]), log_file)
        print_info("CMD", cmd, log_file)
        pid = subprocess.Popen(cmd, shell = True)
        task_pids[data[0]] = pid
        task_num = task_num - 1

        while len(task_pids) == parallel_number or task_num == 0:
            samples = task_pids.keys()
            if len(samples) == 0:
                break
            for sample in samples:
                pid = task_pids[sample]
                if pid.poll() == None:
                    time.sleep(1)
                    continue
                if pid.returncode == 0:
                    print_info("INFO", "run RNA-SeQC for (sample: {}) successful !!!".format(sample), log_file)
                    task_pids.pop(sample)
                    #os.unlink(op.join(res_dir, "rnaseqc_res", sample+".exon_cv.tsv"))
                    #os.unlink(op.join(res_dir, "rnaseqc_res", sample+".metrics.tsv"))
                    break
                else:
                    for sample in samples:
                        task_pids[sample].kill()
                    print_info("ERROR", "run RNA-SeQC for (sample: {}) failed !!!".format(sample), log_file)

        

def get_matrix(meta_info, res_dir, log_file):
    TPM_dir = op.join(res_dir, "TPM_res")
    if not op.exists(TPM_dir):
        os.mkdir(TPM_dir)

    readsCount = pd.concat([pd.read_csv(op.join(res_dir, "rnaseqc_res", data[0]+".gene_reads.gct"), sep = "\t", skiprows = 2).loc[:,data[0]] for data in meta_info], axis = 1)
    readsCount.insert(0, "Gene", pd.read_csv(op.join(res_dir, "rnaseqc_res", meta_info[0][0]+".gene_reads.gct"), sep = "\t", skiprows = 2).loc[:, "Name"])
    readsCount_file = op.join(TPM_dir, "mop.reads.txt")
    readsCount.to_csv(readsCount_file, sep = "\t", index = 0, na_rep = "NA")
    
    TPM_matrix = pd.concat([pd.read_csv(op.join(res_dir, "rnaseqc_res", data[0]+".gene_tpm.gct"), sep = "\t", skiprows = 2).loc[:,data[0]] for data in meta_info], axis = 1)
    TPM_matrix.insert(0, "Gene", pd.read_csv(op.join(res_dir, "rnaseqc_res", meta_info[0][0]+".gene_tpm.gct"), sep = "\t", skiprows = 2).loc[:, "Name"])
    TPM_file = op.join(TPM_dir, "mop.tpm.txt")
    TPM_matrix.to_csv(TPM_file, sep = "\t", index = 0, na_rep = "NA")


# module1: to generate TPM matrix from bam files
def generate_TPM_matrix(args, main_path, meta_info, parallel_number, res_dir, log_file):
    # run collapse_annotation.pt to get gtf file
    print_info("MAIN", "RUN COLLAPSE_ANNOTATION", log_file)
    collapse_gtf(args, main_path, res_dir, log_file)

    # run featureCounts to get reads Count
    print_info("MAIN", "RUN RNA-SeQC", log_file)
    run_rnaseqc(args, main_path, meta_info, parallel_number, res_dir, log_file)

    # generate read count matrix and TPM matrix
    print_info("MAIN", "EXTRACT READ-COUNT MATRIX AND TPM MATRIX", log_file)
    get_matrix(meta_info, res_dir, log_file)
   

##### eOutlier module2 #####

# filter TPM matrix according conditions of GTEx
def GTEx_filter_tpm(res_dir, log_file):
    readCounts_file = op.join(res_dir, "TPM_res", "mop.reads.txt")
    readCounts_mat = pd.read_csv(readCounts_file, sep = "\t")
    
    TPM_file = op.join(res_dir, "TPM_res", "mop.tpm.txt")
    TPM_matrix = pd.read_csv(TPM_file, sep = "\t")
    
   
    print_info("MAIN", "GTEx FILTER", log_file)
    print_info("INFO", "before filter, TPM matrix: {} genes x {} samples".format(TPM_matrix.shape[0], TPM_matrix.shape[1] - 1), log_file)
    
    # retain gene with at least 6 reads and TPM > 0.1 in at least 20% of individuals
    readCounts_mat.index = readCounts_mat.iloc[:,0]
    TPM_matrix.index = TPM_matrix.iloc[:,0]
    samples = TPM_matrix.columns[1:].tolist()
    #index = [sum((readCounts_mat.loc[gene, samples] > 6) & (TPM_matrix.loc[gene, samples] > 0.1)) >= len(samples) * 0.2 for gene in TPM_matrix.index]
    #TPM_matrix = TPM_matrix.loc[index]
    print_info("INFO", "after filter, TPM matrix: {} genes x {} samples".format(TPM_matrix.shape[0], TPM_matrix.shape[1] - 1), log_file)

    
    print_info("INFO", "log2 transform", log_file)
    for sample in samples:
        TPM_matrix[sample] = np.log2(TPM_matrix[sample] + 2)

    print_info("INFO", "z_score normalization", log_file)
    TPM_z_score = TPM_matrix.apply(z_score_norm, axis = 1)
    
    TPM_z_score_file = op.join(res_dir, "TPM_res", "mop.tpm.log2.znorm.txt")
    TPM_z_score.to_csv(TPM_z_score_file, sep = "\t", index = 0, na_rep = "NA")


##### eOutlier module3 #####

# parse arguments for peertool
def parse_peertool(args, main_path, meta_info, res_dir):
    prog = op.join(main_path, "ext", "peertool")
    tpm_file = op.join(res_dir, "TPM_res", "temp.znorm.tpm.tab")
    peertool_dir = op.join(res_dir, "peertool_res")

    sample_size = len(meta_info)
    if sample_size <= 10:
        n_factors = sample_size - 1
    elif sample_size <= 150:
        n_factors = 10
    elif sample_size <= 250:
        n_factors = 30
    elif sample_size <= 350:
        n_factors = 45
    else:
        n_factors = 60

    cmd = [prog, 
            "-f", tpm_file,
            "-o", peertool_dir,
            "--has_header"]

    if args.n_factors:
        cmd.extend(["--n_factors", args.n_factors])
    else:
        cmd.extend(["--n_factors", str(n_factors)])

    if args.sigma_off:
        cmd.extend(["--sigma_off", args.sigma_off])
    if args.var_tol:
        cmd.extend(["--var_tol", args.var_tol])
    if args.bound_tol:
        cmd.extend(["--bound_tol", args.bound_tol])
    if args.e_pb:
        cmd.extend(["--e_pb", args.e_pb])
    if args.e_pa:
        cmd.extend(["--e_pa", args.e_pa])
    if args.a_pb:
        cmd.extend(["--a_pb", args.a_pb])
    if args.a_pa:
        cmd.extend(["--a_pa", args.a_pa])
    if args.n_iter:
        cmd.extend(["--n_iter", args.n_iter])
    if args.prior:
        cmd.extend(["--prior", args.prior])
    if args.cov_file:
        cmd.extend(["--cov_file", args.cov_file])
    if args.var_file:
        cmd.extend(["--var_file", args.var_file])
    if args.add_mean:
        cmd.extend(["--add_mean", args.add_mean])
    if args.no_a_out:
        cmd.extend(["--no_a_out", args.no_a_out])
    if args.no_z_out:
        cmd.extend(["--no_z_out", args.no_z_out])
    if args.no_w_out:
        cmd.extend(["--no_w_out", args.no_w_out])
    if args.no_x_out:
        cmd.extend(["--no_x_out", args.no_x_out])
    
    return " ".join(cmd)


# call peertool to get residuals of TPM matrix
def run_peertool(args, main_path, meta_info, res_dir, log_file):
    TPM_dir = op.join(res_dir, "TPM_res")
    peertool_dir = op.join(res_dir, "peertool_res")

    TPM_file = op.join(TPM_dir, "mop.tpm.log2.znorm.txt")
    TPM_matrix = pd.read_csv(TPM_file, sep = "\t").T
    
    tpm_for_peer_file = op.join(TPM_dir, "temp.znorm.tpm.tab")
    TPM_matrix.to_csv(tpm_for_peer_file, sep = "\t", index = 0, header = 0, na_rep = "NA")

    cmd = parse_peertool(args, main_path, meta_info, res_dir)
    print_info("INFO", "Running peertool", log_file)
    print_info("CMD", cmd, log_file)

    pid = subprocess.Popen(cmd, shell = True)
    pid.wait()
    
    # check wether peertool run successful or failed
    if pid.returncode == 0:
        print_info("INFO", "run peertool successful !!!", log_file)
    if not op.exists(op.join(peertool_dir, "residuals.csv")):
        print_info("ERROR", "run peertool failed !!!", log_file)


# extract residuals matrix from output of peertool
def extract_residuals_matrix(res_dir, log_file):
    TPM_dir = op.join(res_dir, "TPM_res")
    peertool_dir = op.join(res_dir, "peertool_res")

    TPM_file = op.join(TPM_dir, "mop.tpm.log2.znorm.txt")
    TPM_matrix = pd.read_csv(TPM_file, sep = "\t")
    
    # extract residuals matrix
    residuals_file = op.join(peertool_dir, "residuals.csv")
    residuals_matrix = pd.read_csv(residuals_file, header = None).T 
    
    residuals_matrix.insert(0, "GENE", TPM_matrix.iloc[:, 0])
    residuals_matrix.columns = TPM_matrix.columns
    
    residuals_file = op.join(peertool_dir, "residuals.txt")
    residuals_matrix.to_csv(residuals_file, sep = "\t", index = 0, na_rep = "NA")
    
    print_info("INFO", "residuals matrix: {} genes x {} samples".format(residuals_matrix.shape[0], residuals_matrix.shape[1] - 1), log_file)


def generate_residual_matrix(args, main, meta_info, res_dir, log_file):
    # run peertool to elimate batch effect
    print_info("MAIN", "RUN peertool", log_file)
    run_peertool(args, main, meta_info, res_dir, log_file)
    
    
    # extract residuals matrix as input for call_outlier()
    print_info("MAIN", "EXTRACT RESIDUALS MATRIX", log_file)
    extract_residuals_matrix(res_dir, log_file)



##### eOutlier module4 #####


# pick out outliers
def call_outlier(args, res_dir, log_file):
    print_info("MAIN", "CALCULATE Z_SCORE", log_file)
    z_score_dir = op.join(res_dir, "z_score_res")
    if not op.exists(z_score_dir):
        os.makedirs(z_score_dir)

    residuals_file = op.join(res_dir, "peertool_res", "residuals.txt")
    z_score_matrix = pd.read_csv(residuals_file, sep = "\t").apply(z_score_norm, axis = 1)

    z_score_file = op.join(z_score_dir, "mop.ztrans.residuals.txt")
    z_score_matrix.to_csv(z_score_file, sep = "\t", index = 0, na_rep = "NA")
    print_info("INFO", "Z_score matrix: {} genes x {} samples".format(z_score_matrix.shape[0], z_score_matrix.shape[1] - 1), log_file)

    # call outlier
    print_info("MAIN", "CALL OUTLIER", log_file)
    threshold_z = args.threshold
    (e_outlier_picked, e_zscore_extreme) = zscore_outliersFinder.call_outliers_z(z_score_file, threshold_z)
    
    e_outlier_picked.to_csv(op.join(res_dir, "expression_outliers_Z_score.txt"), sep = "\t", index = 0, na_rep = "NA")
    e_zscore_extreme.to_csv(op.join(res_dir, "extreme_Z_score.expression.txt"), sep = "\t", index = 0, na_rep = "NA")
    print_info("INFO", "eOutlier number {}".format(len(e_outlier_picked)), log_file)

    print_info("MAIN", "expression analysis successful", log_file)


# compute z-score 
def z_score_norm(x):
    line = x
    data = line[1:]
    if np.std(data, ddof = 1) < np.finfo(np.float64).eps:
        data = 0
    else:
        data = (data - np.mean(data)) / np.std(data, ddof = 1)
    line[1:] = data
    return line

# pipeline for expression analysis
def expression_call_outlier(args, main_path, meta_info, parallel_number, res_dir):
    log_file = op.join(res_dir, "eOutliers_log.txt")

    print_info("START", "mOutlier expression analysis start", log_file)

    ###### eOutlier module1 #####
    generate_TPM_matrix(args, main_path, meta_info, parallel_number, res_dir, log_file)

    ##### eOutlier module2 #####
    GTEx_filter_tpm(res_dir, log_file)

    ##### eOutlier module3 #####
    generate_residual_matrix(args, main_path, meta_info, res_dir, log_file) 
    
    ##### eOutlier module4 #####
    call_outlier(args, res_dir, log_file)


