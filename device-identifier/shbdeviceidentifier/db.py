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
from typing import Union, Iterable, Generator

import pandas as pd
import pyshark
from influxdb import InfluxDBClient
from loguru import logger

from .utilities.app_utilities import resolve_file_path
from .utilities.capture_utilities import convert_Capture_to_DataFrame


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
    influx_log_path = Path("device-identifier/shbdeviceidentifier/logs/influx.log").resolve()

    default_username = "user"
    influx_process: Union[None, Popen[bytes], Popen] = None

    host = "localhost"
    port = "8086"

    def __init__(
            self,
            db_file=db_file,
            influxdb_binary_path=influxdb_binary_path,
            influx_log_path=influx_log_path,
            default_username=default_username,
            host=host,
            port=port
    ):
        # Handle file paths to make sure they exist and are absolute
        error_msg = (f"InfluxDB log file {self.influx_log_path} does not exist."
                     f" Please check your log directory."
                     f" Default log directory is 'device-identifier/shbdeviceidentifier/logs/influx.log'"
                     f" Current working directory: {os.getcwd()}")
        self.influx_log_path = resolve_file_path(influx_log_path, error_msg=error_msg)

        error_msg = (f"Database file {self.db_file} does not exist."
                     f" Please supply a valid database file."
                     f" Current working directory: {os.getcwd()}")
        self.db_file = resolve_file_path(db_file, error_msg=error_msg)

        error_msg = (f"InfluxDB binary {self.influxdb_binary_path} does not exist. "
                     f"Please check your installation path."
                     f" Current working directory: {os.getcwd()}")
        self.influxdb_binary_path = resolve_file_path(influxdb_binary_path, error_msg=error_msg)

        self.default_username = default_username

        self.host = host
        self.port = port

        self._setup_SQLite_db()
        self.influx_process = self.start_InfluxDB()
        self._setup_InfluxDB_db()

    def _get_InfluxDB_connection(self, **client_kwargs) -> Union[InfluxDBClient, None]:
        """ create a database connection to a InfluxDB database """
        if client_kwargs is None:
            client_kwargs = {"host": self.host, "port": self.port}
        try:
            client = InfluxDBClient(**client_kwargs)
            version = client.ping()
            logger.debug(f"Connected to InfluxDB {version} at {self.host}:{self.port}.")
            return client
        except Exception as e:
            logger.debug(e)
            return None

    def _get_influxdb_credentials(self, user_id: int = 0, username: str = "") -> list:
        """
        Get the credentials for the InfluxDB instance from the main SQLite database.
        """
        # Needs to match the order of the sql_add_user_influxdb query
        search_user_credentials = (
            "SELECT user_id, token, bucket, org, url "
            "FROM users u JOIN influxdb i on u.id = i.user_id "
            "WHERE user_id = ? OR username = ?"
        )

        search_user_credentials_params = (user_id, username)

        query_result = self.query_SQLiteDB(search_user_credentials, search_user_credentials_params)
        if query_result:
            return query_result[0]
        else:
            logger.warning(f"Could not find credentials for user id '{user_id}' or user '{username}'.")
            logger.debug(f"Query result: {query_result}.")

    def _get_SQLite_connection(self) -> sqlite3.Connection:
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            logger.debug(f"Failed to connect to SQLite database at {self.db_file}. \n{e}")
        return conn

    def _setup_InfluxDB_db(self):
        """
        Sets up the InfluxDB database.
        """

        sql_add_user_influxdb = """INSERT OR IGNORE INTO influxdb (user_id, token, bucket, org, url)
                            VALUES(?,?,?,?,?);"""

        sql_find_user = """SELECT id FROM users WHERE username = ?"""

        # find user values in sqlite db
        user_id = self.query_SQLiteDB(sql_find_user, (self.default_username,))[0][0]
        sql_add_user_influxdb_values = self._get_influxdb_credentials(
            user_id=user_id,
            username=self.default_username
        )

        # add user credentials to influxdb table
        if self.query_SQLiteDB(sql_add_user_influxdb, sql_add_user_influxdb_values):
            logger.debug(f"User credentials added successfully for {(self.default_username, user_id)}.")

    def _setup_SQLite_db(self):
        """
        Sets up the SQLite database.
        """
        # engine = create_engine("sqlite+pysqlite://"+db_file, echo=False, future=True)

        sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                               id integer PRIMARY KEY,
                                               username VARCHAR NOT NULL UNIQUE
                                           );"""

        sql_add_user = """INSERT OR IGNORE INTO users (username)
                               VALUES(?);"""
        sql_add_user_values = (self.default_username,)

        sql_create_influxdb_table = """CREATE TABLE IF NOT EXISTS influxdb (
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
            logger.debug("Databases are connected.")
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
        user_id, token, bucket, org, url = self._get_influxdb_credentials(username=self.default_username)
        client = self._get_InfluxDB_connection(token=token, org=org, url=url)
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
                logger.error(e)

    def query(self, query: str, params: dict = None, bind_params: dict = None, db='influx') -> Union[list, None]:
        """
        Convenience function for querying the SQLite and InfluxDB databases.
        Use the db parameter to specify which database to query. db='i' for InfluxDB, db='s' for SQLite.
        Alternatively, use the query_SQLiteDB and query_InfluxDB functions directly.
        """
        if db == 'influx':
            return self.query_InfluxDB(query, params, bind_params)
        elif db == 'sqlite':
            return self.query_SQLiteDB(query, params)

    def start_InfluxDB(self) -> Union[None, Popen[bytes], Popen]:
        try:
            with open(self.influx_log_path, "wb") as influx_log:
                influx_process = subprocess.Popen(
                    self.influxdb_binary_path,
                    stdout=influx_log,
                    stderr=subprocess.STDOUT)
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


# noinspection PyPep8Naming
class DataLoader:
    """
    Class for loading data from various sources into a pandas DataFrame.
    """

    def from_InfluxDB(self, query: str, params: dict = None, bind_params: dict = None) -> Union[list, None]:
        """
        Loads data from the InfluxDB database.
        """
        ...

    @staticmethod
    def from_CSV(file_path: Union[Path, str], **kwargs) -> Union[pd.DataFrame, None]:
        """
        Loads data from a CSV file.
        """
        file_path = resolve_file_path(file_path)
        if file_path:
            return pd.read_csv(file_path, **kwargs)

    @staticmethod
    def from_pcap(file_path: Union[Path, str]) -> Union[pd.DataFrame, None]:
        """
        Loads data from a pcap file.
        """
        file_path = resolve_file_path(file_path)
        if file_path:
            cap = pyshark.FileCapture(file_path)
            converted_cap = convert_Capture_to_DataFrame(cap)

    def from_generator(self, generator: Generator) -> Union[pd.DataFrame, None]:
        """
        Loads data from a generator.
        """
        ...

    def from_dict(self, data: dict) -> Union[pd.DataFrame, None]:
        """
        Constructs a Dataset from data in memory.
        """
        ...
