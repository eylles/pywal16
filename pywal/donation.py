import datetime
import logging


def donation_message():
    url = "https://github.com/eylles/pywal16"
    donate_msg = "if you enjoy pywal16 consider donating at: {}".format(url)
    if datetime.datetime.now().month == 12:
        logging.info(donate_msg)
    else:
        msec_mod = datetime.datetime.now().microsecond % 20
        if msec_mod >= 8:
            logging.info(donate_msg)
