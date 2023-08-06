# veracode-to-sqlite

This is a command-line tool that creates a SQLite database from the JSON results
file of a Veracode scan.

Veracode scans can produce dozens or hundreds of issues that need to be
reviewed. In some settings there's good UI for triaging these issues. In other
cases (such as when running a [pipeline scan]) the results are presented as a
raw JSON file, and must be triaged by hand.

[pipeline scan]: https://docs.veracode.com/r/t_run_pipeline_scan

This tool converts the results from JSON into a SQLite database, which can then
be consumed by a tool like [datasette] for further analysis.

[datasette]: https://datasette.io/
