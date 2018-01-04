import argparse
import os
import pandas as pd

ENSEMBL_TO_HGNC_PATH = './HGNC_Ensembl_mapping_01_03_2018.txt'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This script takes in a tab-separated file containing a column of Ensembl IDs and a string indicating the header for
# this column, and outputs a tab-separated file identical to the input file except that it has an additional column
# containing mapped HGNC gene symbols for each row.
# --------------------------------------------------------------------------------------------------------------------
# Example usages:
# 1. Assuming output path is location of input file
#   /path/to/file_containing_ensembl_column <ensembl_column_header>
# 2. Specifying output path
#   /path/to/file_containing_ensembl_column <ensembl_column_header> --output_path /path/to/output/location
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def load_ensembl_hgnc_mapping(file_path):
    """Load in the file that contains the mappings between Ensembl IDs and HGNC gene symbols, returning a dictionary
    mapping of this information."""
    mapping = pd.read_csv(file_path, sep='\t')
    mapping_dict = {}

    def add_row_to_mapping_dict(r):
        mapping_dict[r['Ensembl Gene ID']] = r['Approved Symbol']
    mapping.apply(add_row_to_mapping_dict, axis=1)

    return mapping_dict


def add_symbol(input_df, ensembl_to_hgnc_mapping, ensembl_header):
    """Take in a dataframe containing the original Ensembl column and add to it a column containing gene symbol"""
    def to_symbol(ensembl_id):
        try:
            symbol = ensembl_to_hgnc_mapping[ensembl_id]
        except KeyError:
            try:
                # Try just mapping to the Ensembl ID section before the '.'
                symbol = ensembl_to_hgnc_mapping[ensembl_id.split('.')[0]]
            except KeyError:
                return 'Unknown'
        return symbol

    input_df['Gene Symbol'] = input_df.apply(lambda row: to_symbol(row[ensembl_header]), axis=1)
    return input_df


def main():
    parser = argparse.ArgumentParser(description='Translate Ensembl IDs to HGNC symbols')
    parser.add_argument('input_file', metavar='input_file', type=str)
    parser.add_argument('ensembl_header', metavar='ensembl_header', type=str)
    parser.add_argument('--output_path', metavar='output_path', type=str)

    args = parser.parse_args()

    input_file = args.input_file
    ensembl_header = args.ensembl_header
    output_path = args.output_path

    ensembl_to_hgnc = load_ensembl_hgnc_mapping(ENSEMBL_TO_HGNC_PATH)
    input_df = pd.read_csv(input_file, sep='\t')

    # Generate a dataframe with Gene Symbol column added
    output_df = add_symbol(input_df, ensembl_to_hgnc, ensembl_header)

    output_filename = '{}.{}'.format(input_file.split('/')[-1], 'hgnc_symbols')

    # If output path is provided, output location is based on this -- otherwise, it is based on input file location
    if output_path:
        output_location = os.path.join(output_path, output_filename)
    else:
        output_location = os.path.join(os.path.dirname(input_file), output_filename)

    # Output tab-separated file to output location
    output_df.to_csv(output_location, sep='\t', index=False)


if __name__ == '__main__':
    main()
