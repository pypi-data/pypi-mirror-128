[![Github Release](https://img.shields.io/badge/release-v1.0.0-brightgreen)](https://github.com/Xu-Dong/mOutlierPipe/releases/tag/v1.0.0)
[![python Release](https://img.shields.io/badge/python-3.8-brightgreen)](https://www.python.org/downloads/)
![system type](https://img.shields.io/badge/GNU-Linux-brightgreen)
![other](https://img.shields.io/badge/perl-v%205.30.0-brightgreen)

## Introduction
**MODER(Molecular Outlier DEtection from Rna sequencing assays)** is a comprehensive and user-friendly toolkit to detect aberrant gene expression, alternative splicing, and allele specific expression from multiple samples. MODER is built on python3 and easy to use. Users only need to provide a list of bam files, and MODER will do all complicated, error-prone processing automatically and return all three kinds of outliers (gene~sample pairs).

## Framework
<img src="./doc/MODER.png" width="640" height="330">

## Documentation
Documentation can be found on *here*

## Dependency
#### bioinfomatics software
* samtools: [![samtools release](https://img.shields.io/badge/samtools-v1.10-lightgrey)](https://github.com/samtools/samtools/releases/tag/1.10)
* bedtools: [![bedtools release](https://img.shields.io/badge/bedtools-v%202.27.1-lightgrey)](https://github.com/arq5x/bedtools2/releases/tag/v2.27.1)
* bcfools: [![bcftools release](https://img.shields.io/badge/bcftools-v1.9-lightgrey)](https://github.com/samtools/bcftools/releases/tag/1.9)
 
If you have installed **conda**, you can easily install samtools and bcftools by following command. 
```
conda install -c bioconda samtools
conda install -c bioconda bedtools
conda install -c bioconda bcftools
```

If your are working with Debian-based linux system, it's convenient for you to install samtools and bctools by package manager -- apt 
```
sudo apt install samtools
sudo apt install bedtools
sudo apt install bcftools
```

#### python package
* [![Cython release](https://img.shields.io/badge/Cython-v0.29.23-green/?style=social&logo=python)](https://pypi.org/project/Cython/0.29.23/)
* [![numpy release](https://img.shields.io/badge/numpy-v%201.19.5-green/?style=social&logo=python)](https://pypi.org/project/numpy/1.19.5/)
* [![pystan release](https://img.shields.io/badge/pystan-v%202.18.0.0-green/?style=social&logo=python)](https://pypi.org/project/pystan/2.18.0.0/)
* [![pysam release](https://img.shields.io/badge/pysam-v0.17.0-green/?style=social&logo=python)](https://pypi.org/project/pysam/0.17.0/)
* [![pandas release](https://img.shields.io/badge/pandas-v%201.2.4-green/?style=social&logo=python)](https://pypi.org/project/pandas/1.2.4/)
* [![plotnine release](https://img.shields.io/badge/plotnine-v%200.8.0-green/?style=social&logo=python)](https://pypi.org/project/plotnine/0.8.0/)
* [![scipy release](https://img.shields.io/badge/scipy-v%201.6.3-green/?style=social&logo=python)](https://pypi.org/project/scipy/1.6.3/)


## Installation
For install MODER, you can use git to pull down all code to your linux system. Make sure samtools, bcttools and all dependency third-party python libraries has been installed, then you call use it easily by a python script named **moder.py**. Look for [**Usgae**](https://github.com/Xu-Dong/mOutlierPipe/blob/singleTissue/README.md#usage) to get more information about how to use this program.
```
git clone -b singleTissue https://github.com/Xu-Dong/mOutlierPipe.git
```

## Usage
**mode argument**
option | description
:-- | :--
--expression | assign mode to analysis Gene Expression data
--splicing | assign mode to analysis Splicing data
--ase | assign mode to analysis ASE data

we provide three arguments to decide which analysis pipeline will be run, and all three analysis pipeline will be run if you don't provide any option of these, :<br>
look [**module1**](https://github.com/Xu-Dong/mOutlierPipe/blob/singleTissue/README.md#module1-expression-data-analysis) for more information of expression pipeline.<br>
look [**module2**](https://github.com/Xu-Dong/mOutlierPipe/blob/singleTissue/README.md#module2-splicing-data-analysis) for more information of splicing pipeline.<br>
look [**module3**](https://github.com/Xu-Dong/mOutlierPipe/blob/singleTissue/README.md#module3-alternative-polyadenylation-data-analysis) for more information of ase pipeline.<br><br>


**basic argument**
option | description
:-- | :--
-i , --input | txt file with all input bam file path (required)
--gtf | genome annotation file of GTF format (required)
-o , --output | directory to store all resulting files <br><font color='red'>(optional and default output dir is current directory)</font>
-p , --parallel | parallel number <br><font color='red'>(optional and default value is 1)</font>
--threshold| threshold of z_score, used to get outliers which abs value larger than threshold defined by this arguments<br><font color='red'>(optional and default value is 2)</font>

more arguments and their usage, you can refer to [featureCounts](http://bioinf.wehi.edu.au/subread-package/SubreadUsersGuide.pdf), [peer](./doc/peer.md), [leafcutter](./doc/leafcutter.md), [SPOT](./doc/SPOT.md), [gtfToGenePred](./doc/gtfToGenePred.md) and [genePredToBed](./doc/genePredToBed.md)

you can run all these pipeline by command as follow:
```
python moder.py -p 8
	--input file_path.txt
	--gtf genome_annotation.gtf
	--vcf example.vcf.gz
	--variation Vg_GTEx_v8.txt
	--tissue MSCLSK
	--threshold 2
```

### module1: Expression Data Analysis
This module is designed to analysis gene expression data. The basic command line arguments and descriptions as follows. More available parameters refer to [RNA-SeQC](http://bioinf.wehi.edu.au/subread-package/SubreadUsersGuide.pdf) and  [PEER](./doc/peer.md)

**command line arguments**
option | description
:--- | :---
--expression | assign mode to analysis Gene Expression data
-i , --input | txt file with all input bam file path (required)
--gtf | genome annotation file in GTF format (required)
-o , --output | directory to store all resulting files<br><font color='red'>(optional and default output dir is current directory)</font>
-p , --parallel | parallel number <br><font color='red'>(optional and defalut value is 1)</font>
--threshold| threshold of z_score, used to filter results' value larger than threshold<br><font color='red'>(optional and default value is 2)</font>

**running example**
```
python mOutlierPipe.py --expression 
	--parallel 8 
	--input file_path.txt
	--gtf sample_annotation.gtf
	--threshold 2
```

### module2: Splicing Data Analysis
This module is designed to analysis splicing data. The basic command line arguments and descriptions as follows. More available parameters refer to [leafcutter](./doc/leafcutter.md), [SPOT](./doc/SPOT.md) and [PEER](./doc/peer.md)

**command line arguments**
option | description
:--- | :---
--splicing | assign mode to analysis Splicing data
-i , --input | txt file with all input bam file path (required)
--gtf | genome annotation file in GTF format, used to translate cluster id to gene id (required)
-o , --output | directory to store all resulting files<br><font color='red'>(optional and default output dir is current directory)</font>
-p , --parallel | parallel number <br><font color='red'>(optional and default value is 1)<font>
--threshold | threshold of z_score, in splicing analysis pipeline, the value of z will be translated to p<br><font color='red'>(optional and default value is 0.0027)<font>

 **running example**
```
python mOutlierPipe.py --splicing 
	--parallel 8
	--input file_path.txt
	--gtf genome_annotation.gtf
	--threshold 2
```

### module3: Allele Specific Expression Analysis
This module is designed to analysis allele specific expression data. The basic command line arguments and descriptions as follows. More available parameters refer to [phASER](./doc/leafcutter.md)

**command line arguments**
option | description
:--- | :---
--ase | assign mode to analysis ASE data
-i , --input | txt file with all input bam file path (required)
--gtf | genome annotation file in GTF format, used to translate cluster id to gene id (required)
--vcf | Variant Call Format file, include variation information about the genome (required)
--variant |  tissue-specific estimates of genetic variation in gene dosage (required)
-o , --output | directory to store all resulting files<br><font color='red'>(optional and default output dir is current directory)</font>
-p , --parallel | parallel number <br><font color='red'>(optional and default value is 1)<font>
--threshold | threshold of z_score, in ase analysis pipeline, the value of z will be translated to p<br><font color='red'>(optional and default value is 0.0027)<font>

 **running example**
```
python mOutlierPipe.py --ase
	--parallel 8
	--input file_path.txt
	--gtf genome_annotation.gtf
	--vcf sample.vcf
	--variant Vg_GTEx_v8.txt
	--threshold 2
```
