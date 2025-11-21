# Routinen zum Umgang mit den in FHEM üblicen Dateinamen
import logging
import os

# from string import isdigits


def nameReduzieren(original0):
    gestripped = original0.strip().lower()
    name1, ext1 = os.path.splitext(gestripped)
    logging.debug(f"nameReduzieren: {gestripped} > {name1} {ext1}")
    if ext1[1:].isdecimal():
        name2, ext2 = os.path.splitext(name1)
        if ext2 == ".log":
            # Datei der Form aaa.log.001
            nurName = name2
            logging.debug(f"{gestripped} > {nurName}")
    else:
        if ext1 == ".log":
            # Datei der Form aaa.log
            nurName = name1
            logging.debug(f"{gestripped} > {nurName}")

    # beginnt mit Angabe des Monats
    if nurName[0:1].isdecimal():
        ohneMonat = nurName[2:]
    elif nurName[0:0].isdecimal():
        ohneMonat = nurName[1:]
    else:
        ohneMonat = nurName

    logging.debug(f"nameReduzieren: {original0} > {ohneMonat}")
    return ohneMonat
