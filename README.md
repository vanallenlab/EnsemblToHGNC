# EnsemblToHGNC

This script takes in a tab-separated file containing at least one column of Ensembl gene or transcript IDs (ENSG/ENST)
and a string indicating the header for this column, and outputs a tab-separated file identical to the input file except
that it has an additional column containing mapped HGNC gene symbols for each row.

The ENSG-HGNC symbol mapping is derived from downloads at this site: https://www.genenames.org/cgi-bin/download. Data is based on Ensembl release 92, from April 2018.

The ENSG-ENST symbol mapping is derived from Ensembl's biomart: http://useast.ensembl.org/biomart/. Data is based on Ensemble release 92, from April 2018.

--------------------------------------------------------------------------------------------------------------------
# Example usages:
1. Assuming output path is location of input file

`python EnsemblToHGNC.py /path/to/file_containing_ensembl_column --ensg_header/--enst_header <ensembl_column_header>`

2. Specifying output path

`python EnsemblToHGNC.py /path/to/file_containing_ensembl_column --ensg_header/--enst_header <ensembl_column_header> --output_path /path/to/output/location`
