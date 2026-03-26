"""QIIME 2 plugin for snpSift."""

import importlib

import qiime2.plugin
from q2_types.feature_data import FeatureData
from q2_types_variant import VariantCall, VariantCallAnnotation, Variants
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
    function=q2_snpsift.filter_quality,
    inputs={"input_vcf": FeatureData[VariantCall | Variants]},  # type: ignore
    parameters={"expression": Str},
    outputs=[("filtered_vcf", FeatureData[VariantCall])],  # type: ignore
    input_descriptions={"input_vcf": "VCF variant calls to filter with a SnpSift expression."},
    parameter_descriptions={
        "expression": (
            "The filtering expression that specifies the conditions for selecting variants "
            "using arbitrary expressions, for example "
            "'(QUAL > 30) | (exists INDEL) | ( countHet() > 2 )'. "
            "The actual expressions can be quite complex, so this allows a lot of flexibility."
        ),
    },
    output_descriptions={"filtered_vcf": "VCF variant calls that satisfy the requested SnpSift filter expression."},
    name="Filter variants with a SnpSift expression",
    description=(
        "SnpSift filter variants based on specific criteria to extract subsets of variants "
        "that meet certain conditions."
    ),
)

plugin.methods.register_function(
    function=q2_snpsift.filter_unique,
    inputs={"variants": FeatureData[VariantCallAnnotation]},  # type: ignore
    parameters={},
    outputs=[("filtered_variants", FeatureData[VariantCallAnnotation])],  # type: ignore
    input_descriptions={"variants": "Per-sample tabular variant annotations to compare across samples."},
    parameter_descriptions={},
    output_descriptions={
        "filtered_variants": "Tabular variant annotations containing only variants unique to a single sample."
    },
    name="Keep only sample-unique variants",
    description=(
        "Filter samples to contain only SNPs that are unique to a given sample. "
        "Variants are compared across all samples in a dataset. "
        "If the variant is present in more than one sample, it is removed from all samples. "
        "The resulting samples contain only unique variants. "
        "If all variants are filtered out of a given sample, the sample remains in the dataset "
        "but has no associated variant data."
    ),
)

plugin.methods.register_function(
    function=q2_snpsift.extract_fields_from_snpeff_output,
    inputs={"vcf_file": FeatureData[VariantCall]},  # type: ignore
    parameters={"fields": Str},
    outputs=[("output_annotations", FeatureData[VariantCallAnnotation])],  # type: ignore
    input_descriptions={"vcf_file": "SnpEff-annotated VCF files from which to extract tabular annotation fields."},
    parameter_descriptions={
        "fields": (
            "Comma-separated list of SnpSift field expressions to extract, for example "
            "`CHROM,POS,REF,ALT,ANN[*].GENE,ANN[*].IMPACT`."
        ),
    },
    output_descriptions={
        "output_annotations": "Tabular variant annotations extracted from the annotated VCF files."
    },
    name="Extract annotation fields from SnpEff output",
    description=(
        "Run `SnpSift extractFields` on SnpEff-annotated VCF files and return a tabular artifact containing "
        "the requested annotation columns."
    ),
)

importlib.import_module("q2_snpsift._transformer")
