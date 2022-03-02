from parsimonious.nodes import Node
from parsimonious.grammar import Grammar, NodeVisitor


class Range:
    start_open: bool
    end_open: bool
    val_type: str
    precision: int
    start: float
    end: float
    floor: bool
    ceil: bool

    def __init__(
        self,
        start_open: bool = False,
        end_open: bool = False,
        val_type: str = "int",
        precision: int = 0,
        start: float = 0,
        end: float = 0,
        floor: bool = False,
        ceil: bool = False,
    ) -> None:
        self.start_open = start_open
        self.end_open = end_open
        self.precision = precision
        self.start = start
        self.end = end
        self.val_type = val_type
        self.floor = floor
        self.ceil = ceil

    def check(self, item: float) -> bool:
        # * case
        if self.floor and self.ceil:
            return True

        # type and precision corrections
        if self.val_type == "int":
            item = int(item)

        if self.precision > 0 and self.val_type == "float":
            item = round(item, self.precision)

        # lower bound
        lower = self.floor or (
            item > self.start if self.start_open else item >= self.start
        )

        # upper bound
        upper = self.ceil or (item < self.end if self.end_open else item <= self.end)

        return lower and upper


class RangeVisitor(NodeVisitor):
    def visit_expr(self, node, visited_children):
        p = Range()
        item = visited_children[0]
        # spot
        if type(item) == Node and item.text.strip() == "*":
            p.ceil = True
            p.floor = True
        elif type(item) == tuple:
            p.start_open = False
            p.end_open = False
            p.val_type = "float" if item[1] else "int"
            p.start = p.end = item[0]
        else:
            rg, tp = item

            p.start_open = rg[0]
            p.end_open = rg[3]

            # check first spot
            if type(rg[1]) == Node:
                p.floor = True
            else:
                p.start = rg[1][0]
                p.val_type = "float" if rg[1][1] else "int"

            # check second spot
            if type(rg[2]) == Node:
                p.ceil = True
            else:
                p.end = rg[2][0]
                p.val_type = "float" if rg[2][1] else "int"

            # override type (if specified)
            if type(tp) != Node:
                p.val_type = tp[0][0]
                p.precision = tp[0][1]
                if p.val_type == "float" and p.precision > 0:
                    p.start = round(p.start, p.precision)
                    p.end = round(p.end, p.precision)

        return p

    def visit_range(self, node, visited_children):
        op, n1, _, n2, cl = visited_children
        return op, n1, n2, cl

    def visit_range_open(self, node, visited_children):
        return node.text.strip() == "("

    def visit_range_close(self, node, visited_children):
        return node.text.strip() == ")"

    def visit_type_expr(self, node, visited_children):
        _, _, _, t = visited_children
        return t

    def visit_spot(self, node, visited_children):
        return visited_children[0]

    def visit_type(self, node, visited_children):
        return visited_children[0]

    def visit_int(self, node, visited_children):
        return "int", 0

    def visit_float(self, node, visited_children):
        _, p = visited_children
        return "float", 0 if type(p) == Node else p[0]

    def visit_paren(self, node, visited_children):
        _, d, _ = visited_children
        return d

    def visit_digits(self, node, visited_children):
        # inferred type is int
        return int(node.text)

    def visit_number(self, node, visited_childern):
        # inferred type is "float" if "."
        return float(node.text), "." in node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


class RangeParser:
    def __init__(self):
        _rangebnf = r"""
            expr        = spot / (range type_expr?)
            range       = range_open spot comma spot range_close
            range_open  = beg_open / beg_closed
            range_close = end_open / end_closed
            beg_open    = ws? "(" ws?
            end_open    = ws? ")" ws?
            beg_closed  = ws? "[" ws?
            end_closed  = ws? "]" ws?
            comma       = ws? "," ws?
            type_expr   = ws? "->" ws? type
            type        = int / float
            int         = "int"
            float       = "float" paren?
            paren       = beg_open digits end_open
            spot        = number / "*"
            ws          = ~r"\s*"
            digits      = ~r"\d+"
            number      = ~r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
        """

        self.grammar = Grammar(_rangebnf)

    def parse(self, source: str) -> Range:
        g = self.grammar.parse(source)
        sv = RangeVisitor()
        p = sv.visit(g)
        return p
