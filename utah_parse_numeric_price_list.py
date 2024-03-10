#!/usr/bin/python3

import csv
import functools
import json
import multiprocessing
import sys
import tempfile
from typing import Optional

import camelot


def parse_page(pdf: str, page: int) -> Optional[list[dict[str, str]]]:
    try:
        tables = camelot.read_pdf(pdf, 
                                pages=str(page), 
                                flavor='stream',
                                table_areas=["0,263,108,44"], 
                                columns=["56"],
                                split_text=True,
                                row_tol=10,
                                column_tol=-10)
    except ValueError:
        print(f"Skipping page {page}, can't parse", file=sys.stderr)
        return None

    table = tables[0]
    with tempfile.NamedTemporaryFile(delete=False) as table_file:
        table_file.close()
        table.to_json(table_file.name)
        with open(table_file.name, "r") as page_fp:
            page = json.load(page_fp)
    return page


def main():
    if len(sys.argv) != 3:
        print("Usage: ./utah_parse_numeric_price_list.py <input file> <output file>", file=sys.stderr)
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2]

    handler = camelot.handlers.PDFHandler(pdf_path)
    page_list = handler._get_pages(pages='all')
    num_pages = max(page_list)
    print(f"Parsing {pdf_path}, {num_pages} pages")
    pdf_rows = 0
    assert len(page_list) == num_pages

    with open(output_path, 'w', newline='') as output_fp:
        output_writer = csv.writer(output_fp)
        output_writer.writerow(("CSC", "UPC"))
        with multiprocessing.Pool() as pool:
            parsed_pages = pool.map(functools.partial(parse_page, pdf_path), page_list)
        for page in parsed_pages:
            if not page:
                continue
            for row in page[1:]:
                pdf_rows += 1
                csc_code = row["0"]
                upc_code = row["1"].strip()
                output_writer.writerow((csc_code, upc_code))

    print()
    print(f"Wrote {pdf_rows} rows to CSV")

if __name__ == "__main__":
    main()