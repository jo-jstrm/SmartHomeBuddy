# for classes that are generic in stubs but not at runtime see
# https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime
from __future__ import annotations

import os
import sqlite3
import subprocess
from pathlib import Path
from sqlite3 import Error
from subprocess import Popen
from typing import Union

from influxdb import InfluxDBClient
from loguru import logger


# noinspection PyPep8Naming
class Database:
    db_file = Path("../SQLite/main.db")
    influxdb_binary = Path("../InfluxData/influxdb/influxd.exe")
    default_username = "user"
    influx_process = None

    def __init__(
            self,
            db_file: Union[str, Path] = db_file,
            influxdb_binary: Union[str, Path] = influxdb_binary,
            default_username=default_username
    ):
        # Handle file paths to make sure they exist and are absolute
        self.db_file = db_file if isinstance(db_file, Path) else Path(db_file)
        self.influxdb_binary = influxdb_binary if isinstance(influxdb_binary, Path) else Path(influxdb_binary)
        if not self.db_file.is_file():
            logger.error(f"Database file {self.db_file} does not exist."
                         f" Please supply a valid database file."
                         f" Current working directory: {os.getcwd()}")
        if not self.influxdb_binary.is_file():
            logger.error(f"InfluxDB binary {self.influxdb_binary} does not exist. "
                         f"Please check your installation path."
                         f" Current working directory: {os.getcwd()}")
        self.db_file = self.db_file.resolve()
        self.influxdb_binary = self.influxdb_binary.resolve()

        self.default_username = default_username

        self._setup_SQLite_db(self.db_file)
        self.influx_process = self.start_InfluxDB()
        self._setup_InfluxDB_db(self.db_file)

    @staticmethod
    def safe_execute(conn, statement, values=None) -> bool:
        try:
            c = conn.cursor()
            if values:
                c.execute(statement, values)
            else:
                c.execute(statement)
            return True
        except Error as e:
            logger.debug(e)
            return False

    @staticmethod
    def safe_fetchone(conn, statement, values=None) -> tuple:
        try:
            c = conn.cursor()
            if values:
                c.execute(statement, values)
            else:
                c.execute(statement)
            return c.fetchone()
        except Error as e:
            logger.debug(e)
            return ()

    @staticmethod
    def _create_SQLite_connection(db_file) -> sqlite3.Connection:
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            logger.debug(f"Connected to SQLite database at {db_file}.")
        except Error as e:
            logger.debug(e)
        return conn

    @staticmethod
    def check_InfluxDB_connection(host='localhost', port='8086') -> bool:
        """ create a database connection to a InfluxDB database """
        try:
            client = InfluxDBClient(host=host, port=port)
            version = client.ping()
            logger.success("Successfully connected to InfluxDB: " + version + ".")
            client.close()
            return True
        except Exception as e:
            logger.debug(e)
            return False

    def _setup_SQLite_db(self, db_file):
        """
        Sets up the SQLite database.
        """
        # engine = create_engine("sqlite+pysqlite://"+db_file, echo=False, future=True)

        sql_create_users_table = """CREATE TABLE users (
                                               id integer PRIMARY KEY,
                                               username VARCHAR NOT NULL UNIQUE
                                           );"""

        sql_add_user = """INSERT INTO users (username)
                               VALUES(?);"""
        sql_add_user_values = (self.default_username,)

        sql_create_influxdb_table = """CREATE TABLE influxdb (
                                           id integer PRIMARY KEY,
                                           user_id integer NOT NULL,
                                           token VARCHAR,
                                           bucket VARCHAR,
                                           url VARCHAR,
                                           org VARCHAR,
                                           CONSTRAINT fk_users_id
                                               FOREIGN KEY (user_id) 
                                               REFERENCES users (id)
                                       );"""

        # create tables
        conn = self._create_SQLite_connection(db_file)
        if conn:
            # Users table
            if self.safe_execute(conn, sql_create_users_table):
                logger.debug("Table users created successfully.")
            # InfluxDB table
            if self.safe_execute(conn, sql_create_influxdb_table):
                logger.debug("Table influxdb created successfully.")
            # Add user
            if self.safe_execute(conn, sql_add_user, sql_add_user_values):
                logger.debug("User added successfully.")

            conn.commit()
            conn.close()

    def _setup_InfluxDB_db(self, db_file):
        """
        Sets up the InfluxDB database.
        """

        # add configurations to sqlite db
        sql_add_user_influxdb = """INSERT INTO influxdb (user_id, token, bucket, org, url)
                            VALUES(?,?,?,?,?);"""
        sql_find_user = """SELECT id FROM users WHERE username = ?"""

        conn = self._create_SQLite_connection(db_file)
        if conn:
            # find and add user_id to values
            user_id = self.safe_fetchone(conn, sql_find_user, (self.default_username,))[0]
            sql_add_user_influxdb_values = self._get_influxdb_credentials(self.default_username)
            sql_add_user_influxdb_values["user_id"] = user_id
            # match the INSERT stmt tuple
            sql_add_user_influxdb_values = (
                sql_add_user_influxdb_values["user_id"],
                sql_add_user_influxdb_values["token"],
                sql_add_user_influxdb_values["bucket"],
                sql_add_user_influxdb_values["org"],
                sql_add_user_influxdb_values["url"]
            )
            # add user credentials to influxdb table
            if self.safe_execute(conn, sql_add_user_influxdb, sql_add_user_influxdb_values):
                logger.debug(f"User credentials added successfully for {(self.default_username, user_id)}.")

            conn.commit()
            conn.close()

    def _get_influxdb_credentials(self, username) -> dict:
        """
        Get the credentials for the InfluxDB instance.
        """
        # TODO get from influxdb
        return {
            "username": self.default_username,
            "token": "S_bFseW7ihLwo_rhz_BK_4OBSOGHarpQwiKxHs3JRiqcX31zoNoIGByCZV61yCjPYxngbNXAEh988brX9gg1Yg==",
            "org": "smarthomebuddy",
            "bucket": "network-traffic",
            "url": "http://localhost:8086",
        }

    @staticmethod
    def start_InfluxDB(binary_path=influxdb_binary) -> Union[None, Popen[bytes], Popen]:
        try:
            influx_process = subprocess.Popen(binary_path)
            logger.debug("InfluxDB started successfully.")
        except Exception as e:
            logger.debug(e)
            logger.error("Failed to start InfluxDB.")
            return None
        return influx_process

    def stop_InfluxDB(self, kill=False) -> bool:
        if self.influx_process:
            if kill:
                self.influx_process.kill()
            else:
                self.influx_process.terminate()
            logger.debug("InfluxDB stopped successfully.")
            return True
        else:
            logger.debug("No InfluxDB process found.")
            return False
