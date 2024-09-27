"""QIIME 2 plugin for snpSift."""

import importlib

import qiime2.plugin
from q2_types.feature_data import FeatureData
from q2_types_variant import VariantCall, VariantCallAnnotation, Variants
from qiime2.plugin import Str, TypeMatch

import q2_snpsift

from . import __version__

T = TypeMatch(FeatureData[VariantCall | VariantCallAnnotation])

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
    input_descriptions={"input_vcf": "VCF input file"},
    parameter_descriptions={
        "expression": "The filtering expression that specifies the conditions for selecting variants using arbitrary expressions e.g., '(QUAL > 30) | (exists INDEL) | ( countHet() > 2 )'. The actual expressions can be quite complex, so it allows for a lot of flexibility",
    },
    output_descriptions={"filtered_vcf": "Output variant data, filtred by quality"},
    name="snpSift filter qiime plugin",
    description=(
        "SnpSift filter variants based on specific criteria to extract subsets of variants that meet certain conditions."
    ),
)

plugin.methods.register_function(
    function=q2_snpsift.filter_unique,
    inputs={"variants": T},
    parameters={},
    outputs=[("filtered_variants", T)],
    input_descriptions={"variants": "Variant data"},
    parameter_descriptions={},
    output_descriptions={"filtered_variants": "Filtered variant data, containing only unique variants"},
    name="snpSift filter qiime plugin",
    description=(
        "Filter samples to contain only those snps which are unique to a given sample. Variants are compared across all samples in a data set. If the variant is present in more than one sample, it is removed from all samples. The resulting samples will contain only unique variants. If all variants are filtered out of a given sample the sample will not be filtered out of the data set but will have not data associated with it."
    ),
)

plugin.methods.register_function(
    function=q2_snpsift.extract_fields_from_snpeff_output,
    inputs={"vcf_file": FeatureData[VariantCall]},  # type: ignore
    parameters={},
    outputs=[("output_vcf", FeatureData[VariantCallAnnotation])],  # type: ignore
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
