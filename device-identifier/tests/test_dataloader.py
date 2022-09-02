from datetime import datetime

import pandas as pd
import pytest

from shbdeviceidentifier.dataloader import DataLoader


class TestDataLoader:
    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_influxdb(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_csv(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_pcap(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_generator(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_dict(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_labels_from_json(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_file(self):
        # TODO: implement
        assert True

    @pytest.mark.parametrize("devices_to_train", [["Google-Nest-Mini", "ESP-1DC41C"], None])
    def test_from_database(self, devices_to_train):
        params = {
            "_start": datetime.strptime("2022-08-01T11:40:00UTC", "%Y-%m-%dT%H:%M:%S%Z"),
            "_stop": datetime.strptime("2022-08-01T11:41:00UTC", "%Y-%m-%dT%H:%M:%S%Z"),
        }
        query = """
                            from(bucket: "network-traffic")
                            |> range(start: _start, stop: _stop)
                            |> filter(fn: (r) => r["_measurement"] == "packet")  
                        """
        train_df, train_labels = DataLoader.from_database(query, params, devices_to_train)

        assert isinstance(train_df, pd.DataFrame)
        assert isinstance(train_labels, pd.Series)
        assert not train_df.empty
        assert not train_labels.empty
