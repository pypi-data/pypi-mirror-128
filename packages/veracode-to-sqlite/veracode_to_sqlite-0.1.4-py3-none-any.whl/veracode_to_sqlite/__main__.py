"CLI interface for Veracode-to-SQLite conversion."
import argparse
import json
import pathlib
import sqlite3
import sys

from . import model, database


parser = argparse.ArgumentParser()

parser.add_argument(
    "-f",
    "--file",
    type=argparse.FileType("r"),
    default=sys.stdin,
    help="Input results.json file (defaults to STDIN).",
)
parser.add_argument(
    "db",
    type=pathlib.Path,
    help="Output database",
)


def main() -> None:
    args = parser.parse_args()

    cxn = sqlite3.connect(args.db)
    outputdb = database.Database(cxn)
    rawscan = json.load(args.file)
    scan = model.Scan.parse(rawscan)
    outputdb.save(scan)


if __name__ == "__main__":
    main()
