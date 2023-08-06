import sys
import os.path as op
from distutils.core import setup
from setuptools import find_packages

bin_path = op.dirname(sys.executable)
print(bin_path)

setup(
    name="glh-test",
    version="0.0.2",
    description="Molecular Outlier DEtection from Rna-seq data",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="GongLihai",
    author_email="gonglihai@outlook.com",
    url="https://github.com/Xu-Dong/MODER/tree/singleTissue",
    install_requires=[
        "cython",
        "bx-python",
        "numpy",
        "pandas",
        "pystan",
        "pysam",
        "plotnine",
        "scipy"],
    license="GNU GENERAL PUBLIC LICENSE",
    packages=[ 
        "src",
        "ext",
        "ext.callOutliers"
        ],
    data_files = [
        (bin_path, ["ext/rnaseqc"]),
        (bin_path, ["ext/peertool"]),
        ],
    package_data = {
        "ext":['*', 'phaser/*', 'SPOT/*', 'leafcutter/*'],
        },
    scripts = ["moder.py"]
    )
