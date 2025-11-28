from dbparam import DBTLOGS
import logging
from os import path
from datetime import datetime
from string import Template

# Typ 2: abwechselnd
# 0                   1       2             3    4 5
# 2025-11-22_17:26:15 T_EG_Wz rel_humidity: 45   %
# 2025-11-22_17:26:15 T_EG_Wz temperature:  22.0 C (measured)

aus = Template(
    """---------------------------------
      Datei $name
      $nm Meldungen mit $nf Fehlern
      Durchschnittlich $pro pro Stunde, $pro2 pro Minute
      über $dauer
      von $von bis $bis"""
)


def ignorieren(zeile):
    if zeile.find("Wetterdaten") == 0:
        return False

    # Wetterdaten Fehlermeldungen ignorieren
    if zeile.find("sys.exit(") >= 0:
        return True
    if zeile.find("Traceback") >= 0:
        return True
    if zeile.find(", in <module") >= 0:
        return True
    if zeile.find("CRITICAL") >= 0:
        return True
    if zeile.find(" Version") >= 0:
        return True
    if zeile.find(" OK") >= 0:
        return True
    if zeile.find(", in main") >= 0:
        return True
    if zeile.find(" Meldung") >= 0:
        return True
    if zeile.find("Exception") >= 0:
        return True
    if zeile.find("at Borys.Wetter.WetterLaden.") >= 0:
        return True

    return False

def zeileAuswertbar(zeile, typ):
    Fehler=False

    teile = zeile.split()
    datstr = teile[0]
    lds = len(datstr)
    if lds != 19:
        # vielleicht gestörte Zeile bei Restart
        if lds > 30:return Fehler
        logging.warning(f"daten: Zeile {zeile} Datum unbrauchbar")
        return Fehler
    if typ == 1:
        l = len(teile)
        if l < 4 or l > 5:
            # Sonderfall Wetterdaten:
            # 2025-10-10_14:43:01 Wetterdaten Errors
            if l == 3 and teile[1] == "Wetterdaten":return Fehler
            logging.warning(f"daten: Zeile {zeile} unbrauchbar")
            return Fehler
    elif typ == 2:
        l = len(teile)
        if l < 5 or l > 6:
            logging.warning(f"daten: Zeile {zeile} l={l} unbrauchbar")
            return Fehler
    else:
        logging.error(f"daten: Unbekannter Log-Typ {typ} in Zeile {zeile}")
        return Fehler

    return True

def datenAuswerten(pfad, typ):
    musterDatum = "%Y-%m-%d_%H:%M:%S"
    erste = datetime.strptime("2099-12-31_0:0:0", musterDatum)
    letzte = datetime.strptime("1900-12-31_0:0:0", musterDatum)

    with open(pfad, "r") as f:
        nZeilen = 0
        nFehler = 0
        for zeile in f.readlines():
            # Wetterdaten-Meldungen ignorieren
            if ignorieren(zeile):
                continue
            nZeilen += 1
            if not zeileAuswertbar(zeile, typ):
                nFehler += 1
                continue
            teile = zeile.split()
            datstr = teile[0]
            zeit = datetime.strptime(datstr, musterDatum)
            if zeit < erste:
                erste = zeit
            if zeit > letzte:
                letzte = zeit
    # logging.debug(f"Zeit: {erste}...{letzte}")
    return (erste, letzte, nZeilen, nFehler)


# eine einzelne Logfile auswerten,
# Ergebnis anzeigen und in DB speichern
# return False, wenn es nicht weitergehen kann
def logAuswerten(db, datei, Dbg=False):
    name = datei["dateiname"]
    typ = datei["typ"]
    pfad = datei["pfad"]
    # logging.debug(f"logAuswerten: {name}")
    if not path.exists(pfad):
        logging.warning(f"logAuswerten: Datei {name} existiert nicht mehr")
        return True

    (von, bis, nZeilen, nFehler) = datenAuswerten(pfad, typ)
    with db.cursor(buffered=True) as cursor:
        sql = f"update {DBTLOGS} set erste='{von}', letzte='{bis}', zeilen='{nZeilen}' where dateiname='{name}'"
        # logging.debug(sql)
        cursor.execute(sql)
    db.commit()

    alterTage = (datetime.now() - bis).total_seconds() / 86400
    dauer = bis - von
    dauerTage = dauer.total_seconds() / 86400
    proStunde = nZeilen / dauer.total_seconds() * 3600
    proMinute = nZeilen / dauer.total_seconds() * 60

    if nZeilen <3:
        print("---------------------------------")
        print(f"      {name}\n***** leeres oder fast leeres Log")
        if alterTage > 7:
            print(f"      welches nicht mehr beschrieben wird: Alter {alterTage:.0f} Tage")
        print("---------------------------------")
        return True

    print(
        aus.substitute(
            name=name,
            dauer=dauer,
            pro=f"{proStunde:.1f}",
            pro2=f"{proMinute:.1f}",
            nf=nFehler,
            nm=nZeilen,
            von=von,
            bis=bis,
        )
    )
    # Anmerkungen
    if name.startswith("autocreated-"):
        print("!>>>> Auto-created Logfile")
    if name.find("CUL_TX") >= 0:
        print("!>>>> kein Name vergeben (CUL_TX)")
    # Plausibilitätsprüfungen
    if dauerTage < 7:
        print("***** kürzer als eine Woche")
    if dauerTage > 35:
        print("***** länger als ein Monat")
    if proStunde > 18:
        print("***** Meldunggen zu dicht")
    if proStunde < 5:
        print("***** Meldunggen zu selten")
    if alterTage > 7:
        print(f"***** altes Log: {alterTage:.1f} Tage")
    if nFehler > 0:
        print(f"***** Fehler im Log {nFehler/nZeilen*100:.1f} %")

    return nFehler < 6
