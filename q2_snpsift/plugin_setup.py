"""QIIME 2 plugin for snpSift."""

import qiime2.plugin
from q2_types.feature_data import FeatureData
from qiime2.plugin import Bool, Choices, Str

import q2_snpsift

from ._format import VCFDirFormat
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
    parameters={"expression": Str, "format": Str % Choices({"2", "3"})},  # "errmissing": Bool},
    outputs=[("filtered_vcf", FeatureData[VCFFormat])],  # type: ignore
    input_descriptions={"input_vcf": "VCF input file"},
    parameter_descriptions={
        "expression": "filter expression",
        "format": "SnpEff format version: {2, 3}"
        # "errmissing": "Error is a field is missing",
    },
    output_descriptions={"filtered_vcf": "filtered VCF file"},
    name="snpSift filter qiime plugin",
    description=("snpSift filter"),
)

plugin.methods.register_function(
    function=q2_snpsift.extractFields,
    inputs={"input_vcf": FeatureData[VCFFormat]},  # type: ignore
    parameters={"fields": Str, "field_separator": Str, "empty_field": Str},
    outputs=[("extracted_vcf", FeatureData[VCFFormat])],  # type: ignore # model.TextFileFormat
    input_descriptions={"input_vcf": "VCF input file"},
    parameter_descriptions={
        "fields": "fields",
        "field_separator": "field separator in input_vcf",
        "empty_field": "rename empty fields",
    },
    output_descriptions={"extracted_vcf": "extracted fields from VCF file"},
    name="snpSift extractFIelds qiime plugin",
    description=("snpSift extractFields"),
)

plugin.register_formats(VCFDirFormat)
plugin.register_semantic_type_to_format(FeatureData[VCFFormat], artifact_format=VCFDirFormat)  # type: ignore
# plugin.register_semantic_types(VCFFormat)
