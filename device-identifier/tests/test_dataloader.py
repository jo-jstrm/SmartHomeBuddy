from datetime import datetime

import pandas as pd
import pytest

from shbdeviceidentifier.commands import read
from shbdeviceidentifier.dataloader import DataLoader
from shbdeviceidentifier.utilities.queries import EARLIEST_TIMESTAMP


class TestDataLoader:
    @pytest.mark.skip(reason="Included in test_from_database().")
    def test_from_influxdb(self):
        pass

    @pytest.mark.parametrize("file_path", ["dummy_csv"])
    def test_from_csv(self, file_path, request):
        file_path = request.getfixturevalue(file_path)
        df = DataLoader.from_csv(file_path)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    @pytest.mark.parametrize("file_path", ["dummy_pcap"])
    def test_from_pcap(self, file_path, request):
        file_path = request.getfixturevalue(file_path)
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

    @pytest.mark.parametrize("training_labels_path", ["dummy_labels_json"])
    def test_labels_from_json(self, training_labels_path, request):
        training_labels_path = request.getfixturevalue(training_labels_path)
        labels = DataLoader.labels_from_json(training_labels_path)

        assert isinstance(labels, pd.DataFrame)
        assert not labels.empty

    @pytest.mark.parametrize("training_data_path", ["dummy_pcap"])
    @pytest.mark.parametrize("training_labels_path", ["dummy_labels_json"])
    @pytest.mark.parametrize("devices_to_train", [["Google-Nest-Mini", "ESP-1DC41C"]])
    def test_from_file(self, training_data_path, training_labels_path, devices_to_train, request):
        training_data_path = request.getfixturevalue(training_data_path)
        training_labels_path = request.getfixturevalue(training_labels_path)
        df, labels = DataLoader.from_file(training_data_path, training_labels_path, devices_to_train)

        if devices_to_train:
            assert isinstance(df, pd.DataFrame)
            assert isinstance(labels, pd.Series)
            assert not df.empty
            assert not labels.empty

    @pytest.mark.parametrize("devices_to_train", [["Google-Nest-Mini", "ESP-1DC41C"]])
    @pytest.mark.parametrize("data_path", ["dummy_pcap"])
    def test_from_database(self, devices_to_train, data_path, db, request):
        data_path = request.getfixturevalue(data_path)

        db.start()
        read(db, data_path, "pcap")
        train_df, train_labels = DataLoader.from_database(from_timestamp=EARLIEST_TIMESTAMP,
                                                          to_timestamp=datetime.now(), measurement="main",
                                                          bucket="network-traffic", devices_to_train=devices_to_train)
        db.stop()

        # TODO: improve this test
        # Since `from_database` can return (None, None) this is still correct,
        # but does not tell us much about the actual purpose of the method.
        if isinstance(train_df, pd.DataFrame):
            assert isinstance(train_labels, pd.Series)
            # TODO: make sure db contains values and test for empty
            # [...]
            assert not train_df.empty
            assert not train_labels.empty
