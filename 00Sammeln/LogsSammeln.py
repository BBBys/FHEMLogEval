#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys
# is licensed under CC BY-NC-ND 4.0.
#
#  LogsSammeln.py

import mysql.connector
import logging, argparse
from dbroutinen import dbcreate
from dbparam import *
from logseintragen import logsEintragen
from mountlogs import mountLogs, unmountLogs

TITEL = "LogsSammeln"
VERSION = "V0"
VERARBEITEN = "verarbeiten!"
DESCRIPTION = """Log-Files suchen und Auftrag zur Auswertung 
in DB schreiben. Mount mit\n
sudo mount.cifs //192.168.1.2/fhemlogs ~/Entwicklung/FHlogs/logs
"""


def EinträgeWiederherstellen(db):
    """stellt fehlende Aufträge wieder her

    Raises:
        Exception: endet immer mit Exception
    """
    logging.debug("kein Startrecord gefunden")
    logging.debug("Einträge wiederherstellen")
    with db.cursor() as cursor:
        SQL = f"insert into {DBTBB} (programm) values ('{TITEL}')"
        cursor.execute(SQL)
    db.commit()
    raise Exception(
        "Tabelle %s Einträge %s erzeugt - Neustart notwendig" % (DBTBB, TITEL)
    )
    # endet hier


def main(keep=False, Dbg=False):
    logPath = mountLogs()
    if logPath is None:
        logging.error("Logs konnten nicht eingebunden werden")
        return "Fehler"
    try:
        mydb = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD
        )  # + ";ConvertZeroDateTime=True;",
        # if ZURÜCK:
        #    logging.info("Zurücksetzen")
        #    zurücksetzenBilder(TITEL, mydb)
        #    logging.info("...zurückgesetzt, Ende")
        #    return 0
        logsEintragen(mydb, logPath, Dbg)
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
    # parser.add_argument(
    #    "pfad",
    #    nargs="?",
    #    default=VERARBEITEN,
    #    help="optional: Pfad\n"
    #    "- wenn angegeben: Pfad wird nach Logs durchsucht und Dateien "
    #    "werden in Auftrags-DB geschrieben.\n"
    #    "- wenn nicht angegeben: Aufträge werden ausgeführt.",
    # )

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
    # parser.add_argument(
    #    "-z",
    #    "--zurücksetzen",
    #    dest="pZurck",
    #    action="store_true",
    #    help="alle Einträge der Bilder-Sammlung löschen",
    # )
    arguments = parser.parse_args()
    # pfad = arguments.pfad
    # ZURÜCK = arguments.pZurck
    keep = arguments.pKeep
    Dbg = arguments.pVerbose
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    sys.exit(main(keep, Dbg))
