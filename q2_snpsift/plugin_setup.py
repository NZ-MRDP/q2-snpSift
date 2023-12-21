"""QIIME 2 plugin for snpSift."""

import importlib

import qiime2.plugin
from q2_types.feature_data import FeatureData
from q2_types_variant import VariantCall, VariantCallAnnotation
from qiime2.plugin import Str

import q2_snpsift

from . import __version__

plugin = qiime2.plugin.Plugin(
    name="snpSift",
    version=__version__,
    description="QIIME 2 plugin for SnpSift",
    website="https://pcingola.github.io/SnpEff/",
    package="q2_snpsift",
)

plugin.methods.register_function(
    function=q2_snpsift.filter,
    inputs={"input_vcf": FeatureData[VariantCall]},
    parameters={"expression": Str},
    outputs=[("filtered_vcf", FeatureData[VariantCall])],
    input_descriptions={"input_vcf": "VCF input file"},
    parameter_descriptions={
        "expression": "The filtering expression that specifies the conditions for selecting variants, e.g. '( QUAL >= 30 )'",
    },
    output_descriptions={"filtered_vcf": "The output VCF file where the filtered variants will be written."},
    name="snpSift filter qiime plugin",
    description=(
        "SnpSift filter variants based on specific criteria to extract subsets of variants that meet certain conditions."
    ),
)

plugin.methods.register_function(
    function=q2_snpsift.extract_fields_from_snpeff_output,
    inputs={"vcf_file": FeatureData[VariantCall]},
    parameters={},
    outputs=[("output_vcf", FeatureData[VariantCallAnnotation])],
    input_descriptions={"vcf_file": "VCF input file"},
    parameter_descriptions={},
    output_descriptions={"output_vcf": "extracted fields from VCF file"},
    name="snpSift extractField",
    description=(
        "Run SnpSift extractFields file.vcf CHROM, POS, REF, ALT, AF, QUAL, DP, QD, EFF on SnpEff output and expand"
        " EFF into separate columns."
    ),
)

importlib.import_module("q2_snpsift._transformer")
