import logging
import matplotlib.pyplot as plt
import pandas as pd


def auswählen(datei, Dbg=False):
    sensors = ["T_Garten"]
    convert_dict = {"messwert": float}

    logging.info(f"Lese Daten aus {datei}")

    df: pd.DataFrame = pd.read_csv(
        datei, sep=";", usecols=[1, 2, 3, 4], parse_dates=["zeitpunkt"]
    )
    dftemp: pd.DataFrame = df.query(" messgröße == 'temperature'")
    # dftemp: pd.DataFrame = df.query("messpunkt == 'T_Garten' and messgröße == 'temperature'")
    dftemp = dftemp.astype(convert_dict, errors="ignore")
    dftemp = dftemp.drop(columns=["messgröße"])
    #Sortieren nach name und Zeit
    df = dftemp.sort_values(["messpunkt", "zeitpunkt"]).copy()
   
    if Dbg:
        print(df.head())
        print(df.tail())
        print(df.info())

    #MultiIndex setzen und resamplen
    result = (
        df.set_index(["messpunkt", "zeitpunkt"])    # MultiIndex: (name, Zeit)
        #df.set_index(["zeitpunkt"])    # MultiIndex: (name, Zeit)
        .resample("10min", level="zeitpunkt") # 10-Minuten-Raster auf Zeit-Ebene
        .interpolate(method="linear", limit_direction="both") # Werte interpolieren
        .reset_index() # Index zurück in Spalten
        .loc[:, ["zeitpunkt", "messpunkt", "messwert"]] # Spaltenordnung
    )
    if Dbg:
        print(result.head())
        print(result.tail())
        print(result.info())

    
    # df_pivot = y.pivot(index='zeitpunkt', columns='messpunkt', values='messgröße')
    # if Dbg:        print(df_pivot.head(55))

    # Plotten
    result.plot(figsize=(10, 6))
    plt.xlabel("Zeit")
    plt.ylabel("Messwert")
    plt.title("Messwerte über Zeit pro Messstelle")
    plt.legend(title="Messstelle")
    plt.show()

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
