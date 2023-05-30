#!/usr/bin/env python3.8
'''
File: filtered_logger.py
'''
import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    '''
    Class redacting formatter
    '''
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''
        initialaize class attributes
        '''
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        log formatter
        '''
        log_message = record.getMessage()
        for field in self.fields:
            log_message = filter_datum([field], self.REDACTION,
                                       log_message, self.SEPARATOR)
        record.msg = log_message
        return super().format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''
    Obfuscates specified fields in the log message.
    '''
    pattern = r'({})=[^{}]+'.format('|'.join(fields), re.escape(separator))
    return re.sub(pattern, r'\1=' + redaction, message)


def get_logger() -> logging.Logger:
    '''
    returns a logging.Logger object
    '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    '''
    function that returns a connector the database
    '''
    username: str = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password: str = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host: str = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database: str = os.environ.get("PERSONAL_DATA_DB_NAME")

    return connect(user=username, password=password,
                   host=host, database=database)
