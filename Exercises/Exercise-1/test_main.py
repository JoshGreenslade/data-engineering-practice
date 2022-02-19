from tempfile import tempdir
import pytest
import os
from pathlib import Path

from main import create_directory_if_not_exists
from main import download_from_url
from main import unzip_file
from main import delete_file
from main import assert_url_exists


def test_create_directory_if_not_exists(tmpdir):
    tmpdir = Path(tmpdir)

    create_directory_if_not_exists(tmpdir / "testdir")

    assert os.path.exists(tmpdir / "testdir")


def test_create_directory_continues_if_exists(tmpdir):
    tmpdir = Path(tmpdir)

    os.mkdir(tmpdir / "test_existing_folder")
    create_directory_if_not_exists(tmpdir / "test_existing_folder")


def test_download_from_url(tmpdir):
    tmpdir = Path(tmpdir)
    url = "https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv"
    fname = url.split("/")[-1]
    print(tmpdir / fname)
    download_from_url(url=url, filepath=tmpdir / fname)

    assert os.path.exists(tmpdir / fname)

    with open(tmpdir / fname, "r") as f:
        res = f.readline()
    assert res == "John,Doe,120 jefferson st.,Riverside, NJ, 08075\n"


def test_assert_url_exists():
    assert assert_url_exists("http://www.google.com")
    assert not assert_url_exists("http://www.someFakeWebsite.com/ThisShouldntwork/")
