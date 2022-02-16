from parsimonious.grammar import Grammar

_ebnf = r"""
expr        = src / func
src         = src_t beg_open word end_open
func        = fun_t beg_open range comma type end_open
range       = range_open floatd comma floatd range_close
range_open  = beg_open / beg_closed
range_close = end_open / end_closed
beg_open    = ws "(" ws
end_open    = ws ")" ws
beg_closed  = ws "[" ws
end_closed  = ws "]" ws
comma       = ws "," ws
src_t       = "src"
fun_t       = "expr"
type        = int / float
int         = "int"
float       = "float" paren?
paren       = beg_open digits end_open
ws          = ~r"\s*"
word        = ~r"[-\w]+"
digits      = ~r"\d+"
floatd      = ~r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
"""


class SourceParser:
    def __init__(self):
        self.grammar = Grammar(_ebnf)

    def parse(self, source):
        return self.grammar.parse(source)
