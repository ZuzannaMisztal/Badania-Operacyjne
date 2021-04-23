from copy import deepcopy
from . import model as m 
from .expressions import objective as o 
from .expressions import constraint as c
import numpy as np 

class Solution:
    """
        A class to represent a solution to linear programming problem.


        Attributes
        ----------
        model : Model
            model corresponding to the solution
        assignment : list[float]
            list with the values assigned to the variables
            order of values should correspond to the order of variables in model.variables list


        Methods
        -------
        __init__(model: Model, assignment: list[float]) -> Solution:
            constructs a new solution for the specified model and assignment
        value(var: Variable) -> float:
            returns a value assigned to the specified variable
        objective_value()
            returns value of the objective function
    """

    def __init__(self, model, assignment):
        "Assignment is just a list of values"
        self.assignment = assignment
        self.model = model

    def value(self, var):
        return self.assignment[var.index]

    def objective_value(self):
        return self.model.objective.evaluate(self.assignment)       

    def __str__(self):
        text = f'- objective value: {self.objective_value()}\n'
        text += '- assignment:'
        for (i, val) in enumerate(self.assignment):
            text += f'\n\t- {self.model.variables[i].name} = {val}'
        return text


class Tableaux:
    """
        A class to represent a solution to linear programming problem.


        Attributes
        ----------
        model : Model
            model corresponding to the tableaux
        table : numpy.Array
            2d-array with the tableaux

        Methods
        -------
        __init__(model: Model, solution: Solution) -> Tableaux:
            constructs a new tableaux for the specified model and solution
        cost_factors() -> numpy.Array:
            returns a vector containing factors in the cost row
        cost() -> float:
            returns the cost of solution represented in tableaux
        is_optimal() -> bool:
            checks whether the current solution is optimal
        choose_entering_variable() -> int:
            finds index of the variable, that should enter the basis next
        is_unbounded(col: int) -> bool:
            checks whether the problem is unbounded
        choose_leaving_variable(col: int) -> int:
            finds index of the variable, that should leave the basis next
        pivot(col: int, row: int):
            updates tableaux using pivot operation with given entering and leaving variables
        extract_solution() -> Solution:
            returns solution corresponding to the tableaux
        extract_basis() -> list[int]
            returns list of indexes corresponding to the variables belonging to the basis
    """

    def __init__(self, model):
        self.model = model
        # the "z column" is always constant so we don't include it in our table
        cost_row = np.array((-1 * model.objective.expression).factors(model) + [0.0])
        self.table = np.array([cost_row] + [c.expression.factors(model) + [c.bound] for c in model.constraints])

    def cost_factors(self):
        return self.table[0, :-1]

    def cost(self):
        return self.table[0, -1]

    def is_optimal(self):
        return all(factor >= 0 for factor in self.cost_factors())

    def choose_entering_variable(self):
        return np.where(self.cost_factors() == min(self.cost_factors()))[0][0]

    def is_unbounded(self, col):
        return all(factor <= 0 for factor in self.table[:, col])

    def choose_leaving_variable(self, col):
        beta_column = self.table[:, -1][1:]
        pivot_column = self.table[:, col][1:]
        decider = [beta / pivot if pivot != 0 else float('inf') for beta, pivot in zip(beta_column, pivot_column)]
        decider = [value if value >= 0 else float('inf') for value in decider]
        return np.where(decider == min(decider))[0][0] + 1

    def pivot(self, row, col):
        old_table = deepcopy(self.table)
        self.table[row, :] /= old_table[row][col]
        self.table[:, col] = [0 if i != row else 1 for i, _ in enumerate(old_table[:, col])]
        for r, _ in enumerate(old_table):
            for c, _ in enumerate(old_table[r, :]):
                if r == row or c == col:
                    continue
                t_prim = old_table[row, c] / old_table[row, col]
                self.table[r][c] = old_table[r, c] + (-old_table[r, col]) * t_prim

    def extract_solution(self):
        # TODO:
        # value of the variable in basis is the beta value (last column of the table)
        # belonging the row, where the variable has value 1.0
        # tip: extract_basis may be helpful
        basis = self.extract_basis()
        result = []
        number_of_variables = self.table.shape[1] - 1
        for var in range(number_of_variables):
            if var in basis:
                variable_value = self.find_variable_value(
                    self.table[:, var], self.table[:, -1])
                result.append(variable_value)
            else:
                result.append(0)
        return result

    @staticmethod
    def find_variable_value(column, rhs):
        for i, v in enumerate(column):
            if v == 1:
                return rhs[i]

    def extract_basis(self):
        rows_n, cols_n = self.table.shape
        basis = [-1 for _ in range(rows_n - 1)]
        for c in range(cols_n - 1):
            column = self.table[:, c]
            belongs_to_basis = column.min() == 0.0 and column.max() == 1.0 and column.sum() == 1.0
            if belongs_to_basis:
                row = np.where(column == 1.0)[0][0]
                # [row-1] because we ignore the cost variable in the basis
                basis[row-1] = c
        return basis

    def __str__(self):
        def cell(x, w):
            return '{0: >{1}}'.format(x, w)

        cost_name = "z" if self.model.objective.factor > 0 else "-z"
        basis = self.extract_basis()
        header = ["basis", cost_name] + [var.name for var in self.model.variables] + ["b"]
        longest_col = max([len(h) for h in header])

        rows = [[cost_name]] + [[self.model.variables[i].name] for i in basis]

        for (i, r) in enumerate(rows):
            cost_factor = 0.0 if i > 0 else 1.0
            r += [str(v) for v in [cost_factor] + list(self.table[i])]
            longest_col = max(longest_col, max([len(v) for v in r]))

        header = [cell(h, longest_col) for h in header]
        rows = [[cell(v, longest_col) for v in row] for row in rows]

        cell_sep = " | "

        result = cell_sep.join(header) + "\n"
        for row in rows:
            result += cell_sep.join(row) + "\n"
        return result


class UnboundedException(Exception):
    def __str__(self) -> str:
        return "LP model is unbounded"
    __repr__ = __str__


class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Solution:
            solves the given model and return the first solution
    """

    def solve(self, model):
        normal_model = self._normalize_model(deepcopy(model))
        tableaux = Tableaux(normal_model)
        while not tableaux.is_optimal():
            pivot_col = tableaux.choose_entering_variable()
            if tableaux.is_unbounded(pivot_col):
                raise UnboundedException("Linear Programming model is unbounded")
            pivot_row = tableaux.choose_leaving_variable(pivot_col)

            tableaux.pivot(pivot_row, pivot_col)
        
        return Solution(normal_model, tableaux.extract_solution())

    def _normalize_model(self, model):
        """
            _normalize_model(model: Model) -> Model:
                returns a normalized version of the given model 
        """
        if model.objective.type == o.ObjectiveType.MIN:
            model.objective.invert()
        
        self.slack_variables = dict()
        for (i, constraint) in enumerate(model.constraints):
            if constraint.type != c.ConstraintType.EQ:
                slack_var = model.create_variable(f"s{i}")
                self.slack_variables[slack_var.index] = i
                
                if constraint.bound < 0:
                    constraint.invert()
                
                constraint.expression = constraint.expression + slack_var * c.ConstraintType.LE.value * -1
                constraint.type = c.ConstraintType.EQ 
        return model


        
        
        
        
        
        

