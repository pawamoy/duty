from __future__ import annotations

from typing import Literal

from duty._internal.tools._base import Tool


class coverage(Tool):  # noqa: N801
    """Call [Coverage.py](https://github.com/nedbat/coveragepy)."""

    cli_name = "coverage"
    """The name of the executable on PATH."""

    @classmethod
    def annotate(
        cls,
        *,
        rcfile: str | None = None,
        directory: str | None = None,
        data_file: str | None = None,
        ignore_errors: bool | None = None,
        include: list[str] | None = None,
        omit: list[str] | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Annotate source files with execution information.

        Make annotated copies of the given files, marking statements that are executed
        with `>` and statements that are missed with `!`.

        Parameters:
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            directory: Write the output files to this directory.
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            ignore_errors: Ignore errors while reading source files.
            include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["annotate"]

        if directory:
            cli_args.append("--directory")
            cli_args.append(directory)

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if ignore_errors:
            cli_args.append("--ignore-errors")

        if include:
            cli_args.append("--include")
            cli_args.append(",".join(include))

        if omit:
            cli_args.append("--omit")
            cli_args.append(",".join(omit))

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def combine(
        cls,
        *paths: str,
        rcfile: str | None = None,
        append: bool | None = None,
        data_file: str | None = None,
        keep: bool | None = None,
        quiet: bool | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Combine a number of data files.

        Combine data from multiple coverage files. The combined results are written to
        a single file representing the union of the data. The positional arguments are
        data files or directories containing data files. If no paths are provided,
        data files in the default data file's directory are combined.

        Parameters:
            paths: Paths to combine.
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            append: Append coverage data to .coverage, otherwise it starts clean each time.
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            keep: Keep original coverage files, otherwise they are deleted.
            quiet: Don't print messages about what is happening.
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["combine", *paths]

        if append:
            cli_args.append("--append")

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if keep:
            cli_args.append("--keep")

        if quiet:
            cli_args.append("--quiet")

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def debug(
        cls,
        topic: Literal["data", "sys", "config", "premain", "pybehave"],
        *,
        rcfile: str | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Display information about the internals of coverage.py.

        Display information about the internals of coverage.py, for diagnosing
        problems. Topics are: `data` to show a summary of the collected data; `sys` to
        show installation information; `config` to show the configuration; `premain`
        to show what is calling coverage; `pybehave` to show internal flags describing
        Python behavior.

        Parameters:
            topic: Topic to display.
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args: list[str] = ["debug", topic]

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def erase(
        cls,
        *,
        rcfile: str | None = None,
        data_file: str | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Erase previously collected coverage data.

        Parameters:
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["erase"]

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def html(
        cls,
        *,
        rcfile: str | None = None,
        contexts: list[str] | None = None,
        directory: str | None = None,
        data_file: str | None = None,
        fail_under: int | None = None,
        ignore_errors: bool | None = None,
        include: list[str] | None = None,
        omit: list[str] | None = None,
        precision: int | None = None,
        quiet: bool | None = None,
        show_contexts: bool | None = None,
        skip_covered: bool | None = None,
        skip_empty: bool | None = None,
        title: str | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Create an HTML report.

        Create an HTML report of the coverage of the files.  Each file gets its own
        page, with the source decorated to show executed, excluded, and missed lines.

        Parameters:
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            contexts: Only display data from lines covered in the given contexts.
                Accepts Python regexes, which must be quoted.
            directory: Write the output files to this directory.
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            fail_under: Exit with a status of 2 if the total coverage is less than the given number.
            ignore_errors: Ignore errors while reading source files.
            include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            precision: Number of digits after the decimal point to display for reported coverage percentages.
            quiet: Don't print messages about what is happening.
            show_contexts: Show contexts for covered lines.
            skip_covered: Skip files with 100% coverage.
            skip_empty: Skip files with no code.
            title: A text string to use as the title on the HTML.
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["html"]

        if contexts:
            cli_args.append("--contexts")
            cli_args.append(",".join(contexts))

        if directory:
            cli_args.append("--directory")
            cli_args.append(directory)

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if fail_under is not None:
            cli_args.append("--fail-under")
            cli_args.append(str(fail_under))

        if ignore_errors:
            cli_args.append("--ignore-errors")

        if include:
            cli_args.append("--include")
            cli_args.append(",".join(include))

        if omit:
            cli_args.append("--omit")
            cli_args.append(",".join(omit))

        if precision is not None:
            cli_args.append("--precision")
            cli_args.append(str(precision))

        if quiet:
            cli_args.append("--quiet")

        if show_contexts:
            cli_args.append("--show-contexts")

        if skip_covered is True:
            cli_args.append("--skip-covered")
        elif skip_covered is False:
            cli_args.append("--no-skip-covered")

        if skip_empty:
            cli_args.append("--skip-empty")

        if title:
            cli_args.append("--title")
            cli_args.append(title)

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def json(
        cls,
        *,
        rcfile: str | None = None,
        contexts: list[str] | None = None,
        data_file: str | None = None,
        fail_under: int | None = None,
        ignore_errors: bool | None = None,
        include: list[str] | None = None,
        omit: list[str] | None = None,
        output: str | None = None,
        pretty_print: bool | None = None,
        quiet: bool | None = None,
        show_contexts: bool | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Create a JSON report of coverage results.

        Parameters:
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            contexts: Only display data from lines covered in the given contexts.
                Accepts Python regexes, which must be quoted.
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            fail_under: Exit with a status of 2 if the total coverage is less than the given number.
            ignore_errors: Ignore errors while reading source files.
            include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            output: Write the JSON report to this file. Defaults to `coverage.json`.
            pretty_print: Format the JSON for human readers.
            quiet: Don't print messages about what is happening.
            show_contexts: Show contexts for covered lines.
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["json"]

        if contexts:
            cli_args.append("--contexts")
            cli_args.append(",".join(contexts))

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if fail_under is not None:
            cli_args.append("--fail-under")
            cli_args.append(str(fail_under))

        if ignore_errors:
            cli_args.append("--ignore-errors")

        if include:
            cli_args.append("--include")
            cli_args.append(",".join(include))

        if omit:
            cli_args.append("--omit")
            cli_args.append(",".join(omit))

        if output:
            cli_args.append("-o")
            cli_args.append(output)

        if pretty_print:
            cli_args.append("--pretty-print")

        if quiet:
            cli_args.append("--quiet")

        if show_contexts:
            cli_args.append("--show-contexts")

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def lcov(
        cls,
        *,
        rcfile: str | None = None,
        data_file: str | None = None,
        fail_under: int | None = None,
        ignore_errors: bool | None = None,
        include: list[str] | None = None,
        omit: list[str] | None = None,
        output: str | None = None,
        quiet: bool | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Create an LCOV report of coverage results.

        Parameters:
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            fail_under: Exit with a status of 2 if the total coverage is less than the given number.
            ignore_errors: Ignore errors while reading source files.
            include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            output: Write the JSON report to this file. Defaults to `coverage.json`.
            quiet: Don't print messages about what is happening.
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["lcov"]

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if fail_under is not None:
            cli_args.append("--fail-under")
            cli_args.append(str(fail_under))

        if ignore_errors:
            cli_args.append("--ignore-errors")

        if include:
            cli_args.append("--include")
            cli_args.append(",".join(include))

        if omit:
            cli_args.append("--omit")
            cli_args.append(",".join(omit))

        if output:
            cli_args.append("-o")
            cli_args.append(output)

        if quiet:
            cli_args.append("--quiet")

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def report(
        cls,
        *,
        rcfile: str | None = None,
        contexts: list[str] | None = None,
        data_file: str | None = None,
        fail_under: int | None = None,
        output_format: Literal["text", "markdown", "total"] | None = None,
        ignore_errors: bool | None = None,
        include: list[str] | None = None,
        omit: list[str] | None = None,
        precision: int | None = None,
        sort: Literal["name", "stmts", "miss", "branch", "brpart", "cover"] | None = None,
        show_missing: bool | None = None,
        skip_covered: bool | None = None,
        skip_empty: bool | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Report coverage statistics on modules.

        Parameters:
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            contexts: Only display data from lines covered in the given contexts.
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            fail_under: Exit with a status of 2 if the total coverage is less than the given number.
            output_format: Output format, either text (default), markdown, or total.
            ignore_errors: Ignore errors while reading source files.
            include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            precision: Number of digits after the decimal point to display for reported coverage percentages.
            sort: Sort the report by the named column: name, stmts, miss, branch, brpart, or cover. Default is name.
            show_missing: Show line numbers of statements in each module that weren't executed.
            skip_covered: Skip files with 100% coverage.
            skip_empty: Skip files with no code.
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["report"]

        if contexts:
            cli_args.append("--contexts")
            cli_args.append(",".join(contexts))

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if fail_under is not None:
            cli_args.append("--fail-under")
            cli_args.append(str(fail_under))

        if output_format:
            cli_args.append("--format")
            cli_args.append(output_format)

        if ignore_errors:
            cli_args.append("--ignore-errors")

        if include:
            cli_args.append("--include")
            cli_args.append(",".join(include))

        if omit:
            cli_args.append("--omit")
            cli_args.append(",".join(omit))

        if precision is not None:
            cli_args.append("--precision")
            cli_args.append(str(precision))

        if sort:
            cli_args.append("--sort")
            cli_args.append(sort)

        if show_missing:
            cli_args.append("--show-missing")

        if skip_covered is True:
            cli_args.append("--skip-covered")
        elif skip_covered is False:
            cli_args.append("--no-skip-covered")

        if skip_empty:
            cli_args.append("--skip-empty")

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def run(
        cls,
        pyfile: str,
        *,
        rcfile: str | None = None,
        append: bool | None = None,
        branch: bool | None = None,
        concurrency: list[str] | None = None,
        context: str | None = None,
        data_file: str | None = None,
        include: list[str] | None = None,
        omit: list[str] | None = None,
        module: bool | None = None,
        pylib: bool | None = None,
        parallel_mode: bool | None = None,
        source: list[str] | None = None,
        timid: bool | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Run a Python program and measure code execution.

        Parameters:
            pyfile: Python script or module to run.
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            append: Append coverage data to .coverage, otherwise it starts clean each time.
            branch: Measure branch coverage in addition to statement coverage.
            concurrency: Properly measure code using a concurrency library. Valid values are:
                eventlet, gevent, greenlet, multiprocessing, thread, or a comma-list of them.
            context: The context label to record for this coverage run.
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            module: The given file is an importable Python module, not a script path, to be run as `python -m` would run it.
            pylib: Measure coverage even inside the Python installed library, which isn't done by default.
            parallel_mode: Append the machine name, process id and random number to the data file name
                to simplify collecting data from many processes.
            source: A list of directories or importable names of code to measure.
            timid: Use a simpler but slower trace method. Try this if you get seemingly impossible results!
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["run", pyfile]

        if append:
            cli_args.append("--append")

        if branch:
            cli_args.append("--branch")

        if concurrency:
            cli_args.append("--concurrency")
            cli_args.append(",".join(concurrency))

        if context:
            cli_args.append("--context")
            cli_args.append(context)

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if include:
            cli_args.append("--include")
            cli_args.append(",".join(include))

        if omit:
            cli_args.append("--omit")
            cli_args.append(",".join(omit))

        if module:
            cli_args.append("--module")

        if pylib:
            cli_args.append("--pylib")

        if parallel_mode:
            cli_args.append("--parallel-mode")

        if source:
            cli_args.append("--source")
            cli_args.append(",".join(source))

        if timid:
            cli_args.append("--timid")

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    @classmethod
    def xml(
        cls,
        *,
        rcfile: str | None = None,
        data_file: str | None = None,
        fail_under: int | None = None,
        ignore_errors: bool | None = None,
        include: list[str] | None = None,
        omit: list[str] | None = None,
        output: str | None = None,
        quiet: bool | None = None,
        skip_empty: bool | None = None,
        debug_opts: list[str] | None = None,
    ) -> coverage:
        """Create an XML report of coverage results.

        Parameters:
            rcfile: Specify configuration file. By default `.coveragerc`, `setup.cfg`, `tox.ini`,
                and `pyproject.toml` are tried [env: `COVERAGE_RCFILE`].
            data_file: Read coverage data for report generation from this file.
                Defaults to `.coverage` [env: `COVERAGE_FILE`].
            fail_under: Exit with a status of 2 if the total coverage is less than the given number.
            ignore_errors: Ignore errors while reading source files.
            include: Include only files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            omit: Omit files whose paths match one of these patterns. Accepts shell-style wildcards, which must be quoted.
            output: Write the JSON report to this file. Defaults to `coverage.json`.
            quiet: Don't print messages about what is happening.
            skip_empty: Skip files with no code.
            debug_opts: Debug options, separated by commas [env: `COVERAGE_DEBUG`].
        """
        cli_args = ["xml"]

        if data_file:
            cli_args.append("--data-file")
            cli_args.append(data_file)

        if fail_under is not None:
            cli_args.append("--fail-under")
            cli_args.append(str(fail_under))

        if ignore_errors:
            cli_args.append("--ignore-errors")

        if include:
            cli_args.append("--include")
            cli_args.append(",".join(include))

        if omit:
            cli_args.append("--omit")
            cli_args.append(",".join(omit))

        if output:
            cli_args.append("-o")
            cli_args.append(output)

        if quiet:
            cli_args.append("--quiet")

        if skip_empty:
            cli_args.append("--skip-empty")

        if debug_opts:
            cli_args.append("--debug")
            cli_args.append(",".join(debug_opts))

        if rcfile:
            cli_args.append("--rcfile")
            cli_args.append(rcfile)

        return cls(cli_args)

    def __call__(self) -> int | None:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        from coverage.cmdline import main as run_coverage  # noqa: PLC0415

        return run_coverage(self.cli_args)
