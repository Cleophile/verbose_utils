#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

from table_verbose import table_verbose

table = [["arroz","China",3.22], ["jamón", "España", 39.9], [["mantequilla\n(Hecho en Alemania)",2], 10]]
header = ["Alimiento", "Lugar\nde Producción", "Precio"]

s = table_verbose(table, header=header, str_align=["left", "right"], edge_line=True, number_align=True, table_format="pretty_ascii", vertical_padding=0)
print(s)
s = table_verbose(table, header=header, str_align=["left", "right"], edge_line=True, number_align=True, table_format="fancy_outline", vertical_padding=0)
print(s)
s = table_verbose(table, header=header, str_align=["left", "right"], edge_line=True, number_align=True, table_format="plain", vertical_padding=0)
print(s)
s = table_verbose(table, header=header, str_align=["left", "right"], edge_line=True, number_align=True, table_format="jira", vertical_padding=0)
print(s)
s = table_verbose(table, header=header, str_align=["left", "right"], edge_line=True, number_align=True, table_format="rst", vertical_padding=0)
print(s)
s = table_verbose(table, header=header, str_align=["left", "right"], edge_line=True, number_align=True, table_format="html", vertical_padding=0)
print(s)

print("np.array test")
import numpy as np
import pandas as pd
table = np.array(table)
s = table_verbose(table, header=header, str_align=["left", "right"], edge_line=True, number_align=True, table_format="pretty_ascii", vertical_padding=0)
print(s)

dta = pd.DataFrame(dict(stock=['600123','600234','600345'], price=[11.34, 11.29, 13.37]))
s = table_verbose(dta, header=['stockId\nsymbol','price'], str_align=["left", "right"], edge_line=True, number_align=True, table_format="pretty_ascii", vertical_padding=0)
print(s)

