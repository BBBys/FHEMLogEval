#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys
# is licensed under CC BY-NC-ND 4.0.
#
#  DateiAusDb.py

import logging
from os import path


def DateiAusDB(pfad, mydb):
    sql = f"""SELECT * from messungen   
                    WHERE 'messpunkt' = 'TGarten'
                    INTO OUTFILE '{pfad}'
                    FIELDS TERMINATED BY ';'
                    OPTIONALLY ENCLOSED BY '\"';"""
    # sql = f"""SELECT zeitpunkt,messpunkt,messgröße,messwert from messungen
    sql = f"""SELECT zeitpunkt,messwert from messungen
                    WHERE 
                        (STRCMP(messpunkt,'TGarten') =0 )
                    INTO OUTFILE '{pfad}'
                    FIELDS TERMINATED BY ';'
                    OPTIONALLY ENCLOSED BY '\"';"""
    logging.debug(sql)
    with mydb.cursor() as cursor:
        cursor.execute(sql)  # result ist immer None

    sz = path.getsize(pfad)
    logging.debug(f"Filesize neu={sz}")
