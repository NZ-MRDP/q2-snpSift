# TODO: Delete after Megan has merged her branch into main

import subprocess

import qiime2.plugin.model as model
from qiime2.plugin import ValidationError

from ._type import VCFFormat


class VCFFileFormat(model.TextFileFormat):
    """VCFFileFormat."""

    # TODO: Test validation by qiime tools import a VCF file
    def _validate_(self, *args):
        result = subprocess.run(["gatk", "ValidateVariants", "-V", str(self)])
        if result.returncode != 0:
            raise ValidationError("This is not a valid VCF file.")


VCFDirFormat = model.SingleFileDirectoryFormat("VCFDirFormat", "vcf.vcf", VCFFileFormat)


class DictFileFormat(model.TextFileFormat):
    """DictFileFormat."""

    # TODO: Add validation
    def _validate_(self, *args):
        pass


DictDirFormat = model.SingleFileDirectoryFormat("DictDirFormat", "fasta.dict", DictFileFormat)


class MetricsFileFormat(model.TextFileFormat):
    """MetricsFileFormat."""

    # TODO: Add validation
    def _validate_(self, *args):
        pass


MetricsDirFormat = model.SingleFileDirectoryFormat("MetricsDirFormat", "metrics.txt", MetricsFileFormat)


class BamIndexFileFormat(model.TextFileFormat):
    """BamIndexFileFormat."""

    # TODO: Add validation
    def _validate_(self, *args):
        pass


class BamIndexDirFormat(model.DirectoryFormat):
    """BamIndexDirFormat."""

    bam_indices = model.FileCollection(r".+\.bai", format=BamIndexFileFormat)

    @bam_indices.set_path_maker
    def bam_indices_path_maker(self, sample_id):
        """bam_indices_path_maker."""
        return "%s.bai" % sample_id
