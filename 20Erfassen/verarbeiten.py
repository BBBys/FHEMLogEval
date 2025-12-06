import logging
from dbparam import DBTMW


# eine geöffnete Datei verarbeiten:
# jede Zeile:
#   Datum Messpunkt Messgröße Messwert
#   in DB eintragen
# keine Kontrolle auf Plausibilität oder doppelte Einträge
def verarbeiten(file, db, Dbg=False):
    iz = 0
    with db.cursor() as cursor:
        # alle Zeilen
        for zeile in file:
            iz += 1
            # if Dbg and iz > 10:
            #    break
            # logging.debug(zeile)
            teile = zeile.split()
            if len(teile) < 4:
                logging.warning(f"Zeile {iz} unvollständig: {zeile}")
                continue
            messgröße = teile[2]
            # jede messgröße endet mit >:<
            if messgröße.endswith(":"):
                messgröße = messgröße[:-1]
            else:
                logging.warning(f"Zeile {iz} keine Messgröße: {zeile}")
                continue
            datum = teile[0]
            messpunkt = teile[1]
            messwert = teile[3]
            sql = f"INSERT INTO {DBTMW} (zeitpunkt, messpunkt, messgröße, messwert) VALUES (%s, %s, %s, %s)"
            # logging.debug(sql)
            val = (datum, messpunkt, messgröße, messwert)
            cursor.execute(sql, val)
    db.commit()
    return
