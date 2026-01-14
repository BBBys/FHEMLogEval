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
>>>   Datei $name
      $nm Meldungen mit $nf Fehlern
      Durchschnittlich $pro pro Stunde, $pro2 pro Minute
      über $dauer
      von $von bis $bis
      enthält $npunkte Messpunkte
      und $nwerte Messwerte $altwarn
      -------------------------------
     gemessen wird"""
)


def mpwsplit(mpw):
    teile = mpw.split("+")
    return (teile[0], teile[1])


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


def zeileAuswertbar1(zeile):
    Fehler = False

    teile = zeile.split()
    datstr = teile[0]
    lds = len(datstr)
    if lds != 19:
        # vielleicht gestörte Zeile bei Restart
        if lds > 30:
            return Fehler
        logging.warning(f"daten: Zeile {zeile} Datum unbrauchbar")
        return Fehler

    l = len(teile)
    if l < 4 or l > 6:
        # Sonderfall Wetterdaten:
        # 2025-10-10_14:43:01 Wetterdaten Errors
        if l == 3 and teile[1] == "Wetterdaten":
            return Fehler
        logging.warning(f"daten: Zeile {zeile} l={l} unbrauchbar")
        return Fehler

    return True


def datenAuswerten1(name, pfad):
    # Muster Zeile:
    # 2025-11-30_17:44:03 T_DG batteryPercent: 90
    # 0                   1    2               3

    musterDatum = "%Y-%m-%d_%H:%M:%S"
    # 1. Zeitabdeckung, Messpunkte
    erste = datetime.strptime("2099-12-31_0:0:0", musterDatum)
    letzte = datetime.strptime("1900-12-31_0:0:0", musterDatum)
    messStellen = set()
    # 2. Messwerte je Messpunkt
    werteMitStellen = set()
    WerteStellenAnzahl = dict()
    with open(pfad, "r") as f:
        zeilen = f.readlines()
    nZeilen = 0
    nFehler = 0
    for zeile in zeilen:
        # Wetterdaten-Meldungen ignorieren
        if ignorieren(zeile):
            continue
        nZeilen += 1
        if not zeileAuswertbar1(zeile):
            nFehler += 1
            continue
        teile = zeile.split()
        # Messwerte enden immer mit >:<
        dieserMessWert = teile[2]
        if dieserMessWert.endswith(":"):
            dieserMessWert = dieserMessWert[:-1]
        else:
            # dann ist es kein Messwert
            continue
        einZeitpunkt = teile[0]
        eineMessStelle = teile[1]
        zeit = datetime.strptime(einZeitpunkt, musterDatum)
        if zeit < erste:
            erste = zeit
        if zeit > letzte:
            letzte = zeit
        messStellen.add(eineMessStelle)
        # Zähle Vorkommen eines Messwertes
        ws_key = f"{eineMessStelle}+{dieserMessWert}"
        werteMitStellen.add(ws_key)
        if ws_key in WerteStellenAnzahl:
            WerteStellenAnzahl[ws_key] += 1
        else:
            WerteStellenAnzahl[ws_key] = 1
    # logging.debug(f"Zeit: {erste}...{letzte}")
    logging.debug(f"Messpunkte: {messStellen}")
    logging.debug(f"Messwerte: {werteMitStellen}")

    # erwartet:
    # (von, bis, nZeilen, alleMessStellen, alleWerteMitStellen, nFehler)
    return (erste, letzte, nZeilen, messStellen, WerteStellenAnzahl, nFehler)


# eine einzelne Logfile auswerten,
# Ergebnis anzeigen und in DB speichern
# return False, wenn es nicht weitergehen kann
def logAuswerten1(name, dateiMitPfad, Dbg=False):
    if not path.exists(dateiMitPfad):
        logging.error(f"logAuswerten: Datei {dateiMitPfad} existiert nicht mehr")
        return True, 0
    # auswerten
    (von, bis, nZeilen, alleMessStellen, alleWerteMitStellen, nFehler) = (
        datenAuswerten1(name, dateiMitPfad)
    )
    # wie alt ist letzter Eintrag ?
    letzterSek = (datetime.now() - bis).total_seconds()
    letzterStunden: float = letzterSek / 3600
    letzterTage: float = letzterSek / 86400
    dauer = bis - von
    # ZeroDivisionError verhindern
    dts = max(dauer.total_seconds(), 1)
    dauerTage: float = dts / 86400
    proStunde: float = nZeilen / dts * 3600
    proMinute: float = nZeilen / dts * 60
    lmp = len(alleMessStellen)
    lmw = len(alleWerteMitStellen)

    if nZeilen < 3:
        print("---------------------------------")
        print(f"      {name}\n***** leeres oder fast leeres Log")
        if letzterTage > 7:
            print(
                f"      welches nicht mehr beschrieben wird: Alter {letzterTage:.0f} Tage"
            )
        print("---------------------------------")
        return True, 0

    if letzterStunden > 6:
        altwarn = f"\n      {letzterStunden:.1f} Stunden alt"
    else:
        altwarn = ""
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
            npunkte=lmp,
            nwerte=lmw,
            altwarn=altwarn,
        )
    )
    for mstelle in alleMessStellen:
        print(f"  ❯\t{mstelle}")
        for mwertstelle in alleWerteMitStellen.keys():
            (diesestelle, dieserwert) = mpwsplit(mwertstelle)
            if diesestelle == mstelle:
                n = alleWerteMitStellen[mwertstelle]
                print(f"\t» {n}\t{dieserwert} ")
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
    if proStunde / lmw > 10:
        print("***** Meldunggen zu dicht")
    if proStunde < 5:
        print("***** Meldunggen zu selten")
    if lmp > 1:
        print("***** mehr als 1 Messstelle")
    if lmw > 3:
        print("***** viele Messwerte")
    if letzterTage > 7:
        print(f"***** altes Log: {letzterTage:.1f} Tage alt")
    elif letzterStunden > 6:
        print(f"***** nicht aktuell: {letzterStunden:.1f} Stunden alt")
    if nFehler > 0:
        print(f"***** Fehler im Log {nFehler/nZeilen*100:.1f} %")

    return (nFehler < 6), nZeilen
