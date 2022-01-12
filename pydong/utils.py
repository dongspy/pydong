#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
common file
"""

# ---------
# Change Logs:
#
# ---------

__author__ = 'Li Pidong'
__email__ = 'lipidong@126.com'
__version__ = '0.0.3'
__status__ = 'Beta'


import logging
from datetime import datetime
import subprocess


def log(file_name=None, logger_name=__name__, quite=False):
    """ logging template

    Parameters
    ----------
    file_name : str, default None
        if set, will generate log file.
    logger_name : str, default __name__
        logger name
    quite : bool, default False
        if True, set log level to ERROR else INFO

    Returns
    -------
        logger

    """
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#         datefmt="%Y-%m-%d %H:%M:%S"
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    if quite:
        console.setLevel(logging.ERROR)
    logger.addHandler(console)
    if file_name:
        handler = logging.FileHandler(file_name)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def time2str(dt, f='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(f)


def str2time(string, f='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(string, f)


def safe_run(shell_cmd, retry=3, has_retry=0):
    """
    Return linux command line executive result

    Parameter
    ---------
    shell_cmd : str
        linux command
    retry : int, default 3
        the number of retry if command fail
    has_retry: int, default 0
        the number of retry which has run

    """
    has_retry += 1
    if has_retry > retry:
        print('{0} Error'.format(shell_cmd))
        return None
    print('run {0}'.format(shell_cmd))
    P = subprocess.Popen(
        shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (P_o, P_e) = P.communicate()
    if P.returncode == 0:
        return P_o
    else:
        safe_run(shell_cmd, retry=retry, has_retry=has_retry)
