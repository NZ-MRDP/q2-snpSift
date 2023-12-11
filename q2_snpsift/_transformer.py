import os
import subprocess
from importlib import resources

import pandas as pd

from q2_snpsift import bin

from ._format import SNPDirFormat, VCFDirFormat
from .plugin_setup import plugin


def extract_fields_from_vcf(vcf_file: VCFDirFormat) -> pd.DataFrame:
    """extractFields.
    Usage: java -jar SnpSift.jar extractFields [options] file.vcf fieldName1 fieldName2 ... fieldNameN > tabFile.txt

    Options:
        -s     : Same field separator. Default: '       '
        -e     : Empty field. Default: ''

    """
    with resources.path(bin, "SnpSift.jar") as executable_path:
        cmd = ["java", "-jar", executable_path, "extractFields"]
        cmd.append(vcf_file)
        cmd.extend(["CHROM", "POS", "REF", "ALT", "AF", "QUAL", "DP", "QD", "EFF"])
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        print(output)
    return output


@plugin.register_transformer
def _1(ff: VCFDirFormat) -> pd.DataFrame:
    return extract_fields_from_vcf(ff)


# @plugin.register_transformer
# def _1(ff: VCFDirFormat) -> str:
#     return VCFDirFormat.path


@plugin.register_transformer
def _2(ff: pd.DataFrame) -> SNPDirFormat:
    SNPDir = SNPDirFormat()
    ff.to_csv(os.path.join(str(SNPDir), "snp.tsv"), sep="\t")
    return SNPDir


@plugin.register_transformer
def _3(ff: VCFDirFormat) -> SNPDirFormat:
    SNPDir = SNPDirFormat()
    df = extract_fields_from_vcf(ff)
    df.to_csv(os.path.join(str(SNPDir), "snp.tsv"), sep="\t")
    return SNPDir
