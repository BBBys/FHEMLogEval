#
# Wichtig:
# export PYTHONPATH="../FLElib"
#
from DatenAusDB import DatenAusDB
import mysql.connector
import logging, argparse
from dbroutinen import dbcreate
from dbparam import DBHOST, DBNAME, DBPORT, DBPWD, DBTMW, DBUSER
from auswerten import auswerten

TITEL = "Plot"
VERSION = "V1.0"
DESCRIPTION = """Messwerte aus der Datenbank holen und darstellen."""


def main(übers=False, Dbg=False):
    try:
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

        df = DatenAusDB(mydb)
        mydb.close()

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

    arguments = parser.parse_args()
    Übersicht = arguments.pÜbersicht
    Dbg = arguments.pVerbose
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    sys.exit(main(Übersicht, Dbg))
