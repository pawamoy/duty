from typing import Optional

CompletionCandidateType = tuple[str, Optional[str]]


class CompletionParser:
    @classmethod
    def parse(cls, candidates: list[CompletionCandidateType], shell: str) -> str:
        """Parses a list of completion candidates for selected shell completion command.

        Parameters:
            candidates: List of completion candidates with optional descriptions.
            shell: Shell for which to parse the candidates.

        Raises:
            NotImplementedError: When parser is not implemented for selected shell.

        Returns:
            String to be passed to shell completion command.
        """
        try:
            return getattr(cls, f"_{shell}")(candidates)
        except AttributeError as exc:
            msg = f"CompletionParser method for {shell!r} shell is not implemented!"
            raise NotImplementedError(msg) from exc

    @staticmethod
    def _zsh(candidates: list[CompletionCandidateType]) -> str:
        def parse_candidate(item: CompletionCandidateType) -> str:
            completion, help_text = item
            # We only have space for one line of description,
            # so I remove descriptions of sub-command parameters from help_text
            # by removing everything after the first newline.
            # I don't think it is the best approach and should be discussed.
            return f"{completion}: {help_text or '-'}".split("\n", 1)[0]

        return "\n".join(parse_candidate(candidate) for candidate in candidates)

    @staticmethod
    def _bash(candidates: list[CompletionCandidateType]) -> str:
        return "\n".join(completion for completion, _ in candidates)
