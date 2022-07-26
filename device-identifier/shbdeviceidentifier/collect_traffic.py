# You can generate an API token from the "API Tokens Tab" in the UI
from typing import List

import logging
import pyshark
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

log = logging.getLogger("identifier")

token = "S_bFseW7ihLwo_rhz_BK_4OBSOGHarpQwiKxHs3JRiqcX31zoNoIGByCZV61yCjPYxngbNXAEh988brX9gg1Yg=="  # TODO secure
org = "smarthomebuddy"
bucket = "network-traffic"
url = "http://localhost:8086"


def collect_traffic():
    # TODO
    ...


def read_pcap(filepath: str, measurement: str = "packet") -> bool:
    cap = pyshark.FileCapture(filepath)

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
        layer_names = [l.layer_name for l in packet.layers]
        ## first layer (usually IP)
        if "ip" in layer_names:
            tags["ip_src"] = packet.ip.src
            tags["ip_dst"] = packet.ip.dst
        ## second layer (usually TCP or UDP)
        if "tcp" in layer_names:
            tags["tcp_src"] = packet.tcp.port
            tags["tcp_dst"] = packet.tcp.dstport
        elif "udp" in  layer_names:
            tags["udp_src"] = packet.udp.port
            tags["udp_dst"] = packet.udp.dstport

        line += "," + ",".join([f"{k}={v}" for k, v in sorted(tags.items())])
        line += " "  # end tag-set (or measurement if no tag-set is present)

        # fields
        fields = {
            "data_len": "0"
        }
        ## third layer (usually data)
        if "DATA" in layer_names:
            # access through attribute not possible, bc of pyshark implementation (capitalized layer name)
            fields["data_len"] = packet.layers[layer_names.index("DATA")].data_len

        line += ",".join([f"{k}={v}" for k, v in sorted(fields.items())])
        line += " "  # end fields-set

        # timestamp converted to nanoseconds from seconds (see influxdb timestamp precision (default: ns))
        line += packet.sniff_timestamp.replace(".", "")

        data.append(line)

    try:
        write_to_influxdb(data)
    except Exception as e:
        log.debug(e)
        return False
    return True


def write_to_influxdb(data: List[str]):
    with InfluxDBClient(url=url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        # write the data sequence to the bucket
        write_api.write(bucket, org, data)

        client.close()
