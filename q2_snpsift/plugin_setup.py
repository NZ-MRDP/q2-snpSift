"""QIIME 2 plugin for snpSift."""

import importlib

import qiime2.plugin
from q2_types.feature_data import FeatureData
from qiime2.plugin import Str

import q2_snpsift

from ._format import VariantAnnotationDirFormat, VariantDirFormat
from ._type import VariantAnnotationType, VariantType

plugin = qiime2.plugin.Plugin(
    name="snpSift",
    version="0.0.0",
    description="QIIME 2 plugin for SnpSift",
    website="https://pcingola.github.io/SnpEff/",
    package="q2_snpsift",
)

plugin.methods.register_function(
    function=q2_snpsift.filter,
    inputs={"input_vcf": FeatureData[VariantType]},
    parameters={"expression": Str},
    outputs=[("filtered_vcf", FeatureData[VariantType])],
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
    inputs={"vcf_file": FeatureData[VariantType]},
    parameters={},
    outputs=[("output_vcf", FeatureData[VariantAnnotationType])],
    input_descriptions={"vcf_file": "VCF input file"},
    parameter_descriptions={},
    output_descriptions={"output_vcf": "extracted fields from VCF file"},
    name="snpSift extractField",
    description=(
        "Run SnpSift extractFields file.vcf CHROM, POS, REF, ALT, AF, QUAL, DP, QD, EFF on SnpEff output and expand"
        " EFF into separate columns."
    ),
)

plugin.register_formats(VariantAnnotationDirFormat, VariantDirFormat)
plugin.register_semantic_type_to_format(FeatureData[VariantType], artifact_format=VariantDirFormat)
plugin.register_semantic_type_to_format(FeatureData[VariantAnnotationType], artifact_format=VariantAnnotationDirFormat)
importlib.import_module("q2_snpsift._transformer")
