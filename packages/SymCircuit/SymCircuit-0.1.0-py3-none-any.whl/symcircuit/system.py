import re
from typing import List, Dict, Set, Tuple, Union, Optional, Iterable

from sympy import StrPrinter, Eq, Symbol, symbols, Expr, Limit
from sympy import Tuple as TTuple
from sympy.core.assumptions import _assume_defined
from sympy.solvers.solvers import _invert as sym_invert

# focus & seek based on https://github.com/sympy/sympy/issues/2720#issuecomment-312437508 by Christopher Smith @smichr

SymbolMap = Dict[str, Symbol]
ExpressionMap = Dict[str, Expr]
SymbolSet = Set[Symbol]
ReplacementRule = Tuple[Symbol, Expr]
ReplacementRules = List[ReplacementRule]


def complexity(e: Union[Eq, Expr]) -> int:
    return e.count_ops(visual=False)


def sortedsyms(s: SymbolSet) -> Iterable[Symbol]:
    return sorted(s, key=lambda sym: sym.name)


def sympy_parse(s: str, locs: SymbolMap) -> Optional[Expr]:
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication
    transformations = standard_transformations + (implicit_multiplication,)
    try:
        return parse_expr(s, local_dict=locs, transformations=transformations)
    except SyntaxError:
        return None


def seek(eqs: List[Eq], goals: SymbolSet, rules: ReplacementRules, *,
         recursive: bool = False, parameters: Optional[SymbolSet] = None, verbose=False):
    if parameters is None:
        parameters = set()
    goals.difference_update(parameters)

    def find_replacement_step():
        # go through equations, try find one that can be solved for a symbol we want
        for e in eqs:
            if not isinstance(e, Eq):
                continue
            for s in sortedsyms(goals):
                # rewrite two-sided equation to single expression == 0
                tozero = e.lhs - e.rhs
                ex, d = sym_invert(tozero, s)
                if d != s:
                    continue
                # didn't fail? note transformation and remove from pool
                rules.append((d, ex))
                eqs.remove(e)
                if verbose:
                    print(f"from {str(e)}: {str(d)} == {ex}")
                return s, ex
        # no equation solves to anything we need. this is bad
        raise ValueError(f"equation system cannot be inverted for: {str(goals)}")

    def replace_in_all(sym, expr):
        rep = {sym: expr}
        for i, eq in enumerate(eqs):
            if not isinstance(eq, Eq):
                continue
            # avoid dividing by zero
            ln, ld = eq.lhs.as_numer_denom()
            rn, rd = eq.rhs.as_numer_denom()
            new: Eq = Eq(ln * rd, rn * ld).xreplace(rep)
            if new is False:
                raise ValueError('inconsistency detected')
            # sometimes invert doesn't do well on complicated polynomials... try expanding it just in case
            eqs[i] = new.expand()
        eqs.sort(key=complexity)

    eqs.sort(key=complexity)

    while goals and eqs:
        try:
            sym, expr = find_replacement_step()
        except ValueError:
            if recursive:
                break
            raise
        goals.remove(sym)
        if recursive:
            goals |= (expr.free_symbols - parameters)
        replace_in_all(sym, expr)


def reduce_replacements(rules: ReplacementRules, final: int) -> ReplacementRules:
    rules = rules.copy()
    while len(rules) > final:
        x, s = rules.pop()
        rep = {x: s}
        for i, (xx, ss) in enumerate(rules):
            rules[i] = (xx, ss.xreplace(rep))
    for i in reversed(range(1, len(rules))):
        x, s = rules[i]
        rep = {x: s}
        for j in range(i):
            y, t = rules[j]
            rules[j] = y, sym_invert(y - t.xreplace(rep), y)[0]
    return rules


class SymbolicSystem:
    def __init__(self, source=None):
        self.debug: bool = False
        self.statements: List[Eq] = []
        self.parameters: SymbolSet = set()
        self.limits: List[Limit] = []
        self.limit_symbol = Symbol("$$fn")
        self.assumptions: SymbolSet = set()

        if isinstance(source, str):
            self.parse(source)
        elif isinstance(source, SymbolicSystem):
            self.extend(source)
        elif isinstance(source, list):
            for s in source:
                if isinstance(s, Eq):
                    self.statements.append(s)

    @property
    def symbols(self) -> SymbolSet:
        return TTuple(*self.statements).free_symbols

    @property
    def symboldict(self) -> SymbolMap:
        return {s.name: s for s in self.symbols}

    @property
    def parameterdict(self) -> SymbolMap:
        return {s.name: s for s in self.parameters}

    def info(self) -> str:
        r = []
        if self.statements:
            r.append("Equations:")
            r.extend("  " + str(s) for s in self.statements)
        if self.assumptions:
            r.append("Assuming:")
            rdict = {}
            for sym in sortedsyms(self.assumptions):
                a = " ".join(k for k, v in sym.assumptions0.items() if v == True)
                if a in rdict:
                    rdict[a].append(sym)
                else:
                    rdict[a] = [sym]
            for a, vs in rdict.items():
                vn = " ".join(v.name for v in vs)
                r.append(f"  {vn} :: {a}")
        if self.parameters:
            r.append("Using parameters:")
            r.append("  " + " ".join(sorted(str(p) for p in self.parameters)))
        if self.limits:
            r.append("Using limits:")
            for lim in self.limits:
                r.append(f"  {lim.args[1]} -> {lim.natural_dir}{lim.args[2]}")
        return "\n".join(r)

    def _parse_expr(self, ex: str) -> Optional[Expr]:
        # parse expressions while carrying all already known symbols and their predefined assumptions
        return sympy_parse(ex, self.symboldict)

    def parse(self, descr: str) -> 'SymbolicSystem':
        """
        Parse a string containing one or more definitions and add them to the current state

        Syntax::

            expr # anything                    comment out everything after #
            [lhs] == [rhs]                     equality statement
            [lhs]                              equality statement with implied "== 0"
            [syms] == const                    syms are constant and should not be removed from equations
            [syms] :: predicate[, predicate]   define syms with assumptions. must be done before any use of the symbols
                                               see https://docs.sympy.org/latest/guides/assumptions.html#predicates for a list
                                               of valid predicates and their implications
            [syms] -> [+-][sym]                after reasoning over statements, syms will be treated in the limit towards sym

        :param descr: system definition acording to the syntax above
        :return: self for chaining
        """
        for sl in descr.splitlines():
            sl = sl.strip()
            try:
                sl = sl[:sl.index("#")].rstrip()
            except ValueError:
                pass
            if not sl:
                continue
            args = []

            def try_match(pat) -> bool:
                nonlocal args
                args.clear()
                m = re.fullmatch("^" + pat + "$", sl, re.IGNORECASE | re.DOTALL)
                if m is None:
                    return False
                for g in m.groups():
                    if g is not None:
                        args.append(g.strip())
                return True

            if try_match(r"(.*)==\s*const\s*"):
                syms = symbols(args[0], seq=True)
                self.parameters.update(syms)
            elif try_match(r"(.*)==(.*)"):
                lhs = self._parse_expr(args[0])
                rhs = self._parse_expr(args[1])
                if lhs is None or rhs is None:
                    raise ValueError(f"Failed to parse statement line: {sl}")
                eq = Eq(lhs, rhs)
                self.statements.append(eq)
            elif try_match(r"(.*)->\s*([+-]?)(oo|0)\s*"):
                syms = symbols(args[0], seq=True)
                ndir = args[1] or "+"
                # SymPy: from where is sym approached, system syntax: to where does sym tend
                dir = "-" if ndir == "+" else "-"
                lim = self._parse_expr(args[2])
                for s in syms:
                    li = Limit(self.limit_symbol, s, lim, dir)
                    li.natural_dir = ndir
                    self.limits.append(li)
            elif try_match(r"(.*)::\s*(!?\w+)(?:\s*[, ]\s*(!?\w+))*\s*"):
                assum = {}
                for a in args[1:]:
                    val = not a.startswith("!")
                    if not val:
                        a = a[1:]
                    if a not in _assume_defined:
                        raise ValueError(f"Invalid assumption predicate: {a}")
                    assum[a] = val
                syms = symbols(args[0], seq=True, **assum)
                self.assumptions.update(syms)
            else:
                # parse expressions while carrying all already known symbols
                lhs = self._parse_expr(sl)
                if lhs is None:
                    raise ValueError(f"Failed to parse statement line: {sl}")
                eq = Eq(lhs, 0)
                self.statements.append(eq)
        return self

    def extend(self, other: 'SymbolicSystem'):
        self.statements.extend(st for st in other.statements if st not in self.statements)
        self.parameters.update(other.parameters)
        for lim in other.limits:
            if lim in self.limits:
                continue
            if any((l.args[1] == lim.args[1]) and not (l.args == lim.args) for l in self.limits):
                raise ValueError("Trying to merge systems with conflicting limit definitions")
            self.limits.append(lim)
        for assu in other.assumptions:
            if assu in self.assumptions:
                continue
            if any(s.name == assu.name for s in self.assumptions):
                raise ValueError("Trying to merge systems with conflicting assumptions")
            self.assumptions.add(assu)

    def __add__(self, other: 'SymbolicSystem') -> 'SymbolicSystem':
        res = SymbolicSystem()
        res.extend(self)
        res.extend(other)
        return res

    def focus(self, *goals, evaluate=True) -> Union[ReplacementRules, ExpressionMap]:
        s = self.symboldict
        goals = set(s[g] if isinstance(g, str) else g for g in goals) & self.symbols - self.parameters
        replacements: ReplacementRules = []
        if goals:
            eqs = self.statements.copy()
            syms = goals.copy()
            # first run to find one expression for each goal
            seek(eqs, syms, replacements, recursive=False, verbose=self.debug)
            if len(syms) or len(replacements) < len(goals):
                raise ValueError(f"Failed to locate all goals: {syms}")
            # now, fill rules that make these depend only on parameters
            for s, e in replacements:
                syms |= e.free_symbols
            seek(eqs, syms, replacements, recursive=True, parameters=self.parameters, verbose=self.debug)
        if evaluate:
            rules = reduce_replacements(replacements, len(goals))
            rdict = {s.name: self.apply_limits(e.simplify()) for s, e in rules}
            return rdict
        else:
            return replacements

    def apply_limits(self, expr: Expr) -> Expr:
        for lim in self.limits:
            lim = lim.subs(self.limit_symbol, expr)
            expr = lim.doit().simplify()
        return expr


def _StrPrinter_print_Relational(self, expr):
    from sympy.printing.precedence import precedence
    return '%s %s %s' % (self.parenthesize(expr.lhs, precedence(expr)),
                         self._relationals.get(expr.rel_op) or expr.rel_op,
                         self.parenthesize(expr.rhs, precedence(expr)))


def _on_import():
    StrPrinter._print_Relational = _StrPrinter_print_Relational


_on_import()
