# for classes that are generic in stubs but not at runtime see
# https://mypy.readthedocs.io/en/stable/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime
from __future__ import annotations

import logging
import os
import platform
import traceback

import requests
import sqlite3
import subprocess
from dataclasses import dataclass
from pathlib import Path
from requests.adapters import HTTPAdapter, Retry
from sqlite3 import Error
from subprocess import Popen
from typing import Union, Iterable, Generator, List, Optional

import influxdb
import influxdb_client
import pandas as pd
from influxdb_client.client.write_api import SYNCHRONOUS
from loguru import logger
from scapy.all import rdpcap

from .utilities.app_utilities import resolve_file_path
from .utilities.capture_utilities import convert_Capture_to_DataFrame
from .utilities.logging_utilities import spinner


@dataclass
class InfluxDbUser:
    name: str
    password: str
    token: str
    bucket: str
    org: str
    url: str


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

    def start(self):
        self.influx_process = self.start_InfluxDB()
        self._create_SQLite_tables()
        if not self._is_InfluxDB_setup():
            self._do_initial_db_setup()

    def _run_influxdb_setup(self) -> Optional[InfluxDbUser]:
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
            name=self.default_username,
            password=self.influxdb_pw,
            token=token,
            bucket=self.influxdb_bucket,
            org=self.influxdb_org,
            url=f"http://{self.influxdb_host}:{self.influxdb_port}",
        )

    def _is_InfluxDB_setup(self) -> bool:
        sql_find_influxdb_user = """SELECT id FROM users WHERE username = ?"""
        # Find user values in SQLite DB.
        influxdb_user_id = self.query_SQLiteDB(sql_find_influxdb_user, (self.default_username,))
        logger.trace(f"The following list should be empty: influxdb_user_id = {influxdb_user_id}")
        return True if influxdb_user_id else False

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
        logger.success("Completed initial DB setup.")

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
        sql_create_devices_table = """CREATE TABLE IF NOT EXISTS devices (
                                                   id integer PRIMARY KEY,
                                                   device_name VARCHAR NOT NULL,
                                                   mac_address VARCHAR UNIQUE                                             
                                               );"""
        conn = self._get_SQLite_connection()
        if conn:
            # Users table
            self.query_SQLiteDB(sql_create_users_table)
            logger.debug("Table 'users' created successfully.")
            # InfluxDB table
            self.query_SQLiteDB(sql_create_influxdb_table)
            logger.debug("Table 'influxdb' created successfully.")
            # Devices table
            self.query_SQLiteDB(sql_create_devices_table)
            logger.debug("Table 'devices' created successfully.")

    def _get_InfluxDB_connection(self, **client_kwargs) -> Optional[influxdb.InfluxDBClient]:
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

    def _get_influxdb_credentials(self, user_id: int = 1, user_name: str = "") -> list:
        """
        Get the credentials for the InfluxDB instance from the main SQLite database.
        """
        # Needs to match the order of the sql_add_user_influxdb query
        search_user_credentials = (
            "SELECT user_id, token, bucket, org, url "
            "FROM users u JOIN influxdb i on u.id = i.user_id "
            "WHERE u.id = ? OR u.username = ?"
        )
        params = (user_id, user_name)
        query_result = self.query_SQLiteDB(search_user_credentials, params)
        if query_result:
            return query_result[0]
        else:
            logger.warning(f"Could not find credentials for user id '{user_id}' or user '{user_name}'.")
            logger.debug(f"Query result: {query_result}.")

    def _get_SQLite_connection(self) -> sqlite3.Connection:
        """create a database connection to a SQLite database"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            logger.debug(f"Failed to connect to SQLite database at {self.db_file}. \n{e}")
        return conn

    def _store_InfluxDB_user(self, user: InfluxDbUser):
        """Inserts the given user into the influxdb table of the SQLite DB."""
        sql_add_user_users = """INSERT OR IGNORE INTO users (username)
                                VALUES(?);"""
        sql_get_user_id = """SELECT id FROM users WHERE username = ?"""
        sql_add_user_influxdb = """INSERT OR IGNORE INTO influxdb (user_id, token, bucket, url, org)
                                   VALUES(?,?,?,?,?);"""
        # Add user to the users table
        self.query_SQLiteDB(sql_add_user_users, [user.name])
        # We could hard code user_id = 1, but this seems more robust.
        user_id = self.query_SQLiteDB(sql_get_user_id, [user.name])[0][0]
        # Add user credentials to influxdb table in SQLite DB.
        self.query_SQLiteDB(
            sql_add_user_influxdb,
            [user_id, user.token, user.bucket, user.url, user.org],
        )
        logger.debug(f"User credentials added successfully for {(user_id, user.name)}.")

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
        user_id, token, bucket, org, url = self._get_influxdb_credentials(user_name=self.default_username)
        client = self._get_InfluxDB_connection(token=token, org=org, url=url)
        if client:
            return client.query(query, params, bind_params)

    def query_SQLiteDB(self, query: str, params: Iterable = None) -> Optional[List]:
        """
        Queries the SQLite database.
        """
        conn = self._get_SQLite_connection()
        if not conn:
            return
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
        except Error:
            lines = traceback.format_exc().splitlines()
            for line in lines:
                logger.error(line)
            logger.error(f"The supplied statements are: {params}")

    def query(self, query: str, params: dict = None, bind_params: dict = None, db="influx") -> Optional[List]:
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
            user_id_, token_, bucket_, org_, url_ = self._get_influxdb_credentials(user_name=username)
        else:
            user_id_, token_, bucket_, org_, url_ = self._get_influxdb_credentials(user_name=self.default_username)
        # replace None values with defaults
        token = token_ if not token else token
        org = org_ if not org else org
        url = url_ if not url else url
        bucket = bucket_ if not bucket else bucket

        try:
            with influxdb_client.InfluxDBClient(url=url, token=token, org=org) as client:
                write_api = client.write_api(write_options=SYNCHRONOUS)
                if isinstance(data, pd.DataFrame):
                    logger.debug(
                        f"Writing DataFrame of shape {data.shape} to InfluxDB, bucket {bucket}, org {org}."
                        f" Using {df_kwargs}."
                    )
                else:
                    logger.debug(f"Writing {len(data)} lines of data to InfluxDB, bucket {bucket}, org {org}.")
                # write the data sequence to the bucket
                write_api.write(bucket=bucket, org=org, record=data, **df_kwargs)
                client.close()
        except Exception as e:
            lines = traceback.format_exc().splitlines()
            for line in lines:
                logger.error(line)
            return False

        return True

    #####################
    ###### Devices ######
    #####################

    def write_device(self, name, mac_address):
        sql_write_device = """INSERT INTO devices (device_name, mac_address)
                                VALUES (?,?);"""
        self.query_SQLiteDB(sql_write_device, [name, mac_address])

    def get_all_devices(self):
        sql_get_devices = """SELECT device_name, mac_address FROM devices;"""
        devices = self.query_SQLiteDB(sql_get_devices)
        return devices


# noinspection PyPep8Naming
class DataLoader:
    """
    Class for loading data from various sources into a pandas DataFrame.
    """

    @staticmethod
    def from_InfluxDB(self, query: str, params: dict = None, bind_params: dict = None) -> Optional[List]:
        """
        Loads data from the InfluxDB database.
        """
        ...

    @staticmethod
    def from_csv(file_path: Union[Path, str], **kwargs) -> Optional[pd.DataFrame]:
        """
        Loads data from a CSV file.
        """
        file_path = resolve_file_path(file_path)
        if file_path:
            return pd.read_csv(file_path, **kwargs)

    @staticmethod
    def from_pcap(file_path: Union[Path, str]) -> Optional[pd.DataFrame]:
        """
        Loads data from a pcap file.
        """
        file_path = resolve_file_path(file_path)
        # Get the file size in Gigabyte
        file_size = os.path.getsize(file_path) * 1e-9
        spinner_text = "Reading file."
        if file_size > 0.25:
            spinner_text += f" This may take a while, since your file exceeds 250 MB (~{file_size:.2f} GB)."
        spinner.text = spinner_text
        spinner.start()
        if file_path:
            # Read pcap
            cap = rdpcap(file_path.as_posix())
            df = convert_Capture_to_DataFrame(cap)
            if not df.empty:
                return df

    @staticmethod
    def from_generator(generator: Generator) -> Optional[pd.DataFrame]:
        """
        Loads data from a generator.
        """
        ...

    @staticmethod
    def from_dict(data: dict) -> Optional[pd.DataFrame]:
        """
        Constructs a Dataset from data in memory.
        """
        ...

    @staticmethod
    def labels_from_json(file_path: Union[Path, str]) -> Optional[pd.DataFrame]:
        """
        Loads labels from a JSON file.
        """
        file_path = resolve_file_path(file_path)
        if file_path:
            return pd.read_json(file_path, orient="index")
        else:
            return None
