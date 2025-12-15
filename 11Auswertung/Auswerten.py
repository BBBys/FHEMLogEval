#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys
# is licensed under CC BY-NC-ND 4.0.
#
#  Auswerten.py
# >>> hier ohne Datenbank! <<<

#
# Wichtig:
# export PYTHONPATH="../FLElib"
#

# import mysql.connector
import logging, argparse

# from dbroutinen import dbcreate
# from dbparam import *
from logsabrufen1 import logsAbrufen1
from mountlogs import mountLogs, unmountLogs

TITEL = "Auswerten"
VERSION = "V1"
VERARBEITEN = "verarbeiten!"
DESCRIPTION = """Log-Files, die im angegebenen Verzeichnis liegen 
grob auswerten zu jedem eine Übersicht ausgeben.
Falls im angegebenen Verzeichnis nicht die FHEM-Logfiles liegen,
was an der Datei fhem.save erkannt wird,
wird dieses Verzeichnis vom FHEM-Server gemounted.

Ausgegeben wird
- Zeitraum
- Anzahl der Meldungen
- fehlerhafte Meldungen
- Messstellen

"""


def main(pfad, keep=False, interaktiv=False, Dbg=False):
    logPath = mountLogs(pfad)
    if logPath is None:
        logging.error("Logs konnten nicht eingebunden werden")
        return "Fehler"
    logsAbrufen1(logPath, interaktiv, Dbg)
    if not keep:
        unmountLogs(logPath)

    return 0


if __name__ == "__main__":
    import sys

    # LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
    LOG_FORMAT = "%(levelname)s %(message)s"
    parser = argparse.ArgumentParser(prog=TITEL, description=DESCRIPTION)
    parser.add_argument(
        "pfad",
        nargs="?",
        default="/opt/fhem/logs",
        help="optional: Pfad - wird nach Logs durchsucht. [/opt/fhem/logs]",
    )
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
    parser.add_argument(
        "-i",
        "--interaktiv",
        dest="Interaktiv",
        action="store_true",
        help="interaktiv: Abbrechen, wenn Eingriff erforderlich",
    )

    arguments = parser.parse_args()
    keep = arguments.pKeep
    pfad = arguments.pfad
    Dbg = arguments.pVerbose
    interaktiv = arguments.Interaktiv
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    sys.exit(main(pfad, keep, interaktiv, Dbg))
