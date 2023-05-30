#!/usr/bin/env python3.8
'''
File: filtered_logger.py
'''
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    '''
    Class redacting formatter
    '''
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
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
