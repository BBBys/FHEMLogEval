import logging
import subprocess,os
from parameter import MNTPUNKT

def mountLogs():
    logging.debug("einhängen")
    cwd=os.getcwd()
    mntp=os.path.join(cwd,MNTPUNKT)
    if not os.path.exists(mntp):
        logging.warning(f"Mounpoint {mntp} fehlt - wird erzeugt")
        os.mkdir(mntp)

    logfile=os.path.join(mntp,"*.log")
    logging.debug(f"Teste auf {logfile}")
    if os.path.exists(logfile):
        logging.info("Logs bereits eingebunden")
        return mntp

    logging.info(f"Remote-Logiles einhängen auf {mntp}")
    rtc= subprocess.run(
        f"sudo mount.smb3 //192.168.1.2/fhemlogs {mntp} -o guest,ro",
        shell=True,timeout=30).returncode
    if rtc==0:
        return mntp
    else:
        logging.error(f"Mount fehlgeschlagen mit {rtc}")
        return None

def unmountLogs(mntp):
    logging.debug("Remote-Logfiles aushängen")
    if not os.path.exists(mntp):
        logging.warning(f"Problem: Mountpoint {mntp} fehlt ")
        return 0
    else:
        return subprocess.run(f"sudo umount {mntp}",shell=True,
                              timeout=3).returncode
