import platform
import shlex
import subprocess
from pathlib import Path
from typing import List, Union, Optional, Dict, Tuple

import pandas as pd
import pyshark
from loguru import logger
from pyshark.capture.capture import Capture

from shbdeviceidentifier.utilities.app_utilities import resolve_file_path


def collect_traffic(interface: Union[Path, str] = None, time: int = -1,
                    output_file: Union[Path, str] = None) -> Optional[pyshark.capture.capture.Capture]:
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
    # TODO: implement
    return pd.DataFrame.from_dict({"Test": [1, 2, 3]})


# noinspection PyPep8Naming
def convert_Capture_to_Line(cap: Capture, measurement: str = "packet", additional_tags: Dict = None) -> List[str]:
    """
    The write_cap_to_db function writes a pyshark.capture.Capture object to an InfluxDB database
        using the Line Protocol format (see https://v2.docs.influxdata.com/v2.0/write-data/#line-protocol).

    Parameters
    ----------
        cap:Capture
            A pyshark capture object containing packets to be written to the database.
        additional_tags: Dict = None
            A dictionary containing additional tags to be added to each line.
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
        # add additional tags
        if additional_tags:
            tags.update(additional_tags)
        line += "," + ",".join([f"{k}={v}" for k, v in sorted(tags.items())])
        line += " "  # end tag-set (or measurement if no tag-set is present)

        # fields
        fields = {
            "data_len": "0"
        }
        # third layer (usually data)
        if "DATA" in layer_names:
            # access through attribute not possible, bc of pyshark implementation (capitalized layer name)
            try:
                fields["data_len"] = packet.layers[layer_names.index("DATA")].data_len
            except AttributeError:
                fields["data_len"] = 0

        line += ",".join([f"{k}={v}" for k, v in sorted(fields.items())])
        line += " "  # end fields-set

        # timestamp converted to nanoseconds from seconds (see influxdb timestamp precision (default: ns))
        line += packet.sniff_timestamp.replace(".", "")

        data.append(line)

    return data


def get_conversations(file_path: Union[str, Path]) -> Tuple[Optional[List[dict]], Optional[List[dict]]]:
    """
    Gets the conversations statistics from tshark.
    Returns it as a list of protocols containing a dictionary per conversation.
    Ordered as tcp, udp.
    """
    file_path = resolve_file_path(file_path)
    tshark_path = resolve_file_path(pyshark.tshark.tshark.get_process_path())
    if tshark_path and file_path:
        # TODO: add support for other operating systems and possibly transport protocols

        # Make sure arguments for tshark call are split properly
        args_tcp = shlex.split(tshark_path.as_posix() + " -q -z conv,tcp -r " + file_path.as_posix())
        args_udp = shlex.split(tshark_path.as_posix() + " -q -z conv,udp -r " + file_path.as_posix())

        # Run tshark and get output as text
        res_tcp = subprocess.run(args_tcp, capture_output=True, text=True).stdout
        res_udp = subprocess.run(args_udp, capture_output=True, text=True).stdout

        # Parse output into list of dictionaries
        res_tcp = _conversations_string_to_list(res_tcp, tag={'protocol': 'tcp'})
        res_udp = _conversations_string_to_list(res_udp, tag={'protocol': 'udp'})

        # Combine results
        return res_tcp, res_udp


def _conversations_string_to_list(conversations: str, tag: Dict = None) -> Optional[List[Dict]]:
    """ Converts a conversations string to a list of dictionaries """
    # Split into lines
    conv = conversations.split("\n")

    # Remove header lines
    # TODO: improve robustness by searching for header lines
    conv = conv[5:-2]

    # Split lines into conversations
    conversations = [line.split() for line in conv]

    # Convert conversations to dictionaries
    # TODO: improve robustness (rm hard coded indices)
    res = []
    for conv in conversations:
        try:
            conv_dict = {
                "src": conv[0],
                "dst": conv[2],
                "incoming_frames": conv[3],
                "incoming_bytes": conv[4] + " " + conv[5],
                "outgoing_frames": conv[6],
                "outgoing_bytes": conv[7] + " " + conv[8],
                "total_frames": conv[9],
                "total_bytes": conv[10] + " " + conv[11],
                "relative_start": conv[12],
                "duration": conv[13],
            }
            if tag:
                conv_dict.update(tag)
            res.append(conv_dict)
        except IndexError as e:
            logger.warning(f"Could not parse conversation: {conv}.")
            logger.debug(e)

    return res if res else None


def get_capinfos(file_path: Union[str, Path]) -> Optional[Dict]:
    """
    Gets the capinfos statistics from tshark.
    Returns it as a dictionary.
    """
    file_path = resolve_file_path(file_path)
    tshark_path = resolve_file_path(pyshark.tshark.tshark.get_process_path())

    system = platform.system()
    if system == 'Windows':
        capinfos_path = 'capinfos.exe'
    else:
        capinfos_path = 'capinfos'
    capinfos_path = resolve_file_path(tshark_path.parents[0] / capinfos_path)

    if capinfos_path and file_path:
        # Make sure arguments for tshark call are split properly
        args = shlex.split(capinfos_path.as_posix() + " " + file_path.as_posix())

        # Run tshark and get output as text
        res = subprocess.run(args, capture_output=True, text=True).stdout

        # Parse output into dictionary
        return _capinfos_string_to_dict(res)


def _capinfos_string_to_dict(capinfos: str) -> Optional[Dict]:
    capinfos = capinfos.split("\n")[:-1]
    capinfos_dict = {}

    for line in capinfos[:-7]:
        try:
            k, v = line.split(":", 1)
            k = k.strip().replace(" ", "_")
            capinfos_dict[k] = v.strip()
        except ValueError as e:
            logger.warning(f"Could not parse capinfos line: {line}")
            logger.debug(e)

    # TODO: add support for multiple interfaces
    # Add interface info
    interface_dict = {}
    for line in capinfos[-6:]:
        try:
            k, v = line.split("=", 1)
            k = k.strip().replace(" ", "_")
            interface_dict[k] = v.strip()
        except ValueError as e:
            logger.warning(f"Could not parse capinfos interface line: {line}")
            logger.debug(e)

    capinfos_dict["interfaces"] = [interface_dict]

    return capinfos_dict if capinfos_dict else None
