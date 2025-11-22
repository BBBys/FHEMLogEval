from datetime import datetime


def istDatum(param, muster="%Y-%m-%d_%H:%M:%S"):
    try:
        datetime.strptime(param, muster)
        return True
    except ValueError:
        return False


def istWert(param):
    try:
        float(param)
        return True
    except ValueError:
        return False


def logAnalyse(datei):
    """Analysiere Logdatei und bestimme den Typ"""
    with open(datei, "r") as f:
        lnr = 0
        for line in f:
            lnr += 1
            if lnr < 5:
                continue
            if lnr > 5:
                break
            if line.find("CUL_HOERM") > 0:
                return 99
            # mögliche Form:
            # Format1: 2024-06-01_12:00:00 Messstelle Einheit: Wert
            teile = line.strip().split(" ")
            spalten = len(teile)
            match spalten:
                case 4:
                    fmt1 = True
                    fmt1 = fmt1 and istDatum(teile[0])
                    assert fmt1
                    fmt1 = fmt1 and teile[2].endswith(":")
                    assert fmt1
                    fmt1 = fmt1 and istWert(teile[3])
                    assert fmt1
                case _:
                    print(line)
                    return -1

            if fmt1:
                return 1
    return -1
