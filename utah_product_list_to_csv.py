#!/usr/bin/python3

import os
import sys

from pandas import read_excel

def main():
    if len(sys.argv) != 2:
        print("Usage: ./utah_product_list_to_csv.py <input file>", file=sys.stderr)
        sys.exit(1)

    xls_path = sys.argv[1]
    output_path = os.path.splitext(xls_path)[0] + ".csv"

    df = read_excel(xls_path, index_col=0)
    df.to_csv(output_path)

if __name__ == "__main__":
    main()