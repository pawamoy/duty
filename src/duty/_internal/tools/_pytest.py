from __future__ import annotations

from typing import Literal

from duty._internal.tools._base import Tool


class pytest(Tool):  # noqa: N801
    """Call [pytest](https://github.com/pytest-dev/pytest)."""

    cli_name = "pytest"
    """The name of the executable on PATH."""

    def __init__(
        self,
        *paths: str,
        config_file: str | None = None,
        select: str | None = None,
        select_markers: str | None = None,
        markers: bool | None = None,
        exitfirst: bool | None = None,
        fixtures: bool | None = None,
        fixtures_per_test: bool | None = None,
        pdb: bool | None = None,
        pdbcls: str | None = None,
        trace: bool | None = None,
        capture: str | None = None,
        runxfail: bool | None = None,
        last_failed: bool | None = None,
        failed_first: bool | None = None,
        new_first: bool | None = None,
        cache_show: str | None = None,
        cache_clear: bool | None = None,
        last_failed_no_failures: Literal["all", "none"] | None = None,
        stepwise: bool | None = None,
        stepwise_skip: bool | None = None,
        durations: int | None = None,
        durations_min: int | None = None,
        verbose: bool | None = None,
        no_header: bool | None = None,
        no_summary: bool | None = None,
        quiet: bool | None = None,
        verbosity: int | None = None,
        show_extra_summary: str | None = None,
        disable_pytest_warnings: bool | None = None,
        showlocals: bool | None = None,
        no_showlocals: bool | None = None,
        traceback: Literal["auto", "long", "short", "line", "native", "no"] | None = None,
        show_capture: Literal["no", "stdout", "stderr", "log", "all"] | None = None,
        full_trace: bool | None = None,
        color: str | None = None,
        code_highlight: bool | None = None,
        pastebin: str | None = None,
        junit_xml: str | None = None,
        junit_prefix: str | None = None,
        pythonwarnings: str | None = None,
        maxfail: int | None = None,
        strict_config: bool | None = None,
        strict_markers: bool | None = None,
        continue_on_collection_errors: bool | None = None,
        rootdir: str | None = None,
        collect_only: bool | None = None,
        pyargs: bool | None = None,
        ignore: list[str] | None = None,
        ignore_glob: list[str] | None = None,
        deselect: str | None = None,
        confcutdir: str | None = None,
        noconftest: bool | None = None,
        keep_duplicates: bool | None = None,
        collect_in_virtualenv: bool | None = None,
        import_mode: Literal["prepend", "append", "importlib"] | None = None,
        doctest_modules: bool | None = None,
        doctest_report: Literal["none", "cdiff", "ndiff", "udiff", "only_first_failure"] | None = None,
        doctest_glob: str | None = None,
        doctest_ignore_import_errors: bool | None = None,
        doctest_continue_on_failure: bool | None = None,
        basetemp: str | None = None,
        plugins: list[str] | None = None,
        no_plugins: list[str] | None = None,
        trace_config: bool | None = None,
        debug: str | None = None,
        override_ini: str | None = None,
        assert_mode: str | None = None,
        setup_only: bool | None = None,
        setup_show: bool | None = None,
        setup_plan: bool | None = None,
        log_level: str | None = None,
        log_format: str | None = None,
        log_date_format: str | None = None,
        log_cli_level: tuple[str, str] | None = None,
        log_cli_format: str | None = None,
        log_cli_date_format: str | None = None,
        log_file: str | None = None,
        log_file_level: str | None = None,
        log_file_format: str | None = None,
        log_file_date_format: str | None = None,
        log_auto_indent: str | None = None,
    ) -> None:
        """Run `pytest`.

        Parameters:
            *paths: Files or directories to select tests from.
            select: Only run tests which match the given substring expression. An expression is a Python evaluatable expression where all names are substring-matched against test names and their parent classes. Example: -k 'test_method or test_other' matches all test functions and classes whose name contains 'test_method' or 'test_other', while -k 'not test_method' matches those that don't contain 'test_method' in their names. -k 'not test_method and not test_other' will eliminate the matches. Additionally keywords are matched to classes and functions containing extra names in their 'extra_keyword_matches' set, as well as functions which have names assigned directly to them. The matching is case-insensitive.
            select_markers: Only run tests matching given mark expression. For example: -m 'mark1 and not mark2'.
            markers: show markers (builtin, plugin and per-project ones).
            exitfirst: Exit instantly on first error or failed test
            fixtures: Show available fixtures, sorted by plugin appearance (fixtures with leading '_' are only shown with '-v')
            fixtures_per_test: Show fixtures per test
            pdb: Start the interactive Python debugger on errors or KeyboardInterrupt
            pdbcls: Specify a custom interactive Python debugger for use with --pdb.For example: --pdbcls IPython.terminal.debugger:TerminalPdb
            trace: Immediately break when running each test
            capture: Per-test capturing method: one of fd|sys|no|tee-sys
            runxfail: Report the results of xfail tests as if they were not marked
            last_failed: Rerun only the tests that failed at the last run (or all if none failed)
            failed_first: Run all tests, but run the last failures first. This may re-order tests and thus lead to repeated fixture setup/teardown.
            new_first: Run tests from new files first, then the rest of the tests sorted by file mtime
            cache_show: Show cache contents, don't perform collection or tests. Optional argument: glob (default: '*').
            cache_clear: Remove all cache contents at start of test run
            last_failed_no_failures: Which tests to run with no previously (known) failures
            stepwise: Exit on test failure and continue from last failing test next time
            stepwise_skip: Ignore the first failing test but stop on the next failing test. Implicitly enables --stepwise.
            durations: Show N slowest setup/test durations (N 0 for all)
            durations_min: Minimal duration in seconds for inclusion in slowest list. Default: 0.005.
            verbose: Increase verbosity
            no_header: Disable header
            no_summary: Disable summary
            quiet: Decrease verbosity
            verbosity: Set verbosity. Default: 0.
            show_extra_summary: Show extra test summary info as specified by chars: (f)ailed, (E)rror, (s)kipped, (x)failed, (X)passed, (p)assed, (P)assed with output, (a)ll except passed (p/P), or (A)ll. (w)arnings are enabled by default (see --disable-warnings), 'N' can be used to reset the list. (default: 'fE').
            disable_pytest_warnings: Disable warnings summary
            showlocals: Show locals in tracebacks (disabled by default)
            no_showlocals: Hide locals in tracebacks (negate --showlocals passed through addopts)
            traceback: Traceback print mode (auto/long/short/line/native/no)
            show_capture: Controls how captured stdout/stderr/log is shown on failed tests. Default: all.
            full_trace: Don't cut any tracebacks (default is to cut)
            color: Color terminal output (yes/no/auto)
            code_highlight: {yes,no} Whether code should be highlighted (only if --color is also enabled). Default: yes.
            pastebin: Send failed|all info to bpaste.net pastebin service
            junit_xml: Create junit-xml style report file at given path
            junit_prefix: Prepend prefix to classnames in junit-xml output
            pythonwarnings: Set which warnings to report, see -W option of Python itself
            maxfail: Exit after first num failures or errors
            strict_config: Any warnings encountered while parsing the `pytest` section of the configuration file raise errors
            strict_markers: Markers not registered in the `markers` section of the configuration file raise errors
            config_file: Load configuration from `file` instead of trying to locate one of the implicit configuration files
            continue_on_collection_errors: Force test execution even if collection errors occur
            rootdir: Define root directory for tests. Can be relative path: 'root_dir', './root_dir', 'root_dir/another_dir/'; absolute path: '/home/user/root_dir'; path with variables: '$HOME/root_dir'.
            collect_only: Only collect tests, don't execute them
            pyargs: Try to interpret all arguments as Python packages
            ignore: Ignore path during collection (multi-allowed)
            ignore_glob: Ignore path pattern during collection (multi-allowed)
            deselect: Deselect item (via node id prefix) during collection (multi-allowed)
            confcutdir: Only load conftest.py's relative to specified dir
            noconftest: Don't load any conftest.py files
            keep_duplicates: Keep duplicate tests
            collect_in_virtualenv: Don't ignore tests in a local virtualenv directory
            import_mode: Prepend/append to sys.path when importing test modules and conftest files. Default: prepend.
            doctest_modules: Run doctests in all .py modules
            doctest_report: Choose another output format for diffs on doctest failure
            doctest_glob: Doctests file matching pattern, default: test*.txt
            doctest_ignore_import_errors: Ignore doctest ImportErrors
            doctest_continue_on_failure: For a given doctest, continue to run after the first failure
            basetemp: Base temporary directory for this test run. (Warning: this directory is removed if it exists.)
            plugins: Early-load given plugin module name or entry point (multi-allowed). To avoid loading of plugins, use the `no:` prefix, e.g. `no:doctest`.
            no_plugins: Early-load given plugin module name or entry point (multi-allowed). To avoid loading of plugins, use the `no:` prefix, e.g. `no:doctest`.
            trace_config: Trace considerations of conftest.py files
            debug: Store internal tracing debug information in this log file. This file is opened with 'w' and truncated as a result, care advised. Default: pytestdebug.log.
            override_ini: Override ini option with "option value" style, e.g. `-o xfail_strict True -o cache_dir cache`.
            assert_mode: Control assertion debugging tools. 'plain' performs no assertion debugging. 'rewrite' (the default) rewrites assert statements in test modules on import to provide assert expression information.
            setup_only: Only setup fixtures, do not execute tests
            setup_show: Show setup of fixtures while executing tests
            setup_plan: Show what fixtures and tests would be executed but don't execute anything
            log_level: Level of messages to catch/display. Not set by default, so it depends on the root/parent log handler's effective level, where it is "WARNING" by default.
            log_format: Log format used by the logging module.
            log_date_format: Log date format used by the logging module.
            log_cli_level: logging level.
            log_cli_format: Log format used by the logging module.
            log_cli_date_format: Log date format used by the logging module.
            log_file: Path to a file when logging will be written to.
            log_file_level: Log file logging level.
            log_file_format: Log format used by the logging module.
            log_file_date_format: Log date format used by the logging module.
            log_auto_indent: Auto-indent multiline messages passed to the logging module. Accepts true|on, false|off or an integer.
        """
        cli_args = list(paths)

        if select:
            cli_args.append("-k")
            cli_args.append(select)

        if select_markers:
            cli_args.append("-m")
            cli_args.append(select_markers)

        if markers:
            cli_args.append("--markers")

        if exitfirst:
            cli_args.append("--exitfirst")

        if fixtures:
            cli_args.append("--fixtures")

        if fixtures_per_test:
            cli_args.append("--fixtures-per-test")

        if pdb:
            cli_args.append("--pdb")

        if pdbcls:
            cli_args.append("--pdbcls")
            cli_args.append(pdbcls)

        if trace:
            cli_args.append("--trace")

        if capture:
            cli_args.append("--capture")

        if runxfail:
            cli_args.append("--runxfail")

        if last_failed:
            cli_args.append("--last-failed")

        if failed_first:
            cli_args.append("--failed-first")

        if new_first:
            cli_args.append("--new-first")

        if cache_show:
            cli_args.append("--cache-show")
            cli_args.append(cache_show)

        if cache_clear:
            cli_args.append("--cache-clear")

        if last_failed_no_failures:
            cli_args.append("--last-failed-no-failures")
            cli_args.append(last_failed_no_failures)

        if stepwise:
            cli_args.append("--stepwise")

        if stepwise_skip:
            cli_args.append("--stepwise-skip")

        if durations:
            cli_args.append("--durations")
            cli_args.append(str(durations))

        if durations_min:
            cli_args.append("--durations-min")
            cli_args.append(str(durations_min))

        if verbose:
            cli_args.append("--verbose")

        if no_header:
            cli_args.append("--no-header")

        if no_summary:
            cli_args.append("--no-summary")

        if quiet:
            cli_args.append("--quiet")

        if verbosity:
            cli_args.append("--verbosity")
            cli_args.append(str(verbosity))

        if show_extra_summary:
            cli_args.append("-r")
            cli_args.append(show_extra_summary)

        if disable_pytest_warnings:
            cli_args.append("--disable-pytest-warnings")

        if showlocals:
            cli_args.append("--showlocals")

        if no_showlocals:
            cli_args.append("--no-showlocals")

        if traceback:
            cli_args.append("--tb")
            cli_args.append(traceback)

        if show_capture:
            cli_args.append("--show-capture")
            cli_args.append(show_capture)

        if full_trace:
            cli_args.append("--full-trace")

        if color:
            cli_args.append("--color")
            cli_args.append(color)

        if code_highlight:
            cli_args.append("--code-highlight")

        if pastebin:
            cli_args.append("--pastebin")
            cli_args.append(pastebin)

        if junit_xml:
            cli_args.append("--junit-xml")
            cli_args.append(junit_xml)

        if junit_prefix:
            cli_args.append("--junit-prefix")
            cli_args.append(junit_prefix)

        if pythonwarnings:
            cli_args.append("--pythonwarnings")
            cli_args.append(pythonwarnings)

        if maxfail:
            cli_args.append("--maxfail")
            cli_args.append(str(maxfail))

        if strict_config:
            cli_args.append("--strict-config")

        if strict_markers:
            cli_args.append("--strict-markers")

        if config_file:
            cli_args.append("-c")
            cli_args.append(config_file)

        if continue_on_collection_errors:
            cli_args.append("--continue-on-collection-errors")

        if rootdir:
            cli_args.append("--rootdir")
            cli_args.append(rootdir)

        if collect_only:
            cli_args.append("--collect-only")

        if pyargs:
            cli_args.append("--pyargs")

        if ignore:
            for ign in ignore:
                cli_args.append("--ignore")
                cli_args.append(ign)

        if ignore_glob:
            for ign_glob in ignore_glob:
                cli_args.append("--ignore-glob")
                cli_args.append(ign_glob)

        if deselect:
            cli_args.append("--deselect")
            cli_args.append(deselect)

        if confcutdir:
            cli_args.append("--confcutdir")
            cli_args.append(confcutdir)

        if noconftest:
            cli_args.append("--noconftest")

        if keep_duplicates:
            cli_args.append("--keep-duplicates")

        if collect_in_virtualenv:
            cli_args.append("--collect-in-virtualenv")

        if import_mode:
            cli_args.append("--import-mode")
            cli_args.append(import_mode)

        if doctest_modules:
            cli_args.append("--doctest-modules")

        if doctest_report:
            cli_args.append("--doctest-report")
            cli_args.append(doctest_report)

        if doctest_glob:
            cli_args.append("--doctest-glob")
            cli_args.append(doctest_glob)

        if doctest_ignore_import_errors:
            cli_args.append("--doctest-ignore-import-errors")

        if doctest_continue_on_failure:
            cli_args.append("--doctest-continue-on-failure")

        if basetemp:
            cli_args.append("--basetemp")
            cli_args.append(basetemp)

        if plugins:
            for plugin in plugins:
                cli_args.append("-p")
                cli_args.append(plugin)

        if no_plugins:
            for no_plugin in no_plugins:
                cli_args.append("-p")
                cli_args.append(f"no:{no_plugin}")

        if trace_config:
            cli_args.append("--trace-config")

        if debug:
            cli_args.append("--debug")
            cli_args.append(debug)

        if override_ini:
            cli_args.append("--override-ini")
            cli_args.append(override_ini)

        if assert_mode:
            cli_args.append("--assert")
            cli_args.append(assert_mode)

        if setup_only:
            cli_args.append("--setup-only")

        if setup_show:
            cli_args.append("--setup-show")

        if setup_plan:
            cli_args.append("--setup-plan")

        if log_level:
            cli_args.append("--log-level")
            cli_args.append(log_level)

        if log_format:
            cli_args.append("--log-format")
            cli_args.append(log_format)

        if log_date_format:
            cli_args.append("--log-date-format")
            cli_args.append(log_date_format)

        if log_cli_level:
            cli_args.append("--log-cli-level")
            cli_args.extend(log_cli_level)

        if log_cli_format:
            cli_args.append("--log-cli-format")
            cli_args.append(log_cli_format)

        if log_cli_date_format:
            cli_args.append("--log-cli-date-format")
            cli_args.append(log_cli_date_format)

        if log_file:
            cli_args.append("--log-file")
            cli_args.append(log_file)

        if log_file_level:
            cli_args.append("--log-file-level")
            cli_args.append(log_file_level)

        if log_file_format:
            cli_args.append("--log-file-format")
            cli_args.append(log_file_format)

        if log_file_date_format:
            cli_args.append("--log-file-date-format")
            cli_args.append(log_file_date_format)

        if log_auto_indent:
            cli_args.append("--log-auto-indent")
            cli_args.append(log_auto_indent)

        super().__init__(cli_args)

    def __call__(self) -> int:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        from pytest import main as run_pytest  # noqa: PT013,PLC0415

        return run_pytest(self.cli_args)
