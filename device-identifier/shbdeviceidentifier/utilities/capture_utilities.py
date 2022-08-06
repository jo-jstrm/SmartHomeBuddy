from pathlib import Path
from typing import List, Union

import pandas as pd
import pyshark
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from loguru import logger
from pyshark.capture.capture import Capture


def collect_traffic(interface: Union[Path, str] = None, time: int = -1,
                    output_file: Union[Path, str] = None) -> Union[pyshark.capture.capture.Capture, None]:
    """
    The collect_traffic function is used to capture traffic on a specified interface for a specified amount of time.
    Either the interface_id or the interface name must be specified.
    If no or non-positive time is specified, it will run indefinitely until the user stops it.
    It can also write the captured packets to an output file if one is provided.

    Parameters
    ----------
        interface: str = None
            The interface to capture traffic on
        time: int = 0
            The time limit for the traffic capture in seconds
        output_file: Union[Path, str]=None
            The path to the output file

    Returns
    -------

        A capture object

    Doc Author
    ----------
        TB
    """
    if not isinstance(interface, Path) and interface.isdigit():
        ix = int(interface)
    else:
        interface = Path(interface)
        available_interfaces = [Path(face) for face in pyshark.LiveCapture().interfaces]
        try:
            ix = available_interfaces.index(interface)
        except ValueError:
            logger.error(f"Interface {interface} not found. Available interfaces are {available_interfaces}.")
            return None

    interface = pyshark.LiveCapture().interfaces[ix]

    if output_file:
        output_file = Path(output_file).resolve()
        logger.info(f"Capturing traffic on interface {interface} and saving to {output_file}.")
    else:
        logger.info(f"Capturing traffic on interface {interface}. No output file specified.")

    cap = pyshark.LiveCapture(interface=interface, output_file=output_file)

    if time > 0:
        cap.sniff(timeout=time)
    else:
        logger.error("Continuously capturing traffic is currently not supported.")
        # TODO: add continuous capture support
        # logger.info("Sniffing indefinitely... (Ctrl-C to stop)")
        # gen = cap.sniff_continuously()
    return cap


# noinspection PyPep8Naming
def convert_Capture_to_DataFrame(cap: Capture) -> pd.DataFrame:
    pass


# noinspection PyPep8Naming
def convert_Capture_to_Line(cap: Capture, measurement: str = "packet") -> List[str]:
    """
    The write_cap_to_db function writes a pyshark.capture.Capture object to an InfluxDB database
        using the Line Protocol format (see https://v2.docs.influxdata.com/v2.0/write-data/#line-protocol).

    Parameters
    ----------
        cap:Capture
            A pyshark capture object containing packets to be written to the database.
        measurement:str="packet"
            The name of the measurement.

    Returns
    -------

        List of Line Protocol strings

    Doc Author
    ----------
        TB
    """
    # TODO: standardize with other convert functions

    # create influx db Line Protocol sequence
    # one string per packet
    data: List[str] = []
    for packet in cap:
        line = ""

        # measurement
        line += measurement

        # tags
        tags = {
            "ip_src": "None",
            "ip_dst": "None",
            "tcp_src": "None",
            "tcp_dst": "None",
            "udp_src": "None",
            "udp_dst": "None",
        }
        layer_names = [layer.layer_name for layer in packet.layers]
        # first layer (usually IP)
        if "ip" in layer_names:
            tags["ip_src"] = packet.ip.src
            tags["ip_dst"] = packet.ip.dst
        # second layer (usually TCP or UDP)
        if "tcp" in layer_names:
            tags["tcp_src"] = packet.tcp.port
            tags["tcp_dst"] = packet.tcp.dstport
        elif "udp" in layer_names:
            tags["udp_src"] = packet.udp.port
            tags["udp_dst"] = packet.udp.dstport

        line += "," + ",".join([f"{k}={v}" for k, v in sorted(tags.items())])
        line += " "  # end tag-set (or measurement if no tag-set is present)

        # fields
        fields = {
            "data_len": "0"
        }
        # third layer (usually data)
        if "DATA" in layer_names:
            # access through attribute not possible, bc of pyshark implementation (capitalized layer name)
            fields["data_len"] = packet.layers[layer_names.index("DATA")].data_len

        line += ",".join([f"{k}={v}" for k, v in sorted(fields.items())])
        line += " "  # end fields-set

        # timestamp converted to nanoseconds from seconds (see influxdb timestamp precision (default: ns))
        line += packet.sniff_timestamp.replace(".", "")

        data.append(line)

    return data


def write_to_influxdb(data: Union[List[str], pd.DataFrame], bucket: str, org: str, token: str, url: str, **df_kwargs):
    """
    The write_to_influxdb function writes data to an InfluxDB bucket.

    Parameters
    ----------
        data:List[str]
            Data to be written to influxdb. Should be a list of Line Protocol strings,
            see Line Protocol format (see https://v2.docs.influxdata.com/v2.0/write-data/#line-protocol)
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
                    The column can be defined as a :class:`~str` value formatted as `2018-10-26`, `2018-10-26 12:00`,
                    `2018-10-26 12:00:00-05:00` or other formats and types supported by `pandas.to_datetime`
                data_frame_timestamp_timezone
                    – name of the timezone which is used for timestamp column - ``DataFrame``


    Returns
    -------

        Nothing

    Doc Author
    ----------
        TB
    """
    with InfluxDBClient(url=url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        # write the data sequence to the bucket
        write_api.write(
            bucket=bucket,
            org=org,
            record_list=data,
            **df_kwargs
        )

        client.close()
