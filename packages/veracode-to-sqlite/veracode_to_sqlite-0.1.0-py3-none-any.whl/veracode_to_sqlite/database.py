import dataclasses
import sqlite3
from . import model


class Database:
    "A database to save Veracode scan into."

    def __init__(self, cxn: sqlite3.Connection):
        self._cxn = cxn
        self._init_db()

    def _init_db(self) -> None:
        "Create tables to store scan results."
        self._cxn.execute(
            "CREATE TABLE IF NOT EXISTS metadata (key TEXT NOT NULL, value TEXT)"
        )
        self._cxn.execute("CREATE TABLE IF NOT EXISTS modules (name TEXT NOT NULL)")
        self._cxn.execute(
            """
            CREATE TABLE IF NOT EXISTS findings (
                title TEXT NOT NULL,
                issue_id INTEGER NOT NULL,
                severity INTEGER NOT NULL,
                issue_type_id TEXT NOT NULL,
                issue_type TEXT NOT NULL,
                cwe_id TEXT NOT NULL,
                display_text TEXT NOT NULL,
                source_path TEXT NOT NULL,
                source_line INTEGER NOT NULL,
                files_raw TEXT NOT NULL,
                flaw_details_link TEXT
            )
        """
        )

    def _save_finding(self, finding: model.Finding) -> None:
        self._cxn.execute(
            "INSERT INTO findings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            dataclasses.astuple(finding),
        )

    def save(self, scan: model.Scan) -> None:
        with self._cxn:
            for finding in scan.findings:
                self._save_finding(finding)

            self._cxn.executemany(
                "INSERT INTO modules (name) VALUES (?)", ((m,) for m in scan.modules)
            )

            skip_fields = ("modules", "findings")
            metadata = [
                (key, val)
                for key, val in dataclasses.asdict(scan).items()
                if key not in skip_fields
            ]
            self._cxn.executemany(
                "INSERT INTO metadata (key, value) VALUES (?, ?)", metadata
            )
