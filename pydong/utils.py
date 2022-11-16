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
import inspect
import typing


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


def format_df(df, int_format="{:,}", float_format="{:,.4f}"):
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

    Examples
    ----------
    >>> from pydong import *
    >>> import pandas as pd
    >>> d = {'col1': [1000, 2123], 'col2': [3.13454334, 40234.12345]}
    >>> df = pd.DataFrame(data=d)
    >>> df
    col1          col2
    0  1000      3.134543
    1  2123  40234.123450
    >>> format_df(df)
        col1         col2
    0  1,000       3.1345
    1  2,123  40,234.1234

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


def try_except(f, require_ipdb=True):
    """the decoratTry/Except decorator

    Parameters
    ----------
    f : function
        the function to be test

    Examples
    ---------
    >>> @try_except
    >>> def divide(a, b):
    >>>     return a/b
    >>> divide(1, 0)
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
            if require_ipdb:
                import ipdb;
                ipdb.set_trace()
        finally:
            pass
    return handle_problems

_ExpType = typing.TypeVar('_ExpType')
def dbg(exp: _ExpType) -> _ExpType:
    """
    The code from https://github.com/tylerwince/pydbg

    Call dbg with any variable or expression.
    Calling dbg will print to stderr the current filename and lineno,
    as well as the passed expression and what the expression evaluates to:
    
    Examples
    --------
    >>> a = 2
    >>> b = 5
    >>> dbg(a+b)
    >>> def square(x: int) -> int:
    >>>     return x * x
    >>> dbg(square(a))
    
    """
    for frame in inspect.stack():
        line = frame.code_context[0]
        if "dbg" in line:
            start = line.find('(') + 1
            end =  line.rfind(')')
            if end == -1:
                end = len(line)
            print(
                f"[{frame.filename}:{frame.lineno}] {line[start:end]} = {exp!r}",
                file=sys.stderr,
            )
            break

    return exp
