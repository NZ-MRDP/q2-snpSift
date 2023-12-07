"""SnpSift functions."""
import os
import subprocess
from importlib import resources
from typing import Any, Optional

from q2_snpsift import bin

from ._format import VCFDirFormat


# TODO
def filter(
    input_vcf: VCFDirFormat,
    expression: str,
    format: Optional[str] = None,  # errmissing: str = "false",, galaxy: bool = False
) -> VCFDirFormat:
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
    # PATH_TO_JAR_FILE?
    # GET ARGUMENTS
    # RUN COMMANDS
    # RETURN FILE
    filtered_vcf = VCFDirFormat()
    with resources.path(bin, "SnpSift.jar") as executable_path:
        cmd = ["java", "-jar", executable_path, "filter"]
        # cmd.append() # options
        # if errmissing:
        #     cmd += ["--errMissing", "true"]
        if format:
            cmd.extend(["--format", format])
        # if galaxy: # @LVN HOW TO?
        #     cmd += ["--galaxy", galaxy]
        cmd.append(expression)
        cmd.append("-f")
        cmd.append(os.path.abspath(os.path.join(str(input_vcf), "*.vcf")))
        subprocess.run(cmd, check=True, stdout=open(os.path.join(str(filtered_vcf), "vcf.vcf"), "w"))
    print("CMD:", " ".join(cmd))
    return filtered_vcf


# TODO
def extractFields(
    input_vcf: VCFDirFormat, fields: str, field_separator: str = "", empty_field: str = ""
) -> Any:  # Create a new format like ChromSnpTable # VCFDirFormat
    """extractFields.
    Usage: java -jar SnpSift.jar extractFields [options] file.vcf fieldName1 fieldName2 ... fieldNameN > tabFile.txt

    Options:
        -s     : Same field separator. Default: '       '
        -e     : Empty field. Default: ''

    """
    # Extract everything?
    ## THIS IS NOW BECOMING A TRANSFORMER!!!!!!
    extracted_vcf = VCFDirFormat()
    with resources.path(bin, "SnpSift.jar") as executable_path:
        cmd = ["java", "-jar", executable_path, "extractFields"]
        if field_separator != "":
            cmd += ["-s", field_separator]
        if empty_field != "":
            cmd += ["-e", empty_field]
        cmd.append(input_vcf)
        cmd += fields.split()
        subprocess.run(cmd, check=True, stdout=open("text.txt", "w"))
    return extracted_vcf


# def NZ_vcf_transformer(snpeff_vcf) -> simple_vcf:
#     java -jar $snpsiftjar extractFields $snpeff_vcf "CHROM" "POS" "REF" "ALT" "AF" "QUAL" "DP" "QD" "EFF" > $simple_vcf
