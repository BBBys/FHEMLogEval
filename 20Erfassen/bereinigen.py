import logging
from dbparam import DBTMW


def bereinigen(mydb, Dbg=False):
    """Bereinigen der Datenbank von doppelten Einträgen

    Args:
        mydb: MySQL Verbindung
        Dbg (bool, optional): Debugmodus. Defaults to False.
    """
    logging.info("Starte Bereinigung der Datenbank...")
    with mydb.cursor(dictionary=True) as cursor:
        sql = f"SELECT COUNT(id) AS anzahl FROM {DBTMW};"
        cursor.execute(sql)
        nDaten = cursor.fetchone()["anzahl"]
        logging.info(f"Anzahl Einträge vorher:\t{nDaten}")
        # Beispielbereinigung: Löschen von Einträgen mit ungültigen Werten
        sql = f"DELETE FROM {DBTMW} WHERE messwert IS NULL OR messwert = '';"
        cursor.execute(sql)
        logging.debug("T in temparatur ändern...")
        sql = f"UPDATE {DBTMW} SET messgröße = 'temperature' where messgröße = 'T' ;"
        cursor.execute(sql)
        logging.debug("Duplikate suchen und entfernen...")
        sql = f"SELECT id,zeitpunkt,messpunkt,messgröße,messwert FROM {DBTMW} ORDER BY zeitpunkt,messpunkt,messgröße,messwert ;"
        cursor.execute(sql)
        messungen = cursor.fetchall()
        for i in range(1, len(messungen)):
            prev = messungen[i - 1]
            curr = messungen[i]
            if (
                prev["zeitpunkt"] == curr["zeitpunkt"]
                and prev["messpunkt"] == curr["messpunkt"]
                and prev["messgröße"] == curr["messgröße"]
                and prev["messwert"] == curr["messwert"]
            ):
                sql_del = f"DELETE FROM {DBTMW} WHERE id = %s;"
                cursor.execute(sql_del, (curr["id"],))
        sql = f"SELECT COUNT(id) AS anzahl FROM {DBTMW};"
        cursor.execute(sql)
        nDaten = cursor.fetchone()["anzahl"]
        logging.info(f"Anzahl Einträge nachher:\t{nDaten}")
        mydb.commit()
    logging.info("Datenbankbereinigung abgeschlossen.")
