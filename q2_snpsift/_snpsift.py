"""SnpSift functions."""
import os
import subprocess
from importlib import resources

from q2_snpsift import bin
from q2_types_variant import VariantCallAnnotationDir, VariantCallDir, VariantCallFile, VCFIndexDirectory, VCFIndexFile


def filter(
    input_vcf: VCFIndexDirectory,
    expression: str,
) -> VCFIndexDirectory:
    """
    Filter variants based on specific expression criteria.

    Arguments:
        input_vcf -- VariantDirFormat
        expression -- str

    Returns:
        VariantDirFormat
    """
    filtered_vcf = VCFIndexDirectory()

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
            subprocess.run(cmd, check=True, stdout=open(os.path.join(str(filtered_vcf.path), str(path.stem)), "w"))
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
