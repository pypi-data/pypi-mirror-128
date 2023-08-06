# ---------------------- load libraries ----------------------
import os
import shutil
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
        print(time_str + "{info_type}:\t{cmd}\n".format(info_type = info_type, cmd = info_str))
        print(time_str + "{info_type}:\t{cmd}\n".format(info_type = info_type, cmd = info_str), file = log_handle)
    else:
        print(time_str + "{info_type}:\t{info_str}\n".format(info_type = info_type, info_str = info_str))
        print(time_str + "{info_type}:\t{info_str}\n".format(info_type = info_type, info_str = info_str), file = log_handle)
    if info_type == "ERROR":
        print(time_str + "\t########## RUN mOutlierPipe FAILED ##########")
        print(time_str + "\t########## RUN mOutlierPipe FAILED ##########", file = log_handle)
        log_handle.close()
        exit(1)
    log_handle.close()


##### sOutlier module1 #####

# generate cmd string for bam2junc.sh
def parse_bam2junc(main_path, bam_file, junc_file):
    prog = op.join(main_path, "ext", "leafcutter", "scripts", "bam2junc.sh")
    cmd = "{prog} {bam} {out}".format(prog=prog, bam=bam_file, out=junc_file)
    return cmd

# call bam2junc.sh to get junction counts
def run_bam2junc(main_path, meta_info, parallel_number, res_dir, log_file):
    if not op.exists(op.join(res_dir, "leafcutter_res")):
        os.mkdir(op.join(res_dir, "leafcutter_res"))
    
    junc_dir = op.join(res_dir, "leafcutter_res", "junc_res")
    if not op.exists(junc_dir):
        os.mkdir(junc_dir)

    task_pids = {}
    task_info = {}
    task_num = len(meta_info)
    
    for data in meta_info:
        junc_file = op.join(junc_dir, data[0] + ".junc")
        mop_junc_file = op.join(junc_dir, "mOutlierPipe." + data[0] + ".junc")
                
        if op.exists(mop_junc_file):
            print_info("INFO", "{} exists. run bam2junc done!".format(mop_junc_file), log_file)
            task_num = task_num - 1
            continue

        task_info[data[0]] = [junc_file, mop_junc_file]

        bam_file = op.abspath(data[1])
        cmd = parse_bam2junc(main_path, bam_file, junc_file)
        print_info("INFO", "Running bam2junc for (sample: {sample})".format(sample = data[0]), log_file)
        print_info("CMD", cmd, log_file)

        pid = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        task_pids[data[0]] = pid
        task_num = task_num - 1

        while len(task_pids) == parallel_number or task_num == 0:
            samples = task_pids.keys()
            if len(samples) == 0:
                break
            for sample in samples:
                pid = task_pids[sample]
                if pid.poll() == None:
                    continue
                if pid.returncode == 0:
                    print_info("INFO", "run bam2junc.sh for (sample: {}) successful !!!".format(sample), log_file)
                    junc_file = task_info[sample][0]
                    mop_junc_file = task_info[sample][1]
                    os.rename(junc_file, mop_junc_file)
                    
                    task_pids.pop(sample)
                    break
                else:
                    for sample in samples:
                        task_pids[sample].kill()
                    print_info("ERROR", "run bam2junc.sh for (sample: {}) failed !!!".format(sample), log_file)


# parse arguments for leafcutter_cluster.py
def parse_leafcutter_cluster(args, main_path, res_dir):
    prog = op.join(main_path, "ext", "leafcutter", "clustering", "leafcutter_cluster.py")
    juncfiles_path = op.join(res_dir, "leafcutter_res", "junc_file_path.txt") 
    run_dir = op.join(res_dir, "leafcutter_res")

    cmd = ["python", prog,
            "-j", juncfiles_path,
            "-r", run_dir]

    if args.maxintrolen:
        cmd.extend(["--maxintrolen", args.maxintrolen])
    if args.minclureads:
        cmd.extend(["--minclureads", args.minclureads])
    if args.minreads:
        cmd.extend(["--minreads", args.minreads])
    if args.mincluratio:
        cmd.extend(["--mincluratio", args.mincluratio])
    if args.checkchrom:
        cmd.extend(["--checkchrom", args.checkrom])
    if args.strand:
        cmd.extend(["--strand", args.strand])

    return " ".join(cmd)


# call leafcutter_cluster.py to generate JC matrix
def run_leafcutter_cluster(args, main_path, meta_info, res_dir, log_file):
    leafcutter_dir = op.join(res_dir, "leafcutter_res")
    junc_dir = op.join(res_dir, "leafcutter_res", "junc_res")

    JC_matrix_file = op.join(leafcutter_dir, "leafcutter_perind_numers.counts.gz")
    mop_JC_matrix_file = op.join(leafcutter_dir, "mOutlierPipe.leafcutter_perind_numers.counts.gz")
    if op.exists(mop_JC_matrix_file):
        print_info("INFO", "{} exists, run leafcutter done!".format(mop_JC_matrix_file), log_file)
        return

    junc_files = pd.Series([op.join(junc_dir, "mOutlierPipe." + x[0] + ".junc") for x in meta_info])
    juncfiles_path = op.join(leafcutter_dir, "junc_file_path.txt")
    junc_files.to_csv(juncfiles_path, index = 0, header = 0)
    
    cmd = parse_leafcutter_cluster(args, main_path, res_dir)
    print_info("INFO", "Running leafcutter_cluster", log_file)
    print_info("CMD", cmd, log_file)

    pid = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    pid.wait()

    if pid.returncode == 0:
        print_info("INFO", "run leafcutter successful !!!", log_file)
        JC_matrix_file = op.join(leafcutter_dir, "leafcutter_perind_numers.counts.gz")
        mop_JC_matrix_file = op.join(leafcutter_dir, "mOutlierPipe.leafcutter_perind_numers.counts.gz")
        os.rename(JC_matrix_file, mop_JC_matrix_file)
    else:
        print_info("ERROR", "run leafcutter failed !!!", log_file)


def gunzip_JC_matrix(meta_info, res_dir, log_file):
    leafcutter_dir = op.join(res_dir, "leafcutter_res")

    # decompression JC matrix file
    JC_matrix_file_gz = op.join(leafcutter_dir, "mOutlierPipe.leafcutter_perind_numers.counts.gz")
    JC_matrix_file = op.join(leafcutter_dir, "mOutlierPipe.leafcutter_perind_numers.counts")
    
    if op.exists(JC_matrix_file_gz) and not op.exists(JC_matrix_file):
        subprocess.Popen("gunzip " + JC_matrix_file_gz, shell = True).wait()
    
    if not op.exists(JC_matrix_file_gz) and not op.exists(JC_matrix_file):
        print_info("ERROR", "can't decompression JC_matrix file, please check your leafcutter run successful or not", log_file)

    columns = ["chrom"] + [x[0] for x in meta_info]
    JC_matrix = pd.read_csv(JC_matrix_file, sep = "\s+", skiprows = 1, names = columns)
    JC_matrix.to_csv(JC_matrix_file, sep = "\t", index = 0)


def generate_JC_matrix(args, main_path, meta_info, parallel_number, res_dir, log_file):
    # run bam2junc.sh to get junction count
    print_info("MAIN", "RUN bam2junc", log_file)
    run_bam2junc(main_path, meta_info, parallel_number, res_dir, log_file)

    # run leafcutter_cluster.py to get JC matrix
    print_info("MAIN", "RUN leafcutter_cluster", log_file)
    run_leafcutter_cluster(args, main_path, meta_info, res_dir, log_file)
    
    # decompress JC matrix file
    print_info("MAIN", "UNCOMPRESS JC_MATRIX FILE", log_file)
    gunzip_JC_matrix(meta_info, res_dir, log_file)


##### sOutlier module2 #####

# filter JC matrix according conditions of GTEx
def GTEx_filter_JC_matrix(res_dir, log_file):
    # deal with results of leafcutter as input for SPOT
    JC_matrix_file = op.join(res_dir, "leafcutter_res", "mOutlierPipe.leafcutter_perind_numers.counts")
    JC_matrix = pd.read_csv(JC_matrix_file, sep = "\t")

    print_info("MAIN", "GTEx FILTER", log_file)
    print_info("INFO", "before filter, JC matrix: {} junctions x {} samples".format(JC_matrix.shape[0], JC_matrix.shape[1] - 1), log_file)
    
    # condition 1
    index = (JC_matrix.iloc[:, 1:] >= 15).apply(sum, axis = 1) > 0
    JC_matrix = JC_matrix.loc[index]
    JC_matrix.index = range(len(JC_matrix))
    
    cluster_id = np.unique([x[3] for x in JC_matrix.chrom.str.split(":")])
    print_info("INFO", "after contidion-1, JC matrix: {} junctions x {} samples".format(JC_matrix.shape[0], JC_matrix.shape[1] - 1), log_file)
    print_info("INFO", "after contidion-1, JC matrix: {} clusters".format(len(cluster_id)), log_file)

    # condition 2
    JC_region_dict = {}
    # x[1]: start position    x[2]: end position    x[3]: cluster ID
    for x in JC_matrix.chrom.str.split(":"):
        if x[3] not in JC_region_dict:
            JC_region_dict[x[3]] = []
        JC_region_dict[x[3]].extend([x[1], x[2]])

    index = pd.Series([JC_region_dict[x[3]].count(x[1]) != 1 or JC_region_dict[x[3]].count(x[2]) != 1 for x in JC_matrix.chrom.str.split(":")])
    JC_matrix = JC_matrix.loc[index]
    JC_matrix.index = range(len(JC_matrix))

    cluster_id = np.unique([x[3] for x in JC_matrix.chrom.str.split(":")])
    print_info("INFO", "after condition-2, JC matrix: {} junctions x {} samples".format(JC_matrix.shape[0], JC_matrix.shape[1] - 1), log_file)
    print_info("INFO", "after condition-2, JC matrix: {} clusters".format(len(cluster_id)), log_file)

    # condition 3
    samples = JC_matrix.columns[1:].tolist()
    JC_matrix.insert(1, "clust", [x[3] for x in JC_matrix.chrom.str.split(":")])
    index = (JC_matrix.iloc[:, 1:].groupby(JC_matrix.clust).sum() < 3).apply(sum, axis = 1) <= len(samples) * 0.1
    JC_index = pd.Series([index[x] for x in JC_matrix.clust])
    JC_matrix = (JC_matrix.loc[JC_index]).drop("clust", axis = 1)
    
    cluster_id = np.unique([x[3] for x in JC_matrix.chrom.str.split(":")])
    print_info("INFO", "after condition-3, JC matrix: {} junctions x {} samples".format(JC_matrix.shape[0], JC_matrix.shape[1] - 1), log_file)
    print_info("INFO", "after condition-3, JC matrix: {} clusters".format(len(cluster_id)), log_file)

    # write to file
    filtered_JC_matrix_file = op.join(res_dir, "leafcutter_res", "filtered_leafcutter_perind_numers.counts")
    JC_matrix.to_csv(filtered_JC_matrix_file, sep = "\t", index = 0)
    


##### sOutlier module3 #####

# split JC matrix to accelarate SPOT's speed
def split_JC_matrix(split_number, res_dir, log_file):
    JC_matrix_file = op.join(res_dir, "leafcutter_res", "filtered_leafcutter_perind_numers.counts")
    
    JC_matrix_files = []
    if split_number == 0:
        JC_matrix_files.append(JC_matrix_file)
    else:
        JC_matrix_dir = op.join(res_dir, "leafcutter_res", "JC_matrix_dir")
        if not op.exists(JC_matrix_dir):
            os.mkdir(JC_matrix_dir)
        
        JC_matrix = pd.read_csv(JC_matrix_file, sep = "\t")
        cluster_id = np.unique([x[3] for x in JC_matrix.chrom.str.split(":")])
        
        # create cluster id group
        split_len = int(len(cluster_id) / split_number)
        split_cluster_id = [cluster_id[(x * split_len) : ((x + 1) * split_len)] for x in range(split_number - 1)]
        split_cluster_id.append(cluster_id[((split_number - 1) * split_len):])
        
        # split JC matrix
        for i in range(split_number):
            index = pd.Series([(x[3] in split_cluster_id[i]) for x in JC_matrix.chrom.str.split(":")])
            sub_JC_matrix = JC_matrix.loc[index]

            JC_file = op.join(JC_matrix_dir, "JC_matrix_file_" + str(i) + ".txt")
            sub_JC_matrix.to_csv(JC_file, sep = "\t", index = 0, na_rep = "NA")
            JC_matrix_files.append(JC_file)

            print_info("INFO", "JC matrix {}: {} junctions x {} samples".format(i, sub_JC_matrix.shape[0], sub_JC_matrix.shape[1] - 1), log_file)


# parse arguments for SPOT
def parse_SPOT(args, main_path, JC_file, prefix):
    prog = op.join(main_path, "ext", "SPOT", "spot.py")

    cmd = ["python", prog,
            "-j", JC_file,
            "--outprefix", prefix]

    if args.maxjunction:
        cmd.extend(["--maxjunction", args.maxjunction])
    if args.numbackgroundsamples:
        cmd.extend(["--numbackgroundsamples", args.numbackgroundsamples])
    if args.numsimulatedreads:
        cmd.extend(["--numsimulatedreads", args.numsimulatedreads])
    if args.seed:
        cmd.extend(["--seed", args.seed])

    return " ".join(cmd)


# call SPOT to generate pvalue matrix
def run_SPOT(args, main_path, meta_info, split_number, res_dir, log_file):
    leafcutter_dir = op.join(res_dir, "leafcutter_res")
    current_path = os.getcwd()
    SPOT_path = op.join(main_path, "ext", "SPOT")

    os.chdir(SPOT_path)
    
    JC_matrix_file = op.join(leafcutter_dir, "filtered_leafcutter_perind_numers.counts")
    if split_number == 0:
        JC_matrix_files = [JC_matrix_file]
    else:
        JC_matrix_files = [op.join(leafcutter_dir, "JC_matrix_dir", "JC_matrix_file_" + str(x) + ".txt") for x in range(split_number)]


    pids = []
    for i in range(split_number):
        cmd = parse_SPOT(args, main_path, JC_matrix_files[i], "spot_" + str(i))
        print_info("INFO", "Running SPOT for {}".format(JC_matrix_files[i]), log_file)
        print_info("CMD", cmd, log_file)

        pid = subprocess.Popen(cmd, shell = True)
        pids.append(pid)
    
    for pid in pids:
        pid.wait()
        if pid.returncode == 0:
            print_info("INFO", "Running SPOT for {} successful !!!".format(JC_matrix_files[i]), log_file)
        else:
            print_info("ERROR", "Running SPOT for {} failed !!!".format(JC_matrix_files[i]), log_file)

    os.chdir(current_path)


# extract P_value matrix from output of SPOT
def extract_P_value_matrix(main_path, split_number, res_dir, log_file):
    SPOT_path = op.join(main_path, "ext", "SPOT")
    spot_dir = op.join(res_dir, "spot_res")
    if not op.exists(spot_dir):
        os.mkdir(spot_dir)

    for i in range(split_number):
        pvalue_file = op.join(SPOT_path, "spot_" + str(i) + "_emperical_pvalue.txt")
        if op.exists(pvalue_file):
            shutil.move(pvalue_file, spot_dir)
        
        mdistance_file = op.join(SPOT_path, "spot_" + str(i) + "_md.txt")
        if op.exists(mdistance_file):
            shutil.move(mdistance_file, spot_dir)


    p_value_files = [op.join(spot_dir, "spot_"+str(x)+"_emperical_pvalue.txt") for x in range(split_number)]
    p_value_matrix = pd.concat([pd.read_csv(x, sep = "\t") for x in p_value_files], axis = 0)
    
    p_value_file = op.join(spot_dir, "spot_emperical_pvalue.txt")
    p_value_matrix.to_csv(p_value_file, sep = "\t", index = 0, na_rep = "NA")
    print_info("INFO", "p value matrix: {} genes x {} samples".format(p_value_matrix.shape[0], p_value_matrix.shape[1] - 1), log_file) 


# find gene id corresponding to specific cluster id
def run_get_cluster_gene(args, main_path, meta_info, res_dir, log_file):
    gtf_file = args.gtf
    cluster_file = op.join(res_dir, "leafcutter_res", "leafcutter_perind.counts.gz")
    prog = op.join(main_path, "ext", "leafcutter", "clustering", "get_cluster_gene.py")

    cmd = "python {prog} {gtf} {cluster}".format(prog=prog, gtf=gtf_file, cluster=cluster_file)
    print_info("INFO", "Running get_cluster_gene", log_file)
    print_info("CMD", cmd, log_file)
    subprocess.Popen(cmd, shell = True).wait()

    cluster2gene_file = op.join(res_dir,"leafcutter_res", "leafcutter.clu2gene.txt")
    gene = []
    with open(cluster2gene_file, "r") as f:
        for line in f:
            line = line.split()
            gene.append(line[0] + ":" + line[4])
    gene = set(gene)

    p_value_file = op.join(res_dir, "spot_res", "spot_emperical_pvalue.txt")
    p_value_matrix = pd.read_csv(p_value_file, sep = "\t")
    
    gene_id = []
    for i in range(len(p_value_matrix)):
        cluster_gene = [x for x in gene if p_value_matrix.CLUSTER_ID[i] in x]
        all_ID = p_value_matrix.CLUSTER_ID[i].split("_")[0:2] + [x.split(":")[1] for x in cluster_gene]
        gene_id.append("-".join(all_ID))
    
    p_value_matrix.CLUSTER_ID = gene_id
    p_value_file = op.join(res_dir, "spot_res", "spot_pvalue.txt")
    p_value_matrix.to_csv(p_value_file, sep = "\t", index = 0, na_rep = "NA")


def generate_pvalue_matrix(args, main_path, meta_info, res_dir, log_file):
    split_number = 5
    print_info("MAIN", "SPLIT JC MATRIX", log_file)
    split_JC_matrix(split_number, res_dir, log_file)

    print_info("MAIN", "RUN SPOT", log_file)
    run_SPOT(args, main_path, meta_info, split_number, res_dir, log_file)
    
    print_info("MAIN", "EXTRACT PVALUE MATRIX", log_file)
    extract_P_value_matrix(main_path, split_number, res_dir, log_file)

    print_info("MAIN", "ADD GENE ID", log_file)
    run_get_cluster_gene(args, main_path, meta_info, res_dir, log_file)
    


##### sOutlier module4 #####

# pick out outliers
def call_outlier(args, res_dir, log_file):
    # call outlier
    print_info("MAIN", "CALL OUTLIER", log_file)
    
    threshold_p = 2 * st.norm.cdf(-np.abs(args.threshold))

    pvalue_file = op.join(res_dir, "spot_res", "spot_pvalue.txt")
    (s_outlier_picked, s_pvalue_extreme) = zscore_outliersFinder.call_outliers_p(pvalue_file, threshold_p)
    s_outlier_picked.to_csv(op.join(res_dir, "splicing_outliers_P_value.txt"), sep = "\t", index = 0, na_rep = "NA")
    s_pvalue_extreme.to_csv(op.join(res_dir, "extreme_P_value.splicing.txt"), sep = "\t", index = 0, na_rep = "NA")
    
    print_info("INFO", "sOutlier number: {}".format(len(s_outlier_picked)), log_file)
    print_info("MAIN", "splicing analysis successful", log_file)

# pipeline for splicing analysis
def splicing_call_outlier(args, main_path, meta_info, parallel_number, res_dir):
    log_file = op.join(res_dir, "sOutliers_log.txt")

    print_info("START", "mOutlier splicing analysis start", log_file)

    ##### sOutlier module1 #####
    generate_JC_matrix(args, main_path, meta_info, parallel_number, res_dir, log_file)
    
    ##### sOutlier module2 #####
    GTEx_filter_JC_matrix(res_dir, log_file)
    
    ##### sOutlier module3 #####
    generate_pvalue_matrix(args, main_path, meta_info, res_dir, log_file)
    
    ##### sOutlier module4 #####
    call_outlier(args, res_dir, log_file)
