# -------------------- load library --------------------
import os
import sys
import time
import math
import argparse
import threading
import os.path as op
from src import splicing
from src import expression
from src import ase

# parse meta info
def get_meta_info(file_path):
    meta_info = []
    with open(file_path, "r") as f:
        i = 0
        for line in f:
            i = i + 1
            data = line.strip().split()
            if len(data) == 1:
                sample_and_file = ("sample" + str(i), data[0])
            else:
                sample_and_file = (data[0], data[1])

            meta_info.append(sample_and_file)

    return meta_info



# -------------------- main function --------------------
def run_mOutlierPipe(args):
    # get ext program path
    try:
        import ext.callOutliers
        main_path = op.dirname(op.dirname(ext.callOutliers.__file__))
    except:
        main_path = op.dirname(op.abspath(sys.argv[0]))
    print(main_path)


    # parse arguments
    file_path = op.abspath(args.input)
    dir = args.output
    
    # get info about bam file
    meta_info = get_meta_info(file_path)
    
    print(meta_info)
    bam_files = [op.abspath(x[1]) for x in meta_info]
    if len(bam_files) != len(set(bam_files)):
        print("ERROE: please check your bam files, same bam files are not allowed")
        exit(1)

    # create output directory
    if dir == ".":
        dir = "output"
    if not dir.startswith("/"):
        dir = "./" + dir
    dir = op.abspath(dir)
    if not op.exists(dir):
        os.makedirs(dir)

    # invoke data analysis pipeline
    if args.expression:
        expression.expression_call_outlier(args, main_path, meta_info, args.parallel, dir)
    elif args.splicing:
        splicing.splicing_call_outlier(args, main_path, meta_info, args.parallel, dir)
    elif args.ase:
        ase.ase_call_outlier(args, main_path, meta_info, args.parallel, dir)
    else:
        try:
            expression_parallel = max(math.ceil(args.parallel / 3), 1) 
            splicing_parallel = max(math.ceil(args.parallel / 3), 1)
            ase_parallel = max(args.parallel - expression_parallel - splicing_parallel, 1)

            # expression data analysis
            expression_dir = op.join(dir, "expression_res")
            if not op.exists(expression_dir):
                os.makedirs(expression_dir)
            t1 = threading.Thread(target = expression.expression_call_outlier, args = (args, main_path, meta_info, expression_parallel, expression_dir))
            t1.daemon = True
            # splicing data analysis
            splicing_dir = op.join(dir, "splicing_res")
            if not op.exists(splicing_dir):
                os.makedirs(splicing_dir)
            t2 = threading.Thread(target = splicing.splicing_call_outlier, args = (args, main_path, meta_info, splicing_parallel, splicing_dir))
            t2.daemon = True
            # ase data analysis
            ase_dir = op.join(dir, "ase_res")
            if not op.exists(ase_dir):
                os.makedirs(ase_dir)
            t3 = threading.Thread(target = ase.ase_call_outlier, args = (args, main_path, meta_info, ase_parallel, ase_dir))


            t1.start()
            t2.start()
            t3.start()
            t1.join()
            t2.join()
            t3.join()

            if op.exists(op.join(expression_dir, "expression_outliers_Z_score.txt")) and op.exists(op.join(expression_dir, "extreme_Z_score.expression.txt")):
                print("Success: expression pipeline!")
            else:
                print("Error: expression pipeline, you can add --expression option to run it again")
            if op.exists(op.join(splicing_dir, "splicing_outliers_P_value.txt")) and op.exists(op.join(splicing_dir, "extreme_P_value.splicing.txt")):
                print("Success: splicing pipeline!")
            else:
                print("Error: splicing pipeline, you can add --splicing option to run it again")
            if op.exists(op.join(ase_dir, "ase_outliers_P_value.txt")) and op.exists(op.join(ase_dir, "extreme_P_value.splicing.txt")):
                print("Success: ase pipeline!")
            else:
                print("Error: ase pipeline, you can add --ase option to run it again")
        except KeyboardInterrupt as e:
            print("ERROR: KeyboardInterrupt")



# -------------------- parse arguments --------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "mOutlierPipe", 
        usage = "python mOutlierPipe.py -i input_bam.txt --gtf genome.gtf -o ./output_dir -p 8")

    # mode Arguments
    modeArgs = parser.add_mutually_exclusive_group(required = False)
    modeArgs.add_argument("--splicing", action = "store_true", 
        help = "assign mode to analysis Splicing data")
    modeArgs.add_argument("--expression", action = "store_true", 
        help = "assign mode to analysis Gene Expression data")
    modeArgs.add_argument("--ase", action = "store_true", 
        help = "assign mode to analysis ASE data")
    
    # basic Arguments
    basicArgs = parser.add_argument_group("Basic Arguments")
    basicArgs.add_argument("-i", "--input", required = True, metavar = "",
        help = "txt file with all input like (sample name, bam file path) which separated by tab")
    basicArgs.add_argument("-o", "--output", required = False, metavar = "", default = ".", 
        help = "separate diretory to store all resulting files. by default, \
                program will create a directory in current working directory")
    basicArgs.add_argument("-p", "--parallel", required = False, metavar = "", type = int, default = 1,
        help = "an int type number, assign max progress number and thread number to perform calculations")
    basicArgs.add_argument("--gtf", required = False, metavar = "",
        help = "Genome annotation file in GTF format")
    basicArgs.add_argument("--vcf", required = False, metavar = "",
        help = "vcf file path")
    basicArgs.add_argument("--variant", required = False, metavar = "",
        help = "variant file path")
    basicArgs.add_argument("--single_end", action = "store_true",
        help = "required for single-end libraries")
    basicArgs.add_argument("--tissue", required = False, metavar = "",
        help = "tissue of the sample")

    basicArgs.add_argument("-z", "--threshold", required = False, metavar = "", type = float, default = 2,
        help = "threshold of z_score, control filtering condition by adjusting this \
                argument to find results which z_score's absolute value larger than threshod")
    basicArgs.add_argument("--min_read_count", required = False, metavar = "", type = float, default = 6,
        help = "threshold of minimal reads counts in expression pipeline")
    basicArgs.add_argument("--min_TPM", required = False, metavar = "", type = float, default = 0.1,
        help = "threshold of minimal TPM value in expression pipeline")
    basicArgs.add_argument("--min_junction", required = False, metavar = "", type = float, default = 15,
        help = "threshold of minimal junction counts in splicing pipeline")
    basicArgs.add_argument("--min_alleic_counts", required = False, metavar = "", type = int, default = 8,
        help = "threshold of minimal alleic counts in ase pipeline")
    basicArgs.add_argument("--expression_percent", required = False, metavar = "", type = float, default = 0.1,
        help = "the maximum percent missing data allowed in any row in TPM matrix")
    basicArgs.add_argument("--splicing_percent", required = False, metavar = "", type = float, default = 0.1,
        help = "the maximum percent missing data allowed in any row in JC matrix")


    # RNA-SeQC Arguments
    rnaseqcArgs = parser.add_argument_group("RNA-SeQC Arguments")

    rnaseqcArgs.add_argument("--bed", required = False, metavar = "",
        help = "Optional input BED file containin non-overlapping exons used \
                for fragment size calculations")
    rnaseqcArgs.add_argument("--fasta", required = False, metavar = "",
        help = "Optional input FASTA/FASTQ file containing the reference used\
                for parsing CRAM files")
    rnaseqcArgs.add_argument("--chimeric_distance", required = False, metavar = "", default = "2000000",
        help = "Set the maximum accepted distance between read mates. Mates beyond \
                this distance will be counted as chimeric pairs. Default: 2000000 [bp]")
    rnaseqcArgs.add_argument("--fragment_samples", required = False, metavar = "", default = "1000000",
        help = "Set the number of samples to take when computing fragment sizes. \
                will be counted as chimeric pairs. Default: 2000000 [bp]")
    rnaseqcArgs.add_argument("--mapping_quality", required = False, metavar = "", default = "255",
        help = "Set the lower bound on read quality for exon coverage counting. Reads \
                below this number are excluded from coverage metrics. Default: 255")
    rnaseqcArgs.add_argument("--base_mismatch", required = False, metavar = "", default = "6",
        help = "Set the maximum number of allowed mismatches between a read and the \
                reference sequence. Reads with more than this number of mismatches are \
                excluded from coverage metrics. Default: 6")
    rnaseqcArgs.add_argument("--offset", required = False, metavar = "", default = "150",
        help = "Set the offset into the gene for the 3' and 5' windows in bias calculation. \
                A positive value shifts the 3' and 5' windows towards eachother, while a \
                negative value shifts them apart. Default: 150 [bp]")
    rnaseqcArgs.add_argument("--window_size", required = False, metavar = "", default = "100",
        help = "Set the size of the 3' and 5' windows in bias calculation. Default: 100 [bp]")
    rnaseqcArgs.add_argument("--gene_length", required = False, metavar = "", default = "600",
        help = "Set the minimum size of a gene for bias calculation. Genes below this \
                size are ignored in the calculation. Default: 600[bp]")
    rnaseqcArgs.add_argument("--legacy", action = "store_true", 
        help = "Use legacy counting rules. Gene and exon counts match output of RNA-SeQC 1.1.9")
    rnaseqcArgs.add_argument("--stranded", required = False, metavar = "", 
        help = "Use strand-specific metrics. Only features on the same strand of a read will \
                be considered. Allowed values are 'RF', 'rf', 'FR', and 'fr'")
    rnaseqcArgs.add_argument("--tag", required = False, metavar = "",
        help = "Filter out reads with the specified tag.")
    rnaseqcArgs.add_argument("--chimeric_tag", required = False, metavar = "",
        help = "Reads maked with the specified tag will be labeled as Chimeric.")
    rnaseqcArgs.add_argument("--exclude_chimeric", action = "store_true",
        help = "Exclude chimeric reads from the read counts")
    rnaseqcArgs.add_argument("--rpkm", action = "store_true",
        help = "Output gene RPKM values instead of TPMs")
    rnaseqcArgs.add_argument("--coverage", required = False, metavar = "",
        help = "If this flag is provided, coverage statistics for each transcript will \
                be written to a table. Otherwise, only summary coverage statistics are \
                generated and added to the metrics table")
    rnaseqcArgs.add_argument("--coverage_mask", required = False, metavar = "", default = "500",
        help = "Sets how many bases at both ends of a transcript are masked out when \
                computing per-base exon coverage. Default: 500bp")
    rnaseqcArgs.add_argument("--detection_threshold", required = False, metavar = "", default = "5",
        help = "Number of counts on a gene to consider the gene 'detected'. Additionally, \
                genes below this limit are excluded from 3' bias computation. Default: 5 reads")

    # peertool arguments
    peertoolArgs = parser.add_argument_group("peertool Arguments")
    peertoolArgs.add_argument("--sigma_off", required = False, metavar = "",
        help = "Variance inactive component")
    peertoolArgs.add_argument("--var_tol", required = False, metavar = "",
        help = "Variation tolerance")
    peertoolArgs.add_argument("--bound_tol", required = False, metavar = "",
        help = "Bound tolerance")
    peertoolArgs.add_argument("--e_pb", required = False, metavar = "", 
        help = "Eps node prior parameter b")
    peertoolArgs.add_argument("--e_pa", required = False, metavar = "",
        help = "Eps node prior parameter a")
    peertoolArgs.add_argument("--a_pb", required = False, metavar = "",
        help = "Alpha node prior parameter b")
    peertoolArgs.add_argument("--a_pa", required = False, metavar = "",
        help = "Alpha node prior parameter a")
    peertoolArgs.add_argument("--n_iter", required = False, metavar = "",
        help = "Number of iterations")
    peertoolArgs.add_argument("--n_factors", required = False, metavar = "",
        help = "Number of hidden factors")
    peertoolArgs.add_argument("--prior", required = False, metavar = "",
        help = "Factor prior file")
    peertoolArgs.add_argument("--cov_file", required = False, metavar = "",
        help = "Covariate data file")
    peertoolArgs.add_argument("--var_file", required = False, metavar = "",
        help = "Expression uncertainty (variance) data file")
    peertoolArgs.add_argument("--add_mean", required = False, metavar = "",
        help = "Add a covariate to model mean effect")
    peertoolArgs.add_argument("--no_a_out", required = False, metavar = "",
        help = "No output of weight precision")
    peertoolArgs.add_argument("--no_z_out", required = False, metavar = "",
        help = "No output of posterior sparsity prior")
    peertoolArgs.add_argument("--no_w_out", required = False, metavar = "",
        help = "No output of estimated factor weights")
    peertoolArgs.add_argument("--no_x_out", required = False, metavar = "",
        help = "No output of estimated factors")
    peertoolArgs.add_argument("--ignore_rest", required = False, metavar = "",
        help = "Ignores the rest of the labeled arguments following this flag.")


    # leafcutter arguments
    leafcutterArgs = parser.add_argument_group("leafcutter Arguments")
    leafcutterArgs.add_argument("--maxintrolen", required = False, metavar = "",
        help = "maximum intron length in bp (default 100,000bp)")
    leafcutterArgs.add_argument("--minclureads", required = False, metavar = "",
        help = "minimum reads in a cluster (default 30 reads)")
    leafcutterArgs.add_argument("--minreads", required = False, metavar = "",
        help = "minimum reads for an intron (default 5 reads)")
    leafcutterArgs.add_argument("--mincluratio", required = False, metavar = "",
        help = "minimum fraction of reads in a cluster that support a junction (default 0.001)")
    leafcutterArgs.add_argument("--checkchrom", required = False, metavar = "",
        help = "check that the chromosomes are well formated e.g. chr1, chr2, ..., or 1, 2, ... (default=False)")
    leafcutterArgs.add_argument("--strand", required = False, metavar = "",
        help = "use strand info")

    # SPOT arguments
    spotArgs = parser.add_argument_group("SPOT Arguments")
    spotArgs.add_argument("--maxjunction", required = False, metavar = "",
        help = "maximum number of junctions per LeafCutter cluster")
    spotArgs.add_argument("--numbackgroundsamples", required = False, metavar = "", default = "1000000",
        help = "Number of randomly drawn samples per cluster used to generate an emperical mahalanobis distance distribution")
    spotArgs.add_argument("--numsimulatedreads", required = False, metavar = "", default = "20000",
        help = "Number of reads per simulated sample")
    spotArgs.add_argument("--seed", required = False, metavar = "",
        help = "Seed used for random number generator in both optimization and \
                generating random samples for a mahalanobis distance emperical distribution")


    # phaser arguments
    phaserArgs = parser.add_argument_group("phASER Arguments")
    phaserArgs.add_argument("--mapq", required = False, metavar = "", default = "255",
        help = "Minimum MAPQ for reads to be used for phasing. Can be  comma separated list, \
                each value corresponding to the min MAPQ for a file in the input BAM list. Useful \
                in cases when using both for example DNA and RNA libraries which might have \
                differing mapping qualities.")
    phaserArgs.add_argument("--baseq", required = False, metavar = "", default = "10",
        help = "Minimum baseq for bases to be used for phasing")
    phaserArgs.add_argument("--haplo_count_blacklist", required = False, metavar = "",
        help = "BED file containing genomic intervals to be excluded from haplotypic counts. Reads from \
                any variants which lie within these regions will not be counted for haplotypic counts.")
    phaserArgs.add_argument("--cc_threshold", required = False, metavar = "", 
        help = "Threshold for significant conflicting variant configuration. The connection between \
                any two variants with a conflicting configuration having p-value lower than this \
                threshold will be removed.")
    phaserArgs.add_argument("--isize", required = False, metavar = "",
        help = "Maximum allowed insert size for read pairs. Can be a comma separated list, each value \
                corresponding to a max isize for a file in the input BAM list. Set to 0 for no maximum size.")
    phaserArgs.add_argument("--as_q_cutoff", required = False, metavar = "",
        help = "Bottom quantile to cutoff for read alignment score.")
    phaserArgs.add_argument("--blacklist", required = False, metavar = "",
        help = "BED file containing genomic intervals to be excluded from phasing (for example HLA).")
    phaserArgs.add_argument("--write_vcf", required = False, metavar = "",
        help = "Create a VCF containing phasing information (0,1).")
    phaserArgs.add_argument("--include_indels", required = False, metavar = "",
        help = "Include indels in the analysis (0,1). NOTE: since mapping is a problem for indels \
                including them will likely result in poor quality phasing unless specific precautions \
                have been taken.")
    phaserArgs.add_argument("--output_read_ids", required = False, metavar = "",
        help = "Output read IDs in the coverage files (0,1).")
    phaserArgs.add_argument("--remove_dups", required = False, metavar = "",
        help = "Remove duplicate reads from all analyses (0,1).")
    phaserArgs.add_argument("--pass_only", required = False, metavar = "",
        help = "Only use variants labled with PASS in the VCF filter field (0,1).")
    phaserArgs.add_argument("--unphased_vars", required = False, metavar = "",
        help = "Output unphased variants (singletons) in the haplotypic_counts and haplotypes \
                files (0,1).")
    phaserArgs.add_argument("--chr_prefix", required = False, metavar = "",
        help = "Add the string to the begining of the VCF contig name. For example set to 'chr' \
                if VCF contig is listed as '1' and bam reference is 'chr1'.")
    phaserArgs.add_argument("--gw_phase_method", required = False, metavar = "",
        help = "Method to use for determing genome wide phasing. NOTE requires input VCF to be \
                phased and have allele frequencies for MAF weighted mode (see --gw_af_field) \
                0 = Use most common haplotype phase. 1 = MAF weighted phase anchoring.")
    phaserArgs.add_argument("--gw_af_field", required = False, metavar = "",
        help = "Field from --vcf to use for allele frequency.")
    phaserArgs.add_argument("--gw_phase_vcf", required = False, metavar = "",
        help = "Replace GT field of output VCF using phASER genome wide phase. 0: do not replace; \
                1: replace when gw_confidence >= --gw_phase_vcf_min_confidence; 2: as in (1), \
                but in addition replace with haplotype block phase when gw_confidence < \
                --gw_phase_vcf_min_confidence and include PS field. See --gw_phase_method \
                for options.")
    phaserArgs.add_argument("--gw_phase_vcf_min_confidence", required = False, metavar = "",
        help = "If replacing GT field in VCF, only replace when phASER haplotype gw_confidence \
                >= this value.")
    phaserArgs.add_argument("--max_block_size", required = False, metavar = "",
        help = "Maximum number of variants to phase at once. Number of haplotypes tested = 2 ^ # \
                variants in block. Blocks larger than this will be split into sub blocks, phased, \
                and then the best scoring sub blocks will be phased with each other.")
    phaserArgs.add_argument("--max_items_per_thread", required = False, metavar = "",
        help = "Maximum number of items that can be assigned to a single thread to process. NOTE: \
                if this number is too high Python will stall when trying to join the pools.")
    phaserArgs.add_argument("--unique_ids", required = False, metavar = "",
        help = "Generate and output unique IDs instead of those provided in the VCF (0,1). NOTE: \
                this should be used if your VCF does not contain a unique ID for each variant.")
    phaserArgs.add_argument("--output_network", required = False, metavar = "",
        help = "Output the haplotype connection network for the given variant.")
    phaserArgs.add_argument("--process_slow", required = False, metavar = "",
        help = "Argument to process data slow in chunks (by chromosome) to handle memory limits.")
    phaserArgs.add_argument("--id_separator", required = False, metavar = "",
        help = "Separator used for generating unique variant IDs when phASER was run.")
    phaserArgs.add_argument("--gw_cutoff", required = False, metavar = "",
        help = "Minimum genome wide phase confidence for phASER haplotype blocks.")
    phaserArgs.add_argument("--min_cov", required = False, metavar = "",
        help = "Minimum total coverage for a feature to be outputted.")
    phaserArgs.add_argument("--min_haplo_maf", required = False, metavar = "",
        help = "The minimum MAF used to phase a haplotype for it to be considered genome wide phased when \
                generating gene level counts. Setting this number higher will result in more confident \
                phasing if genotypes were population prephased. Value must be between 0 and 0.5.")

    # call main function
    args = parser.parse_args()
    run_mOutlierPipe(args)
