"""SnpSift functions."""

import os
import subprocess
from importlib import resources
import pandas as pd

from q2_types_variant import VariantCallAnnotationDir, VariantCallDir, VariantCallFile, VCFIndexDirectory, VariantDir

from q2_snpsift import bin


def filter_quality(
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
        for path, _ in input_vcf.vcf.iter_views(view_type=VariantCallFile):  # type: ignore
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


def filter_unique(
    variants: VariantDir,
) -> VariantDir:
    """
    Filter variants based on specific expression criteria.

    Arguments:
        variants -- VariantDir

    Returns:
        VariantDirFormat
    """
    filtered_variants = VariantDir()

    dfs = []
    snp_set = set()

    # If the data ever gets large, this might be slow
    base_path = str(variants)
    for file_name in os.listdir(base_path):

        df = pd.read_csv(f"{base_path}/{file_name}", sep="\t")

        df["snp"] = df["CHROM"] + df["POS"].astype(str)
        snp_set = snp_set.symmetric_difference(set(df["snp"]))
        dfs.append((df, file_name))

    for df, file_name in dfs:
        df = df[df["snp"].isin(snp_set)]
        df = df.drop(["snp"], axis=1)

        df.to_csv(open(os.path.join(str(filtered_variants), f"{file_name}"), "w"), sep="\t")
    return filtered_variants
