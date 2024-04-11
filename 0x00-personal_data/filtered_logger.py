#!/usr/bin/python3
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
    pattern = '|'.join(map(re.escape, fields))
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        """
        Initialize RedactingFormatter with a list of fields
        """
        super().__init__(self.FORMAT)
        self.fields = fields if fields else []

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and redat specified fields.
        Args:
            record: the log record to format.
        Returns:
            the formatted log message with redacted fields.
        """
        message = super().format(record)
        for field in self.fields:
            message = re.sub(rf"{field}=[^;]+",
                             f"{field}={self.REDACTION}",
                             message)
        return message


def get_logger() -> logging.Logger:
    """ returns a logger named 'user-data'. """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler = StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


PII_FIELDS = ["name", "email", "phone", "credit_card", "address"]


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
        host=db_host,
        user=username,
        password=password,
        database=db_name
    )
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
