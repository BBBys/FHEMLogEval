from dbparam import DBTLOGS
import os, mysql.connector
import logging
from logauswerten import logAuswerten
from loganalyse import logAnalyse
from fhemnamen import nameReduzieren


def logsEintragen(db, pfad, Dbg=False):
    if not os.path.exists(pfad):
        logging.fatal(f"logsEintragen: Pfad {pfad} existiert nicht.")
        return f"Pfad {pfad} existiert nicht."
    for root, dirs, files in os.walk(pfad):
        # logging.debug("logsEintragen:root %s", root)
        # logging.debug("logsEintragen:dirs= %s", dirs)
        # logging.debug("logsEintragen:files %s", files)
        for file in files:
            if file.endswith("fhem.log"):
                continue
            if file == "fhem.save":
                continue
            if file == "eventTypes.txt":
                continue
            fileMitPfad = os.path.join(root, file)
            if os.path.getsize(fileMitPfad) < 10:
                logging.debug(f"logsEintragen: Datei {file} zu klein, übersprungen")
                continue
            # Datei bekannt?
            basisName = nameReduzieren(file)
            # logfile = {"name": basisName, "path": fileMitPfad}
            with db.cursor() as cursor:
                sql = f"select * from {DBTLOGS} where dateiname='{file}'"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result is None:
                    # Datei noch U. N. B. Kant
                    typ = logAnalyse(fileMitPfad)
                    assert typ is not None
                    if typ == 99:
                        logging.debug(f"{file} übersprungen")
                        continue
                    if typ < 1:
                        raise Exception(f"logsEintragen: Typ {typ} von {file} unbekannt")
                    sql = f"INSERT INTO {DBTLOGS} (basisname,dateiname,pfad,typ) VALUES ('{basisName}','{file}','{fileMitPfad}',{typ})"
                    logging.debug(sql)
                    cursor.execute(sql)
                    db.commit()
                    if Dbg:
                        return
                else:
                    # Datei bekannt
                    pass
        return
        logAuswerten(db, logfile)

        return

    with db.cursor() as cursor:
        # sql = f"INSERT INTO {DBTBB} (programm,parameter) VALUES ('{titel}','{pfad}')"
        # logging.debug(sql)
        # cursor.execute(sql)
        pass
    # db.commit()
    return
