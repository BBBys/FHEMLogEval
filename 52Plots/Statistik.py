from string import Template
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging

aus = Template(
    """---------------------------------
>>> Daten $name Übersicht:

Anfang
$anf

Ende
$end

Beschreibung
$des

Quantile
$qua
-------------------------------"""
)


def datenInfo(daten, name):
    quants = daten[name].quantile([0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99])
    print(
        aus.substitute(
            name=name,
            anf=daten.head(),
            end=daten.tail(),
            des=daten.describe(),
            qua=quants,
        )
    )
    return


def statistik(df):
    BINS = 50
    print("\nStatistik-Auswertung...")
    datenInfo(df, "messwert")

    sns.set_style("whitegrid")
    fig, ax = plt.subplots()
    df["messwert"].hist(ax=ax, bins=BINS)
    ax.set_yscale("log")
    ax.tick_params(labelsize=14)
    ax.set_xlabel("Messwert", fontsize=14)
    ax.set_ylabel("Anzahl", fontsize=14)
    plt.show()

    fig, ax = plt.subplots()
    df["messwert"].hist(ax=ax, bins=BINS)
    # for pos in quantile:
    #    handle = plt.axvline(pos, color="r")
    # ax.legend([handle], ["deciles"], fontsize=14)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.tick_params(labelsize=14)
    ax.set_xlabel("Messwert", fontsize=14)
    ax.set_ylabel("Anzahl", fontsize=14)
    plt.show()

    if df["messwert"].min() < 0.001:
        logging.warning("Messwert zu klein für Log-Darstellung")
        return

    log_review_count = np.log10(df["messwert"] + 1)

    plt.figure()
    ax = plt.subplot(2, 1, 1)
    df["messwert"].hist(ax=ax, bins=BINS)
    ax.tick_params(labelsize=14)
    # ax.set_xlabel("Messwert", fontsize=14)
    # ax.set_ylabel("Occurrence", fontsize=14)

    ax = plt.subplot(2, 1, 2)
    log_review_count.hist(ax=ax, bins=BINS)
    ax.tick_params(labelsize=14)
    ax.set_xlabel("log10(Messwert))", fontsize=14)
    ax.set_ylabel("Occurrence", fontsize=14)
    plt.show()

    return
