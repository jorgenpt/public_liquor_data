#!/usr/bin/python3

import json
import os
import sys

from xlrd import open_workbook, XL_CELL_EMPTY

def main():
    if len(sys.argv) != 2:
        print("Usage: ./oregon_product_list_to_json.py <Excel file>", file=sys.stderr)
        sys.exit(1)

    xls_path = sys.argv[1]
    output_path = os.path.splitext(xls_path)[0] + ".json"

    book = open_workbook(xls_path)
    document_started = False
    all_items = []
    current_item = None
    for sheet_index in range(book.nsheets):
        sheet_index = book.sheet_by_index(sheet_index)
        for row_index in range(sheet_index.nrows):
            row = sheet_index.row(row_index)

            # Skip the per-page legend (and anything beofre the first one)
            if row[1].value == "* Non-Standard Code":
                document_started = True
                continue
            if not document_started:
                continue

            # Skip empty rows
            if all((cell.ctype == XL_CELL_EMPTY for cell in row)):
                continue
            # Skip header rows
            if row[0].value == "Item Code" or row[4].value == "Description":
                continue
            # Skip final report row
            if row[0].value.startswith("LIQUOR STORE REPORTS"):
                continue

            if row[0].ctype != XL_CELL_EMPTY:
                for unused_index in (1, 3, 5, 6, 7):
                    assert row[unused_index].ctype == XL_CELL_EMPTY
                all_items.append({
                    "ItemCode": row[0].value,
                    "NewItemCode": row[2].value,
                    "Description": row[4].value,
                    "Size": row[8].value,
                    "Price": None,
                    "Codes": [],
                })
                current_item = all_items[-1]
            else:
                if row[15].ctype != XL_CELL_EMPTY:
                    assert current_item["Price"] is None
                    current_item["Price"] = row[15].value
                current_item["Codes"].append({"CodeType": row[10].value, "Code": row[12].value})

    with open(output_path, "w") as output_fp:
        json.dump(all_items, output_fp)


if __name__ == "__main__":
    main()