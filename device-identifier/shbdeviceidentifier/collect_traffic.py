# You can generate an API token from the "API Tokens Tab" in the UI
from typing import List

import pyshark
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

token = "S_bFseW7ihLwo_rhz_BK_4OBSOGHarpQwiKxHs3JRiqcX31zoNoIGByCZV61yCjPYxngbNXAEh988brX9gg1Yg=="  # TODO secure
org = "smarthomebuddy"
bucket = "network-traffic"
url = "http://localhost:8086"


def collect_traffic():
    # TODO
    ...


def read_pcap(filepath: str, tags: dict = None, fields: dict = None) -> bool:
    cap = pyshark.FileCapture(filepath)

    # create influx db Line Protocol sequence
    # one string per packet
    data: List[str] = []
    for packet in cap:
        line = ""

        # measurement
        line += "packet"

        # tags
        if tags:
            line += "," + ",".join([f"{k}={v}" for k, v in sorted(tags.items())])
        line += " "  # end tag-set (or measurement if no tag-set is present)

        # fields
        if not fields:
            fields = {
                # first layer (usually IP)
                f"{packet.layers[1].layer_name}_src": packet.layers[1].src,
                f"{packet.layers[1].layer_name}_dst": packet.layers[1].dst,
                # second layer (usually TCP/UDP)
                f"{packet.layers[2].layer_name}_src": packet.layers[2].src,
                f"{packet.layers[2].layer_name}_dst": packet.layers[2].dst,
                # third layer (usually DATA)
                f"{packet.layers[3].layer_name}_len": packet.layers[3].data_len  # TODO: check if this is correct
            }
        line += ",".join([f"{k}={v}" for k, v in sorted(fields.items())])
        line += " "  # end fields-set

        # timestamp
        line += packet.sniff_timestamp

        print(line)

        data.append(line)

    try:
        write_to_influxdb(data)
    except Exception as e:
        print(e)
        return False
    return True


def write_to_influxdb(data: List[str]):
    with InfluxDBClient(url=url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        # write the data sequence to the bucket
        write_api.write(bucket, org, data)

        client.close()
