#compdef duty

# Zsh completion script for duty.
# To be installed as `_duty` in one of the directories of `fpath`.

local -a candidates

# `words` contains the entire command line up til now (including the program name).
# We hand it to duty so it can figure out the current context:
# global options, duty names, the current duty's parameters, or some combination.
# Candidates are printed one per line, as `word:description` pairs
# (the colon and description are omitted when there is no description).
candidates=("${(@f)$(duty --complete=zsh -- "${words[@]}")}")

# Drop empty lines, they would show up as empty candidates.
candidates=("${(@)candidates:#}")

# `_describe` completes words while displaying their descriptions.
_describe -t duties 'duty' candidates
