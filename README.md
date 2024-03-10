# Public Liquor Data

In order to build tools that work with bar codes for liquor bottles, I've tried to collect and parse publicly available data.
These data dumps were received under public records requests or publicly available from US states' various liquor control bodies.

All the scripts are [licensed under the MIT license](LICENSE), and the data is made available under the public record laws of the relevant state.

## Data sources

### [Oregon](https://github.com/jorgenpt/public_liquor_data/tree/main/data/oregon/)

These are records received from OLCC.PublicRecords@oregon.gov.

The "GTIN List With Price" is a slightly awkward Excel format, but parseable with [`xlrd`](https://xlrd.readthedocs.io/en/latest/) and some logic, [see oregon_gtin_list_to_json.py](oregon_gtin_list_to_json.py).

### [Utah](https://github.com/jorgenpt/public_liquor_data/tree/main/data/utah/)

These are public records published on the following URLs:

- https://abs.utah.gov/shop-products/interactive-product-list/
- https://abs.utah.gov/vendors/monthly-price-books/

The "Product List" Excel spreadsheet is excellent and easily parseable (with [`pandas`](https://pandas.pydata.org/) in this case, [see utah_product_list_to_csv.py](utah_product_list_to_csv.py)), but does not contain any bar code information.

The "Numeric Price List" on the other hand has a mapping from Utah's "CSC" product codes to bar codes, but is only available as a PDF. While somewhat painful to parse, [`camelot`](https://camelot-py.readthedocs.io/) provides a lot of help.

### [Washington](https://github.com/jorgenpt/public_liquor_data/tree/main/data/washington/)

This is a dump received from publicrecords@lcb.wa.gov, containing the latest data before the state stopped running their own liquor stores. Unclear if this will be useful, so it has not been parsed yet.
