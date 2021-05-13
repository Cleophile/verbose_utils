#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

from collections import namedtuple
from typing import List, Union

# Line generators
def __markdown_below_header_generator(grid_space, align):
    if align=="center":
        s = [":" + "-"*i + ":" for i in grid_space]
    elif align=="left":
        s = [":" + "-"*i for i in grid_space]
    elif align=="right":
        s = ["-"*i + ":" for i in grid_space]
    else:
        raise ValueError("Align must be center, left or right")

    return "|" + "|".join(s) + "|"

def __jira_table_format(table, header, number_align, *args, **kwargs):
    column_count = __convert_table(table, number_align)
    print(table)
    if header:
        line_count = __convert_header(header)
        header_delta = max(0, column_count - line_count)
        column_count = max(column_count, line_count)
        s = "||"
        for i in header:
            s += i[0] + "||" * i[1]
        s += "||" * header_delta + "\n"
    else:
        s = "\n"

    for line in table:
        line_str = "|"
        for i in line:
            line_str += i[0] + "|" * i[1]
        s += line_str + "\n"
    return s

# A table structure is suppposed to be:
#         
#     --- head_note(not based on column)
#     --- line_above ---------(based on column)
#         header_row (column names)
#     --- line_below_header --- (based on column)
#         data_row
#     --- line_bewteen_rows ---
#     ... (more datarows) ...
#     --- line_bewteen_rows ---
#         data_row (last one)
#     --- line_below ---------
#
# TableFormat's line elements that are based on column can be
#
#   - either None, if the element is not used,
#   - or a Line tuple,
#   - or a function: [col_widths], [col_alignments] -> string.
#
# TableFormat's header_row or data_row elements can be
#
#   - either None, if the element is not used,
#   - or a DataRow tuple,
#   - or a function: [cell_values], [col_widths], col_alignment OR [col_alignments] -> string.
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
        "head_note",
        "line_above",
        "header_row",
        "line_below_header",
        "line_between_rows",
        "line_below",
        "data_row",
        "end_note",
        "force_padding",
        "force_top",
        "force_left",
        "force_right",
        "force_bottom"
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
    "ascii": TableFormat(
        head_note=None,
        line_above=LineFormat("-","-","-","-"),
        line_below_header=LineFormat("=","=","=","="),
        line_between_rows=None,
        line_below=LineFormat("-","-","-","-"),
        header_row=LineFormat(""," "," ",""),
        data_row=LineFormat(""," "," ",""),
        end_note=None,
        force_padding=0,
        force_left=False,
        force_bottom=None,
        force_top=None,
        force_right=False
    ),
    "pretty_ascii": TableFormat(
        head_note=None,
        line_above=LineFormat("+","-","+","+"),
        line_below_header=LineFormat("+","=","+","+"),
        line_between_rows=LineFormat("+","-","+","+"),
        line_below=LineFormat("+","-","+","+"),
        header_row=LineFormat("|"," ","|","|"),
        data_row=LineFormat("|"," ","|","|"),
        end_note=None,
        force_padding=1,
        force_left=None,
        force_bottom=None,
        force_top=None,
        force_right=None
    ),
    "jira": __jira_table_format,
    "markdown": TableFormat(
        head_note=None,
        line_above=None,
        line_below_header=__markdown_below_header_generator,
        line_between_rows=None,
        line_below=None,
        header_row=LineFormat("|","","|","|"),
        data_row=LineFormat("|","","|","|"),
        end_note=None,
        force_padding=0,
        force_left=True,
        force_bottom=False,
        force_top=False,
        force_right=True
    ),
}

def __format_line(fmt: LineFormat, count, left, right):
    str_list = fmt.separate.join([fmt.fill*c for c in count])
    if left:
        str_list = fmt.begin + str_list
    if right:
        return str_list + fmt.end
    else:
        return str_list


def __format_data_line_center(fmt: LineFormat, data, count, left, right, padding):
    i = 0
    str_list = []
    for grid, grid_length in data:
        total_length = sum(count[i : i + grid_length]) + 2 * grid_length * padding + grid_length - 1
        i += grid_length

        str_length = len(grid)
        left_length = (total_length - str_length) // 2
        right_length = total_length - str_length - left_length

        str_list.append(fmt.fill*left_length + grid + fmt.fill*right_length)

    str_list = fmt.separate.join(str_list)

    if left:
        str_list = fmt.begin + str_list
    if right:
        return str_list + fmt.end
    else:
        return str_list

def __format_data_line_left(fmt: LineFormat, data, count, left, right, padding):
    i = 0
    str_list = []
    for grid, grid_length in data:
        total_length = sum(count[i : i + grid_length])
        i += grid_length

        str_length = len(grid)
        left_length = padding
        right_length = total_length - str_length + padding * (2 * grid_length - 1) + grid_length - 1

        str_list.append(fmt.fill*left_length + grid + fmt.fill*right_length)

    str_list = fmt.separate.join(str_list)

    if left:
        str_list = fmt.begin + str_list
    if right:
        return str_list + fmt.end
    else:
        return str_list

def __format_data_line_right(fmt: LineFormat, data, count, left, right, padding):
    i = 0
    str_list = []
    for grid, grid_length in data:
        total_length = sum(count[i : i + grid_length])
        i += grid_length

        str_length = len(grid)
        right_length = padding
        left_length = total_length - str_length + padding * (2 * grid_length - 1) + grid_length - 1

        str_list.append(fmt.fill*left_length + grid + fmt.fill*right_length)

    str_list = fmt.separate.join(str_list)

    if left:
        str_list = fmt.begin + str_list
    if right:
        return str_list + fmt.end
    else:
        return str_list

DataLineGenerator = {
    "center": __format_data_line_center,
    "left": __format_data_line_left,
    "right": __format_data_line_right
}

def __align_float(table, i):
    # convert all to float before processing
    pass

def __convert_table(table, number_align):
    column_count = 0
    for line in table:
        line_count = 0
        for i in range(len(line)):
            if hasattr(line[i], "__getitem__") and \
                    len(line[i])==2 and isinstance(line[i][1], int) and line[i][1] > 0:
                if not isinstance(line[i][0], (int, float)):
                    line[i][0] = str(line[i][0])
                line_count += line[i][1]
            else:
                line[i] = [str(line[i]),1]
                line_count += 1

        column_count = max(column_count, line_count)

    # notice on not normal number col
    number_line = [True for _ in range(column_count)]
    for line in table:
        count = 0
        for i in line:
            if i[1] == 1:
                if not isinstance(i[0], (int, float)):
                    number_line[count] = False
            count += i[1]

    if isinstance(number_align, bool):
        for i in range(column_count):
            number_line[i] = number_line[i] and number_align
    else:
        align_idx = min(len(number_align), column_count)
        for i in range(align_idx):
            number_line[i] = number_align[i] and number_align[i]

        for i in range(align_idx, column_count):
            number_line[i] = False

    __align_float(table, number_line)
    print(number_line)

    return column_count

def __convert_header(header):
    line_count = 0
    for i in range(len(header)):
        if hasattr(header[i],"__getitem__") and \
                len(header[i])==2 and isinstance(header[i][1],int) and header[i][1] > 0:
            if not isinstance(header[i][0], (int, float)):
                header[i][0] = str(header[i][0])
            line_count += header[i][1]
        else:
            header[i] = [str(header[i]),1]
            line_count += 1

    return line_count

def __calculate_space(table, column_count):
    length = [0 for _ in range(column_count)]
    for line in table:
        i = 0
        for grid, grid_spread in line:
            if grid_spread == 1:
                if length[i] < len(grid):
                    length[i] = len(grid)
            else:
                # TODO
                pass
            i += grid_spread
    return length

def __calculate_header_space(header, column_count):
    length = [0 for _ in range(column_count)]
    i = 0
    for grid, grid_spread in header:
        if grid_spread == 1:
            if length[i] < len(grid):
                length[i] = len(grid)
        else:
            current_length = sum(length[i:i+grid_spread])
            if current_length < len(grid):
                average_add = (len(grid) - current_length) // grid_spread
                modulo = (len(grid) - current_length) % grid_spread
                for i in range(modulo):
                    length[i] += average_add + 1
                for i in range(modulo, grid_spread):
                    length[i] += average_add
        i += grid_spread
    return length

def table_verbose(table,
                  header=None,
                  table_format="pretty_ascii",
                  str_aligh="center",
                  number_align=False,
                  restrict_float=False,
                  edge_line=True,
                  padding=0,
                  vertical_padding=0,
                  ):
    if table_format not in TableFormatter:
        raise ValueError("Choose one from {}".format(list(TableFormatter.keys())))
    formatter = TableFormatter[table_format]

    if not isinstance(formatter, TableFormat):
        return formatter(table, header, str_aligh, number_align,
                         restrict_float, edge_line, padding, vertical_padding)

    padding = max(formatter.force_padding, padding)

    if str_aligh not in DataLineGenerator:
        raise ValueError("Choose one from {}".format(list(TableFormatter.keys())))
    data_line_formatter = DataLineGenerator[str_aligh]

    column_edge = {"top": True, "left": True, "right": True, "bottom": True}
    # top bottom left right
    if edge_line is False:
        column_edge = {"top": False, "left": False, "right": False, "bottom": False}
    #  elif edge_line is not False:
    if formatter.force_left is not None:
        column_edge['left'] = formatter.force_left
    if formatter.force_right is not None:
        column_edge['right'] = formatter.force_right
    if formatter.force_top is not None:
        column_edge['top'] = formatter.force_top
    if formatter.force_bottom is not None:
        column_edge['bottom'] = formatter.force_bottom

    column_count = __convert_table(table, number_align)
    space_count = __calculate_space(table, column_count)

    if header and formatter.header_row is not None:
        header_column_count = __convert_header(header)
        header[-1][1] += column_count - header_column_count
        header_count = __calculate_header_space(header, column_count)
        for i in range(len(header_count)):
            space_count[i] = max(space_count[i], header_count[i])

    space_after_padding = [i + padding * 2 for i in space_count]
    print(space_count)

    str_list = []

    # notes or configs at the beginning of the table
    if formatter.head_note is not None:
        str_list.append(formatter.head_note)
    if column_edge['top'] and formatter.line_above is not None:
        str_list.append(__format_line(formatter.line_above, space_after_padding, column_edge['left'], column_edge['right']))


    # header configuration
    if header and formatter.header_row is not None:
        str_list.append(data_line_formatter(formatter.header_row, header, space_count, column_edge['left'], column_edge['right'], padding))

    if header and formatter.line_below_header is not None:
        if isinstance(formatter.line_below_header, LineFormat):
            str_list.append(__format_line(formatter.line_below_header, space_after_padding, column_edge['left'], column_edge['right']))
        else:
            str_list.append(formatter.line_below_header(space_after_padding, str_aligh))

    if formatter.line_between_rows is not None:
        middle_line = "\n" +  __format_line(formatter.line_between_rows, space_after_padding, column_edge['left'], column_edge['right']) + "\n"
    else:
        middle_line = "\n"
    data_list = []

    for data in table:
        padding = 1
        data_list.append(data_line_formatter(formatter.data_row, data, space_count, column_edge['left'], column_edge['right'], padding))

    str_list.append(middle_line.join(data_list))

    if column_edge['bottom'] and formatter.line_below is not None:
        str_list.append(__format_line(formatter.line_below, space_after_padding, column_edge['left'], column_edge['right']))

    if formatter.end_note is not None:
        str_list.append(formatter.end_note)

    return "\n".join(str_list)

if __name__=="__main__":
    table = [["Rice",12.232],["Shrimp",399.9],["",100.2]]
    #  header = ["Food Product","Price in Dollars"]
    header = ["Food Product Food Food Food Food"]
    s = table_verbose(table, header=header, str_aligh="center", edge_line=True, number_align=True)
    #  s = table_verbose(table, header=header, str_aligh="right", edge_line=True)
    #  s = table_verbose(table)
    print(s)
