import requests
from pathlib import Path
import os
import logging
import zipfile

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.DEBUG
)
log = logging.getLogger()


def create_directory_if_not_exists(folderpath: Path) -> None:
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)


def assert_url_exists(url: str) -> bool:
    try:
        r = requests.head(url)
        return r.status_code == requests.codes.ok
    except requests.ConnectionError as exception:
        log.warning("Url {url} does not exist.")
        return False


def download_from_url(url: str, filepath: Path) -> None:
    response = requests.get(url)
    open(filepath, "wb").write(response.content)


def unzip_file(filepath: Path, destination: Path) -> None:
    log.info(f"Unzipping {filepath}")
    try:
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(destination)
    except Exception as e:
        print(f"Error: {e}")


def delete_file(filepath: Path) -> None:
    log.info(f"Deleting {filepath}")
    if os.path.exists(filepath):
        os.remove(filepath)


def main():
    # your code here
    FOLDERPATH = Path("./downloads")

    # Create a "downloads" directory
    create_directory_if_not_exists(folderpath=FOLDERPATH)

    for url in download_uris:
        filepath = FOLDERPATH / url.split("/")[-1]
        if assert_url_exists(url):
            download_from_url(url=url, filepath=filepath)
            unzip_file(filepath=filepath, destination=FOLDERPATH)
            delete_file(filepath=filepath)
        else:
            log.warning(f"Couldn't download {url}. Skipping")


if __name__ == "__main__":
    main()
