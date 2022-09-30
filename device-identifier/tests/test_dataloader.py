from datetime import datetime

import pandas as pd
import pytest
import pytest_check as check

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
        check.is_true(isinstance(df, pd.DataFrame))
        check.is_true(not df.empty)

    @pytest.mark.parametrize("file_path", ["dummy_pcap"])
    def test_from_pcap(self, file_path, request):
        file_path = request.getfixturevalue(file_path)
        df = DataLoader.from_pcap(file_path)
        check.is_true(isinstance(df, pd.DataFrame))
        check.is_true(not df.empty)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_generator(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.skip(reason="Not implemented yet.")
    def test_from_dict(self):
        # TODO: implement
        check.is_true(True)

    @pytest.mark.parametrize("training_labels_path", ["dummy_labels_json"])
    def test_labels_from_json(self, training_labels_path, request):
        training_labels_path = request.getfixturevalue(training_labels_path)
        labels = DataLoader.labels_from_json(training_labels_path)

        check.is_true(isinstance(labels, pd.DataFrame))
        check.is_true(not labels.empty)

    @pytest.mark.parametrize("training_data_path", ["dummy_pcap"])
    @pytest.mark.parametrize("training_labels_path", ["dummy_labels_json"])
    @pytest.mark.parametrize("devices_to_train", [["Google-Nest-Mini", "ESP-1DC41C"]])
    def test_from_file(self, training_data_path, training_labels_path, devices_to_train, request):
        training_data_path = request.getfixturevalue(training_data_path)
        training_labels_path = request.getfixturevalue(training_labels_path)
        df, labels = DataLoader.from_file(training_data_path, training_labels_path, devices_to_train)

        if devices_to_train:
            check.is_true(isinstance(df, pd.DataFrame))
            check.is_true(isinstance(labels, pd.Series))
            check.is_true(not df.empty)
            check.is_true(not labels.empty)

    @pytest.mark.parametrize("devices_to_train", [["Google-Nest-Mini", "ESP-1DC41C"]])
    @pytest.mark.parametrize("data_path", ["dummy_pcap"])
    def test_from_database(self, devices_to_train, data_path, db, request):
        data_path = request.getfixturevalue(data_path)

        db.start()
        read(db, data_path, "pcap")
        train_df, train_labels = DataLoader.from_database(
            from_timestamp=EARLIEST_TIMESTAMP,
            to_timestamp=datetime.now(),
            measurement="main",
            bucket="network-traffic",
            devices_to_train=devices_to_train,
        )
        db.stop()

        # TODO: improve this test
        # Since `from_database` can return (None, None) this is still correct,
        # but does not tell us much about the actual purpose of the method.
        if isinstance(train_df, pd.DataFrame):
            check.is_true(isinstance(train_labels, pd.Series))
            # TODO: make sure db contains values and test for empty
            # [...]
            check.is_true(not train_df.empty)
            check.is_true(not train_labels.empty)
