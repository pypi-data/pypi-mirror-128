# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['variant']

package_data = \
{'': ['*']}

install_requires = \
['pyensembl>=1.9.4,<2.0.0', 'varcode']

entry_points = \
{'console_scripts': ['variant-effect = variant.effect:run']}

setup_kwargs = {
    'name': 'variant',
    'version': '0.0.6',
    'description': '',
    'long_description': '# Python pakcage for genomic variant analysis\n\n## `variant-effect` command can infer the effect of a mutation\n\nThe input file has 5 columns: `chromosome`, `position`, `strand`, `reference allele`, `alternative allele`.\n\n- No header is required.\n- The 3rd column (strand) is not used by default, just for compatibility with RNA mode.\n- By default, the base of reference and alternative allele are based on DNA information\n- For RNA mode (through `--rna` argument), the base of reference and alternative allele is reverse complement if the strand is negative(-).\n\neg:\n\n```\nchr16   400560      .      G       T\nchr17   41690930    .      G       T\nchr6    61574496    .      A       T\nchr2    84906522    .      G       T\nchr2    216205243   .      G       T\nchr4    73455665    .      G       T\nchr2    101891316   .      G       T\nchr2    69820761    .      G       T\nchr6    30723661    .      A       T\n```\n\n- The output can be stdout stdout, or a file.\n\n```\n#chrom  pos        strand  ref     alt     mut_type        gene_name       transcript_id   transcript_pos  transcript_motif        coding_pos      codon_ref       aa_pos  aa_ref\nchr16   400560     .       G       T       ThreePrimeUTR   NME4    ENST00000219479 806     GCACCAAAGTGCCGGACAACC   None    None    None    None\nchr17   41690930   .       G       T       Substitution    EIF1    ENST00000591776 515     CTTGTATAATGTAACCATTTG   363     ATG     121     M\nchr6    61574496   .       A       T       Intergenic      None    None    None    None    None    None    None    None                                                                                                                        chr2    84906522        G       T       ThreePrimeUTR   TMSB10  ENST00000233143 312     AAGCTGCACTGTGAACCTGGG   None    None    None    None\nchr2    216205243  .       G       T       ThreePrimeUTR   XRCC5   ENST00000392133 2701    TGCCATCGCTGTGATGCTGGG   None    None    None    None\nchr4    73455665   .       G       T       Substitution    AFP     ENST00000226359 1836    TTCATTCGGTGTGAACTTTTC   1820    TGT     607     C\nchr2    101891316  .       G       T       ThreePrimeUTR   MAP4K4  ENST00000350878 4267    GGAATTCCTTGTAACTGGAGC   None    None    None    None\nchr2    69820761   .       G       T       Substitution    ANXA4   ENST00000394295 934     AAATTGACATGTTGGATATCC   846     ATG     282     M\nchr6    30723661   .       A       T       Substitution    TUBB    ENST00000327892 754     GATGAGACCTATTGCATTGAC   599     TAT     200     Y\n```\n',
    'author': 'Chang Ye',
    'author_email': 'yech1990@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
