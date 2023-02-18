"""Callable for [isort](https://github.com/PyCQA/isort)."""

from __future__ import annotations

import sys

from duty.callables import lazy

# TODO: remove once support for Python 3.7 is dropped
if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

Multiline = Literal[
    "GRID",
    "VERTICAL",
    "HANGING_INDENT",
    "VERTICAL_HANGING_INDENT",
    "VERTICAL_GRID",
    "VERTICAL_GRID_GROUPED",
    "VERTICAL_GRID_GROUPED_NO_COMMA",
    "NOQA",
    "VERTICAL_HANGING_INDENT_BRACKET",
    "VERTICAL_PREFIX_FROM_MODULE_IMPORT",
    "HANGING_INDENT_WITH_PARENTHESES",
    "BACKSLASH_GRID",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
]


@lazy("isort")
def run(
    *files: str,
    settings: str | None = None,
    verbose: bool | None = None,
    only_modified: bool | None = None,
    dedup_headings: bool | None = None,
    quiet: bool | None = None,
    stdout: bool | None = None,
    overwrite_in_place: bool | None = None,
    show_config: bool | None = None,
    show_files: bool | None = None,
    diff: bool | None = None,
    check: bool | None = None,
    ignore_whitespace: bool | None = None,
    config_root: str | None = None,
    resolve_all_configs: bool | None = None,
    profile: str | None = None,
    jobs: int | None = None,
    atomic: bool | None = None,
    interactive: bool | None = None,
    format_error: str | None = None,
    format_success: str | None = None,
    sort_reexports: bool | None = None,
    filter_files: bool | None = None,
    skip: list[str] | None = None,
    extend_skip: list[str] | None = None,
    skip_glob: list[str] | None = None,
    extend_skip_glob: list[str] | None = None,
    skip_gitignore: bool | None = None,
    supported_extension: list[str] | None = None,
    blocked_extension: list[str] | None = None,
    dont_follow_links: bool | None = None,
    filename: str | None = None,
    allow_root: bool | None = None,
    add_import: str | None = None,
    append_only: bool | None = None,
    force_adds: bool | None = None,
    remove_import: str | None = None,
    float_to_top: bool | None = None,
    dont_float_to_top: bool | None = None,
    combine_as: bool | None = None,
    combine_star: bool | None = None,
    balanced: bool | None = None,
    from_first: bool | None = None,
    force_grid_wrap: int | None = None,
    indent: str | None = None,
    lines_before_imports: int | None = None,
    lines_after_imports: int | None = None,
    lines_between_types: int | None = None,
    line_ending: str | None = None,
    length_sort: bool | None = None,
    length_sort_straight: bool | None = None,
    multi_line: Multiline | None = None,
    ensure_newline_before_comments: bool | None = None,
    no_inline_sort: bool | None = None,
    order_by_type: bool | None = None,
    dont_order_by_type: bool | None = None,
    reverse_relative: bool | None = None,
    reverse_sort: bool | None = None,
    sort_order: Literal["natural", "native"] | None = None,
    force_single_line_imports: bool | None = None,
    single_line_exclusions: list[str] | None = None,
    trailing_comma: bool | None = None,
    use_parentheses: bool | None = None,
    line_length: int | None = None,
    wrap_length: int | None = None,
    case_sensitive: bool | None = None,
    remove_redundant_aliases: bool | None = None,
    honor_noqa: bool | None = None,
    treat_comment_as_code: str | None = None,
    treat_all_comment_as_code: bool | None = None,
    formatter: str | None = None,
    color: bool | None = None,
    ext_format: str | None = None,
    star_first: bool | None = None,
    split_on_trailing_comma: bool | None = None,
    section_default: Literal["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"] | None = None,
    only_sections: bool | None = None,
    no_sections: bool | None = None,
    force_alphabetical_sort: bool | None = None,
    force_sort_within_sections: bool | None = None,
    honor_case_in_force_sorted_sections: bool | None = None,
    sort_relative_in_force_sorted_sections: bool | None = None,
    force_alphabetical_sort_within_sections: bool | None = None,
    top: str | None = None,
    combine_straight_imports: bool | None = None,
    no_lines_before: list[str] | None = None,
    src_path: list[str] | None = None,
    builtin: str | None = None,
    extra_builtin: str | None = None,
    future: str | None = None,
    thirdparty: str | None = None,
    project: str | None = None,
    known_local_folder: str | None = None,
    virtual_env: str | None = None,
    conda_env: str | None = None,
    python_version: Literal["all", "2", "27", "3", "36", "37", "38", "39", "310", "311", "auto"] | None = None,
) -> None:
    """Run `isort`.

    Sort Python import definitions alphabetically within logical sections.
    Run with no arguments to see a quick start guide, otherwise, one or more files/directories/stdin must be provided.
    Use `-` as the first argument to represent stdin. Use --interactive to use the pre 5.0.0 interactive behavior.
    If you've used isort 4 but are new to isort 5, see the upgrading guide:
    https://pycqa.github.io/isort/docs/upgrade_guides/5.0.0.html.

    Parameters:
        *files: One or more Python source files that need their imports sorted.
        settings: Explicitly set the settings path or file instead of auto determining based on file location.
        verbose: Shows verbose output, such as when files are skipped or when a check is successful.
        only_modified: Suppresses verbose output for non-modified files.
        dedup_headings: Tells isort to only show an identical custom import heading comment once, even if there are multiple sections with the comment set.
        quiet: Shows extra quiet output, only errors are outputted.
        stdout: Force resulting output to stdout, instead of in-place.
        overwrite_in_place: Tells isort to overwrite in place using the same file handle. Comes at a performance and memory usage penalty over its standard approach but ensures all file flags and modes stay unchanged.
        show_config: See isort's determined config, as well as sources of config options.
        show_files: See the files isort will be run against with the current config options.
        diff: Prints a diff of all the changes isort would make to a file, instead of changing it in place
        check: Checks the file for unsorted / unformatted imports and prints them to the command line without modifying the file. Returns 0 when nothing would change and returns 1 when the file would be reformatted.
        ignore_whitespace: Tells isort to ignore whitespace differences when --check-only is being used.
        config_root: Explicitly set the config root for resolving all configs. When used with the --resolve-all-configs flag, isort will look at all sub-folders in this config root to resolve config files and sort files based on the closest available config(if any)
        resolve_all_configs: Tells isort to resolve the configs for all sub-directories and sort files in terms of its closest config files.
        profile: Base profile type to use for configuration. Profiles include: black, django, pycharm, google, open_stack, plone, attrs, hug, wemake, appnexus. As well as any shared profiles.
        jobs: Number of files to process in parallel. Negative value means use number of CPUs.
        atomic: Ensures the output doesn't save if the resulting file contains syntax errors.
        interactive: Tells isort to apply changes interactively.
        format_error: Override the format used to print errors.
        format_success: Override the format used to print success.
        sort_reexports: Automatically sort all re-exports (module level __all__ collections)
        filter_files: Tells isort to filter files even when they are explicitly passed in as part of the CLI command.
        skip: Files that isort should skip over. If you want to skip multiple files you should specify twice: --skip file1 --skip file2. Values can be file names, directory names or file paths. To skip all files in a nested path use --skip-glob.
        extend_skip: Extends --skip to add additional files that isort should skip over. If you want to skip multiple files you should specify twice: --skip file1 --skip file2. Values can be file names, directory names or file paths. To skip all files in a nested path use --skip-glob.
        skip_glob: Files that isort should skip over.
        extend_skip_glob: Additional files that isort should skip over (extending --skip-glob).
        skip_gitignore: Treat project as a git repository and ignore files listed in .gitignore. NOTE: This requires git to be installed and accessible from the same shell as isort.
        supported_extension: Specifies what extensions isort can be run against.
        blocked_extension: Specifies what extensions isort can never be run against.
        dont_follow_links: Tells isort not to follow symlinks that are encountered when running recursively.
        filename: Provide the filename associated with a stream.
        allow_root: Tells isort not to treat / specially, allowing it to be run against the root dir.
        add_import: Adds the specified import line to all files, automatically determining correct placement.
        append_only: Only adds the imports specified in --add-import if the file contains existing imports.
        force_adds: Forces import adds even if the original file is empty.
        remove_import: Removes the specified import from all files.
        float_to_top: Causes all non-indented imports to float to the top of the file having its imports sorted (immediately below the top of file comment). This can be an excellent shortcut for collecting imports every once in a while when you place them in the middle of a file to avoid context switching. *NOTE*: It currently doesn't work with cimports and introduces some extra over-head and a performance penalty.
        dont_float_to_top: Forces --float-to-top setting off. See --float-to-top for more information.
        combine_as: Combines as imports on the same line.
        combine_star: Ensures that if a star import is present, nothing else is imported from that namespace.
        balanced: Balances wrapping to produce the most consistent line length possible
        from_first: Switches the typical ordering preference, showing from imports first then straight ones.
        force_grid_wrap: Force number of from imports (defaults to 2 when passed as CLI flag without value) to be grid wrapped regardless of line length. If 0 is passed in (the global default) only line length is considered.
        indent: String to place for indents defaults to " " (4 spaces).
        lines_before_imports: Number of lines to insert before imports.
        lines_after_imports: Number of lines to insert after imports.
        lines_between_types: Number of lines to insert between imports.
        line_ending: Forces line endings to the specified value. If not set, values will be guessed per-file.
        length_sort: Sort imports by their string length.
        length_sort_straight: Sort straight imports by their string length. Similar to `length_sort` but applies only to straight imports and doesn't affect from imports.
        multi_line: Multi line output (0-grid, 1-vertical, 2-hanging, 3-vert-hanging, 4-vert-grid, 5-vert-grid-grouped, 6-deprecated-alias-for-5, 7-noqa, 8-vertical-hanging-indent-bracket, 9-vertical-prefix-from- module-import, 10-hanging-indent-with-parentheses).
        ensure_newline_before_comments: Inserts a blank line before a comment following an import.
        no_inline_sort: Leaves `from` imports with multiple imports 'as-is' (e.g. `from foo import a, c ,b`).
        order_by_type: Order imports by type, which is determined by case, in addition to alphabetically. **NOTE**: type here refers to the implied type from the import name capitalization. isort does not do type introspection for the imports. These "types" are simply: CONSTANT_VARIABLE, CamelCaseClass, variable_or_function. If your project follows PEP8 or a related coding standard and has many imports this is a good default, otherwise you likely will want to turn it off. From the CLI the `--dont-order-by-type` option will turn this off.
        dont_order_by_type: Don't order imports by type, which is determined by case, in addition to alphabetically. **NOTE**: type here refers to the implied type from the import name capitalization. isort does not do type introspection for the imports. These "types" are simply: CONSTANT_VARIABLE, CamelCaseClass, variable_or_function. If your project follows PEP8 or a related coding standard and has many imports this is a good default. You can turn this on from the CLI using `--order-by-type`.
        reverse_relative: Reverse order of relative imports.
        reverse_sort: Reverses the ordering of imports.
        sort_order: Specify sorting function. Can be built in (natural[default] = force numbers to be sequential, native = Python's built-in sorted function) or an installable plugin.
        force_single_line_imports: Forces all from imports to appear on their own line
        single_line_exclusions EXCLUSIONS: One or more modules to exclude from the single line rule.
        trailing_comma: Includes a trailing comma on multi line imports that include parentheses.
        use_parentheses: Use parentheses for line continuation on length limit instead of slashes. **NOTE**: This is separate from wrap modes, and only affects how individual lines that are too long get continued, not sections of multiple imports.
        line_length: The max length of an import line (used for wrapping long imports).
        wrap_length: Specifies how long lines that are wrapped should be, if not set line_length is used. NOTE: wrap_length must be LOWER than or equal to line_length.
        case_sensitive: Tells isort to include casing when sorting module names
        remove_redundant_aliases: Tells isort to remove redundant aliases from imports, such as `import os as os`. This defaults to `False` simply because some projects use these seemingly useless aliases to signify intent and change behaviour.
        honor_noqa: Tells isort to honor noqa comments to enforce skipping those comments.
        treat_comment_as_code: Tells isort to treat the specified single line comment(s) as if they are code.
        treat_all_comment_as_code: Tells isort to treat all single line comments as if they are code.
        formatter: Specifies the name of a formatting plugin to use when producing output.
        color: Tells isort to use color in terminal output.
        ext_format: Tells isort to format the given files according to an extensions formatting rules.
        star_first: Forces star imports above others to avoid overriding directly imported variables.
        split_on_trailing_comma: Split imports list followed by a trailing comma into VERTICAL_HANGING_INDENT mode
        section_default: Sets the default section for import options: ('FUTURE', 'STDLIB', 'THIRDPARTY', 'FIRSTPARTY', 'LOCALFOLDER')
        only_sections: Causes imports to be sorted based on their sections like STDLIB, THIRDPARTY, etc. Within sections, the imports are ordered by their import style and the imports with the same style maintain their relative positions.
        no_sections: Put all imports into the same section bucket
        force_alphabetical_sort: Force all imports to be sorted as a single section
        force_sort_within_sections: Don't sort straight-style imports (like import sys) before from-style imports (like from itertools import groupby). Instead, sort the imports by module, independent of import style.
        honor_case_in_force_sorted_sections: Honor `--case-sensitive` when `--force-sort-within-sections` is being used. Without this option set, `--order-by-type` decides module name ordering too.
        sort_relative_in_force_sorted_sections: When using `--force-sort-within-sections`, sort relative imports the same way as they are sorted when not using that setting.
        force_alphabetical_sort_within_sections: Force all imports to be sorted alphabetically within a section
        top: Force specific imports to the top of their appropriate section.
        combine_straight_imports: Combines all the bare straight imports of the same section in a single line. Won't work with sections which have 'as' imports
        no_lines_before: Sections which should not be split with previous by empty lines
        src_path: Add an explicitly defined source path (modules within src paths have their imports automatically categorized as first_party). Glob expansion (`*` and `**`) is supported for this option.
        builtin: Force isort to recognize a module as part of Python's standard library.
        extra_builtin: Extra modules to be included in the list of ones in Python's standard library.
        future: Force isort to recognize a module as part of Python's internal future compatibility libraries. WARNING: this overrides the behavior of __future__ handling and therefore can result in code that can't execute. If you're looking to add dependencies such as six, a better option is to create another section below --future using custom sections. See: https://github.com/PyCQA/isort#custom- sections-and-ordering and the discussion here: https://github.com/PyCQA/isort/issues/1463.
        thirdparty: Force isort to recognize a module as being part of a third party library.
        project: Force isort to recognize a module as being part of the current python project.
        known_local_folder: Force isort to recognize a module as being a local folder. Generally, this is reserved for relative imports (from . import module).
        virtual_env: Virtual environment to use for determining whether a package is third-party
        conda_env: Conda environment to use for determining whether a package is third-party
        python_version: Tells isort to set the known standard library based on the specified Python version. Default is to assume any Python 3 version could be the target, and use a union of all stdlib modules across versions. If auto is specified, the version of the interpreter used to run isort (currently: 311) will be used.
    """
    from isort.main import main as isort

    cli_args = list(files)

    if verbose:
        cli_args.append("--verbose")

    if only_modified:
        cli_args.append("--only-modified")

    if dedup_headings:
        cli_args.append("--dedup-headings")

    if quiet:
        cli_args.append("--quiet")

    if stdout:
        cli_args.append("--stdout")

    if overwrite_in_place:
        cli_args.append("--overwrite-in-place")

    if show_config:
        cli_args.append("--show-config")

    if show_files:
        cli_args.append("--show-files")

    if diff:
        cli_args.append("--diff")

    if check:
        cli_args.append("--check")

    if ignore_whitespace:
        cli_args.append("--ignore-whitespace")

    if settings:
        cli_args.append("--settings")
        cli_args.append(settings)

    if config_root:
        cli_args.append("--config-root")
        cli_args.append(config_root)

    if resolve_all_configs:
        cli_args.append("--resolve-all-configs")

    if profile:
        cli_args.append("--profile")
        cli_args.append(profile)

    if jobs:
        cli_args.append("--jobs")
        cli_args.append(str(jobs))

    if atomic:
        cli_args.append("--atomic")

    if interactive:
        cli_args.append("--interactive")

    if format_error:
        cli_args.append("--format-error")
        cli_args.append(format_error)

    if format_success:
        cli_args.append("--format-success")
        cli_args.append(format_success)

    if sort_reexports:
        cli_args.append("--sort-reexports")

    if filter_files:
        cli_args.append("--filter-files")

    if skip:
        cli_args.append("--skip")
        cli_args.append(",".join(skip))

    if extend_skip:
        cli_args.append("--extend-skip")
        cli_args.append(",".join(extend_skip))

    if skip_glob:
        cli_args.append("--skip-glob")
        cli_args.append(",".join(skip_glob))

    if extend_skip_glob:
        cli_args.append("--extend-skip-glob")
        cli_args.append(",".join(extend_skip_glob))

    if skip_gitignore:
        cli_args.append("--skip-gitignore")

    if supported_extension:
        cli_args.append("--supported-extension")
        cli_args.append(",".join(supported_extension))

    if blocked_extension:
        cli_args.append("--blocked-extension")
        cli_args.append(",".join(blocked_extension))

    if dont_follow_links:
        cli_args.append("--dont-follow-links")

    if filename:
        cli_args.append("--filename")
        cli_args.append(filename)

    if allow_root:
        cli_args.append("--allow-root")

    if add_import:
        cli_args.append("--add-import")
        cli_args.append(add_import)

    if append_only:
        cli_args.append("--append-only")

    if force_adds:
        cli_args.append("--force-adds")

    if remove_import:
        cli_args.append("--remove-import")
        cli_args.append(remove_import)

    if float_to_top:
        cli_args.append("--float-to-top")

    if dont_float_to_top:
        cli_args.append("--dont-float-to-top")

    if combine_as:
        cli_args.append("--combine-as")

    if combine_star:
        cli_args.append("--combine-star")

    if balanced:
        cli_args.append("--balanced")

    if from_first:
        cli_args.append("--from-first")

    if force_grid_wrap:
        cli_args.append("--force-grid-wrap")
        cli_args.append(str(force_grid_wrap))

    if indent:
        cli_args.append("--indent")
        cli_args.append(indent)

    if lines_before_imports:
        cli_args.append("--lines-before-imports")
        cli_args.append(str(lines_before_imports))

    if lines_after_imports:
        cli_args.append("--lines-after-imports")
        cli_args.append(str(lines_after_imports))

    if lines_between_types:
        cli_args.append("--lines-between-types")
        cli_args.append(str(lines_between_types))

    if line_ending:
        cli_args.append("--line-ending")
        cli_args.append(line_ending)

    if length_sort:
        cli_args.append("--length-sort")

    if length_sort_straight:
        cli_args.append("--length-sort-straight")

    if multi_line:
        cli_args.append("--multi-line")
        cli_args.append(multi_line)

    if ensure_newline_before_comments:
        cli_args.append("--ensure-newline-before-comments")

    if no_inline_sort:
        cli_args.append("--no-inline-sort")

    if order_by_type:
        cli_args.append("--order-by-type")

    if dont_order_by_type:
        cli_args.append("--dont-order-by-type")

    if reverse_relative:
        cli_args.append("--reverse-relative")

    if reverse_sort:
        cli_args.append("--reverse-sort")

    if sort_order:
        cli_args.append("--sort-order")
        cli_args.append(sort_order)

    if force_single_line_imports:
        cli_args.append("--force-single-line-imports")

    if single_line_exclusions:
        cli_args.append("--single-line-exclusions")
        cli_args.append(",".join(single_line_exclusions))

    if trailing_comma:
        cli_args.append("--trailing-comma")

    if use_parentheses:
        cli_args.append("--use-parentheses")

    if line_length:
        cli_args.append("--line-length")
        cli_args.append(str(line_length))

    if wrap_length:
        cli_args.append("--wrap-length")
        cli_args.append(str(wrap_length))

    if case_sensitive:
        cli_args.append("--case-sensitive")

    if remove_redundant_aliases:
        cli_args.append("--remove-redundant-aliases")

    if honor_noqa:
        cli_args.append("--honor-noqa")

    if treat_comment_as_code:
        cli_args.append("--treat-comment-as-code")
        cli_args.append(treat_comment_as_code)

    if treat_all_comment_as_code:
        cli_args.append("--treat-all-comment-as-code")

    if formatter:
        cli_args.append("--formatter")
        cli_args.append(formatter)

    if color:
        cli_args.append("--color")

    if ext_format:
        cli_args.append("--ext-format")
        cli_args.append(ext_format)

    if star_first:
        cli_args.append("--star-first")

    if split_on_trailing_comma:
        cli_args.append("--split-on-trailing-comma")

    if section_default:
        cli_args.append("--section-default")
        cli_args.append(section_default)

    if only_sections:
        cli_args.append("--only-sections")

    if no_sections:
        cli_args.append("--no-sections")

    if force_alphabetical_sort:
        cli_args.append("--force-alphabetical-sort")

    if force_sort_within_sections:
        cli_args.append("--force-sort-within-sections")

    if honor_case_in_force_sorted_sections:
        cli_args.append("--honor-case-in-force-sorted-sections")

    if sort_relative_in_force_sorted_sections:
        cli_args.append("--sort-relative-in-force-sorted-sections")

    if force_alphabetical_sort_within_sections:
        cli_args.append("force-alphabetical-sort-within-sections")

    if top:
        cli_args.append("--top")
        cli_args.append(top)

    if combine_straight_imports:
        cli_args.append("--combine-straight-imports")

    if no_lines_before:
        cli_args.append("--no-lines-before")
        cli_args.append(",".join(no_lines_before))

    if src_path:
        cli_args.append("--src-path")
        cli_args.append(",".join(src_path))

    if builtin:
        cli_args.append("--builtin")
        cli_args.append(builtin)

    if extra_builtin:
        cli_args.append("--extra-builtin")
        cli_args.append(extra_builtin)

    if future:
        cli_args.append("--future")
        cli_args.append(future)

    if thirdparty:
        cli_args.append("--thirdparty")
        cli_args.append(thirdparty)

    if project:
        cli_args.append("--project")
        cli_args.append(project)

    if known_local_folder:
        cli_args.append("--known-local-folder")
        cli_args.append(known_local_folder)

    if virtual_env:
        cli_args.append("--virtual-env")
        cli_args.append(virtual_env)

    if conda_env:
        cli_args.append("--conda-env")
        cli_args.append(conda_env)

    if python_version:
        cli_args.append("--python-version")
        cli_args.append(python_version)

    isort(cli_args)
