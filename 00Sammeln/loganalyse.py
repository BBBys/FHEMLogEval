def logAnalyse(datei):
    """Analysiere Logdatei und bestimme den Typ"""
    with open(datei, "r") as f:
        for line in f:
            print(line)
            return
