import logging
from dbparam import DBTMW


def verarbeiten(file, db, Dbg=False):
    iz = 0
    with db.cursor() as cursor:
        for zeile in file:
            iz += 1
            if Dbg and iz > 10:
                break
            logging.debug(zeile)
            teile = zeile.split()
            if len(teile) < 3:
                continue
            datum = teile[0]
            messpunkt = teile[1]
            messgröße = teile[2]
            messwert = teile[3]
            sql = f"INSERT INTO {DBTMW} (zeitpunkt, messpunkt, messgröße, messwert) VALUES (%s, %s, %s, %s)"
            logging.debug(sql)
            val = (datum, messpunkt, messgröße, messwert)
            cursor.execute(sql, val)
    db.commit()
    return
