"""SnpSift functions."""
import os
import subprocess
from importlib import resources

from q2_snpsift import bin

from ._format import VariantAnnotationDirFormat, VariantDirFormat


# TODO
def filter(
    input_vcf: VariantDirFormat,
    expression: str,
) -> VariantDirFormat:
    """filter.

    Usage: java -jar SnpSift.jar filter [options] 'expression' [input.vcf]

    java -jar SnpSift.jar filter "( exists INDEL ) & (QUAL >= 20)" input.vcf
    java -jar SnpSift.jar filter -a "(QUAL >= 20)" "( exists INDEL )" input.vcf

    java -jar SnpSift.jar filter -r "(QUAL >= 20)" "( exists INDEL ) & (QUAL >= 20)" input.vcf
    java -jar SnpSift.jar filter "( exists INDEL )" input.vcf

    Options:
    -a|--addFilter   : Add a string to FILTER VCF field if 'expression' is true. Default: '' (none)
    -e|--exprFile    : Read expression from a file
    -f|--file        : VCF input file. Default: STDIN
    -i|--filterId    : ID for this filter (##FILTER tag in header and FILTER VCF field). Default: 'SnpSift'
    -n|--inverse     : Inverse. Show lines that do not match filter expression
    -p|--pass        : Use 'PASS' field instead of filtering out VCF entries
    -r|--rmFilter    : Remove a string from FILTER VCF field if 'expression' is true (and 'str' is in the field). Default: '' (none)
    -s|--set         : Create a SET using 'file'
    --errMissing     : Error is a field is missing. Default: false
    --format         : SnpEff format version: {2, 3}. Default: Auto
    --galaxy         : Used from Galaxy (expressions have been sanitized).
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
        vcf_file (SNPDirFormat)

    Returns:
        SNPDirFormat
    """
    return vcf_file


# def NZ_vcf_transformer(snpeff_vcf) -> simple_vcf:
#     java -jar $snpsiftjar extractFields $snpeff_vcf "CHROM" "POS" "REF" "ALT" "AF" "QUAL" "DP" "QD" "EFF" > $simple_vcf


# @transformer
# def _transform_vcf(ff: VCF) -> pd.DataFrame:
#  txt = extractFields()
#  return_txt
