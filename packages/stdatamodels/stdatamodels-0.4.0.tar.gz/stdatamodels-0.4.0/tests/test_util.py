from datetime import datetime, timedelta

import pytest

import asdf
from astropy.io import fits
import numpy as np
from numpy.testing import assert_array_equal
from asdf.tags.core import Software, HistoryEntry

from stdatamodels import util


def test_gentle_asarray_array_input():
    """
    Test gentle_asarray with various forms of np.ndarray input,
    which may need to be cast to a different data type.
    """
    # Array that already bears the correct dtype:
    inp = np.array([1, 2, 3, 4], dtype=np.int16)
    result = util.gentle_asarray(inp, dtype=np.int16)
    assert result.dtype == np.int16
    assert_array_equal(result, inp)

    # This will require casting, since int8 != int16:
    result = util.gentle_asarray(inp, dtype=np.int8)
    assert result.dtype == np.int8
    assert_array_equal(result, inp)

    # Test broadcasting the same 1D array to a recarray with
    # two columns.  The input array should be copied into
    # each column and cast as necessary:
    dtype = np.dtype([("col1", np.int16), ("col2", np.float32)])
    result = util.gentle_asarray(inp, dtype=dtype)
    assert result.dtype == dtype
    assert result["col1"].dtype == np.int16
    assert_array_equal(result["col1"], np.array([1, 2, 3, 4], dtype=np.int16))
    assert result["col2"].dtype == np.float32
    assert_array_equal(result["col1"], np.array([1, 2, 3, 4], dtype=np.float32))


def test_gentle_asarray_recarray_input():
    """
    Test gentle_asarray input that is already an np.recarray.
    """
    # This is just the simple case where the dtype already matches
    # the desired output, but it follows a different code path
    # from array input:
    dtype = np.dtype([("col1", np.int16), ("col2", np.float32)])
    inp = np.array([1, 2, 3, 4], dtype=dtype)
    result = util.gentle_asarray(inp, dtype=dtype)
    assert result.dtype == dtype
    assert_array_equal(result, inp)


def test_gentle_asarray_fits_rec_input():
    """
    Test gentle_asarray with FITS_rec array input.
    """
    # 'e' is the FITS data type code for single-precision float:
    cols = [fits.Column("col1", format="e", array=np.array([1, 2, 3, 4]))]
    inp = fits.FITS_rec.from_columns(cols)
    out_dtype = np.dtype([("col1", np.float32)])
    result = util.gentle_asarray(inp, dtype=out_dtype)
    assert result.dtype == out_dtype
    assert_array_equal(result, inp)


def test_gentle_asarray_fits_rec_pseudo_unsigned(tmp_path):
    """
    Test gentle_asarray handling of a FITS_rec with a pseudo unsigned
    integer column, which is a special case due to a bug in astropy.
    """
    # 'j' is the FITS data type code for 32-bit integer.  A column
    # is only considered "pseudo unsigned" for certain values of
    # bezero, one of which is 2**31.
    cols = [fits.Column("col1", format="j", array=np.array([1, 2, 3, 4], np.uint32), bzero=2**31)]
    inp = fits.FITS_rec.from_columns(cols)
    out_dtype = np.dtype([("col1", np.uint32)])
    result = util.gentle_asarray(inp, dtype=out_dtype)
    # If not handled, the astropy bug would result in a signed
    # int column dtype:
    assert result["col1"].dtype == np.uint32
    assert result["col1"][0] == 1
    assert result["col1"][1] == 2
    assert result["col1"][2] == 3
    assert result["col1"][3] == 4

    # This tests the case where a table with a pseudo unsigned integer column
    # is opened from a FITS file and needs to be cast.  This requires special
    # handling on our end to dodge the bug.
    file_path = tmp_path / "test.fits"

    data = np.array([(0,)], dtype=[("col1", np.uint16)])
    hdu = fits.BinTableHDU()
    hdu.data = data
    hdul = fits.HDUList([fits.PrimaryHDU(), hdu])
    hdul.writeto(file_path)

    with fits.open(file_path) as hdul:
        result = util.gentle_asarray(hdul[-1].data, dtype=[("col1", np.uint32)])
        # Without the fix, the value in the array would be 128 due to bzero
        # shift being applied twice.
        assert result[0][0] == 0


def test_gentle_asarray_nested_array():
    """
    Test gentle_asarray with nested arrays in one of the record
    fields.
    """
    # '2f' is a numpy data type code for an array of two 32-bit floats:
    in_dtype = np.dtype([("col1", np.dtype("2f")), ("col2", np.int16)])
    inp = np.array([1, 2, 3, 4], dtype=in_dtype)
    out_dtype = np.dtype([("col1", np.dtype("2f")), ("col2", np.int8)])
    result = util.gentle_asarray(inp, dtype=out_dtype)
    assert result.dtype == out_dtype
    assert_array_equal(result["col2"], inp["col2"])


def test_gentle_asarray_mismatched_field_names():
    """
    Test gentle_asarray with input field names that don't
    match the requested output field names.
    """
    in_dtype = np.dtype([("col1", np.int16), ("col2", np.float32)])
    inp = np.array([1, 2, 3, 4], dtype=in_dtype)
    out_dtype = np.dtype([("col1", np.int16), ("foo", np.float32)])
    with pytest.raises(ValueError):
        util.gentle_asarray(inp, dtype=out_dtype)


def test_gentle_asarray_field_name_case():
    """
    Test gentle_assary with input and output field names that
    only differ by case.
    """
    in_dtype = np.dtype([("col1", np.int16), ("col2", np.float32)])
    inp = np.array([1, 2, 3, 4], dtype=in_dtype)
    out_dtype = np.dtype([("COL1", np.int16), ("COL2", np.float32)])
    result = util.gentle_asarray(inp, dtype=out_dtype)
    assert result.dtype == out_dtype


def test_gentle_asarray_scalar_input():
    """
    Test gentle_asarray with scalar input.
    """
    result = util.gentle_asarray(3.14159, dtype=np.float32)
    assert result.dtype == np.float32
    assert_array_equal(result, np.array([3.14159], dtype=np.float32))


def test_gentle_asarray_invalid_conversion():
    """
    Test gentle_asarray with input that cannot be cast
    to an array.
    """
    with pytest.raises(ValueError):
        util.gentle_asarray(object(), dtype=np.float32)


def test_create_history_entry():
    entry = util.create_history_entry("Once upon a time...")
    assert isinstance(entry, HistoryEntry)
    assert entry["description"] == "Once upon a time..."
    assert entry.get("software") is None
    assert (datetime.utcnow() - entry["time"]) < timedelta(seconds=10)

    software = {"name": "PolarBearSoft", "version": "1.2.3"}
    entry = util.create_history_entry("There was a tie-dyed polar bear...", software)
    assert isinstance(entry["software"], Software)
    assert entry["software"]["name"] == "PolarBearSoft"
    assert entry["software"]["version"] == "1.2.3"

    software = [
        {"name": "PolarBearSoft", "version": "1.2.3"},
        {"name": "BanjoSoft", "version": "4.5.6"},
    ]
    entry = util.create_history_entry("Who loved to strum the banjo.", software)
    assert isinstance(entry["software"], list)
    assert all(isinstance(s, Software) for s in entry["software"])
    assert entry["software"][0]["name"] == "PolarBearSoft"
    assert entry["software"][0]["version"] == "1.2.3"
    assert entry["software"][1]["name"] == "BanjoSoft"
    assert entry["software"][1]["version"] == "4.5.6"


@pytest.mark.parametrize(
    "value,expected_result",
    [
        ("0", False),
        ("false", False),
        ("FALSE", False),
        ("f", False),
        ("no", False),
        ("n", False),
        ("1", True),
        ("-1", True),
        ("198815238", True),
        ("true", True),
        ("TRUE", True),
        ("t", True),
        ("yes", True),
        ("y", True),
    ]
)
def test_get_envar_as_boolean(monkeypatch, value, expected_result):
    monkeypatch.setenv("TEST_VAR", value)
    assert util.get_envar_as_boolean("TEST_VAR") is expected_result


def test_get_envar_as_boolean_default(monkeypatch):
    monkeypatch.delenv("TEST_VAR", raising=False)
    assert util.get_envar_as_boolean("TEST_VAR") is False
    assert util.get_envar_as_boolean("TEST_VAR", default=False) is False
    assert util.get_envar_as_boolean("TEST_VAR", default=True) is True


def test_get_envar_as_boolean_invalid(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "foo")
    with pytest.raises(ValueError):
        assert util.get_envar_as_boolean("TEST_VAR")


def test_get_model_type():
    assert util.get_model_type(asdf.AsdfFile()) is None
    assert util.get_model_type(asdf.AsdfFile({"meta": {"model_type": "SomeModel"}})) == "SomeModel"

    assert util.get_model_type(fits.HDUList([fits.PrimaryHDU()])) is None

    hdu = fits.PrimaryHDU()
    hdu.header["DATAMODL"] = "SomeOtherModel"
    assert util.get_model_type(fits.HDUList([hdu])) == "SomeOtherModel"
