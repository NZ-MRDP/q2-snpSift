"""snpSift python library."""

from ._snpsift import extract_fields_from_snpeff_output, filter_quality, filter_unique

__version__ = "0.1.4"

__all__ = ["filter_quality", "extract_fields_from_snpeff_output", "filter_unique"]
