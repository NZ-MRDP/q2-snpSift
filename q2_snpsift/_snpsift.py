"""SnpSift functions."""
import os
import subprocess
from importlib import resources

from q2_snpsift import bin
from q2_types_variant import (VariantCallAnnotationDir, VariantCallDir,
                              VariantCallFile, VCFIndexDirectory)


def filter(
    input_vcf: VCFIndexDirectory,
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
        for path, _ in input_vcf.vcf.iter_views(view_type=VariantCallFile):
            cmd = [
                "java",
                "-jar",
                executable_path,
                "filter",
                expression,
                "-f",
                os.path.join(str(input_vcf.path), str(path.stem) + ".vcf"),
            ]
            with open(os.path.join(str(filtered_vcf.path), str(path.stem) + ".vcf"), "w") as output_vcf_path:
                subprocess.run(cmd, check=True, stdout=output_vcf_path)

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
