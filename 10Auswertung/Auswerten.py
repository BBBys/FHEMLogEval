#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys
# is licensed under CC BY-NC-ND 4.0.
#
#  Auswerten.py

#
# Wichtig:
# export PYTHONPATH="../FLElib"
#

import mysql.connector
import logging, argparse
from dbroutinen import dbcreate
from  dbparam import *
from logsabrufen import logsAbrufen
from mountlogs import mountLogs, unmountLogs

TITEL = "Auswerten"
VERSION = "V0"
VERARBEITEN = "verarbeiten!"
DESCRIPTION = """Log-Files, die in der Datenbank stehen, \n
grob auswerten und die wichtigsten Eigenschaften abspeichern
"""

def main(keep=False, Dbg=False):
    logPath = mountLogs()
    if logPath is None:
        logging.error("Logs konnten nicht eingebunden werden")
        return "Fehler"
    try:
        mydb = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, 
            password=DBPWD
        )  # + ";ConvertZeroDateTime=True;",
        logsAbrufen(mydb, logPath, Dbg)
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

    if not keep:
        unmountLogs(logPath)

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
        "-k",
        "--keep",
        dest="pKeep",
        action="store_true",
        help="Logfiles behalten (kein Un-Mount nach Verarbeitung)",
    )

    arguments = parser.parse_args()
    keep = arguments.pKeep
    Dbg = arguments.pVerbose
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    sys.exit(main(keep, Dbg))
