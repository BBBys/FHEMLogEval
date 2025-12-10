import logging
#import pprint as pp
import pandas as pd


def auswählen(datei, Dbg=False):
    sensors = [
        "EG_Wohn",
        "EG_Kueche",
        "OG_Schlaf",
        "DG_Studio",
        "Keller",
        "Strasse",
        "Garten",
    ]
    logging.info(f"Lese Daten aus Datei: {datei}")
    df = (
        pd.read_csv(datei, sep=";",
                    usecols=[1,2,3,4],
                    parse_dates=["zeitpunkt"])
        .set_index("zeitpunkt")
        )
    if Dbg:print(df.head(33))

    return


    df = (
        pd.read_csv(datei, sep=";",
                    usecols=[1,2,3,4],
                    parse_dates=["zeitpunkt"])
        .set_index("zeitpunkt")
        .resample("5min")
        .mean(numeric_only=True)
        .interpolate()
    )
    if Dbg:print(df.head(15))
