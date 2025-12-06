#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys
# is licensed under CC BY-NC-ND 4.0.
#
#  Erfassen.py

#
# Wichtig:
# export PYTHONPATH="../FLElib"
#

import mysql.connector
import logging, argparse
from dbroutinen import dbcreate
from dbparam import *
from suchen import suchen
from bereinigen import bereinigen

# from logsabrufen import logsAbrufen
# from mountlogs import mountLogs, unmountLogs

TITEL = "Erfassen"
VERSION = "V0"
DESCRIPTION = """Log-Files durchsuchen und Messwerte in eine Datenbank 
schreiben, von wo aus sie sortiert und weiterverarbetet werden können.
Wahlweise DB löschen und neu erfassen oder vorhandene Einträge
mit neuen Daten erweitern
"""


def main(pfad, neu=False, Dbg=False):
    try:
        mydb = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD
        )
        if neu:
            with mydb.cursor() as cursor:
                cursor.execute(f"TRUNCATE TABLE {DBTMW};")
        if pfad is not None:
            suchen(pfad, mydb, Dbg)
        bereinigen(mydb, Dbg)
    except mysql.connector.errors.ProgrammingError as e:
        logging.error(e)
        match e.errno:
            case 1064:
                print("Syntax Error: {}".format(e))
            case 1146:
                dbcreate(mydb, e.msg)
            case _:
                logging.exception(e)
    except Exception as e:
        logging.exception(e)
    finally:
        mydb.close()

    return 0


if __name__ == "__main__":
    import sys

    # LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
    LOG_FORMAT = "%(levelname)s %(message)s"
    parser = argparse.ArgumentParser(prog=TITEL, description=DESCRIPTION)
    parser.add_argument(
        "-v",
        "--verbose",
        dest="pVerbose",
        action="store_true",
        help="Debug-Ausgabe",
    )
    parser.add_argument(
        "-n",
        "--neu",
        dest="pNeu",
        action="store_true",
        help="DB leeren und neu erfassen (sonst nur ergänzen)",
    )
    parser.add_argument(
        "pfad",
        nargs="?",
        default=None,
        help="optional: Pfad - wenn angegeben wird nach Logs durchsucht (sonst nur schon vorhandene Messwerte)",
    )

    arguments = parser.parse_args()
    pfad = arguments.pfad
    Dbg = arguments.pVerbose
    neu = arguments.pNeu
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    sys.exit(main(pfad, neu, Dbg))
