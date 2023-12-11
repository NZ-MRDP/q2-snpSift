"""QIIME 2 plugin for snpSift."""

import importlib

import qiime2.plugin
from q2_types.feature_data import FeatureData
from q2_types.feature_table import FeatureTable, Frequency
from qiime2.plugin import Bool, Choices, Str

import q2_snpsift

from ._format import SNPDirFormat, VCFDirFormat
from ._type import SNPType, VCFFormat

plugin = qiime2.plugin.Plugin(
    name="snpSift",
    version="0.0.0",
    description="QIIME 2 plugin for samtools",
    website="https://pcingola.github.io/SnpEff/",
    package="q2_snpsift",
)

# TODO: Change VCFFormat to VCFIndex
plugin.methods.register_function(
    function=q2_snpsift.filter,
    inputs={"input_vcf": FeatureData[VCFFormat]},  # type: ignore
    parameters={"expression": Str},  # , "format": Str % Choices({"2", "3"})},  # "errmissing": Bool},
    outputs=[("filtered_vcf", FeatureData[VCFFormat])],  # type: ignore
    input_descriptions={"input_vcf": "VCF input file"},
    parameter_descriptions={
        "expression": "filter expression",
        # "format": "SnpEff format version: {2, 3}"
        # "errmissing": "Error is a field is missing",
    },
    output_descriptions={"filtered_vcf": "filtered VCF file"},
    name="snpSift filter qiime plugin",
    description=("snpSift filter"),
)

# plugin.methods.register_function(
#     function=q2_snpsift.extractFields,
#     inputs={"input_vcf": FeatureData[VCFFormat]},  # type: ignore
#     parameters={
#         "fields": Str,
#         "field_separator": Str,
#         "empty_field": Str,
#     },  # remove field_separator by changing it in _format.py
#     outputs=[("extracted_vcf", FeatureData[VCFFormat])],  # type: ignore # model.TextFileFormat
#     input_descriptions={"input_vcf": "VCF input file"},
#     parameter_descriptions={
#         "fields": "fields",
#         "field_separator": "field separator in input_vcf",
#         "empty_field": "rename empty fields",
#     },
#     output_descriptions={"extracted_vcf": "extracted fields from VCF file"},
#     name="snpSift extractFIelds qiime plugin",
#     description=("snpSift extractFields"),
# )

plugin.methods.register_function(
    function=q2_snpsift.filter_vcf,
    inputs={"vcf_file": FeatureData[VCFFormat]},  # type: ignore
    parameters={},  # remove field_separator by changing it in _format.py
    outputs=[("output_vcf", FeatureData[SNPType])],  # type: ignore # model.TextFileFormat
    input_descriptions={"vcf_file": "VCF input file"},
    parameter_descriptions={},
    output_descriptions={"output_vcf": "extracted fields from VCF file"},
    name="filter vcf qiime plugin",
    description=("filter vcf"),
)

plugin.register_formats(SNPDirFormat, VCFDirFormat)
plugin.register_semantic_type_to_format(FeatureData[VCFFormat], artifact_format=VCFDirFormat)  # type: ignore
plugin.register_semantic_type_to_format(FeatureData[SNPType], artifact_format=SNPDirFormat)  # type: ignore
importlib.import_module("q2_snpsift._transformer")
