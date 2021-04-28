#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

def isMatch(s: str, p: str) -> bool:
    ls = len(s)
    lp = len(p)

    result = [[0 for i in range(lp + 1)] for j in range(ls + 1)]

    for i in range(ls + 1):
        result[i][0] = 1

    for i in range(lp):
        if p[i]!='*':
            break
        result[0][i + 1] = 1

    if ls == 0:
        return bool(result[ls][lp])

    for i in range(lp):
        if p[i]=="*":
            if result[1][i]:
                result[1][i+1] = result[0][i+1] + 1
            else:
                result[1][i+1] = result[0][i+1]
            continue
        if (p[i]=="?" or p[i]==s[0]) and result[0][i]:
            result[1][i+1] = result[0][i+1] + 1
        else:
            result[1][i+1] = result[0][i+1]

    for j in range(lp):
        for i in range(1, ls):
            if p[j] != '*':
                if (p[j]=='?' or p[j]==s[i]) and result[i-1][j] != result[i][j]:
                    result[i+1][j+1] = result[i][j+1] + 1
                else:
                    result[i+1][j+1] = result[i][j+1]
                continue
            if result[i+1][j]:
                result[i+1][j+1] = result[i][j+1] + 1
            else:
                result[i+1][j+1] = result[i][j+1]
    for i in range(ls + 1):
        for j in range(lp + 1):
            print(result[i][j],end=' ')
        print("")

    return result[ls][lp]!=result[ls-1][lp]
