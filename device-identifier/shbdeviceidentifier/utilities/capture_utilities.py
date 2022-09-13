from typing import List, Optional, Dict

import numba as nb
import numpy as np
import pandas as pd
from loguru import logger
from numba_progress import ProgressBar
from scapy.all import TCP, UDP, IP
from scapy.packet import Packet

from .logging_utilities import spinner


# noinspection PyPep8Naming
@nb.jit(forceobj=True, parallel=True)
def _convert_Capture_to_DataFrame_JIT(cap, num_of_packets, progress_proxy) -> pd.DataFrame:
    """
    The _convert_Capture_to_DataFrame_JIT function is the JIT compiled part of the
     convert_Capture_to_DataFrame function.
    It is used to speed up the conversion of a pyshark.capture.Capture object to a pandas.DataFrame.
    The function is JIT compiled using numba.
    The function is not intended to be used directly, but within a tqdm progress bar.
    """
    src_series = np.empty((num_of_packets,), dtype=object)
    dst_series = np.empty((num_of_packets,), dtype=object)
    ts_series = np.empty((num_of_packets,), dtype=pd.Timestamp)
    protocol_series = np.empty((num_of_packets,), dtype=object)
    data_len_series = np.empty((num_of_packets,), dtype="uint16")

    for i in nb.prange(num_of_packets):
        src_series[i] = _get_address_from_scapy_packet(cap[i], src=True)
        dst_series[i] = _get_address_from_scapy_packet(cap[i], src=False)
        ts_series[i] = _get_timestamp_from_scapy_packet(cap[i])
        protocol_series[i] = _get_protocol_from_scapy_packet(cap[i])
        data_len_series[i] = _get_data_len_from_scapy_packet(cap[i])
        progress_proxy.update(1)

    df = pd.DataFrame(
        {"src": src_series, "dst": dst_series, "L4_protocol": protocol_series, "data_len": data_len_series},
        index=ts_series,
    )

    # Filter out packets that do not have a transport layer protocol
    df = df[df["L4_protocol"].astype(bool)]

    # Create stream IDs
    # TODO: check performance cost of this
    df["conv"] = [" <-> ".join(i) for i in np.sort(df[["src", "dst"]], axis=1)]
    df = df.assign(stream_id=df.groupby(["conv"]).ngroup())
    df.drop(columns=["conv"], inplace=True)
    df["stream_id"] = df["stream_id"].astype("uint16")

    return df


# noinspection PyPep8Naming
def convert_Capture_to_DataFrame(cap) -> pd.DataFrame:
    num_of_packets = len(cap)
    spinner.stop()
    with ProgressBar(update_interval=1, total=num_of_packets, desc="Converting file to pandas DataFrame") as progress:
        df = _convert_Capture_to_DataFrame_JIT(cap, num_of_packets, progress)
    return df


# noinspection PyPep8Naming
def convert_Capture_to_Line(cap, measurement: str = "packet", additional_tags: Dict = None) -> List[str]:
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
        fields = {"data_len": "0"}
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


def _conversations_string_to_list(conversations: str, tag: Dict = None) -> Optional[List[Dict]]:
    """Converts a conversations string to a list of dictionaries"""
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


@nb.jit(forceobj=True)
def _get_data_len_from_scapy_packet(packet: Packet) -> np.uint16:
    """
    Returns the length of the data in a scapy packet in bytes.
    """
    # TODO: decide which length to return
    # Currently returning the size of the Ethernet Frame!
    return np.uint16(len(packet))


@nb.jit(forceobj=True)
def _get_protocol_from_scapy_packet(packet: Packet) -> str:
    """
    Returns the transport layer protocol name of a scapy packet.
    """
    if TCP in packet:
        return "tcp"
    elif UDP in packet:
        return "udp"
    else:
        return ""


@nb.jit(forceobj=True)
def _get_timestamp_from_scapy_packet(packet: Packet) -> pd.Timestamp:
    """
    Returns the timestamp of a packet in nanoseconds.
    """
    time = pd.NaT

    if hasattr(packet, "time"):
        # Cannot use fromtimestamp with microseconds, so we split the timestamp up and
        # merge them again explicitly afterwards
        timestamp, fractions = str(packet.time).split(".")
        time = pd.Timestamp.fromtimestamp(int(timestamp))

        time = pd.Timestamp(
            year=time.year,
            month=time.month,
            day=time.day,
            hour=time.hour,
            minute=time.minute,
            second=time.second,
            microsecond=int(fractions),
        )
    return time


@nb.jit(forceobj=True)
def _get_address_from_scapy_packet(packet: Packet, src: bool = True) -> str:
    """
    Returns the source address and port of a scapy packet.
    Per default the source address is returned. Set src to `False` to get the destination address.
    """
    addr: str = ""

    if not IP in packet:
        return addr

    if src:
        if hasattr(packet[IP], "src"):
            addr = str(packet[IP].src)
            if hasattr(packet[IP], "sport"):
                addr += ":" + str(packet[IP].sport)
    else:
        if hasattr(packet[IP], "dst"):
            addr = str(packet[IP].dst)
            if hasattr(packet[IP], "dport"):
                addr += ":" + str(packet[IP].dport)

    return addr
