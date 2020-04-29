#!/usr/bin/env python3


import pandas as pd


class Var:
    '''`Building blocks for expressions`'''

    def __init__(self, name, negated=False):
        self.name = name
        self.negated = negated

    def __str__(self):
        return f'{"~" if self.negated else ""}{self.name}'

    def __eq__(self, other):
        return self.name == other.name and self.negated == other.negated

    def __hash__(self):
        return hash(self.name) ^ hash(self.negated)

    def conj(self):
        return Var(self.name, not self.negated)


class Prod:
    '''Order doesn't matter'''

    def __init__(self, vars_=None, removed_vars=None):
        self.vars_ = set(vars_) if vars_ else set()
        self.removed_vars = set(removed_vars) if removed_vars else set()
        self.simplify()

    def __str__(self):
        return ''.join(str(var) for var in
                       sorted(self.vars_, key=lambda var: var.name))

    def __mul__(self, other):
        assert isinstance(other, Prod)
        return Prod(self.vars_ | other.vars_,
                    self.removed_vars | other.removed_vars)

    def simplify(self):
        simpler_vars = set()
        for var in self.vars_:
            conj = var.conj()
            if conj not in self.vars_ and conj not in self.removed_vars:
                simpler_vars.add(var)
            else:
                self.removed_vars.add(var)
        self.vars_ = simpler_vars


class Sum:
    '''Ordered, as per requirements.'''

    def __init__(self, vars_=None):
        self.vars_ = list(vars_) if vars_ else []

    def __add__(self, other):
        if isinstance(other, Sum):
            return Sum(self.vars_ + other.vars_)
        if isinstance(other, Prod):
            return Sum(self.vars_ + [other])
        raise TypeError(
            'Sum objects can only be added to Sum and Prod objects.')

    def __str__(self):
        return '+'.join(str(var) for var in self.vars_)


ROWS = [Prod([Var('B'), Var('D', True)]),
        Prod([Var('B'), Var('D')]),
        Prod([Var('B', True), Var('D')]),
        Prod([Var('B', True), Var('D', True)]),
        ]
COLS = [Prod([Var('A'), Var('C', True)]),
        Prod([Var('A'), Var('C')]),
        Prod([Var('A', True), Var('C')]),
        Prod([Var('A', True), Var('C', True)]),
        ]

SIZE = 4


class Diagram:
    def __init__(self, n):
        binarystr = f'{n:>0{SIZE ** 2}b}'
        mat = [[int(digit) for digit in binarystr[i: i + SIZE]]
               for i in range(0, len(binarystr), SIZE)]
        self.df = pd.DataFrame(mat, index=ROWS, columns=COLS)
        self.simplified_df = pd.DataFrame(mat, index=ROWS, columns=COLS)
        self.terms = Sum()
        self.simplify()

    def __str__(self):
        return str(self.df)

    def _add_term_from_slice(self, slice_):
        term = Prod()
        for row_label in slice_.index:
            term *= row_label
        for col_label in slice_.columns:
            term *= col_label
        self.terms += term

    def find_eights_rows(self):
        for row_i in range(self.simplified_df.shape[0] - 1):  # 0, 1, 2
            row_slice = self.simplified_df.iloc[[row_i, row_i + 1], :]
            if row_slice.all().all():
                self._add_term_from_slice(row_slice)
                self.simplified_df.iloc[[row_i, row_i + 1], :] = 0

    def find_eights_cols(self):
        for col_i in range(self.simplified_df.shape[1] - 1):  # 0, 1, 2
            col_slice = self.simplified_df.iloc[:, [col_i, col_i + 1]]
            if col_slice.all().all():
                self._add_term_from_slice(col_slice)
                self.simplified_df.iloc[:, [col_i, col_i + 1]] = 0

    def find_edge_eights(self):
        edge_rows = self.simplified_df.iloc[[0, -1], :]
        if edge_rows.all().all():
            self._add_term_from_slice(edge_rows)
            self.simplified_df.iloc[[0, -1], :] = 0
        edge_cols = self.simplified_df.iloc[:, [0, -1]]
        if edge_cols.all().all():
            self._add_term_from_slice(edge_cols)
            self.simplified_df.iloc[:, [0, -1]] = 0

    def find_eights(self):
        self.find_eights_rows()
        self.find_eights_cols()
        self.find_edge_eights()

    def find_fours_rows(self):
        for row_i in range(self.simplified_df.shape[0]):
            row_slice = self.simplified_df.iloc[[row_i], :]
            if row_slice.all().all():
                self._add_term_from_slice(row_slice)
                self.simplified_df.iloc[[row_i], :] = 0

    def find_fours_cols(self):
        for col_i in range(self.simplified_df.shape[1]):
            col_slice = self.simplified_df.iloc[:, [col_i]]
            if col_slice.all().all():
                self._add_term_from_slice(col_slice)
                self.simplified_df.iloc[:, [col_i]] = 0

    def find_fours_blocks(self):
        # based on top left corner
        for corner_row_i in range(self.simplified_df.shape[0] - 1):
            for corner_col_i in range(self.simplified_df.shape[1] - 1):
                block_slice = self.simplified_df.iloc[[corner_row_i,
                                                       corner_row_i + 1],
                                                      [corner_col_i,
                                                       corner_col_i + 1]]
                if block_slice.all().all():
                    self._add_term_from_slice(block_slice)
                    self.simplified_df.iloc[[corner_row_i,
                                             corner_row_i + 1],
                                            [corner_col_i,
                                             corner_col_i + 1]] = 0

    def find_edge_fours(self):
        for corner_row_i in range(self.simplified_df.shape[0] - 1):  # 0, 1, 2
            edge_block = self.simplified_df.iloc[[
                corner_row_i, corner_row_i + 1], [0, -1]]
            if edge_block.all().all():
                self._add_term_from_slice(edge_block)
                self.simplified_df.iloc[[
                    corner_row_i, corner_row_i + 1], [0, -1]] = 0
        for corner_col_i in range(self.simplified_df.shape[1] - 1):  # 0, 1, 2
            edge_block = self.simplified_df.iloc[[
                0, -1], [corner_col_i, corner_col_i + 1]]
            if edge_block.all().all():
                self._add_term_from_slice(edge_block)
                self.simplified_df.iloc[[0, -1],
                                        [corner_col_i, corner_col_i + 1]] = 0

    def check_four_corners(self):
        four_corners = self.simplified_df.iloc[[0, -1], [0, -1]]
        if four_corners.all().all():
            self._add_term_from_slice(four_corners)
            self.simplified_df.iloc[[0, -1], [0, -1]] = 0

    def find_fours(self):
        self.find_fours_rows()
        self.find_fours_cols()
        self.find_fours_blocks()
        self.find_edge_fours()
        self.check_four_corners()

    def find_twos_rows(self):
        # based on left tile
        for row_i in range(self.simplified_df.shape[0]):
            for col_i in range(self.simplified_df.shape[1] - 1):
                row_slice = self.simplified_df.iloc[[
                    row_i], [col_i, col_i + 1]]
                if row_slice.all().all():
                    self._add_term_from_slice(row_slice)
                    self.simplified_df.iloc[[row_i], [col_i, col_i + 1]] = 0

    def find_twos_cols(self):
        # based on top tile
        for row_i in range(self.simplified_df.shape[0] - 1):
            for col_i in range(self.simplified_df.shape[1]):
                row_slice = self.simplified_df.iloc[[
                    row_i, row_i + 1], [col_i]]
                if row_slice.all().all():
                    self._add_term_from_slice(row_slice)
                    self.simplified_df.iloc[[row_i, row_i + 1], [col_i]] = 0

    def find_edge_twos(self):
        for row_i in range(self.simplified_df.shape[0]):
            two_edges = self.simplified_df.iloc[[row_i], [0, -1]]
            if two_edges.all().all():
                self._add_term_from_slice(two_edges)
                self.simplified_df.iloc[[row_i], [0, -1]] = 0
        for col_i in range(self.simplified_df.shape[1]):
            two_edges = self.simplified_df.iloc[[0, -1], [col_i]]
            if two_edges.all().all():
                self._add_term_from_slice(two_edges)
                self.simplified_df.iloc[[0, -1], [col_i]] = 0

    def find_twos(self):
        self.find_twos_rows()
        self.find_twos_cols()
        self.find_edge_twos()

    def find_ones(self):
        for row_i in range(self.simplified_df.shape[0]):
            for col_i in range(self.simplified_df.shape[1]):
                cell = self.simplified_df.iloc[[row_i], [col_i]]
                if cell.all().all():
                    self._add_term_from_slice(cell)
                    self.simplified_df.iloc[[row_i], [col_i]] = 0

    def simplify(self):
        self.find_eights()
        self.find_fours()
        self.find_twos()
        self.find_ones()


if __name__ == "__main__":
    d = Diagram(0x6090)
    print(d.terms)
