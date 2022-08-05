# for classes that are generic in stubs but not at runtime see
# https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime
from __future__ import annotations

import os
import platform
import sqlite3
import subprocess
from pathlib import Path
from sqlite3 import Error
from subprocess import Popen
from typing import Union, Iterable

from influxdb import InfluxDBClient
from loguru import logger


# noinspection PyPep8Naming
class Database:
    # SQLite database file path
    db_file = Path("SQLite/main.db").resolve()

    # InfluxDB database file path
    binary_name = ''
    system = platform.system()
    if system == 'Linux':
        binary_name = 'influxd'
    elif system == 'Windows':
        binary_name = 'influxd.exe'
    else:
        logger.error(f"Unsupported system: {system}. Please use Linux or Windows. "
                     f"Alternatively, start the influxdb server manually.")
    influxdb_binary_path = Path("InfluxData/influxdb/", binary_name).resolve()

    default_username = "user"
    influx_process = None

    host = "localhost"
    port = "8086"

    def __init__(
            self,
            db_file: Path = db_file,
            influxdb_binary: Path = influxdb_binary_path,
            default_username=default_username,
            host=host,
            port=port
    ):
        # Handle file paths to make sure they exist and are absolute
        self.db_file = db_file if isinstance(db_file, Path) else Path(db_file)
        self.influxdb_binary_path = influxdb_binary if isinstance(influxdb_binary, Path) else Path(influxdb_binary)
        if not self.db_file.is_file():
            logger.error(f"Database file {self.db_file} does not exist."
                         f" Please supply a valid database file."
                         f" Current working directory: {os.getcwd()}")
        if not self.influxdb_binary_path.is_file():
            logger.error(f"InfluxDB binary {self.influxdb_binary_path} does not exist. "
                         f"Please check your installation path."
                         f" Current working directory: {os.getcwd()}")
        self.db_file = self.db_file.resolve()
        self.influxdb_binary_path = self.influxdb_binary_path.resolve()

        self.default_username = default_username

        self.host = host
        self.port = port

        self._setup_SQLite_db()
        self.influx_process = self.start_InfluxDB()
        self._setup_InfluxDB_db()

    def _get_InfluxDB_connection(self) -> Union[InfluxDBClient, None]:
        """ create a database connection to a InfluxDB database """
        try:
            client = InfluxDBClient(host=self.host, port=self.port)
            version = client.ping()
            logger.debug(f"Connected to InfluxDB {version} at {self.host}:{self.port}.")
            return client
        except Exception as e:
            logger.debug(e)
            return None

    def _get_influxdb_credentials(self, username) -> dict:
        """
        Get the credentials for the InfluxDB instance.
        """
        # TODO get from sqlite db
        return {
            "username": self.default_username,
            "token": "S_bFseW7ihLwo_rhz_BK_4OBSOGHarpQwiKxHs3JRiqcX31zoNoIGByCZV61yCjPYxngbNXAEh988brX9gg1Yg==",
            "org": "smarthomebuddy",
            "bucket": "network-traffic",
            "url": "http://localhost:8086",
        }

    def _get_SQLite_connection(self) -> sqlite3.Connection:
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            logger.debug(f"Connected to SQLite database at {self.db_file}.")
        except Error as e:
            logger.debug(e)
        return conn

    def _setup_InfluxDB_db(self):
        """
        Sets up the InfluxDB database.
        """

        # add configurations to sqlite db
        sql_add_user_influxdb = """INSERT INTO influxdb (user_id, token, bucket, org, url)
                            VALUES(?,?,?,?,?);"""
        sql_find_user = """SELECT id FROM users WHERE username = ?"""

        conn = self._get_SQLite_connection()
        if conn:
            # find and add user_id to values
            user_id: str = self.query_SQLiteDB(sql_find_user, (self.default_username,))[0]
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
            if self.query_SQLiteDB(sql_add_user_influxdb, sql_add_user_influxdb_values):
                logger.debug(f"User credentials added successfully for {(self.default_username, user_id)}.")

    def _setup_SQLite_db(self):
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
                                           user_id integer NOT NULL UNIQUE,
                                           token VARCHAR,
                                           bucket VARCHAR,
                                           url VARCHAR,
                                           org VARCHAR,
                                           CONSTRAINT fk_users_id
                                               FOREIGN KEY (user_id) 
                                               REFERENCES users (id)
                                       );"""

        # create tables
        conn = self._get_SQLite_connection()
        if conn:
            # Users table
            if self.query_SQLiteDB(sql_create_users_table):
                logger.debug("Table 'users' created successfully.")
            # InfluxDB table
            if self.query_SQLiteDB(sql_create_influxdb_table):
                logger.debug("Table 'influxdb' created successfully.")
            # Add user
            if self.query_SQLiteDB(sql_add_user, sql_add_user_values):
                logger.debug(f"User '{sql_add_user_values[0]}' added successfully.")

    def is_connected(self) -> bool:
        """
        Check if the Databases are connected.
        """
        influx_con = self._get_InfluxDB_connection()
        sqlite_con = self._get_SQLite_connection()
        if influx_con and sqlite_con:
            influx_con.close()
            sqlite_con.close()
            logger.success("Databases are connected.")
            return True
        elif influx_con:
            influx_con.close()
            logger.debug("Could not establish a connection to the SQLite database.")
        elif sqlite_con:
            sqlite_con.close()
            logger.debug("Could not establish a connection to the InfluxDB database. Try running db.start_InfluxDB().")
        return False

    def query_InfluxDB(self, query: str, params: dict = None, bind_params: dict = None):
        """
        Queries the InfluxDB instance.
        """
        client = self._get_InfluxDB_connection()
        if client:
            return client.query(query, params, bind_params)

    def query_SQLiteDB(self, query: str, params: Iterable = None) -> Union[list, None]:
        """
        Queries the SQLite database.
        """
        conn = self._get_SQLite_connection()
        if conn:
            try:
                c = conn.cursor()
                if params:
                    c.execute(query, params)
                else:
                    c.execute(query)

                res = c.fetchall()
                conn.commit()
                conn.close()
                return res

            except Error as e:
                logger.debug(e)
                return None

    def start_InfluxDB(self) -> Union[None, Popen[bytes], Popen]:
        try:
            influx_process = subprocess.Popen(self.influxdb_binary_path)
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
