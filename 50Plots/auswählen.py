import logging

# import pprint as pp
import pandas as pd


def auswählen(datei, Dbg=False):
    sensors = ["T_Garten"]
    convert_dict = {"messwert": float}
    logging.info(f"Lese Daten aus Datei: {datei}")

    df: pd.DataFrame = pd.read_csv(
        datei, sep=";", usecols=[1, 2, 3, 4], parse_dates=["zeitpunkt"]
    )
    if Dbg:
        print(df.head(15))
    #T_EG_K";"temperature
    x: pd.DataFrame = df.query("messpunkt == 'T_Garten' and messgröße == 'temperature'")
    if Dbg:        print(x.head(15))
    x = x.drop(columns=["messpunkt", "messgröße"])
    #x = x.drop(columns=["messpunkt"])
    if Dbg:        print(x.head(15))
    if Dbg:        print(x.dtypes)

    x = x.astype(convert_dict, errors="ignore")
    # x[['messwert']] = x[['messwert']].apply(pd.to_numeric)
    if Dbg:        print(x.dtypes)
    if Dbg:        print(x.head(15))

    y = x.set_index(["zeitpunkt"]).resample("10min").mean().interpolate()

    if Dbg:        print(y.head(55))

    """
    x: pd.DataFrame = df.query(
        "messpunkt == 'T_DG' and messgröße == 'rel_humidity'"
        )
    x = x.drop(columns=["messpunkt", "messgröße"])
    if Dbg:print(x.head(33))
    x["messwert"] = pd.to_numeric(x["messwert"])
    y = x.set_index(["zeitpunkt"]).resample("10min").interpolate()
    if Dbg:
        print(y.head(15))
    """
    return
    df = pd.read_csv(
        datei, sep=";", usecols=[1, 2, 3, 4], parse_dates=["zeitpunkt"]
    ).set_index(["zeitpunkt"])
    if Dbg:
        print(df.head(10))

    x = df.query("messpunkt == 'T_Garten' and messgröße == 'temperature'").drop(
        columns=["messpunkt", "messgröße"]
    )
    print(x.head(33))

    # y = x.resample("1min").mean().interpolate()
    y = x.resample("1min").interpolate()

    if Dbg:
        print(y.head(15))
