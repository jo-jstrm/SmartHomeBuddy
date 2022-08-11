# for classes that are generic in stubs but not at runtime see
# https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime
from __future__ import annotations

import logging
import os
import platform
import requests
import sqlite3
import subprocess
from dataclasses import dataclass
from pathlib import Path
from requests.adapters import HTTPAdapter, Retry
from sqlite3 import Error
from subprocess import Popen
from typing import Union, Iterable, Generator, List, Dict

import influxdb
import influxdb_client
import pandas as pd
import pyshark
from influxdb_client.client.write_api import SYNCHRONOUS
from loguru import logger

from .utilities.app_utilities import resolve_file_path
from .utilities.capture_utilities import convert_Capture_to_Line, convert_Capture_to_DataFrame


@dataclass
class InfluxDbUser:
    user_id: str
    user_name: str
    password: str
    token: str
    bucket: str
    org: str
    url: str

    def to_list(self) -> List[str]:
        return [self.user_id, self.user_name, self.password, self.token, self.bucket, self.org, self.url]

    def get_entries_for_db(self) -> List[str]:
        return [self.user_name, self.token, self.bucket, self.url, self.org]


# noinspection PyPep8Naming
class Database:
    # SQLite database file path
    db_file = Path("SQLite/main.db").resolve()

    # InfluxDB database file path
    binary_name = ""
    system = platform.system()
    if system == "Linux":
        binary_name = "influxd"
    elif system == "Windows":
        binary_name = "influxd.exe"
    else:
        logger.error(
            f"Unsupported system: {system}. Please use Linux or Windows. "
            f"Alternatively, start the influxdb server manually."
        )
    influxdb_binary_path = Path("InfluxData/influxdb/", binary_name).resolve()
    influx_log_path = Path("device-identifier/shbdeviceidentifier/logs/influx.log").resolve()

    default_username = "user"
    influx_process: Union[None, Popen[bytes], Popen] = None

    influxdb_pw = "SHBadmin"
    influxdb_host = "localhost"
    influxdb_port = "8086"
    influxdb_org = "SmartHomeBuddy"
    influxdb_bucket = "network-traffic"

    def __init__(
        self,
        db_file=db_file,
        influxdb_binary_path=influxdb_binary_path,
        influx_log_path=influx_log_path,
        default_username=default_username,
        influxdb_host=influxdb_host,
        influxdb_port=influxdb_port,
        influxdb_org=influxdb_org,
        influxdb_bucket=influxdb_bucket,
        influxdb_pw=influxdb_pw,
    ):
        # Handle file paths to make sure they exist and are absolute
        error_msg = (
            f"InfluxDB log file {self.influx_log_path} does not exist."
            f" Please check your log directory."
            f" Default log directory is 'device-identifier/shbdeviceidentifier/logs/influx.log'"
            f" Current working directory: {os.getcwd()}"
        )
        self.influx_log_path = resolve_file_path(influx_log_path, error_msg=error_msg)

        error_msg = (
            f"Database file {self.db_file} does not exist."
            f" Please supply a valid database file."
            f" Current working directory: {os.getcwd()}"
        )
        if not Path(db_file).exists():
            logger.debug(f"No sqlite db file found. Creating at {db_file}")
            Path(db_file).touch()
        self.db_file = resolve_file_path(db_file, error_msg=error_msg)

        error_msg = (
            f"InfluxDB binary {self.influxdb_binary_path} does not exist. "
            f"Please check your installation path."
            f" Current working directory: {os.getcwd()}"
        )
        self.influxdb_binary_path = resolve_file_path(influxdb_binary_path, error_msg=error_msg)

        self.default_username = default_username

        self.influxdb_host = influxdb_host
        self.influxdb_port = influxdb_port
        self.influxdb_org = influxdb_org
        self.influxdb_bucket = influxdb_bucket
        self.influxdb_pw = influxdb_pw

        self.influx_process = self.start_InfluxDB()
        self._create_SQLite_tables()
        if not self._is_InfluxDB_setup():
            self._do_initial_db_setup()

    def _get_InfluxDB_connection(self, **client_kwargs) -> Union[influxdb.InfluxDBClient, None]:
        """create a database connection to a InfluxDB database server."""
        if client_kwargs is None:
            client_kwargs = {"host": self.influxdb_host, "port": self.influxdb_port}
        try:
            client = influxdb.InfluxDBClient(**client_kwargs)
            version = client.ping()
            logger.debug(f"Connected to InfluxDB {version} at {self.influxdb_host}:{self.influxdb_port}.")
            return client
        except Exception as e:
            logger.debug(e)
            return None

    def _run_influxdb_setup(self) -> Union[InfluxDbUser, None]:
        """Runs the "setup" routine from InfluxDBs API. It sets up the admin user for InfluxDB and return an access token.
        API doc: https://docs.influxdata.com/influxdb/v2.3/api/#tag/Setup
        Returns
        -------
        InfluxDbUser:  Check the InfluxDbUser.token indicates if the setup has been successful.
        None: If there was an unknown error during setup.

        """
        url = f"http://{self.influxdb_host}:{self.influxdb_port}/api/v2/setup"
        req_body = {
            "username": self.default_username,
            "password": self.influxdb_pw,
            "bucket": self.influxdb_bucket,
            "org": self.influxdb_org,
        }
        s = requests.Session()
        # InfluxDB takes a moment to start, therefore some retries might be necessary.
        retries = Retry(total=5, backoff_factor=1)
        s.mount("http://", HTTPAdapter(max_retries=retries))
        res = s.post(url, json=req_body)
        res_body = res.json()
        res_code = res.status_code
        if res_code == 201:
            token = res_body["auth"]["token"]
            logging.debug(f"Token: {token}")
        elif res_code == 422:
            token = None
        else:
            # TODO Raise exception?
            logger.error("Initial InfluxDB setup failed for unknown reasons.")
            logger.error(res_code)
            logger.error(res_body)
            return None
        return InfluxDbUser(
            user_id="0",
            user_name=self.default_username,
            password=self.influxdb_pw,
            token=token,
            bucket=self.influxdb_bucket,
            org=self.influxdb_org,
            url=f"{self.influxdb_host}:{self.influxdb_port}",
        )

    def _do_initial_db_setup(self):
        influxdb_admin = self._run_influxdb_setup()
        if influxdb_admin == None:
            raise ValueError("InfluxDB setup failed for unknown reasons")
        elif influxdb_admin.token == None:
            logger.warning(
                "The InfluxDB setup has already been run. No new token was received. "
                "Check the SQLite DB, if there is an admin token"
            )
            return
        self._store_InfluxDB_user(influxdb_admin)

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
        """create a database connection to a SQLite database"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            logger.debug(f"Failed to connect to SQLite database at {self.db_file}. \n{e}")
        return conn

    def _is_InfluxDB_setup(self) -> bool:
        sql_find_influxdb_user = """SELECT id FROM users WHERE username = ?"""
        # Find user values in SQLite DB.
        influxdb_user_id = self.query_SQLiteDB(sql_find_influxdb_user, (self.default_username,))
        logger.trace(f"The following list should be empty: influxdb_user_id = {influxdb_user_id}")
        return True if influxdb_user_id else False

    def _store_InfluxDB_user(self, influxdb_admin: InfluxDbUser):
        """Inserts the given user into the influxdb table of the SQLite DB."""
        sql_add_user_influxdb = """INSERT OR IGNORE INTO influxdb (user_id, token, bucket, org, url)
                                   VALUES(?,?,?,?,?);"""
        sql_add_user_users = """INSERT OR IGNORE INTO users (username)
                                VALUES(?);"""
        # Add user to the users table
        if self.query_SQLiteDB(sql_add_user_users, [influxdb_admin.user_name]):
            logger.debug(f'User {influxdb_admin.user_name} successfully added into "users" table.')
        # Add user credentials to influxdb table in SQLite DB.
        if self.query_SQLiteDB(sql_add_user_influxdb, influxdb_admin.get_entries_for_db()):
            logger.debug(
                f"User credentials added successfully for {(influxdb_admin.user_id, influxdb_admin.user_name)}."
            )

    def _create_SQLite_tables(self):
        """
        Sets up the SQLite database.
        """
        # engine = create_engine("sqlite+pysqlite://"+db_file, echo=False, future=True)

        sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                               id integer PRIMARY KEY,
                                               username VARCHAR NOT NULL UNIQUE
                                           );"""
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
        conn = self._get_SQLite_connection()
        if conn:
            # Users table
            if self.query_SQLiteDB(sql_create_users_table):
                logger.debug("Table 'users' created successfully.")
            # InfluxDB table
            if self.query_SQLiteDB(sql_create_influxdb_table):
                logger.debug("Table 'influxdb' created successfully.")

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
                logger.error(f"The supplied statements are: {params}")

    def query(self, query: str, params: dict = None, bind_params: dict = None, db="influx") -> Union[list, None]:
        """
        Convenience function for querying the SQLite and InfluxDB databases.
        Use the db parameter to specify which database to query. db='i' for InfluxDB, db='s' for SQLite.
        Alternatively, use the query_SQLiteDB and query_InfluxDB functions directly.
        """
        if db == "influx":
            return self.query_InfluxDB(query, params, bind_params)
        elif db == "sqlite":
            return self.query_SQLiteDB(query, params)

    def start_InfluxDB(self) -> Union[None, Popen[bytes], Popen]:
        try:
            with open(self.influx_log_path, "wb") as influx_log:
                influx_process = subprocess.Popen(
                    self.influxdb_binary_path, stdout=influx_log, stderr=subprocess.STDOUT
                )
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

    def write_to_InfluxDB(
        self,
        data: Union[List[str], pd.DataFrame],
        username: str = None,
        bucket: str = None,
        org: str = None,
        token: str = None,
        url: str = None,
        **df_kwargs,
    ) -> bool:
        """
        The write_to_influxdb function writes data to an InfluxDB bucket.

        Parameters
        ----------
            data:List[str]
                Data to be written to influxdb. Should be a list of Line Protocol strings,
                see Line Protocol format (see https://v2.docs.influxdata.com/v2.0/write-data/#line-protocol)
            username:str="user"
                Username to be used to get InfluxDB credentials.
            bucket:str="network-traffic"
                The name of the bucket in which data will be stored in InfluxDB, e.g., "network-traffic".
            org:str="smarthomebuddy"
                The name of the organization in which the bucket is stored in InfluxDB, e.g., "smarthomebuddy".
            token:str=<user-token>
                Authentication token for the influxdb api.
            url:str="http://localhost:8086"
                Url of the influxdb instance.
            df_kwargs:dict=None:
                Keyword arguments when supplying a pandas.DataFrame as data.
                Available are (from InfluxDbClient.write_api.write):
                    data_frame_measurement_name
                        – name of measurement for writing Pandas DataFrame - ``DataFrame``
                    data_frame_tag_columns
                        – list of DataFrame columns which are tags, rest columns will be fields - ``DataFrame``
                    data_frame_timestamp_column
                        – name of DataFrame column which contains a timestamp.
                        The column can be defined as a str value formatted as `2018-10-26`, `2018-10-26 12:00`,
                        `2018-10-26 12:00:00-05:00` or other formats and types supported by `pandas.to_datetime`
                    data_frame_timestamp_timezone
                        – name of the timezone which is used for timestamp column - ``DataFrame``


        Returns
        -------

            True if successful, False otherwise.

        Doc Author
        ----------
            TB
        """
        # TODO: Authentication & security refactoring
        if username:
            user_id_, token_, bucket_, org_, url_ = self._get_influxdb_credentials(username=username)
        else:
            user_id_, token_, bucket_, org_, url_ = self._get_influxdb_credentials(username=self.default_username)

        # replace None values with defaults
        token = token_ if not token else token
        org = org_ if not org else org
        url = url_ if not url else url
        bucket = bucket_ if not bucket else bucket

        try:
            with influxdb_client.InfluxDBClient(url=url, token=token, org=org) as client:
                write_api = client.write_api(write_options=SYNCHRONOUS)

                # write the data sequence to the bucket
                write_api.write(bucket=bucket, org=org, record_list=data, **df_kwargs)

                client.close()
                return True
        except Exception as e:
            logger.error(e)
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
    def from_pcap(file_path: Union[Path, str], db: Database, credentials: Dict = None) -> Union[pd.DataFrame, None]:
        """
        Loads data from a pcap file.
        """
        if not credentials:
            credentials = {}

        file_path = resolve_file_path(file_path)
        if file_path:
            cap = pyshark.FileCapture(file_path, keep_packets=False)

            # TODO: skip conversion to Line Protocol and write with DataFrame directly
            converted_cap = convert_Capture_to_Line(cap)
            if not db.write_to_InfluxDB(converted_cap, **credentials):
                return None

            return convert_Capture_to_DataFrame(cap)

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
