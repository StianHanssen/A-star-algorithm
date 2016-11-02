#!/usr/bin/python

import copy
import itertools
import os
from sys import platform

'''
Class given for exercise
'''


class CSP:

    def __init__(self):
        # self.__variables is a list of the variable names in the CSP
        self.__variables = []

        # self.__domains[i] is a list of legal values for variable i
        self.__domains = {}

        # self.__constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.__constraints = {}

        self.__backtrack_called = 0
        self.__backtrack_failed = 0

    def __get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def __get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.__constraints for j in self.__constraints[i]]

    def __get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in __get_all_arcs().
        """
        return [(i, var) for i in self.__constraints[var]]

    def __is_complete(self, assignment):
        for domain in assignment.values():
            if len(domain) != 1:
                return False
        return True

    def __backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.
        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.
        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.
        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        self.__backtrack_called += 1
        if self.__is_complete(assignment):
            return assignment
        var = self.__select_unassigned_variable(assignment)
        for value in assignment[var]:
            test_assignment = copy.deepcopy(assignment)
            test_assignment[var] = [value]
            if value in self.__domains[var]:
                if self.__inference(test_assignment, self.__get_all_arcs()):
                    result = self.__backtrack(test_assignment)
                    if result is not None:
                        return result
        self.__backtrack_failed += 1
        return None

    def __select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        return min([(len(domain), name) for name, domain in assignment.iteritems() if len(domain) != 1])[1]

    def __inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        while queue:
            (i, j) = queue.pop(0)
            if self.__revise(assignment, i, j):
                if not self.__domains.get(i):
                    return False
                for neigh_arc in self.__get_all_neighboring_arcs(i):
                    if neigh_arc != (i, j):
                        queue.append(neigh_arc)
        return True

    def __revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        legal_moves = set(self.__constraints[i][j])
        revised = False
        for x in assignment[i]:
            moves = set(itertools.product(x, assignment[j]))
            if not moves.intersection(legal_moves):
                assignment[i].remove(x)
                revised = True
        return revised

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.__variables.append(name)
        self.__domains[name] = list(domain)
        self.__constraints[name] = {}

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.__domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.__inference(assignment, self.__get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.__backtrack(assignment)

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if j not in self.__constraints[i]:
            # First, get a list of all possible pairs of values between
            # variables i and j
            self.__constraints[i][j] = self.get_all_possible_pairs(
                self.__domains[i], self.__domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.__constraints[i][j] = filter(
            lambda value_pair: filter_function(*value_pair), self.__constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if j not in self.__constraints[i]:
            # First, get a list of all possible pairs of values between
            # variables i and j
            self.__constraints[i][j] = self.get_all_possible_pairs(
                self.__domains[i], self.__domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.__constraints[i][j] = filter(
            lambda value_pair: filter_function(*value_pair), self.__constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def get_backtrack_called(self):
        return self.__backtrack_called

    def get_backtrack_failed(self):
        return self.__backtrack_failed

    @staticmethod
    def get_board_path(imageName):
        slash = "\\" if platform == "win32" else "/"
        path = os.path.dirname(os.path.abspath(__file__))
        path += slash + "Boards" + slash + imageName
        return path

    @staticmethod
    def create_map_coloring_csp():
        """Instantiate a CSP representing the map coloring problem from the
        textbook. This can be useful for testing your CSP solver as you
        develop your code.
        """
        csp = CSP()
        states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
        edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
                 'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
        colors = ['red', 'green', 'blue']
        for state in states:
            csp.add_variable(state, colors)
        for state, other_states in edges.items():
            for other_state in other_states:
                csp.add_constraint_one_way(
                    state, other_state, lambda i, j: i != j)
                csp.add_constraint_one_way(
                    other_state, state, lambda i, j: i != j)
        return csp

    @staticmethod
    def create_sudoku_csp(filename):
        """Instantiate a CSP representing the Sudoku board found in the text
        file named 'filename' in the current directory.
        """
        csp = CSP()
        board = map(lambda x: x.strip(), open(filename, 'r'))

        for row in range(9):
            for col in range(9):
                if board[row][col] == '0':
                    csp.add_variable('%d-%d' % (row, col),
                                     map(str, range(1, 10)))
                else:
                    csp.add_variable('%d-%d' % (row, col), [board[row][col]])

        for row in range(9):
            csp.add_all_different_constraint(
                ['%d-%d' % (row, col) for col in range(9)])
        for col in range(9):
            csp.add_all_different_constraint(
                ['%d-%d' % (row, col) for row in range(9)])
        for box_row in range(3):
            for box_col in range(3):
                cells = []
                for row in range(box_row * 3, (box_row + 1) * 3):
                    for col in range(box_col * 3, (box_col + 1) * 3):
                        cells.append('%d-%d' % (row, col))
                csp.add_all_different_constraint(cells)

        return csp

    @staticmethod
    def print_sudoku_solution(solution):
        """Convert the representation of a Sudoku solution as returned from
        the method CSP.backtracking_search(), into a human readable
        representation.
        """
        for row in range(9):
            for col in range(9):
                print solution['%d-%d' % (row, col)][0],
                if col == 2 or col == 5:
                    print '|',
            print
            if row == 2 or row == 5:
                print '------+-------+------'


if __name__ == '__main__':
    sudoku_solver = CSP.create_sudoku_csp(CSP.get_board_path("world_hardest.txt"))
    sudoku_solver.print_sudoku_solution(sudoku_solver.backtracking_search())
    print "\nBacktrack called:", sudoku_solver.get_backtrack_called()
    print "Backtrack failed:", sudoku_solver.get_backtrack_failed()
