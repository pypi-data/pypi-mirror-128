"""
Concrete datatypes representing interesting results in a Veracode scan.
"""
import dataclasses
import inspect
import json
import typing


@dataclasses.dataclass
class Finding:
    "Represents an issue in a Veracode scan."
    title: str
    issue_id: int
    severity: int
    issue_type_id: str
    issue_type: str
    cwe_id: str
    display_text: str
    source_path: str
    source_line: int
    files_raw: str
    flaw_details_link: typing.Optional[str] = None

    @classmethod
    def parse(cls, rawfinding: typing.Mapping[str, typing.Any]) -> "Finding":
        expected_fields = set(inspect.signature(cls).parameters)
        findingvalues = {
            nm: val for nm, val in rawfinding.items() if nm in expected_fields
        }
        findingvalues["source_path"] = rawfinding["files"]["source_file"]["file"]
        findingvalues["source_line"] = rawfinding["files"]["source_file"]["line"]
        findingvalues["files_raw"] = json.dumps(rawfinding["files"])
        return cls(**findingvalues)


@dataclasses.dataclass
class Scan:
    "Represents a Veracode scan result."
    scan_id: str
    scan_status: str
    message: str
    modules: typing.List[str]
    findings: typing.List[Finding]
    dev_stage: str

    @classmethod
    def parse(cls, rawscan: typing.Mapping[str, typing.Any]) -> "Scan":
        findings = [Finding.parse(f) for f in rawscan["findings"]]
        modules = list(rawscan["modules"])
        return cls(
            scan_id=rawscan["scan_id"],
            scan_status=rawscan["scan_status"],
            message=rawscan["message"],
            modules=modules,
            findings=findings,
            dev_stage=rawscan["dev_stage"],
        )
