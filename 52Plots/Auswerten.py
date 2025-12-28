#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FHEM Logs Evaluator  © 2025 by Dr. Burkhard Borys
# is licensed under CC BY-NC-ND 4.0.
#
#  auswählen.py

import logging
import matplotlib.pyplot as plt
import pandas as pd


def auswerten(df: pd.DataFrame, Dbg=False):
    sensors = ["TGarten"]
    anzahl = len(df)
    logging.info(f"Datensätze: {anzahl}")
    if anzahl < 2:
        logging.fatal("Nicht genügend Datensätze für Auswertung vorhanden.")
        return
    if Dbg:
        print(df.info())
        print(df.head())
        print(df.tail())
        print(df.index)
        print(type(df.index))
    dfresa = df.resample("10min").mean()  # 10-Minuten-Raster auf Zeit-Ebene
    if Dbg:
        print(dfresa.info())
        print(dfresa.head())
        print(dfresa.tail())

    dfinterp = dfresa.interpolate(method="time", limit_direction="both")
    if Dbg:
        print(dfinterp.info())
        print(dfinterp.head())
        print(dfinterp.tail())

    # Plotten
    logging.basicConfig(level=logging.CRITICAL)
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
