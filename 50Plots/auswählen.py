import logging
import matplotlib.pyplot as plt
import pandas as pd


def auswählen(datei, Dbg=False):
    sensors = ["TGarten"]
    convert_dict = {"zeitpunkt": "datetime64[ns]", "messwert": float}

    logging.info(f"Lese Daten aus {datei}")

    df: pd.DataFrame = pd.read_csv(datei, sep=";", usecols=[0, 1, 2], parse_dates=[0])
    if Dbg or True:
        print(df.info())
        print(df.head())
        print(df.tail())
        print(df.index)
        print(type(df.index))
    df.columns = ["zeitpunkt", "messpunkt", "messwert"]
    print("Vorher:", df["zeitpunkt"].dtype)
    df = df.astype(convert_dict, errors="ignore")
    df["zeitpunkt"] = pd.to_datetime(df["zeitpunkt"], format="mixed")
    print("Nachher:", df["zeitpunkt"].dtype)
    # df.set_index(["messpunkt", "zeitpunkt"])  # MultiIndex: (name, Zeit)
    # df=df.set_index(["zeitpunkt"])
    df = df.set_index("zeitpunkt")
    print("Index-Typ:", type(df.index))

    if Dbg or True:
        print(df.info())
        print(df.head())
        print(df.tail())
        print(df.index)
        print(type(df.index))

    dfresa = df.resample("30min").asfreq()  # 10-Minuten-Raster auf Zeit-Ebene
    if Dbg or True:
        print(dfresa.info())
        print(dfresa.head())
        print(dfresa.tail())
    dfinterp = dfresa.interpolate(
        method="time"
    )  # , limit_direction="both")  # Werte interpolieren
    if Dbg or True:
        print(dfinterp.info())
        print(dfinterp.head())
        print(dfinterp.tail())
    # df = dftemp.sort_values(["messpunkt", "zeitpunkt"]).copy()
    # df_pivot = y.pivot(index='zeitpunkt', columns='messpunkt', values='messgröße')
    # if Dbg:        print(df_pivot.head(55))

    # Plotten
    logging.basicConfig(level=logging.info)
    dfinterp.plot(figsize=(10, 6))
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
