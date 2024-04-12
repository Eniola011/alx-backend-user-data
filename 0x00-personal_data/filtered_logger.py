#!/usr/bin/env python3
"""

Filtered Datum

"""


from typing import List
import logging
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
        >> Returns an obscured log message.
        >> fields: representing all fields to obfuscate.
        >> redaction: representing by what the field will be obfuscated.
        >> message: representing the log line.
        >> separator: representing by which character is separating...
           all fields in the log line (message).
    """
    regex = '|'.join(f'(?<={field}=)[^{separator}]+' for field in fields)
    return re.sub(regex, redaction, message)


class RedactingFormatter(logging.Formatter):
    """
        >> Redacting Formatter class: accepts a list..
           of strings fields constructor argument.
        >> Redacts specified fields from log records.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            >> Filters values in incoming log records using filter_datum.
            >> Values for fields in fields should be filtered.
            >> Do not extrapolate FORMAT manually.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)
