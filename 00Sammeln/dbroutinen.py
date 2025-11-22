from dbparam import *
import mysql.connector
import logging

DBTCREATEBB = """ CREATE TABLE `blackboard` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'simpler Zähler',
 `programm` tinytext DEFAULT NULL,
 `version` tinyint(4) DEFAULT 0 COMMENT 'Programmversion, falls es Unterschiede gibt',
 `parameter` tinytext DEFAULT NULL COMMENT 'Parameter für das Programm',
 `parameter2` tinytext DEFAULT NULL COMMENT 'zusätzlicher Parameter',
 `zeit` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'wann der Eintrag erzeugt wurde',
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""
DBTCREATELOGFILES = """CREATE TABLE `logfiles` (
 `basisname` tinytext DEFAULT NULL COMMENT 'reduzierter Dateiname',
 `dateiname` tinytext NOT NULL COMMENT 'Dateiname, ohne Pfad, ist Zugriffskriterium',
 `pfad` tinytext DEFAULT NULL COMMENT 'vollständiger Pfad und Name',
 `typ` tinyint(3) unsigned DEFAULT NULL COMMENT 'aus Inhalt ermittelter Typ',
 PRIMARY KEY (`dateiname`(40))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='bekannte Logfiles und ihr Typ'
"""

DBTCREATEBILDER = """ CREATE TABLE `bilder` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'simpler Zähler',
 `pfad` tinytext DEFAULT NULL,
 `name` tinytext DEFAULT NULL,
 `ext` tinytext DEFAULT NULL,
 `version` tinyint(4) DEFAULT 0 COMMENT 'Programmversion, falls es Unterschiede gibt',
 `arbkopie` TINYTEXT NULL DEFAULT NULL COMMENT 'Pfad der Arbeitskopie',
 `zeit` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'wann der Eintrag erzeugt wurde',
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""


def zurücksetzenDaten(titel, db):
    """Daten löschen, zurücksetzen

    Raises:
        Exception: aus falschem Programm
        Exception: nicht zurückgesetzt
    """
    if titel != "P0Sammeln":
        raise Exception(f"Zurücksetzen aus falschem Programm aufgerufen:{titel}")
    ja = input("Zurücksetzen? Ja:")
    if ja != "Ja":
        raise Exception(f"Zurücksetzen nicht bestätigt: {ja}")
    with db.cursor() as cursor:
        sql = f"truncate {DBTBILDER};"
        logging.debug(sql)
        cursor.execute(sql)
    db.commit()
    logging.info("...zurückgesetzt")


def dbcreate(db, errtext):
    """erzeugt eine fehlende Tabelle

    Args:
        cursor (MySQL-Cursor): cursor
        tabelle (string): Tabellenname

    Raises:
        Exception: wenn Name der Tabelle nicht stimmt

    Returns:
        -: 0
    """
    tabelle = errtext.split("fhemlogs.")[1].split("'")[0]
    logging.debug(f"dbcreate: {tabelle}")
    with db.cursor() as cursor:
        match tabelle:
            case "logfiles":
                cursor.execute(DBTCREATELOGFILES)
            case "blackboard":
                cursor.execute(DBTCREATEBB)
            case _:
                raise Exception("Tabelle %s Erzeugung unbekannt" % (tabelle))
    logging.critical("Tabelle nicht vorhanden - erzeugt")
    return 0


def zurücksetzenBilder(titel, db):
    """Daten löschen, zurücksetzen

    Raises:
        Exception: aus falschem Programm
        Exception: nicht zurückgesetzt
    """
    if titel != "P0Sammeln":
        raise Exception(f"Zurücksetzen aus falschem Programm aufgerufen:{titel}")
    ja = input("Zurücksetzen? Ja:")
    if ja != "Ja":
        raise Exception(f"Zurücksetzen nicht bestätigt: {ja}")
    with db.cursor() as cursor:
        sql = f"truncate {DBTBILDER};"
        cursor.execute(sql)

    db.commit()
    logging.info("...zurückgesetzt")
