import numpy as np
import pytest
import datamol as dm
import zarr

from polaris.dataset import Dataset, MultiTaskBenchmarkSpecification, SingleTaskBenchmarkSpecification
from polaris.dataset import Modality
from polaris.utils import fs


def _get_zarr_archive(tmp_path, datapoint_per_array: bool):
    tmp_path = fs.join(str(tmp_path), "data.zarr")
    root = zarr.open_group(tmp_path, mode="w")
    group_a = root.create_group("A/")
    group_b = root.create_group("B/")

    def _populate_group(group):
        if datapoint_per_array:
            for i in range(100):
                group.array(i, data=np.random.random((2048,)))
        else:
            group.array("data", data=np.random.random((100, 2048)))

    _populate_group(group_a)
    _populate_group(group_b)

    root.attrs["C"] = {i: 0.0 for i in range(100)}
    root.attrs["name"] = "Test"
    root.attrs["description"] = "Go wild in your test cases with this awesome dataset"
    root.attrs["source"] = "Imagination"
    root.attrs["annotations"] = {"A": "MOLECULE_3D", "B": "IMAGE"}
    return tmp_path


@pytest.fixture(scope="module")
def test_data():
    return dm.data.freesolv()[:100]


@pytest.fixture(scope="module")
def test_dataset(test_data):
    return Dataset(
        table=test_data,
        name="Test",
        description="Go wild in your test cases with this awesome dataset",
        source="Datamol",
        annotations={
            "smiles": Modality.MOLECULE,
        },
    )


@pytest.fixture(scope="function")
def test_zarr_archive_multiple_arrays(tmp_path):
    return _get_zarr_archive(tmp_path, datapoint_per_array=True)


@pytest.fixture(scope="function")
def test_zarr_archive_single_array(tmp_path):
    return _get_zarr_archive(tmp_path, datapoint_per_array=False)


@pytest.fixture(scope="module")
def test_single_task_benchmark(test_dataset):
    train_indices = list(range(90))
    test_indices = list(range(90, 100))
    return SingleTaskBenchmarkSpecification(
        dataset=test_dataset,
        metrics=["mean_absolute_error", "mean_squared_error"],
        split=(train_indices, test_indices),
        target_cols="expt",
        input_cols="smiles",
    )


@pytest.fixture(scope="module")
def test_single_task_benchmark_multiple_test_sets(test_dataset):
    train_indices = list(range(90))
    test_indices = {"test_1": list(range(90, 95)), "test_2": list(range(95, 100))}
    return SingleTaskBenchmarkSpecification(
        dataset=test_dataset,
        metrics=["mean_absolute_error", "mean_squared_error"],
        split=(train_indices, test_indices),
        target_cols="expt",
        input_cols="smiles",
    )


@pytest.fixture(scope="module")
def test_multi_task_benchmark(test_dataset):
    # For the sake of simplicity, just use a small set of indices
    train_indices = list(range(90))
    test_indices = list(range(90, 100))
    return MultiTaskBenchmarkSpecification(
        dataset=test_dataset,
        metrics=["mean_absolute_error"],
        split=(train_indices, test_indices),
        target_cols=["expt", "calc"],
        input_cols="smiles",
    )
