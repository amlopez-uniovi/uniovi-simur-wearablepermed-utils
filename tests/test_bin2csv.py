import pytest
from uniovi_simur_wearablepermed_utils.bin2csv import bin2csv
import filecmp


def test_matrix_bin2csv():
    res = bin2csv('tests/data_import/MATA00.bin', 'tests/data_import/MATA00_conversion_result.csv')
    assert res == 0 and filecmp.cmp('tests/data_import/MATA00_expected_conversion.csv', 'tests/data_import/MATA00_conversion_result.csv', shallow=False)
