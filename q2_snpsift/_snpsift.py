"""SnpSift functions."""

import os
import subprocess
from importlib.resources import as_file, files
from typing import Union

import pandas as pd
from q2_types_variant import (
    VariantCallAnnotationDir,
    VariantCallDir,
    VariantCallFile,
    VCFIndexDirectory,
)

from q2_snpsift import bin


def filter_quality(
    input_vcf: Union[VariantCallDir, VCFIndexDirectory],
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

    with as_file(files(bin).joinpath("SnpSift.jar")) as executable_path:
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
            output_path = os.path.join(str(filtered_vcf.path), str(path.stem) + ".vcf")
            with open(output_path, "w", encoding="utf-8") as output_vcf_path:
                subprocess.run(cmd, check=True, stdout=output_vcf_path)

    return filtered_vcf


def extract_fields_from_snpeff_output(
    vcf_file: VariantCallDir,
    fields: str = "CHROM,POS,REF,ALT,AF,QUAL,DP,ANN[*].EFFECT,ANN[*].IMPACT,ANN[*].GENE",
) -> VariantCallAnnotationDir:
    """Extract selected SnpEff annotation fields into a tabular artifact."""
    output_vcf = VariantCallAnnotationDir()
    requested_fields = [field.strip() for field in fields.split(",") if field.strip()]

    with as_file(files(bin).joinpath("SnpSift.jar")) as executable_path:
        for path, _ in vcf_file.vcf.iter_views(view_type=VariantCallFile):
            input_path = os.path.join(str(vcf_file.path), str(path.stem) + ".vcf")
            cmd = [
                "java",
                "-jar",
                executable_path,
                "extractFields",
                input_path,
                *requested_fields,
            ]
            output_path = os.path.join(str(output_vcf.path), str(path.stem) + ".tsv")
            with open(output_path, "w", encoding="utf-8") as output_fh:
                subprocess.run(cmd, check=True, stdout=output_fh)

    return output_vcf


def filter_unique(
    variants: VariantCallAnnotationDir,
) -> VariantCallAnnotationDir:
    """
    Filter variants based on specific expression criteria.

    Arguments:
        variants -- VariantCallAnnotationDir

    Returns:
        VariantCallAnnotationDir
    """
    filtered_variants = VariantCallAnnotationDir()

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

        output_path = os.path.join(str(filtered_variants), file_name)
        with open(output_path, "w", encoding="utf-8") as output_fh:
            df.to_csv(output_fh, sep="\t", index=False)
    return filtered_variants
