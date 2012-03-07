'''
Purpose of this module (is it a module?) is simply to set up
logging for the server.
'''

import logging

_FMT_A = "[%(asctime)s] %(message)s"
_DATE_FMT = "%d/%m %H:%M:%S"
_FMT_B = "%(message)s"

_f1 = logging.Formatter(_FMT_A, _DATE_FMT)
_f2 = logging.Formatter(_FMT_B)

_h1 = logging.FileHandler("server.log")
_h1.setLevel(logging.DEBUG)
_h1.setFormatter(_f1)

_h2 = logging.StreamHandler()
_h2.setLevel(logging.INFO)
_h2.setFormatter(_f2)

logger = logging.getLogger('serverLogger')
logger.setLevel(logging.DEBUG)

logger.addHandler(_h1)
logger.addHandler(_h2)
