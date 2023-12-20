"""SnpSift functions."""
import os
import subprocess
from importlib import resources

from q2_snpsift import bin
from q2_types_variant import VariantCallAnnotationDir, VariantCallDir


def filter(
    input_vcf: VariantCallDir,
    expression: str,
) -> VariantCallDir:
    """
    Filter variants based on specific expression criteria.

    Arguments:
        input_vcf -- VariantDirFormat
        expression -- str

    Returns:
        VariantDirFormat
    """
    filtered_vcf = VariantCallDir()

    with resources.path(bin, "SnpSift.jar") as executable_path:
        cmd = [
            "java",
            "-jar",
            executable_path,
            "filter",
            expression,
            "-f",
            os.path.abspath(os.path.join(str(input_vcf), "vcf.vcf")),
        ]
        subprocess.run(cmd, check=True, stdout=open(os.path.join(str(filtered_vcf), "vcf.vcf"), "w"))

    return filtered_vcf


def extract_fields_from_snpeff_output(vcf_file: VariantCallAnnotationDir) -> VariantCallAnnotationDir:
    """
    Extract fields from a VCF file to a txt, tab separated format, file.

    Arguments:
        vcf_file -- VariantAnnotationDirFormat

    Returns:
        VariantAnnotationDirFormat
    """
    return vcf_file
