'''
#Convert a gtf into a bed file with 12 columns. In the output bed file, each row represents a transcript and blocks in each transcript are exons.
#Input: a gtf file
#Output: a bed file and a tab-separated file indicates the transcript_id and its corresponding gene_name
Usage: python gtf2bed12.py --gtf <gtf> --out <bed>
Code by: Xudong Zou
Start time: 2021-06-09
'''

import argparse
import re

# Function --------------------------------

# input a gtf file and generate a dictionary{transcript:[(s,e),(s,e),...]}
def extract_exon(gtf_file, comment):
    keep_chr = []
    keep_geneType = ["protein_coding", "protein_code", "lincRNA", "lncRNA"]
    for i in range(22):
        keep_chr.extend(["chr" + str(i + 1), str(i + 1)])
    keep_chr = keep_chr + ["chrX", "chrY", "X", "Y"]
    with open(gtf_file, "r") as fh:
        gene_exon = {}
        geneid, transcript_id, genename, genetype = "", "", "", ""
        for line in fh.readlines():
            if line.strip().startswith(comment):
                continue
            w = line.strip().split()
            w = w[0:8] + [" ".join(w[8:])]
            chrn = w[0]
            strand = w[6]
            entry_type = w[2]
            
            # build match patterns
            geneid_patt = re.search(r'gene_id\s"(\w+|\w+\.\d+)";', w[8])
            transcript_patt = re.search(r'transcript_id\s"(\w+|\w+\.\d+)";', w[8])
            genename_patt = re.search(r'gene_name\s"(.*?)";', w[8])
            genetype_patt = re.search(r'gene_[biotype|type]+\s"(.*?)";', w[8])

            gene_id = geneid_patt.group(1) if geneid_patt else "NA"
            genename = genename_patt.group(1) if genename_patt else "NA"
            genetype = genetype_patt.group(1) if genetype_patt else "NA"
            
            if geneid_patt:
                if genetype in keep_geneType:
                    gene_id = geneid_patt.group(1)
                    gene_id = gene_id + ":" + genename + ":" + chrn + ":" + strand

                    if entry_type == "exon" and chrn in keep_chr:
                        exon = (int(w[3]), int(w[4])) # 1-based coordinate ??
                        if gene_id not in gene_exon:
                            gene_exon[gene_id] = [exon]
                        else:
                            gene_exon[gene_id].append(exon)
                    else:
                        continue
                else:
                    continue

    return gene_exon


def extract_Codon(gtf_file, comment, codon_type):
    keep_chr = []
    keep_geneType = ["protein_coding", "protein_code", "lincRNA", "lncRNA"]
    for i in range(22):
        keep_chr.extend(["chr" + str(i + 1), str(i + 1)])
    keep_chr = keep_chr + ["chrX", "chrY", "X", "Y"]
    with open(gtf_file, "r") as fh:
        gene_Codon = {}
        geneid, transcript_id, genename, genetype = "", "", "", ""
        for line in fh.readlines():
            if line.strip().startswith(comment):
                continue
            w = line.strip().split()
            w = w[0:8] + [" ".join(w[8:])]
            chrn = w[0]
            strand = w[6]
            entry_type = w[2]
            
            # build match patterns
            geneid_patt = re.search(r'gene_id\s"(\w+|\w+\.\d+)";', w[8])
            transcript_patt = re.search(r'transcript_id\s"(\w+|\w+\.\d+)";', w[8])
            genename_patt = re.search(r'gene_name\s"(.*?)";', w[8])
            genetype_patt = re.search(r'gene_[biotype|type]+\s"(.*?)";', w[8])

            gene_id = geneid_patt.group(1) if geneid_patt else "NA"
            genename = genename_patt.group(1) if genename_patt else "NA"
            genetype = genetype_patt.group(1) if genetype_patt else "NA"

            if geneid_patt:
                if genetype in keep_geneType:
                    gene_id = geneid_patt.group(1) if geneid_patt else "NA"
                    gene_id = gene_id + ":" + genename + ":" + chrn + ":" + strand

                    if entry_type == codon_type and chrn in keep_chr:
                        gene_Codon[gene_id] = w[3]
                    else:
                        continue
                else:
                    continue
    
    return gene_Codon


def extract_transcript(gtf_file, comment):
    keep_chr = []
    keep_geneType = ["protein_coding", "protein_code", "lincRNA", "lncRNA"]
    for i in range(22):
        keep_chr.extend(["chr" + str(i + 1), str(i + 1)])
    keep_chr = keep_chr + ["chrX", "chrY", "X", "Y"]
    with open(gtf_file, "r") as fh:
        gene = {}
        geneid, transcript_id, genename, genetype = "", "", "", ""
        for line in fh.readlines():
            if line.strip().startswith(comment):
                continue
            w = line.strip().split()
            w = w[0:8] + [" ".join(w[8:])]
            chrn = w[0]
            strand = w[6]
            entry_type = w[2]
            
            # build match patterns
            geneid_patt = re.search(r'gene_id\s"(\w+|\w+\.\d+)";', w[8])
            transcript_patt = re.search(r'transcript_id\s"(\w+|\w+\.\d+)";', w[8])
            genename_patt = re.search(r'gene_name\s"(.*?)";', w[8])
            genetype_patt = re.search(r'gene_[biotype|type]+\s"(.*?)";', w[8])

            gene_id = geneid_patt.group(1) if geneid_patt else "NA"
            genename = genename_patt.group(1) if genename_patt else "NA"
            genetype = genetype_patt.group(1) if genetype_patt else "NA"

            if geneid_patt:
                if genetype in keep_geneType:
                    gene_id = geneid_patt.group(1) if geneid_patt else "NA"
                    gene_id = gene_id + ":" + genename + ":" + chrn + ":" + strand
                
                    if entry_type == "transcript" and chrn in keep_chr:
                            t_coord = (int(w[3]), int(w[4])) #1-based coordinate??
                            gene[gene_id] = t_coord
                    else:
                        continue
                else:   
                    continue
    
    return gene




parser = argparse.ArgumentParser(description="")
parser.add_argument("-g", "--gtf", help = "specify a gtf file", required = True)
parser.add_argument("-o", "--out_bed", help = "specify a filename for exon output", default = "gene_annotation.bed")
parser.add_argument("--transcript2genename", help = "specify a filename for file to record transcript to genename", default = "transcript_to_geneName.txt")


args = parser.parse_args()

exon_dict = extract_exon(args.gtf, "#")
startCodon_dict = extract_Codon(args.gtf, "#", "start_codon")
stopCodon_dict = extract_Codon(args.gtf, "#", "stop_codon")
transcript_coord = extract_transcript(args.gtf, "#")



# print out gene annotation in bed12 format; transcript_id+":"+gene_id+":"+genename+":"+chrn+":"+strand
fho = open(args.out_bed, "w")
fho2 = open(args.transcript2genename, "w")

s_codon, e_codon = "", ""
for t in exon_dict:
    gid, gname, chrname, strand = t.split(":")
    print("%s\t%s" % (gid, gname), file = fho2)
    t_start, t_end = transcript_coord[t]
    sorted_exons = sorted(exon_dict[t], key = lambda x:x[0])
    exons_starts = [x[0] - t_start for x in sorted_exons]
    exons_sizes = [y - x + 1 for x, y in sorted_exons]
    count = len(exons_starts)

    exons_starts_str = ",".join(list(map(str, exons_starts))) + ","
    exons_sizes_str = ",".join(list(map(str, exons_sizes))) + ","

    if t in startCodon_dict and t in stopCodon_dict:
        s_codon = startCodon_dict[t]
        e_codon = stopCodon_dict[t]
    else:
        s_codon = str(t_start)
        e_codon = str(t_end)
    
    print("%s\t%d\t%d\t%s\t%d\t%s\t%d\t%d\t%d\t%d\t%s\t%s" % (chrname,t_start-1,t_end,gid,0,strand,int(s_codon)-1,int(e_codon)-1,0,count,exons_sizes_str,exons_starts_str), file = fho)

fho.close()
fho2.close()
print("Done!")
