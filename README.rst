=======
cellSNP
=======

|PyPI| |Build Status| |DOI|

.. |PyPI| image:: https://img.shields.io/pypi/v/cellSNP.svg
    :target: https://pypi.org/project/cellSNP
.. |Build Status| image:: https://travis-ci.org/PMBio/cellSNP.svg?branch=master
   :target: https://travis-ci.org/PMBio/cellSNP
.. |DOI| image:: https://zenodo.org/badge/145724973.svg
   :target: https://zenodo.org/badge/latestdoi/145724973
   
   
This version aims to mimick cellsnp-lite (v1.2.4) cmdline options,
especially the read filtering part.
   

cellSNP aims to pileup the expressed alleles in single-cell or bulk RNA-seq 
data, which can be directly used for donor deconvolution in multiplexed 
single-cell RNA-seq data, particularly with vireo_, which assigns cells to 
donors and detects doublets, even without genotyping reference.

cellSNP heavily depends on pysam_, a Python interface for samtools and bcftools. 
This program should give very similar results as samtools/bcftools mpileup. 
Also, there are two major differences comparing to bcftools mpileup:

1. cellSNP can pileup either the whole genome or a list of positions, with 
   directly splitting into a list of cell barcodes, e.g., for 10x genome. With 
   bcftools, you may need to manipulate the RG tag in the bam file if you want 
   to divide reads into cell barcode groups.
2. cellSNP uses simple filtering for outputting SNPs, i.e., total UMIs or counts
   and minor alleles fractions. The idea here is to keep most information of 
   SNPs and the downstream statistical model can take the full use of it.
   
cellSNP has now a C version named cellsnp-lite_, which is basically more efficient 
with higher speed and less memory usage.




.. _vireo: https://github.com/huangyh09/vireo
.. _cellsnp-lite: https://github.com/single-cell-genetics/cellsnp-lite
.. _snapshot: https://github.com/huangyh09/cellSNP/blob/master/doc/manual.rst
.. _pysam: https://github.com/pysam-developers/pysam
.. _pypi: https://pypi.org/project/cellSNP/
.. _gnomAD: http://gnomad.broadinstitute.org
.. _1000_Genome_Project: http://www.internationalgenome.org
.. _script: https://github.com/huangyh09/cellSNP/blob/master/SNPlist_1Kgenome.sh
.. _folder: https://sourceforge.net/projects/cellsnp/files/SNPlist/
.. _LiftOver_vcf: https://github.com/huangyh09/cellSNP/tree/master/liftOver
.. _release.rst: https://github.com/huangyh09/cellSNP/blob/master/doc/release.rst
.. _FAQ.rst: https://github.com/huangyh09/cellSNP/blob/master/doc/FAQ.rst
.. _issue: https://github.com/huangyh09/cellSNP/issues
