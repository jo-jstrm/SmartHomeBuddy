from datetime import datetime

import pandas as pd
import pytest

from shbdeviceidentifier.dataloader import DataLoader
from shbdeviceidentifier.utilities.app_utilities import DATA_DIR


@pytest.fixture
def dummy_pcap():
    return (DATA_DIR / "pcaps" / "dummy.pcap").as_posix()


@pytest.fixture
def dummy_labels_json():
    return (DATA_DIR / "pcaps" / "dummy_labels.json").as_posix()


class TestDataLoader:
    @pytest.mark.skip(reason="Included in test_from_database()")
    def test_from_influxdb(self):
        pass

    @pytest.mark.parametrize("file_path", [dummy_pcap()])
    def test_from_csv(self, file_path):
        df = DataLoader.from_csv(file_path)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    @pytest.mark.parametrize("file_path", [dummy_pcap()])
    def test_from_pcap(self, file_path):
        df = DataLoader.from_pcap(file_path)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_generator(self):
        # TODO: implement
        assert True

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_dict(self):
        # TODO: implement
        assert True

    @pytest.mark.parametrize("training_labels_path", [dummy_labels_json()])
    def test_labels_from_json(self, training_labels_path):
        labels = DataLoader.labels_from_json(training_labels_path)

        assert isinstance(labels, pd.DataFrame)
        assert not labels.empty

    @pytest.mark.parametrize("training_data_path", [dummy_pcap()])
    @pytest.mark.parametrize("training_labels_path", [dummy_labels_json()])
    @pytest.mark.parametrize("devices_to_train", [["Google-Nest-Mini", "ESP-1DC41C"], None])
    def test_from_file(self, training_data_path, training_labels_path, devices_to_train):
        df, labels = DataLoader.from_file(training_data_path, training_labels_path, devices_to_train)

        if devices_to_train:
            assert isinstance(df, pd.DataFrame)
            assert isinstance(labels, pd.Series)
            assert not df.empty
            assert not labels.empty

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

        if devices_to_train:
            assert isinstance(train_df, pd.DataFrame)
            assert isinstance(train_labels, pd.Series)
            assert not train_df.empty
            assert not train_labels.empty
