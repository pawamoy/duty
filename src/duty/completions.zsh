#compdef duty
local -a subcmds
IFS=$'\n' subcmds=( $(duty --complete=zsh -- "${words[@]}") )
_describe 'duty' subcmds
