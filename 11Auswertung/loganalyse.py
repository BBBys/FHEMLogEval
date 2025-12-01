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
            # untersucht wird die 2. ZEILE
            if lnr < 2:
                continue
            if lnr > 2:
                break
            if line.find("CUL_HOERM") > 0:
                return 99
            # mögliche Form:
            # Format 1: 2024-06-01_12:00:00 Messpunkt Größe: Wert
            #           0                   1         2      3
            # Format 2: 2025-11-22_17:46:16 Messpunkt Größe: Wert C (measured)
            # oder:     2025-11-22_18:01:15 Messpunkt Größe: Wert %
            #           0                   1         2      3    4       5

            teile = line.strip().split(" ")
            spalten = len(teile)
            fmt1 = fmt2 = False
            match spalten:
                case 4:
                    fmt1 = True
                    fmt1 = fmt1 and istDatum(teile[0])
                    assert fmt1
                    fmt1 = fmt1 and teile[2].endswith(":")
                    assert fmt1
                    fmt1 = fmt1 and istWert(teile[3])
                    assert fmt1
                case 5 | 6:
                    fmt2 = True
                    fmt2 = fmt2 and istDatum(teile[0])
                    assert fmt2
                    fmt2 = fmt2 and teile[2].endswith(":")
                    assert fmt2
                    fmt2 = fmt2 and istWert(teile[3])
                    assert fmt2
                case _:
                    print(line)
                    return -1

            if fmt1:
                return 1
            if fmt2:
                return 2
    return -1
