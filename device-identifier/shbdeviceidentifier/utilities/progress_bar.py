from numba_progress import ProgressBar

from ..rpc.client import ReadUpdateClient


class PacketProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.client = ReadUpdateClient()
        self.total_num_packets = kwargs["total"]

    def update(self, value: int):
        super().update(value)
        pct = int(100 * value / self.total_num_packets)
        self.client.send_update(pct)
