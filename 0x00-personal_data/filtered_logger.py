#!/usr/bin/env python3
"""

Filtered Datum

"""


from typing import List
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
