import argparse
import os
import pandas as pd
import sys

package_path = os.path.dirname(os.path.realpath(__file__))
ENSG_TO_HGNC_PATH = os.path.join(package_path, 'HGNC_Ensembl_mapping_04_18_2018.txt')
ENST_TO_ENSG_PATH = os.path.join(package_path,'ENST_ENSG_MAPPING_04_18_2018.txt')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This script takes in a tab-separated file containing at least one column of Ensembl IDs and a string indicating the
# header for this column, and outputs a tab-separated file identical to the input file except that it has an additional
# column containing mapped HGNC gene symbols for each row.
# --------------------------------------------------------------------------------------------------------------------
# Example usages:
# 1. Assuming output path is location of input file
#   /path/to/file_containing_ensembl_column <ensembl_column_header>
# 2. Specifying output path
#   /path/to/file_containing_ensembl_column <ensembl_column_header> --output_path /path/to/output/location
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def load_ensg_hgnc_mapping(file_path):
    """Load in the file that contains the mappings between Ensembl Gene IDs and HGNC gene symbols,
    returning a dictionary mapping of this information."""
    mapping = pd.read_csv(file_path, sep='\t')
    mapping_dict = {}

    def add_row_to_mapping_dict(r):
        mapping_dict[r['Ensembl Gene ID']] = r['Approved Symbol']
    mapping.apply(add_row_to_mapping_dict, axis=1)

    return mapping_dict


def load_enst_ensg_mapping(file_path):
    mapping = pd.read_csv(file_path, sep='\t')
    mapping_dict = {}

    def add_row_to_mapping_dict(r):
        mapping_dict[r['Transcript stable ID']] = r['Gene stable ID']
    mapping.apply(add_row_to_mapping_dict, axis=1)

    return mapping_dict

def map_enst_to_hgnc(enst_ensg, ensg_hgnc):
    """Make a dictionary mapping ENST IDs to HGNC gene symbols"""
    enst_hgnc_mapping = {}
    for enst, ensg in enst_ensg.items():
        enst_hgnc_mapping[enst] = ensg_hgnc.get(ensg)

    return enst_hgnc_mapping


def add_symbol_from_enst(input_df, enst_to_hgnc_mapping, enst_header):
    """Take in a dataframe containing the original ENST column and add to it a column containing gene symbol"""
    def enst_to_symbol(enst):
        try:
            symbol = enst_to_hgnc_mapping[enst]
        except KeyError:
            try:
                # Try just mapping to the Ensembl ID section before the '.'
                symbol = enst_to_hgnc_mapping[enst.split('.')[0]]
            except KeyError:
                return 'Unknown'
        return symbol

    input_df['Gene Symbol'] = input_df.apply(lambda row: enst_to_symbol(row[enst_header]), axis=1)
    return input_df


def add_symbol_from_ensg(input_df, ensg_to_hgnc_mapping, ensg_header):
    """Take in a dataframe containing the original ENSG column and add to it a column containing gene symbol"""
    def ensg_to_symbol(ensg):
        try:
            symbol = ensg_to_hgnc_mapping[ensg]
        except KeyError:
            try:
                # Try just mapping to the Ensembl ID section before the '.'
                symbol = ensg_to_hgnc_mapping[ensg.split('.')[0]]
            except KeyError:
                return 'Unknown'
        return symbol

    input_df['Gene Symbol'] = input_df.apply(lambda row: ensg_to_symbol(row[ensg_header]), axis=1)
    return input_df


def main():
    parser = argparse.ArgumentParser(description='Translate Ensembl IDs to HGNC symbols')
    parser.add_argument('input_file', metavar='input_file', type=str)
    parser.add_argument('--ensg_header', metavar='ensg_header', type=str)
    parser.add_argument('--enst_header', metavar='enst_header', type=str)
    parser.add_argument('--output_path', metavar='output_path', type=str)

    args = parser.parse_args()

    input_file = args.input_file
    ensg_header = args.ensg_header
    enst_header = args.enst_header
    output_path = args.output_path

    if enst_header and ensg_header:
        sys.exit("Only one of enst_header or ensg_header should be provided\n")
    if not enst_header and not ensg_header:
        sys.exit("One of enst_header or ensg_header must be provided\n")

    input_df = pd.read_csv(input_file, sep='\t')

    ensg_to_hgnc = load_ensg_hgnc_mapping(ENSG_TO_HGNC_PATH)
    enst_to_ensg = load_enst_ensg_mapping(ENST_TO_ENSG_PATH)

    if ensg_header:
        # Generate a dataframe with Gene Symbol column added
        output_df = add_symbol_from_ensg(input_df, ensg_to_hgnc, ensg_header)
    elif enst_header:
        enst_to_hgnc = map_enst_to_hgnc(enst_to_ensg, ensg_to_hgnc)
        output_df = add_symbol_from_enst(input_df, enst_to_hgnc, enst_header)
    else:
        # Should never get to this line...
        output_df = input_df

    output_filename = '{}.{}.{}'.format(os.path.basename(input_file).split('.')[0], 'hgnc_symbols', 'tsv')

    # If output path is provided, output location is based on this -- otherwise, it is based on input file location
    if output_path:
        output_location = os.path.join(output_path, output_filename)
    else:
        output_location = os.path.join(os.path.dirname(input_file), output_filename)

    # Output tab-separated file to output location
    output_df.to_csv(output_location, sep='\t', index=False)


if __name__ == '__main__':
    main()
