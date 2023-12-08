import os

import numpy as np
import pandas as pd
import qiime2

from ._format import SNPDirFormat, VCFDirFormat
from .plugin_setup import plugin


def extract_fields_from_vcf(vcf_file: VCFDirFormat) -> pd.DataFrame:
    # extracted_vcf = VCFDirFormat()
    # with resources.path(bin, "SnpSift.jar") as executable_path:
    #     cmd = ["java", "-jar", executable_path, "extractFields"]
    #     if field_separator != "":
    #         cmd += ["-s", field_separator]
    #     if empty_field != "":
    #         cmd += ["-e", empty_field]
    #     cmd.append(input_vcf)
    #     cmd += fields.split()
    #     subprocess.run(cmd, check=True, stdout=open("text.txt", "w"))

    return pd.DataFrame([[0, 1], [2, 3]], index=["foo", "bar"], columns=["foo2", "bar2"])


# @plugin.register_transformer
# def _1(ff: VCFDirFormat) -> pd.DataFrame:
#     return extract_fields_from_vcf(ff)

# @plugin.register_transformer
# def _1(ff: VCFDirFormat) -> str:
#     return VCFDirFormat.path

# @plugin.register_transformer
# def _2(ff: pd.DataFrame) -> SNPDirFormat:
#     SNPDir = SNPDirFormat()
#     ff.to_csv(os.path.join(str(SNPDir), "snp.tsv"), sep="\t")
#     return SNPDir


@plugin.register_transformer
def _3(ff: VCFDirFormat) -> SNPDirFormat:
    SNPDir = SNPDirFormat()
    df = extract_fields_from_vcf(ff)
    df.to_csv(os.path.join(str(SNPDir), "snp.tsv"), sep="\t")
    return SNPDir
