"""QIIME 2 plugin for snpSift."""

import qiime2.plugin
from q2_types.feature_data import FeatureData
from qiime2.plugin import Str

import q2_snpsift

from ._type import VCFFormat

plugin = qiime2.plugin.Plugin(
    name="snpSift",
    version="0.0.0",
    description="QIIME 2 plugin for samtools",
    website="https://pcingola.github.io/SnpEff/",
    package="q2_snpsift",
)

plugin.methods.register_function(
    function=q2_snpsift.filter,
    inputs={"input_vcf": FeatureData[VCFFormat]},  # type: ignore
    parameters={"expression": Str},
    outputs=[("filtered_vcf", FeatureData[VCFFormat])],  # type: ignore
    input_descriptions={"input_vcf": "VCF input file"},
    parameter_descriptions={"expression": "filter expression"},
    output_descriptions={"filtered_vcf": "filtered VCF file"},
    name="snpSift qiime plugin",
    description=("snpSift filter"),
)