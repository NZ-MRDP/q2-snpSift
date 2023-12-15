"""SnpSift functions."""
import os
import subprocess
from importlib import resources

from q2_snpsift import bin

from ._format import VariantAnnotationDirFormat, VariantDirFormat


def filter(
    input_vcf: VariantDirFormat,
    expression: str,
) -> VariantDirFormat:
    """filter.

    Args:
        input_vcf (VariantDirFormat)
        expression (str)

    Returns:
        VariantDirFormat
    """
    filtered_vcf = VariantDirFormat()
    with resources.path(bin, "SnpSift.jar") as executable_path:
        cmd = ["java", "-jar", executable_path, "filter"]
        cmd.append(expression)
        cmd.append("-f")
        cmd.append(os.path.abspath(os.path.join(str(input_vcf), "vcf.vcf")))
        subprocess.run(cmd, check=True, stdout=open(os.path.join(str(filtered_vcf), "vcf.vcf"), "w"))
    return filtered_vcf


def extract_fields_from_snpeff_output(vcf_file: VariantAnnotationDirFormat) -> VariantAnnotationDirFormat:
    """Run SnpSift extractFields on a SnpEff output.

    Args:
        vcf_file (VariantAnnotationDirFormat)

    Returns:
        VariantAnnotationDirFormat
    """
    return vcf_file
