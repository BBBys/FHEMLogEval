import sys, logging
import subprocess, os
from parameter import  TESTFILE
from time import sleep


def mountLogs(pfad):
    logging.debug("einhängen")
    mntp = pfad
    if not os.path.exists(mntp):
        logging.warning(f"Mountpoint {mntp} fehlt - wird erzeugt")
        os.mkdir(mntp)
    # das wären dann die Logs
    logfile = os.path.join(mntp, TESTFILE)
    # sind sie schon da?
    logging.debug(f"Teste auf {logfile}")
    if os.path.exists(logfile):
        logging.info("Logs bereits eingebunden")
        return mntp

    logging.info(f"Remote-Logiles einhängen auf {mntp}")
    rtc = subprocess.run(
        f"sudo mount.smb3 //192.168.1.2/fhemlogs {mntp} -o guest,ro",
        shell=True,
        timeout=30,
    ).returncode
    if rtc == 0:
        return mntp
    else:
        logging.error(f"Mount fehlgeschlagen mit {rtc}")
        return None


def unmountLogs(mntp):
    logging.debug("Remote-Logfiles aushängen")
    logfile = os.path.join(mntp, TESTFILE)
    # sind sie noch da?
    logging.debug(f"Teste auf {logfile}")
    if not os.path.exists(logfile):
        logging.warning(f"Logfiles unerwartet nicht mehr da")
        return 10
    logging.info(f"Remote-Logiles aushängen von {mntp}")
    rtn = subprocess.run(f"sudo umount {mntp}", shell=True, timeout=22).returncode
    if not os.path.exists(logfile):
        logging.info(f"...ausgehängt")
        return 0
    logging.warning(f"unmount fehlgeschlagen mit {rtn}")
    sleep(5)
    logging.info("Remote-Logiles erneut aushängen")
    rtn = subprocess.run(f"sudo umount {mntp}", shell=True, timeout=44).returncode
    if not os.path.exists(logfile):
        logging.info(f"...ausgehängt")
        return 0
    logging.warning(f"unmount fehlgeschlagen mit {rtn}")
    sleep(10)
    logging.info(f"Remote-Logiles drittes Mal aushängen von {mntp}")
    rtn = subprocess.run(f"sudo umount {mntp}", shell=True, timeout=5000).returncode
    if not os.path.exists(logfile):
        logging.info(f"...ausgehängt")
        return 0
    logging.error(f"Logfiles noch da, unmount fehlgeschlagen mit {rtn}")
    return rtn
