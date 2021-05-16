#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

from table_verbose import table_verbose

table = [["arroz","China",3.22], ["jamón", "España", 39.9], [["mantequilla\n(Hecho en Alemania)",2], 10]]
#  header = ["Food Product","Price in Dollars"]
header = ["Alimiento", "Lugar\nde Producción", "Precio"]
s = table_verbose(table, header=header, str_align=["left", "right"], edge_line=True, number_align=True, table_format="pretty_ascii", vertical_padding=0)
#  s = table_verbose(table, header=header, str_align="right", edge_line=True)
#  s = table_verbose(table)
print(s)
