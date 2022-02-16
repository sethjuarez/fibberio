from parsimonious.grammar import Grammar


class Parser:
    def __init__(self):
        self.grammar = Grammar(
          r"""
          text        =  src / func
          src         = src func_start name_exp func_end
          func        = expr func_start func_exp func_end
          func_exp     = func_range comma type
          func_range  = func_start num_exp comma num_exp func_end
          func_start  = "[" / "("
          func_end    = "]" / ")"
          comma       = ws? "," ws?
          src         = "src"
          expr        = "expr"
          type        = int / float
          int         = "int"
          float       = "float"
          ws          = ~"\s*"
          num_exp     = ~"[0-9]*"i
          name_exp    = ~"[A-Z 0-9]*"i
          """
        )

    def parse(self, source):
        return self.grammar.parse(source)
