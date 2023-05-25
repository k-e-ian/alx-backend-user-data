#!/usr/bin/env python3.8
'''
File: filtered_logger.py
'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    '''
    Obfuscates specified fields in the log message.
    '''
    pattern = '|'.join(fields)
    return re.sub(pattern + r'=[^' + re.escape(separator) + r']+', redaction,
                  message)
