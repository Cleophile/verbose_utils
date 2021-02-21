#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

from collections import namedtuple

# A table structure is suppposed to be:
#
#     --- line_above ---------
#         header_row
#     --- line_below_header ---
#         data_row
#     --- line_bewteen_rows ---
#     ... (more datarows) ...
#     --- line_bewteen_rows ---
#         data_row (last one)
#     --- line_below ---------
#
# TableFormat's line* elements can be
#
#   - either None, if the element is not used,
#   - or a Line tuple,
#   - or a function: [col_widths], [col_alignments] -> string.
#
# TableFormat's *row elements can be
#
#   - either None, if the element is not used,
#   - or a DataRow tuple,
#   - or a function: [cell_values], [col_widths], [col_alignments] -> string.
#
# padding (an integer) is the amount of minimum white space around data values.
#
# with_header_hide:
#
#   - either None, to display all table elements unconditionally,
#   - or a list of elements not to be displayed if the table has column headers.
#

TableFormat = namedtuple(
    "TableFormat",
    [
        "line_above",
        "line_below_header",
        "line_between_rows",
        "line_below",
        "header_row",
        "data_row",
        "force_padding",
        "with_header_hide"
    ],
)

# DataRowFormat
# like | aa | bb |
# begin=separate=end=|

DataRowFormat = namedtuple(
    "DataRowFormat",
    [
        "begin",
        "separate",
        "end"
    ]
)

# LineFormat
# like +----+----+
# begin=end=separate=+, fill=-

LineFormat = namedtuple(
    "LineFormat",
    [
        "begin",
        "fill",
        "separate",
        "end"
    ]
)

TableFormatter = {
    "pretty_ascii": TableFormat(),
}


def main():
    # Insert Code Here...
    pass

if __name__ == "__main__":
    main()

def __format_line():
    pass

def __convert_table(table):
    pass

def __calculate_space(table):
    pass

def __align_number(table, i):
    pass

def table_verbose(table,
                  table_format="plain",
                  str_aligh="center",
                  number_align=False,
                  edge_line=True,
                  
                  ):
    if table_format not in TableFormatter:
        raise ValueError("Choose one from {}".format(list(TableFormatter.keys())))
