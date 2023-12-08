# TODO: Delete after Megan has merged her branch into main

from q2_types.feature_data import FeatureData
from qiime2.plugin import SemanticType

VCFFormat = SemanticType("VCFFormat", variant_of=FeatureData.field["type"])

SNPType = SemanticType("SNPType", variant_of=FeatureData.field["type"])

DictFormat = SemanticType("DictFormat", variant_of=FeatureData.field["type"])

MetricsFormat = SemanticType("MetricsFormat", variant_of=FeatureData.field["type"])

BamIndexFormat = SemanticType("BamIndexFormat", variant_of=FeatureData.field["type"])
