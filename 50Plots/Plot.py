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
from subprocess import call

TITEL = "Plot"
VERSION = "V0"
DESCRIPTION = """Messwerte aus CSV-Datei plotten. 
Diese Datei wird vorher aus der Datenbank durch Export erzeugt.
"""


def main(pfad, neu=False, übers=False, Dbg=False):
    MINSIZE = 100

    try:
        fehlt = not os.path.isfile(pfad)
        # in der Datei sollte auch was drin sein
        if not fehlt:
            sz = os.path.getsize(pfad)
            logging.debug(f"Filesize={sz}")
            if sz < MINSIZE or neu:
                rc = call(f"sudo rm {pfad}", shell=True)
                assert rc == 0
                fehlt = True

        if übers or fehlt:
            mydb = mysql.connector.connect(
                host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD
            )
            # Übersicht angefordert
            if übers:
                logging.info("Übersicht angefordert...")
                with mydb.cursor(dictionary=True) as cursor:
                    sql = f"SELECT messgröße FROM  {DBTMW} GROUP BY messgröße"
                    cursor.execute(sql)
                    messungen = cursor.fetchall()
                    print("----------\n\nMessungen:\n")
                    for messung in messungen:
                        print(messung["messgröße"])
                    sql = f"SELECT messpunkt FROM  {DBTMW} GROUP BY messpunkt"
                    cursor.execute(sql)
                    messungen = cursor.fetchall()
                    print("-----------\n\nMesspunkte:\n")
                    for messung in messungen:
                        print(messung["messpunkt"])
                logging.info("...Abfrage beendet")
                return

            if fehlt:
                # wenn Datei fehlt
                sql = f"""SELECT * from messungen   
                    WHERE 'messpunkt' = 'TGarten'
                    INTO OUTFILE '{pfad}'
                    FIELDS TERMINATED BY ';'
                    OPTIONALLY ENCLOSED BY '\"';"""
                # sql = f"""SELECT zeitpunkt,messpunkt,messgröße,messwert from messungen
                sql = f"""SELECT zeitpunkt,messpunkt,messwert from messungen
                    WHERE 
                        (STRCMP(messpunkt,'TGarten') =0 
                        or 
                        STRCMP(messpunkt,'Lufttemperatur') =0)
                    INTO OUTFILE '{pfad}'
                    FIELDS TERMINATED BY ';'
                    OPTIONALLY ENCLOSED BY '\"';"""
                logging.debug(sql)
                with mydb.cursor() as cursor:
                    cursor.execute(sql)  # result ist immer None

                sz = os.path.getsize(pfad)
                logging.debug(f"Filesize neu={sz}")

            mydb.close()

        # jetzt muss die Datei da sein
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
    LOG_FORMAT = "%(levelname)s: %(message)s"
    parser = argparse.ArgumentParser(prog=TITEL, description=DESCRIPTION)
    parser.add_argument(
        "-v",
        "--verbose",
        dest="pVerbose",
        action="store_true",
        help="Debug-Ausgabe",
    )
    parser.add_argument(
        "-ü",
        "--übersicht",
        dest="pÜbersicht",
        action="store_true",
        help="schreibe Übersicht über Datenbank-Inhalt",
    )
    parser.add_argument(
        "-n",
        "--neu",
        dest="pNeu",
        action="store_true",
        help="lösche Datei und schreibe Datenbank-Inhalt erneut aus",
    )
    parser.add_argument(
        "pfad", default=None, help="Datei mit Pfad, wo Daten liegen [sollen]"
    )

    arguments = parser.parse_args()
    pfad = arguments.pfad
    Übersicht = arguments.pÜbersicht
    Neu = arguments.pNeu
    Dbg = arguments.pVerbose
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    sys.exit(main(pfad, Neu, Übersicht, Dbg))
