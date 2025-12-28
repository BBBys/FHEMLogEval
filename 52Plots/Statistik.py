import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def statistik(df):
    deciles = df["messwert"].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    print(deciles)

    sns.set_style("whitegrid")
    fig, ax = plt.subplots()
    df["messwert"].hist(ax=ax, bins=100)
    ax.set_yscale("log")
    ax.tick_params(labelsize=14)
    ax.set_xlabel("Messwert", fontsize=14)
    ax.set_ylabel("Occurrence", fontsize=14)
    plt.show()

    sns.set_style("whitegrid")
    fig, ax = plt.subplots()
    df["messwert"].hist(ax=ax, bins=100)
    for pos in deciles:
        handle = plt.axvline(pos, color="r")
    ax.legend([handle], ["deciles"], fontsize=14)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.tick_params(labelsize=14)
    ax.set_xlabel("Messwert", fontsize=14)
    ax.set_ylabel("Occurrence", fontsize=14)
    plt.show()

    log_review_count = np.log10(df["messwert"] + 1)

    plt.figure()
    ax = plt.subplot(2, 1, 1)
    df["messwert"].hist(ax=ax, bins=100)
    ax.tick_params(labelsize=14)
    ax.set_xlabel("Messwert", fontsize=14)
    ax.set_ylabel("Occurrence", fontsize=14)

    ax = plt.subplot(2, 1, 2)
    log_review_count.hist(ax=ax, bins=100)
    ax.tick_params(labelsize=14)
    ax.set_xlabel("log10(Messwert))", fontsize=14)
    ax.set_ylabel("Occurrence", fontsize=14)
    plt.show()

    return
