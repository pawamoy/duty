from __future__ import annotations

from typing import Literal

from duty._internal.tools._base import Tool


class git_changelog(Tool):  # noqa: N801
    """Call [git-changelog](https://github.com/pawamoy/git-changelog)."""

    cli_name = "git-changelog"
    """The name of the executable on PATH."""

    def __init__(
        self,
        repository: str | None = None,
        *,
        config_file: str | None = None,
        bump: str | None = None,
        versioning: Literal["semver", "pep440"] | None = None,
        in_place: bool = False,
        version_regex: str | None = None,
        marker_line: str | None = None,
        output: str | None = None,
        provider: Literal["github", "gitlab", "bitbucket"] | None = None,
        parse_refs: bool = False,
        release_notes: bool = False,
        input: str | None = None,  # noqa: A002
        convention: Literal["basic", "angular", "conventional"] | None = None,
        sections: list[str] | None = None,
        template: str | None = None,
        git_trailers: bool = False,
        omit_empty_versions: bool = False,
        no_zerover: bool = False,
        filter_commits: str | None = None,
        jinja_context: list[str] | None = None,
        version: bool = False,
        debug_info: bool = False,
    ) -> None:
        r"""Run `git-changelog`.

        Parameters:
            repository: The repository path, relative or absolute. Default: current working directory.
            config_file: Configuration file(s).
            bump: Specify the bump from latest version for the set of unreleased commits.
                Can be one of `auto`, `major`, `minor`, `patch` or a valid SemVer version (eg. 1.2.3).
                For both SemVer and PEP 440 versioning schemes (see -n), `auto` will bump the major number
                if a commit contains breaking changes (or the minor number for 0.x versions, see -Z),
                else the minor number if there are new features, else the patch number. Default: unset (false).
            versioning: Versioning scheme to use when bumping and comparing versions.
                The selected scheme will impact the values accepted by the `--bump` option.
                Supported: `pep440`, `semver`.

                PEP 440 provides the following bump strategies: `auto`, `epoch`, `release`, `major`, `minor`, `micro`, `patch`,
                `pre`, `alpha`, `beta`, `candidate`, `post`, `dev`.
                Values `auto`, `major`, `minor`, `micro` can be suffixed with one of `+alpha`, `+beta`, `+candidate`, and/or `+dev`.
                Values `alpha`, `beta` and `candidate` can be suffixed with `+dev`.
                Examples: `auto+alpha`, `major+beta+dev`, `micro+dev`, `candidate+dev`, etc..

                SemVer provides the following bump strategies: `auto`, `major`, `minor`, `patch`, `release`.
                See the docs for more information. Default: unset (`semver`).
            in_place: Insert new entries (versions missing from changelog) in-place.
                An output file must be specified. With custom templates, you can pass two additional
                arguments: `--version-regex` and `--marker-line`.
                When writing in-place, an `in_place` variable will be injected in the Jinja context,
                allowing to adapt the generated contents (for example to skip changelog headers or footers).
                Default: unset (false).
            version_regex: A regular expression to match versions in the existing changelog
                (used to find the latest release) when writing in-place.
                The regular expression must be a Python regex with a `version` named group.
                Default: `^## \[(?P<version>v?[^\]]+)`.
            marker_line: A marker line at which to insert new entries (versions missing from changelog).
                If two marker lines are present in the changelog, the contents between those two lines
                will be overwritten (useful to update an 'Unreleased' entry for example). Default: `<!-- insertion marker -->`.
            output: Output to given file. Default: standard output.
            provider: Explicitly specify the repository provider. Default: unset.
            parse_refs: Parse provider-specific references in commit messages (GitHub/GitLab/Bitbucket issues, PRs, etc.).
                Default: unset (false).
            release_notes: Output release notes to stdout based on the last entry in the changelog. Default: unset (false).
            input: Read from given file when creating release notes. Default: `CHANGELOG.md`.
            convention: The commit convention to match against. Default: `basic`.
            sections: A comma-separated list of sections to render.
                See the available sections for each supported convention in the description. Default: unset (None).
            template: The Jinja2 template to use.
                Prefix it with `path:` to specify the path to a Jinja templated file. Default: `keepachangelog`.
            git_trailers: Parse Git trailers in the commit message.
                See https://git-scm.com/docs/git-interpret-trailers. Default: unset (false).
            omit_empty_versions: Omit empty versions from the output. Default: unset (false).
            no_zerover: By default, breaking changes on a 0.x don't bump the major version, maintaining it at 0.
                With this option, a breaking change will bump a 0.x version to 1.0.
            filter_commits: The Git revision-range filter to use (e.g. `v1.2.0..`). Default: no filter.
            jinja_context: Pass additional key/value pairs to the template.
                Option can be used multiple times.
                The key/value pairs are accessible as 'jinja_context' in the template.
            version: Show the current version of the program and exit.
            debug_info: Print debug information.
        """
        cli_args = []

        if repository:
            cli_args.append(repository)

        if config_file:
            cli_args.append("--config-file")
            cli_args.append(config_file)

        if bump:
            cli_args.append("--bump")
            cli_args.append(bump)

        if versioning:
            cli_args.append("--versioning")
            cli_args.append(versioning)

        if in_place:
            cli_args.append("--in-place")

        if version_regex:
            cli_args.append("--version-regex")
            cli_args.append(version_regex)

        if marker_line:
            cli_args.append("--marker-line")
            cli_args.append(marker_line)

        if output:
            cli_args.append("--output")
            cli_args.append(output)

        if provider:
            cli_args.append("--provider")
            cli_args.append(provider)

        if parse_refs:
            cli_args.append("--parse-refs")

        if release_notes:
            cli_args.append("--release-notes")

        if input:
            cli_args.append("--input")
            cli_args.append(input)

        if convention:
            cli_args.append("--convention")
            cli_args.append(convention)

        if sections:
            cli_args.append("--sections")
            cli_args.append(",".join(sections))

        if template:
            cli_args.append("--template")
            cli_args.append(template)

        if git_trailers:
            cli_args.append("--git-trailers")

        if omit_empty_versions:
            cli_args.append("--omit-empty-versions")

        if no_zerover:
            cli_args.append("--no-zerover")

        if filter_commits:
            cli_args.append("--filter-commits")
            cli_args.append(filter_commits)

        if jinja_context:
            for key_value in jinja_context:
                cli_args.append("--jinja-context")
                cli_args.append(key_value)

        if version:
            cli_args.append("--version")

        if debug_info:
            cli_args.append("--debug-info")

        super().__init__(cli_args)

    def __call__(self) -> int:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        from git_changelog.cli import main as run_git_changelog  # noqa: PLC0415

        return run_git_changelog(self.cli_args)
