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
