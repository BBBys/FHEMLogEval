import logging
from dbparam import DBTMW
from datetime import datetime
from string import Template


def statistik(mydb, Dbg=False):
    """Erstellen von Statistiken aus den Messwerten in der Datenbank

    Args:
        mydb: MySQL Verbindung
        Dbg (bool, optional): Debugmodus. Defaults to False.
    """
    aus = Template(
        """----- Statistik -----
Erfasst wurden $nwerte Messwerte
im Zeitraum $von bis $bis 
($dauer Tage)
also $mpt Messwerte pro Tag.
"""
    )

    logging.info("Starte Statistikberechnung...")
    with mydb.cursor(dictionary=True) as cursor:
        sql = f"SELECT COUNT(id) AS anzahl FROM {DBTMW};"
        cursor.execute(sql)
        nWerte = cursor.fetchone()["anzahl"]
        logging.info(f"Anzahl Einträge insgesamt:\t{nWerte}")
        # Beispielstatistik: Durchschnittlicher Messwert pro Messpunkt
        sql = f"SELECT min(zeitpunkt) as von, max(zeitpunkt) as bis FROM {DBTMW} ;"
        cursor.execute(sql)
        erg = cursor.fetchall()[0]
        von = erg["von"]
        bis = erg["bis"]
        dauer = bis - von
        # ZeroDivisionError verhindern
        dts = max(dauer.total_seconds(), 1)
        dauerTage = dts / 86400
        mpt = nWerte / dauerTage

        print(
            aus.substitute(
                nwerte=nWerte,
                bis=bis,
                von=von,
                dauer=f"{dauerTage:.1f}",
                mpt=f"{mpt:.0f}",
            )
        )
        logging.info("Statistikberechnung abgeschlossen.")
