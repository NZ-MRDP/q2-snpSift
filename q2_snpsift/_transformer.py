"""Transformers for SnpSift views and artifacts."""

import os
import subprocess
from importlib.resources import as_file, files

from q2_types_variant import VariantCallAnnotationDir, VariantCallDir, VariantCallFile

from q2_snpsift import bin

from .plugin_setup import plugin


def extract_fields_from_vcf(vcf_file: str) -> str:
    """Extract a default tabular summary from a SnpEff-annotated VCF file."""
    with as_file(files(bin).joinpath("SnpSift.jar")) as executable_path:
        cmd = [
            "java",
            "-jar",
            executable_path,
            "extractFields",
            vcf_file,
        ]
        cmd.extend(["CHROM", "POS", "REF", "ALT", "AF", "QUAL", "DP", "QD", "EFF"])
        output = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, text=True)
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
def _1(ff: VariantCallDir) -> VariantCallAnnotationDir:
    VCADir = VariantCallAnnotationDir()
    for path, _ in ff.vcf.iter_views(view_type=VariantCallFile):
        df = extract_fields_from_vcf(os.path.join(str(ff.path), str(path.stem) + ".vcf"))

        with open(os.path.join(str(VCADir), str(path.stem) + ".tsv"), "w", encoding="utf-8") as file:
            file.write(df)

    return VCADir
