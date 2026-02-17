import datetime
import logging
import os


def donation_message():
    url = "https://github.com/eylles/pywal16"
    donate_msg = "if you enjoy pywal16 consider donating at: {}".format(url)
    no_donations = int(os.getenv(
        "JOBLESS_FAT_BASTARD_STOP_BEGGING_FOR_MONEY", 0
        ))
    if not no_donations:
        if datetime.datetime.now().month == 12:
            logging.info(donate_msg)
        else:
            msec_mod = datetime.datetime.now().microsecond % 20
            if msec_mod >= 6:
                logging.info(donate_msg)
