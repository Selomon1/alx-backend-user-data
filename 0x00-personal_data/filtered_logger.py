#!/usr/bin/env python3
"""
Filtered_logger module contains functions to handle personal data
"""
import logging
import csv
from os import environ
from mysql.connector import connection

from logging import StreamHandler
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates sensitive information in a log message.
    Args:
        fields: List of strings representing the fields
        redaction: the value
        message: the log line
        separartor: the character used to separate
    """
    pattern = rf"({'|'.join(fields)})=.+?{separator}"
    return re.sub(pattern, f"\\1={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize RedactingFormatter with a list of fields
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and redat specified fields.
        Args:
            record: the log record to format.
        Returns:
            the formatted log message with redacted fields.
        """
        record.msg = filter_datum(self._fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ returns a logger named 'user-data'. """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> connection.MySQLConnection:
    """
    Connect to MySQL database
    Retrives database credentials from environmental variables
    Returns:
        MySQLConnection: A connection object to the MySQL database.
    """
    username = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = environ.get('PERSONAL_DATA_DB_NAME')

    db_connection = connection.MySQLConnection(
        user=username,
        password=password,
        host=db_host,
        database=db_name)
    return db_connection


def main() -> None:
    """
    Main function to retrieve user data from the database and log it in a
    filtered format.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    logger = get_logger()

    for row in rows:
        name, email, phone, ssn, password, ip, last_login, user_agent = row
        message = (f"name={name}; email={email}; phone={phone}; ssn={ssn}; "
                   f"password={password}; ip={ip}; last_login={last_login}; "
                   f"user_agent={user_agent}")
        filtered_message = filter_datum(PII_FIELDS, '***', message, ';')
        logger.info(filtered_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
