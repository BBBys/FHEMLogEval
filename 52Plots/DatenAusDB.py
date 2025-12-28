#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys
# is licensed under CC BY-NC-ND 4.0.
#
#  DatenAusDb.py

import logging
import pandas as pd
from dbparam import DBTMW

# import mysql.connector


def DatenAusDB(mydb):
    # DFCOLUMNS =["zeitpunkt", "messpunkt", "messwert"]
    DFCOLUMNS = ["zeitpunkt", "messwert"]
    convert_dict = {"zeitpunkt": "datetime64[ns]", "messwert": float}

    sql = f"""SELECT zeitpunkt,Messwert from {DBTMW}
                    WHERE 
                        messpunkt='VBad'
                    ORDER BY zeitpunkt;"""
    logging.debug(sql)
    df = pd.read_sql(sql, mydb)
    df.columns = DFCOLUMNS
    df = df.astype(convert_dict, errors="ignore")
    df["zeitpunkt"] = pd.to_datetime(df["zeitpunkt"], format="mixed")
    df = df.set_index("zeitpunkt")
    logging.info(f"Anzahl Datensätze: {len(df)}")
    logging.debug(f"\n{df.head(10)}")

    return df
