from DatenAusDB import DatenAusDB
import mysql.connector
import logging, argparse
from dbroutinen import dbcreate
from dbparam import DBHOST, DBNAME, DBPORT, DBPWD, DBTMW, DBUSER


def übersicht(mydb):
    logging.info("Übersicht angefordert...")
    with mydb.cursor(dictionary=True) as cursor:
        sql = f"SELECT messgröße FROM  {DBTMW} GROUP BY messgröße"
        cursor.execute(sql)
        messungen = cursor.fetchall()
        print("----------\nMessgrößen:\n")
        for messung in messungen:
            print(messung["messgröße"])
        sql = f"SELECT messpunkt FROM  {DBTMW} GROUP BY messpunkt"
        cursor.execute(sql)
        messungen = cursor.fetchall()
        print("-----------\n\nMesspunkte:\n")
        for messung in messungen:
            print(messung["messpunkt"])
    logging.info("...Abfrage beendet")
