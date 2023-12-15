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
    description="QIIME 2 plugin for samtools",
    website="https://pcingola.github.io/SnpEff/",
    package="q2_snpsift",
)

plugin.methods.register_function(
    function=q2_snpsift.filter,
    inputs={"input_vcf": FeatureData[VariantType]},  # type: ignore
    parameters={"expression": Str},
    outputs=[("filtered_vcf", FeatureData[VariantType])],  # type: ignore
    input_descriptions={"input_vcf": "VCF input file"},
    parameter_descriptions={
        "expression": "filter expression",
    },
    output_descriptions={"filtered_vcf": "filtered VCF file"},
    name="snpSift filter qiime plugin",
    description=("snpSift filter"),
)

plugin.methods.register_function(
    function=q2_snpsift.extract_fields_from_snpeff_output,
    inputs={"vcf_file": FeatureData[VariantType]},  # type: ignore
    parameters={},
    outputs=[("output_vcf", FeatureData[VariantAnnotationType])],  # type: ignore
    input_descriptions={"vcf_file": "VCF input file"},
    parameter_descriptions={},
    output_descriptions={"output_vcf": "extracted fields from VCF file"},
    name="snpSift extractField",
    description=(
        "Run SnpSift extractFields file.vcf CHROM, POS, REF, ALT, AF, QUAL, DP, QD, EFF on SnpEff output and expand"
        + "EFF into separate columns."
    ),
)

plugin.register_formats(VariantAnnotationDirFormat, VariantDirFormat)
plugin.register_semantic_type_to_format(FeatureData[VariantType], artifact_format=VariantDirFormat)  # type: ignore
plugin.register_semantic_type_to_format(
    FeatureData[VariantAnnotationType], artifact_format=VariantAnnotationDirFormat  # type: ignore
)
importlib.import_module("q2_snpsift._transformer")
