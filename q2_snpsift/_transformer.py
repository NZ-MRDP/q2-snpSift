import os
import subprocess
from importlib import resources

from q2_snpsift import bin

from ._format import VariantAnnotationDirFormat, VariantDirFormat
from .plugin_setup import plugin


def extract_fields_from_vcf(vcf_file: VariantDirFormat) -> str:
    """extractFields.

    Usage: java -jar SnpSift.jar extractFields [options] file.vcf fieldName1 fieldName2 ... fieldNameN > tabFile.txt

    Options:
        -s     : Same field separator. Default: '       '
        -e     : Empty field. Default: ''

    """
    with resources.path(bin, "SnpSift.jar") as executable_path:
        cmd = ["java", "-jar", executable_path, "extractFields"]
        cmd.append(os.path.abspath(os.path.join(str(vcf_file), "vcf.vcf")))
        cmd.extend(["CHROM", "POS", "REF", "ALT", "AF", "QUAL", "DP", "QD", "EFF"])
        output = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return str(output.stdout)


@plugin.register_transformer
def _1(ff: VariantDirFormat) -> VariantAnnotationDirFormat:
    SNPDir = VariantAnnotationDirFormat()
    df = extract_fields_from_vcf(ff)
    with open(os.path.join(str(SNPDir), "snp.tsv"), "w") as file:
        file.write(df)
    return SNPDir
