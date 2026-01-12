#
# Wichtig:
# export PYTHONPATH="../FLElib"
#
from DatenAusDB import DatenAusDB
import mysql.connector
import logging, argparse
from dbroutinen import dbcreate
from dbparam import DBHOST, DBNAME, DBPORT, DBPWD, DBUSER
from Auswerten import auswerten
from Statistik import statistik
from Übersicht import übersicht

TITEL = "Plot"
VERSION = "V1.0"
DESCRIPTION = """Messwerte aus der Datenbank holen und darstellen."""


def main(übers=False, stat=False, plot=False, Dbg=False):
    try:
        mydb = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD
        )
        # Übersicht angefordert
        if übers:
            übersicht(mydb)
            return

        df = DatenAusDB(mydb)
        mydb.close()

        if stat:
            statistik(df)

        if plot:
            auswerten(df, Dbg)

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
        "-z",
        "--zeichne",
        dest="pPlot",
        action="store_true",
        help="zeichne Daten (Wert über Zeit)",
    )
    parser.add_argument(
        "-s",
        "--statistik",
        dest="pStatistik",
        action="store_true",
        help="gib Überblick über Daten (Verteilung, ...)",
    )

    arguments = parser.parse_args()
    Übersicht = arguments.pÜbersicht
    Dbg = arguments.pVerbose
    Plot = arguments.pPlot
    Statistik = arguments.pStatistik
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    sys.exit(main(Übersicht, Statistik, Plot, Dbg))
