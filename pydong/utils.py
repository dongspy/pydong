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
import sys
import traceback


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
    """Convert time to string"""
    return dt.strftime(f)


def str2time(string, f='%Y-%m-%d %H:%M:%S'):
    """Convert string to datetime"""
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


def format_df(df, int_format="{:,}", float_format="{:,4f}"):
    """
    Formats the columns of pandas.DataFrame with the type of int and float

    Parameters
    ---------
    df : pandas.DataFrame
        the df to revise
    int_format: str, optional
        the format of int columns, refer to the python f-string
    float_format: str, optional
        the format of float columns, refer to the python f-string

    Returns
    ----------
    pandas.DataFrame
    """
    dtypes_dict = df.dtypes.to_dict()
    int_columns = [k for k, v in dtypes_dict.items() if 'int' in str(v)]
    float_columns = [k for k, v in dtypes_dict.items() if 'float' in str(v)]
    for xx in int_columns:
        df[xx] = df[xx].apply(lambda x: int_format.format(x))
    for xx in float_columns:
        df[xx] = df[xx].apply(lambda x: float_format.format(x))
    return df


def safe_open(file_name, mode='r'):
    """open the file safely

    Parameters
    ----------
    file_name : str
        the name of file path
    mode : str, optional
        the opem mode, by default 'r'

    Returns
    -------
    file_handle
    """
    if file_name.endswith('.gz'):
        import gzip
        return gzip.open(file_name, mode + 't')
    else:
        return open(file_name, mode)


def try_except(f):
    """the decoratTry/Except decorator

    Parameters
    ----------
    f : function
        the function to be test
    """
    def handle_problems(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            message = '\n{0}\n{1}:\n{2}'.format(
                formatted_traceback,
                exc_type.__name__,
                exc_instance
            )
            print(exc_type(message))
        finally:
            pass
    return handle_problems
