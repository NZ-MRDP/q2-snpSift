"""QIIME 2 plugin for snpSift."""

import qiime2.plugin

plugin = qiime2.plugin.Plugin(
    name="snpSift",
    version="0.0.0",
    description="QIIME 2 plugin for samtools",
    website="https://pcingola.github.io/SnpEff/",
    package="q2_snpsift",
)
