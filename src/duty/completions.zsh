#compdef duty
local -a subcmds
subcmds=( $(duty --complete -- "${words[@]}") )
_describe 'duty' subcmds
