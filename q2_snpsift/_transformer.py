import os
import subprocess
from importlib import resources

from q2_snpsift import bin

from ._format import VariantAnnotationDirFormat, VariantDirFormat
from .plugin_setup import plugin


def extract_fields_from_vcf(vcf_file: VariantDirFormat) -> str:
    """
    extract_fields_from_vcf.

    Run SnpSift extractFields file.vcf CHROM, POS, REF, ALT, AF, QUAL, DP, QD, EFF on SnpEff output and expand
    EFF into separate columns.

    Arguments:
        vcf_file -- VariantDirFormat

    Returns:
        str
    """
    with resources.path(bin, "SnpSift.jar") as executable_path:
        cmd = [
            "java",
            "-jar",
            executable_path,
            "extractFields",
            os.path.abspath(os.path.join(str(vcf_file), "vcf.vcf")),
        ]
        cmd.extend(["CHROM", "POS", "REF", "ALT", "AF", "QUAL", "DP", "QD", "EFF"])
        output = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        columns = [
            "CHROM",
            "POS",
            "REF",
            "ALT",
            "AF",
            "QUAL",
            "DP",
            "QD",
            "EFF",
            "Effect_Impact",
            "Functional_Class",
            "Codon_Change",
            "Amino_Acid_change",
            "Gene_Name",
            "Transcript_BioType",
            "Gene_Coding",
            "Transcript_ID",
            "Exon",
            "ERRORS",
            "WARNINGS",
        ]
        output_str = str(output.stdout).replace("(", "\t").replace("|", "\t").replace(")", "\t")

    return "\t".join(columns) + "\n" + output_str.split("\n", 1)[1]


@plugin.register_transformer
def _1(ff: VariantDirFormat) -> VariantAnnotationDirFormat:
    SNPDir = VariantAnnotationDirFormat()
    df = extract_fields_from_vcf(ff)

    with open(os.path.join(str(SNPDir), "snp.tsv"), "w") as file:
        file.write(df)

    return SNPDir
