#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 09:39:48 2020

@author: NickBrown
"""

# lttable

import pandas as pd
import re

r1 = "<...>"
#bool(re.search("<...>", "<4gf> is a string"))
#re.findall("<...>", "<4gf> is a string")

r2 = "<\??...>"
#re.findall("<\??...>", "<?rzk> is a string")

r3 = "<.*z.*z.*z.*>"
#re.findall("<.*z.*z.*z.*>", "<Pizzaz> is string")

r4 = "<[^z]*z[^z]*z[^z]*z[^z]*>"
#re.findall("<[^z]*z[^z]*z[^z]*z[^z]*>", "<Bizz>z is string")

r5 = "-?[0-9]*\.[0-9]*"
#re.findall("-?[0-9]*\.[0-9]*", "A decimal number: 00.99")

def read_lttable(a):
    # initial split
    z = re.sub(r"(.?\.*?\\hline)+", r"\\\\", a)
    y = re.sub(" ", "", z)
    x = re.split(r"\\\\",y)
    
    # creation of data frames (still concerned about specific ranges, may not apply to other tables, not sure how to avoid that)
    data = x[1:(len(x)-2)]
    column_names = data[0]
    column_names = re.split("&", column_names)
    
    # rows
    rows = data[2:(len(data))]
    rows = pd.Series(rows)
    rows = rows.str.split("&")
    row_list = rows.tolist()
    
    # data frame
    df = pd.DataFrame(row_list)
    df.columns = column_names
    return df


f = open("lttable.tex", "r")
s = f.read()
f.close()
read_lttable(s)



