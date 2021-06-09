#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

from collections import namedtuple
from typing import List, Union
from pandas import DataFrame

# Line generators
def __markdown_below_header_generator(grid_space, align_list):
    s = []
    for i, align in zip(grid_space, align_list):
        if align == "center":
            s.append(":" + "-" * i + ":")
        elif align == "left":
            s.append(":" + "-" * i)
        else:
            s.append("-" * i + ":")

    return "|" + "|".join(s) + "|"

def __jira_table_format(table, header, number_align, *args, **kwargs):
    column_count = __convert_table(table, number_align)
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

def __html_table_format(table, header, str_align, number_align,
                        restrict_float, edge_line, padding,
                        vertical_padding, *args, **kwargs):
    __convert_table(table, number_align)
    if header:
        __convert_header(header)
        grid_str = []
        for grid, grid_length in header:
            grid = grid.replace("\n", "<br />")
            if grid_length == 1:
                grid_str.append(f"<th>{grid}</th>")
            else:
                grid_str.append(f"<th colspan=\"{grid_length}\">{grid}</th>")
        header_str = "<thead>\n" + "\n".join(grid_str) + "\n</thead>\n"
    else:
        header_str = "<thead></thead>"

    line_str = []
    for line in table:
        grid_str = []
        for grid, grid_length in line:
            grid = grid.replace("\n", "<br />")
            if grid_length == 1:
                grid_str.append(f"<td>{grid}</td>")
            else:
                grid_str.append(f"<td colspan=\"{grid_length}\">{grid}</td>")
        line_str.append("".join(grid_str))

    line_str = "<tbody>\n<tr>\n" + "</tr>\n<tr>\n".join(line_str) + "\n</tr>\n</tbody>"

    return header_str + line_str

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
#   - or a LineFormat tuple,
#   - or a function: [col_widths], [col_alignments] -> string.
#
# TableFormat's header_row or data_row elements can be
#
#   - either None, if the element is not used,
#   - or a LineFormat tuple,
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
        "force_bottom",
        "illegal"
    ],
)

# DataRowFormat
# like | aa | bb |
# begin=separate=end='|'

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
# begin=end=separate='+', fill='-'

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
    "plain": TableFormat(
        head_note=None,
        line_above=None,
        line_below_header=None,
        line_between_rows=None,
        line_below=None,
        header_row=LineFormat(" "," "," "," "),
        data_row=LineFormat(" "," "," "," "),
        end_note=None,
        force_padding=0,
        force_left=None,
        force_bottom=None,
        force_top=None,
        force_right=None,
        illegal={'\t'}
    ),
    "ascii": TableFormat(
        head_note=None,
        line_above=LineFormat("-","-","-","-"),
        line_below_header=LineFormat("=","=","=","="),
        line_between_rows=None,
        line_below=LineFormat("-","-","-","-"),
        header_row=LineFormat(" "," "," "," "),
        data_row=LineFormat(" "," "," "," "),
        end_note=None,
        force_padding=0,
        force_left=None,
        force_bottom=None,
        force_top=None,
        force_right=None,
        illegal={'\t'}
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
        force_right=None,
        illegal={"\t"}
    ),
    "rst": TableFormat(
        head_note=None,
        line_above=LineFormat("", "=", "  ", ""),
        line_below_header=LineFormat("", "=", "  ", ""),
        line_between_rows=None,
        line_below=LineFormat("", "=", "  ", ""),
        header_row=LineFormat("", " ", "  ", ""),
        data_row=LineFormat("", " ", "  ", ""),
        end_note=None,
        force_padding=1,
        force_left=None,
        force_bottom=None,
        force_top=None,
        force_right=None,
        illegal={"\t"}
    ),
    "jira": __jira_table_format,
    "html": __html_table_format,
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
        force_right=True,
        illegal={'\t', "\n"}
    ),
    "fancy_grid": TableFormat(
        head_note=None,
        line_above=LineFormat("╒", "═", "╤", "╕"),
        line_below_header=LineFormat("╞", "═", "╪", "╡"),
        line_between_rows=LineFormat("├", "─", "┼", "┤"),
        line_below=LineFormat("╘", "═", "╧", "╛"),
        header_row=LineFormat("│", " ", "│", "│"),
        data_row=LineFormat("│", " ", "│", "│"),
        end_note=None,
        force_padding=0,
        force_left=None,
        force_bottom=True,
        force_top=True,
        force_right=None,
        illegal={'\t'}
    ),
    "fancy_outline": TableFormat(
        head_note=None,
        line_above=LineFormat("╒", "═", "╤", "╕"),
        line_below_header=LineFormat("╞", "═", "╪", "╡"),
        line_between_rows=None,
        line_below=LineFormat("╘", "═", "╧", "╛"),
        header_row=LineFormat("│", " ", "│", "│"),
        data_row=LineFormat("│", " ", "│", "│"),
        end_note=None,
        force_padding=0,
        force_left=None,
        force_bottom=True,
        force_top=True,
        force_right=None,
        illegal={'\t'}
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


def __format_grid_center(fill, block_length, grid, grid_length, padding):
    total_length = block_length + 2 * grid_length * padding + grid_length - 1

    str_length = len(grid)
    left_length = (total_length - str_length) // 2
    right_length = total_length - str_length - left_length

    return fill * left_length + grid + fill * right_length

def __format_grid_left(fill, block_length, grid, grid_length, padding):
    str_length = len(grid)
    left_length = padding
    right_length = block_length - str_length + padding * (2 * grid_length - 1) + grid_length - 1

    return fill * left_length + grid + fill * right_length

def __format_grid_right(fill, block_length, grid, grid_length, padding):
    str_length = len(grid)
    right_length = padding
    left_length = block_length - str_length + padding * (2 * grid_length - 1) + grid_length - 1

    return fill * left_length + grid + fill * right_length

GridGenerator = {
    "center": __format_grid_center,
    "left": __format_grid_left,
    "right": __format_grid_right
}

def __format_data_line(fmt: LineFormat, data, count, left, right, padding, align_list, vertical_padding):
    length_list = []
    grid_list = []
    for grid, grid_length in data:
        length_list.append(grid_length)
        grid_list.append(grid.split("\n"))
    longest = max([len(i) for i in grid_list]) + 2 * vertical_padding
    str_mat = [[] for _ in range(longest)]
    i = 0
    for line, grid_length in zip(grid_list, length_list):
        align = align_list[i]
        grid_generator = GridGenerator[align]
        n = len(line)
        lower = (longest - n ) // 2
        upper = longest - lower - n
        c = 0
        for _ in range(upper):
            str_mat[c].append(grid_generator(fmt.fill, sum(count[i : i + grid_length]), "", grid_length, padding))
            c += 1
        for grid in line:
            str_mat[c].append(grid_generator(fmt.fill, sum(count[i : i + grid_length]), grid, grid_length, padding))
            c += 1
        for _ in range(lower):
            str_mat[c].append(grid_generator(fmt.fill, sum(count[i : i + grid_length]), "", grid_length, padding))
            c += 1
        i += grid_length

    for i in range(longest):
        str_mat[i] = fmt.separate.join(str_mat[i])

    if left:
        for i in range(longest):
            str_mat[i] = fmt.begin + str_mat[i]
    if right:
        for i in range(longest):
            str_mat[i] = str_mat[i] + fmt.end
    return "\n".join(str_mat)

def __align_float(table, number_align, column_count):
    decimal_left = [0 for _ in range(column_count)]
    # decimal_right includes the decimal point
    decimal_right = [0 for _ in range(column_count)]
    for line in table:
        count = 0
        for i in line:
            if i[1] != 1 or (not number_align[count]):
                count += i[1]
                continue
            decimal_id = i[0].find(".")
            if decimal_id == -1:
                decimal_left[count] = max(decimal_left[count], len(i[0]))
            else:
                decimal_left[count] = max(decimal_left[count], decimal_id)
                decimal_right[count] = max(decimal_right[count], len(i[0]) - decimal_id)
            count += i[1]

    for line in table:
        count = 0
        for i in line:
            if i[1] != 1 or (not number_align[count]):
                count += i[1]
                continue
            decimal_id = i[0].find(".")
            if decimal_id == -1:
                i[0] = " " * (decimal_left[count] - len(i[0])) + i[0] + " " * decimal_right[count]
            else:
                i[0] = " " * (decimal_left[count] - decimal_id) + i[0] + " " * (decimal_right[count] - len(i[0]) + decimal_id)
            count += i[1]

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
                if isinstance(line[i], (int, float)):
                    line[i] = [line[i],1]
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
                else:
                    i[0] = str(i[0])
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

    __align_float(table, number_line, column_count)

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
        current_length = __calculate_header_space(line, column_count)
        for i in range(column_count):
            length[i] = max(current_length[i], length[i])
    return length

def __calculate_header_space(header, column_count):
    length = [0 for _ in range(column_count)]
    i = 0
    for grid, grid_spread in header:
        letters = max([len(i) for i in grid.split("\n")])
        if grid_spread == 1:
            if length[i] < letters:
                length[i] = letters
        else:
            current_length = sum(length[i:i+grid_spread])
            if current_length < letters:
                average_add = (letters - current_length) // grid_spread
                modulo = (letters - current_length) % grid_spread
                for j in range(modulo):
                    length[j] += average_add + 1
                for j in range(modulo, grid_spread):
                    length[j] += average_add
        i += grid_spread
    return length

def table_verbose(table,
                  header=None,
                  table_format="pretty_ascii",
                  str_align : Union[str, List[str]]="center",
                  number_align=False,
                  restrict_float=False,
                  edge_line=True,
                  padding=0,
                  vertical_padding=0,
                  ):
    if isinstance(table, DataFrame):
        if header is None:
            header = list(table.columns)
        table = table.to_numpy()

    if table_format not in TableFormatter:
        raise ValueError("Choose one from {}".format(list(TableFormatter.keys())))
    formatter = TableFormatter[table_format]

    if not isinstance(formatter, TableFormat):
        return formatter(table, header, str_align, number_align,
                         restrict_float, edge_line, padding, vertical_padding)

    padding = max(formatter.force_padding, padding)

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

    if isinstance(str_align, str):
        if str_align not in GridGenerator:
            raise ValueError("Choose one from {}".format(list(GridGenerator.keys())))
        str_align = [str_align for _ in range(column_count)]
    else:
        for align in str_align:
            if align not in GridGenerator:
                raise ValueError("Choose one from {}".format(list(GridGenerator.keys())))
        if len(str_align) > column_count:
            str_align = str_align[:column_count]
        elif len(str_align) < column_count:
            str_align.extend([str_align[-1] for _ in range(column_count - len(str_align))])

    space_after_padding = [i + padding * 2 for i in space_count]

    str_list = []

    # notes or configs at the beginning of the table
    if formatter.head_note is not None:
        str_list.append(formatter.head_note)
    if column_edge['top'] and formatter.line_above is not None:
        str_list.append(__format_line(formatter.line_above, space_after_padding, column_edge['left'], column_edge['right']))

    # header configuration
    if header and formatter.header_row is not None:
        str_list.append(__format_data_line(formatter.header_row, header, space_count, column_edge['left'], column_edge['right'], padding, str_align, 0))

    if header and formatter.line_below_header is not None:
        if isinstance(formatter.line_below_header, LineFormat):
            str_list.append(__format_line(formatter.line_below_header, space_after_padding, column_edge['left'], column_edge['right']))
        else:
            str_list.append(formatter.line_below_header(space_after_padding, str_align))

    if formatter.line_between_rows is not None:
        middle_line = "\n" +  __format_line(formatter.line_between_rows, space_after_padding, column_edge['left'], column_edge['right']) + "\n"
    else:
        middle_line = "\n"
    data_list = []

    for data in table:
        data_list.append(__format_data_line(formatter.data_row, data, space_count, column_edge['left'], column_edge['right'], padding, str_align, vertical_padding))

    str_list.append(middle_line.join(data_list))

    if column_edge['bottom'] and formatter.line_below is not None:
        str_list.append(__format_line(formatter.line_below, space_after_padding, column_edge['left'], column_edge['right']))

    if formatter.end_note is not None:
        str_list.append(formatter.end_note)

    return "\n".join(str_list)
