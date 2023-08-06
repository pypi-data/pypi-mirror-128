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
from ext.callOutliers import anevadot

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
        print(time_str + "\t########## RUN MODER FAILED ##########")
        print(time_str + "\t########## RUN MODER FAILED ##########")
        log_handle.close()
        exit(1)
    log_handle.close()


# call gtf2bed12.py to convert gtf file to bed file
def run_gtf2bed12(args, main_path, res_dir, log_file):
    phaser_dir = op.join(res_dir, "phaser_res")
    if not op.exists(phaser_dir):
        os.mkdir(phaser_dir)

    gtf_file = op.abspath(args.gtf)
    bed_file = op.join(res_dir, "phaser_res", "genome_anno.bed")
    mop_bed_file = op.join(res_dir, "phaser_res", "mop.genome_anno.bed")

    if op.exists(mop_bed_file):
        print_info("INFO", "{} exists, run gtf2bed12 done!".format(mop_bed_file), log_file)
        return

    prog = op.join(main_path, "ext", "callOutliers", "gtf2bed12.py")
    transcript2genename_file = op.join(op.dirname(bed_file), "transcript_to_geneName.txt")
    cmd = ["python", prog,
            "--gtf", gtf_file,
            "--out_bed", bed_file,
            "--transcript2genename", transcript2genename_file]
    cmd = " ".join(cmd)

    print_info("CMD", cmd, log_file)
    pid = subprocess.Popen(cmd, shell = True)
    pid.wait()

    # check wether gtf2bed12.py run successful or failed
    if pid.returncode == 0:
        print_info("INFO", "run gtf2bed12.py successful !!!", log_file)
        os.rename(bed_file, mop_bed_file)
    else:
        print_info("ERROR", "run gtf2bed12.py failed !!!", log_file)


# run samtools index 
def run_samtools_index(meta_info, parallel_number, res_dir, log_file):
    for data in meta_info:
        bam_file = op.abspath(data[1])
        cmd = "samtools index -@ " + str(parallel_number) + " " + bam_file
        print_info("INFO", "Running samtools index for (sample: {sample})".format(sample = data[0]), log_file)
        print_info("INFO", cmd, log_file)

        pid = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        pid.wait()

        if pid.returncode == 0:
            print_info("INFO", "run samtools index for (sample: {}) successfule !!!".format(data[0]), log_file)
        else:
            print_info("ERROR", "run samtools index for (sample: {}) failed !!!".format(data[0]), log_file)

# parse arguments for phASER
def parse_phaser(args, main_path, sample, bam_file, res_dir):
    prog = op.join(main_path, "ext", "phaser", "phaser", "phaser.py")
    sample_dir = op.join(res_dir, "phaser_res", sample)
    if not op.exists(sample_dir):
        os.mkdir(sample_dir)

    cmd = ["python", prog,
            "--mapq", args.mapq,
            "--baseq", args.baseq,
            "--bam", bam_file,
            "--vcf", args.vcf,
            "--sample", sample,
            "--o", op.join(sample_dir, sample),
            "--threads", str(args.parallel)]

    if args.single_end:
        cmd.extend(["--paired_end", "0"])
    else:
        cmd.extend(["--paired_end", "1"])

    if args.haplo_count_blacklist:
        cmd.extend(["--haplo_count_blacklist", args.haplo_count_blacklist])
    if args.cc_threshold:
        cmd.extend(["--cc_threshold", args.cc_threshold])
    if args.isize:
        cmd.extend(["--isize", args.isize])
    if args.as_q_cutoff:
        cmd.extend(["--as_q_cutoff", args.as_q_cutoff])
    if args.blacklist:
        cmd.extend(["--blacklist", args.blacklist])
    if args.write_vcf:
        cmd.extend(["--write_vcf", args.write_vcf])
    if args.include_indels:
        cmd.extend(["--include_indels", args.include_indels])
    if args.output_read_ids:
        cmd.extend(["--output_read_ids", args.output_read_ids])
    if args.remove_dups:
        cmd.extend(["--remove_dups", args.remove_dups])
    if args.pass_only:
        cmd.extend(["--pass_only", args.pass_only])
    if args.unphased_vars:
        cmd.extend(["--unphased_vars", args.unphased_vars])
    if args.chr_prefix:
        cmd.extend(["--chr_prefix", args.chr_prefix])
    if args.gw_phase_method:
        cmd.extend(["--gw_phase_method", args.gw_phase_method])
    if args.gw_af_field:
        cmd.extend(["--gw_af_field", args.gw_af_field])
    if args.gw_phase_vcf:
        cmd.extend(["--gw_phase_vcf", args.gw_phase_vcf])
    if args.gw_phase_vcf_min_confidence:
        cmd.extend(["--gw_phase_vcf_min_confidence", args.gw_phase_vcf_confidence])
    if args.max_block_size:
        cmd.extend(["--max_block_size", args.max_block_size])
    if args.max_items_per_thread:
        cmd.extend(["--max_items_per_thread", args.max_items_per_thread])
    if args.unique_ids:
        cmd.extend(["--unique_ids", args.unique_ids])
    if args.output_network:
        cmd.extend(["--output_network", args.output_network])
    if args.process_slow:
        cmd.extend(["--process_slow", args.process_slow])
    if args.id_separator:
        cmd.extend(["--id_separator", args.id_separator])
    if args.gw_cutoff:
        cmd.extend(["--gw_cutoff", args.gw_cutoff])
    if args.min_cov:
        cmd.extend(["--min_cov", args.min_cov])
    if args.min_haplo_maf:
        cmd.extend(["--min_haplo_maf", args.min_haplo_maf])

    return " ".join(cmd)

# run phaser
def run_phaser(args, main_path, meta_info, parallel_number, res_dir, log_file):
    prog = op.join(main_path, "ext", "phaser", "phaser", "phaser.py")

    for data in meta_info:
        cmd = parse_phaser(args, main_path, data[0], data[1], res_dir)
        print_info("INFO", "Running phaser for (sample: {})".format(data[0]), log_file)
        print_info("CMD", cmd, log_file)

        pid = subprocess.Popen(cmd, shell = True)
        pid.wait()

        if pid.returncode == 0:
            print_info("INFO", "run phaser for (sample: {}) successful !!!".format(data[0]), log_file)
        else:
            print_info("ERROR", "run phaser for (sample: {}) failed !!!".format(data[0]), log_file)


# parse arguments for phaser_gene_ae
def parse_phaser_gene_ae(args, main_path, sample, res_dir):
    prog = op.join(main_path, "ext", "phaser", "phaser_gene_ae", "phaser_gene_ae.py")
    
    phaser_dir = op.join(res_dir, "phaser_res")
    sample_dir = op.join(res_dir, "phaser_res", sample)
    hap_counts_file = op.join(res_dir, "phaser_res", sample, sample+".haplotypic_counts.txt")
    bed_file = op.join(res_dir, "phaser_res", "mop.genome_anno.bed")

    cmd = ["python", prog,
            "--haplotypic_counts", hap_counts_file,
            "--features", bed_file,
            "--o", op.join(phaser_dir, sample+".phaser_gene_ae.txt")]

    if args.id_separator:
        cmd.extend(["--id_separator", args.id_separator])
    if args.gw_cutoff:
        cmd.extend(["--gw_cutoff", args.gw_cutoff])
    if args.min_cov:
        cmd.extend(["--min_cov", args.min_cov])
    if args.min_haplo_maf:
        cmd.extend(["--min_haplo_maf", args.min_haplo_maf])

    return " ".join(cmd)


# run phaser
def run_phaser_gene_ae(args, main_path, meta_info, parallel_number, res_dir, log_file):
    task_pids = {}
    task_info = {}
    task_num = len(meta_info)

    for data in meta_info:
        task_info[data[0]] = data[1]
        cmd = parse_phaser_gene_ae(args, main_path, data[0], res_dir)
        print_info("INFO", "Running phaser_gene_ar for (sample: {})".format(data[0]), log_file)
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
                    print_info("INFO", "run phaser_gene_ae for (sample: {}) successful !!!".format(sample), log_file)
                    task_pids.pop(sample)
                    break
                else:
                    for sample in samples:
                        task_pids[sample].kill()
                    print_info("ERROR", "run phaser_gene_ae for (sample: {}) failed !!!".format(sample), log_file)



# run ANEVA-DOT
def run_aneva_dot(args, meta_info, parallel_number, res_dir, log_file):
    aneva_dir = op.join(res_dir, "aneva_res")
    if not op.exists(aneva_dir):
        os.mkdir(aneva_dir)

    ase_res = {}
    task_pids = {}
    task_info = {}
    task_num = len(meta_info)
    for data in meta_info:
        task_info[data[0]] = data[1]
        ase_res[data[0]] = []

        ase_count_file = op.join(res_dir, "phaser_res", data[0]+".ase_count.txt")
        ase_count_mat = pd.read_csv(ase_count_file, sep = "\t")
        ase_count_mat["GENE_ID"] = [x.split(".")[0].strip() for x in ase_count_mat["GENE_ID"].tolist()]
        ase_res[data[0]].append(ase_count_mat)

        tissue = args.tissue
        Vg_GTEx_v7 = pd.read_csv(args.variance, sep = "\t")
        ase_count_mat.insert(1, "TISSUE_ID", tissue)
        ase_count_mat.insert(5, "NULL_RATIO", anevadot.get_r0(ase_count_mat, eh1 = "REF_COUNT", eh2 = "ALT_COUNT"))

        covered_ase_data = ase_count_mat.loc[ase_count_mat.GENE_ID.isin(Vg_GTEx_v7.IDs)].copy()
        covered_ase_data.sort_values("GENE_ID", inplace = True)

        output_columns = ["GENE_ID", "TISSUE_ID", "REF_COUNT", "ALT_COUNT", "TOTAL_COUNT", "NULL_RATIO"]

        covered_Vgs = Vg_GTEx_v7.loc[Vg_GTEx_v7.IDs.isin(ase_count_mat.GENE_ID), :]
        covered_Vgs = covered_Vgs.loc[:, ["IDs", tissue]]
        covered_Vgs.columns = ["GENE_ID", tissue]
        covered_Vgs = pd.merge(covered_ase_data, covered_Vgs)

        covered_gene_SDgs = np.sqrt(covered_Vgs[tissue])
        
        covered_ase_data.index = range(0, len(covered_ase_data.index))
        
        ANEVADOT_scores = anevadot.ANEVADOT_test(covered_ase_data,
                Eg_std = covered_gene_SDgs,
                output_columns = output_columns,
                eh1 = "REF_COUNT",
                eh2 = "ALT_COUNT",
                r0 = covered_ase_data["NULL_RATIO"],
                coverage = 10)
        
        ANEVADOT_scores = ANEVADOT_scores.loc[ANEVADOT_scores["p_value"].notnull()]
        ANEVADOT_scores.index = ANEVADOT_scores["GENE_ID"]
        outlier_gene = ANEVADOT_scores.loc[ANEVADOT_scores["p_value"] < 0.05]
        outlier_gene = outlier_gene["p_value"]

        print(outlier_gene)
        ase_res[data[0]].append(outlier_gene)

        aneva_file = op.join(res_dir, "aneva_res", data[0]+".aneva.txt")
        ANEVADOT_scores.to_csv(aneva_file, sep = "\t", index = 0)

    samples = np.array([x for x in ase_res])
    test_gene = np.array([len(ase_res[x][0]) for x in ase_res])
    outlier_gene = np.array([len(ase_res[x][1]) for x in ase_res])

    lower = np.quantile(test_gene, 0.25)
    higher = np.quantile(test_gene, 0.75)
    print(lower, higher)
    test_gene = test_gene >= lower - 1.5 * (higher - lower)

    lower = np.quantile(outlier_gene, 0.25)
    higher = np.quantile(outlier_gene, 0.75)
    print(lower, higher)
    outlier_gene = outlier_gene <= higher + 1.5 * (higher - lower)

    samples = samples[test_gene & outlier_gene]
    print(test_gene)
    print(outlier_gene)
    print(test_gene & outlier_gene)
    
    pvalue_mat = pd.concat([ase_res[x][1] for x in samples], axis = 1)
    pvalue_mat.columns = samples
    pvalue_mat.insert(0, "Gene", pvalue_mat.index)
    pvalue_mat = pvalue_mat.fillna(1)
    print(pvalue_mat)

# -------------------- ASE OUTLIERS MODULE --------------------

##### aseOutliers module1 #####
def generate_ASE_count(args, main_path, meta_info, parallel_number, res_dir, log_file):
    print_info("MAIN", "RUN gtf2bed", log_file)
    run_gtf2bed12(args, main_path, res_dir, log_file)

    print_info("MAIN", "RUN samtool index", log_file)
    run_samtools_index(meta_info, parallel_number, res_dir, log_file)

    print_info("MAIN", "RUN phaser", log_file)
    run_phaser(args, main_path, meta_info, parallel_number, res_dir, log_file)

    print_info("MAIN", "RUN phaser_gene_ae", log_file)
    run_phaser_gene_ae(args, main_path, meta_info, parallel_number, res_dir, log_file)


###### aseOutlier module2 #####
def GTEx_filter_ASE_count(args, meta_info, res_dir, log_file):
    print("MAIN", "GTEx FILTER", log_file)

    for data in meta_info:
        ase_count_file = op.join(res_dir, "phaser_res", data[0]+".phaser_gene_ae.txt")
        ase_count_mat = pd.read_csv(ase_count_file, sep = "\t")
        ase_count_mat = ase_count_mat.loc[:, ["name", "aCount", "bCount", "totalCount"]]
        ase_count_mat.columns = ["GENE_ID", "REF_COUNT", "ALT_COUNT", "TOTAL_COUNT"]
        ase_count_mat = ase_count_mat.loc[ase_count_mat.TOTAL_COUNT >= args.min_alleic_counts]
        
        ase_count_file = op.join(res_dir, "phaser_res", data[0]+".ase_count.txt")
        ase_count_mat.to_csv(ase_count_file, sep = "\t", index = 0)


##### aseOutliers module3 #####
def compute_pvalue(args, meta_info, parallel_number, res_dir, log_file):
    print_info("MAIN", "RUN ANEVA-DOT", log_file)
    run_aneva_dot(args, meta_info, parallel_number, res_dir, log_file)



# pipeline for ase analysis
def ase_call_outlier(args, main_path, meta_info, parallel_number, res_dir):
    log_file = op.join(res_dir, "aseOutliers_log.txt")
    
    print_info("START", "mOutlierPipe ASE analysis start", log_file)

    ##### aseOutliers module1 #####
    generate_ASE_count(args, main_path, meta_info, parallel_number, res_dir, log_file)

    ##### aseOutliers module2 #####
    GTEx_filter_ASE_count(args, meta_info, res_dir, log_file)

    ##### aseOutliers module3 #####
    compute_pvalue(args, meta_info, parallel_number, res_dir, log_file)
    
