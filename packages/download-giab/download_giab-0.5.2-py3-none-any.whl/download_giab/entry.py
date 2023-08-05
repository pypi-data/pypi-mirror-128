import argparse
import csv
import os.path

import requests
import subprocess
import sys
import time

from typing import List, Optional
from urllib.parse import urlparse


DOWNLOAD_ATTEMPTS = 3
DOWNLOAD_FAILURE_SLEEP = 15


def get_file_md5(path: str) -> bytes:
    return subprocess.check_output(["md5sum", path]).split(b" ")[0]


def download_file(file_url, md5: bytes, already_downloaded: dict, cat_to: Optional[str] = None):
    file_name = file_url.split("/")[-1]

    if not cat_to:
        if file_name not in already_downloaded:
            already_downloaded[file_name] = 1
        else:
            already_downloaded[file_name] += 1
            file_name_parts = file_name.split(".")
            file_name_parts[0] += f"_{already_downloaded[file_name]:03}"
            file_name = ".".join(file_name_parts)

        if os.path.exists(file_name):
            h = get_file_md5(file_name)
            if h == md5:
                sys.stdout.write(f"Skipping {file_name} (already exists with correct checksum)\n")
            else:
                sys.stdout.write(f"Error: encountered conflicting existing file with name {file_name}\n")
            return

    sys.stdout.write(f"Downloading and verifying {file_name}... ")
    sys.stdout.flush()

    attempts = 1

    while True:
        try:
            subprocess.check_call(
                ["wget", "-O", file_name, file_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            h = get_file_md5(file_name)

            if h == md5:
                break

            sys.stdout.write(f"\n\thash mismatch: downloaded file hash '{h}' != recorded hash '{md5}'\n")

        except subprocess.CalledProcessError:
            sys.stdout.write(f"\n\twget returned non-0 exit status, sleeping for {DOWNLOAD_FAILURE_SLEEP} seconds...\n")
            time.sleep(DOWNLOAD_FAILURE_SLEEP)

        attempts += 1
        if attempts > DOWNLOAD_ATTEMPTS:
            sys.stdout.write("DOWNLOAD FAILED (DOWNLOAD FAILURES OR HASH MISMATCHES.)\n")
            return

        sys.stdout.write(f"\tretrying (attempt {attempts} of {DOWNLOAD_ATTEMPTS})\n")
        subprocess.check_output(["rm", "-f", file_name])

    if cat_to:
        subprocess.check_call(f"cat '{file_name}' >> '{cat_to}'", shell=True)
        subprocess.check_output(["rm", "-f", file_name])

    sys.stdout.write("done.\n")
    sys.stdout.flush()


def main(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        description="Utility Python package to download Genome-in-a-Bottle data from their index files.")

    parser.add_argument("index", help="Index file or URL to get data links and hashes from.")
    parser.add_argument(
        "--cat-paired",
        action="store_true",
        help="Concatenates paired-end read FASTQ files into two files (row 1 in file 1 has a pair in row 1 of file 2) "
             "instead of downloading them individually."
    )

    p_args = parser.parse_args(args or sys.argv[1:])

    index = p_args.index
    index_parts = urlparse(index)

    if index_parts.scheme in ("http", "https", "ftp"):
        if index_parts.netloc == "github.com":
            path_parts = index_parts.path.split("/")
            if path_parts[3] == "blob":  # Non-raw GH content
                index = index_parts.scheme + "://" + index_parts.netloc + \
                    "/".join(path_parts[:3]) + "/raw/" + "/".join(path_parts[4:])

        index_res = requests.get(index, allow_redirects=True)

        if index_res.status_code >= 300:
            print(f"Error: index request returned non-2XX status code: {index_res.status_code}")
            exit(1)

        index_contents = index_res.content.decode("utf-8").split("\n")

    else:
        with open(index, "r") as fh:
            index_contents = fh.read()

    already_downloaded = {}
    index_reader = csv.DictReader(index_contents, delimiter="\t")

    for row in index_reader:
        # sequences

        sample: Optional[str] = row.get("NIST_SAMPLE_NAME", "paired")
        cat_out_1 = f"{sample}_1.fastq.gz" if p_args.cat_paired else None
        cat_out_2 = f"{sample}_2.fastq.gz" if p_args.cat_paired else None

        if "FASTQ" in row:
            download_file(row["FASTQ"], bytes(row["FASTQ_MD5"], encoding="ascii"), already_downloaded,
                          cat_to=cat_out_1)
        if "PAIRED_FASTQ" in row:
            download_file(row["PAIRED_FASTQ"], bytes(row["PAIRED_FASTQ_MD5"], encoding="ascii"), already_downloaded,
                          cat_to=cat_out_2)

        if "FASTA" in row:
            download_file(row["FASTA"], bytes(row["FASTA_MD5"], encoding="ascii"), already_downloaded)

        if "FASTA_FASTQ" in row:
            download_file(row["FASTA_FASTQ"], bytes(row["FASTA_FASTQ_MD5"], encoding="ascii"), already_downloaded)

        if "XSQ" in row:
            download_file(row["XSQ"], bytes(row["XSQ_MD5"], encoding="ascii"), already_downloaded)

        # alignments

        if "BAM" in row:
            download_file(row["BAM"], bytes(row["BAM_MD5"], encoding="ascii"), already_downloaded)
        if "BAI" in row:
            download_file(row["BAI"], bytes(row["BAI_MD5"], encoding="ascii"), already_downloaded)

        if "XMAP_CMAP" in row:
            download_file(row["XMAP_CMAP"], bytes(row["XMAP_CMAP_MD5"], encoding="ascii"), already_downloaded)


if __name__ == "__main__":
    main()
