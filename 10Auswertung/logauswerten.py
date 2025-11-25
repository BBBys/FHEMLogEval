from dbparam import DBTLOGS
import logging
from datetime import datetime

# Typ 2: abwechselnd
# 0                   1       2             3    4 5
# 2025-11-22_17:26:15 T_EG_Wz rel_humidity: 45   %
# 2025-11-22_17:26:15 T_EG_Wz temperature:  22.0 C (measured)

def daten(pfad,typ):
    muster="%Y-%m-%d_%H:%M:%S"
    erste=datetime.strptime("2099-12-31_0:0:0", muster)
    letzte=datetime.strptime("1900-12-31_0:0:0", muster)
    
    with open(pfad, "r") as f:
        nzeilen=0
        for zeile in f.readlines():
            nzeilen+=1
            teile = zeile.split()
            datstr = teile[0]
            if typ==1:
                datstr = teile[0]
                l= len(teile)
                if l< 4 or l>5:
                    logging.warning(f"daten: Zeile {zeile} unbrauchbar")
                    continue
                if len(datstr)!=19:
                    logging.warning(f"daten: Zeile {zeile} unbrauchbar")
                    continue
            elif typ==2:
                l= len(teile)
                if l<5 or l>6   :
                    logging.warning(f"daten: Zeile {zeile} l={l} unbrauchbar")
                    continue
                if len(datstr)!=19:
                    logging.warning(f"daten: Zeile {zeile} unbrauchbar")
                    continue
            else:
                logging.error(f"daten: Unbekannter Log-Typ {typ} in Zeile {zeile}")
                return (0,0,0)
                
            zeit=datetime.strptime(datstr, muster)
            if zeit < erste:
                erste=zeit
            if zeit > letzte:
                letzte=zeit
    logging.debug(f"Zeit: {erste}...{letzte}")
    return (erste, letzte,nzeilen  )

def logAuswerten(db, datei):
    name =datei['dateiname']
    typ =datei['typ']
    pfad =datei['pfad']
    logging.debug(f"logAuswerten: {name}")
    (von,bis,nzeilen)=daten(pfad,typ)
    with db.cursor( buffered=True) as cursor:
            sql = f"update {DBTLOGS} set erste='{von}', letzte='{bis}', zeilen='{nzeilen}' where dateiname='{name}'"
            logging.debug(sql)
            cursor.execute(sql)

    return True
