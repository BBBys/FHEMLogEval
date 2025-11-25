from dbparam import DBTLOGS
import sys, os, mysql.connector
import logging
from logauswerten import logAuswerten
from loganalyse import logAnalyse

def logsAbrufen(db, pfad, Dbg=False):
    if not os.path.exists(pfad):
        logging.fatal(f"logsEintragen: Pfad {pfad} existiert nicht.")
        return f"Pfad {pfad} existiert nicht."
    with db.cursor(dictionary=True, buffered=True) as cursor:
        sql = f"select dateiname,pfad,typ from {DBTLOGS} "
        cursor.execute(sql)
        result = cursor.fetchall()
    for datei in result:
        logging.debug(datei)
        OK=logAuswerten(db, datei)
        if OK:db.commit()
    return
