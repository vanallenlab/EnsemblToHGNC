# EnsemblToHGNC

This script takes in a tab-separated file containing at least one column of Ensembl IDs and a string indicating the
header for this column, and outputs a tab-separated file identical to the input file except that it has an additional
column containing mapped HGNC gene symbols for each row.

--------------------------------------------------------------------------------------------------------------------
# Example usages:
1. Assuming output path is location of input file
/path/to/file_containing_ensembl_column <ensembl_column_header>

2. Specifying output path
/path/to/file_containing_ensembl_column <ensembl_column_header> --output_path /path/to/output/location
