# Based on pyinvoke implementation of zsh completion
_complete_duty() {
    reply=( $(duty --complete -- ${words}) )
}

compctl -K _complete_duty + -f duty
