#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys
# is licensed under CC BY-NC-ND 4.0.
#
#  Plot.py

#
# Wichtig:
# export PYTHONPATH="../FLElib"
#

import mysql.connector
import logging, argparse, os
from dbroutinen import dbcreate
from dbparam import *
from auswählen import auswählen

TITEL = "Plot"
VERSION = "V0"
DESCRIPTION = """Messwerte aus CSV-Datei plotten. 
Diese Datei muss vorher aus der Datenbank durch Export erzeugt werden.
"""


def main(pfad, Dbg=False):
    
    try:
        if not os.path.isfile(pfad):
            #Datei fehlt
            mydb = mysql.connector.connect(host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD)
            sql=f"SELECT * from messungen INTO OUTFILE '{pfad}' "\
                "FIELDS TERMINATED BY ';'" \
                "OPTIONALLY ENCLOSED BY '\"';"
            #sql="SELECT * FROM `messungen` ORDER BY `zeitpunkt` ASC"
            logging.debug(sql)
            with mydb.cursor() as cursor:
                cursor.execute(sql)
            mydb.close()
        #jetzt muss die Datei da sein
        if not os.path.isfile(pfad):
            logging.fatal(f"Datei nicht gefunden: {pfad}")
        auswählen(pfad, Dbg)

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

    return 0


if __name__ == "__main__":
    import sys

    global Dbg
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
    parser.add_argument("pfad", default=None, help="Datei mit Pfad, wo Daten liegen")

    arguments = parser.parse_args()
    pfad = arguments.pfad
    Dbg = arguments.pVerbose
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    sys.exit(main(pfad, Dbg))
