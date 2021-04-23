from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
from typing import List 
from ...integer.model import Model
from ...simplex.expressions.expression import Expression


class IntegerSolver(AbstractSolver):
    """
    An Integer Programming solver for the knapsack problems

    Methods:
    --------
    create_model() -> Models:
        creates and returns an integer programming model based on the self.problem
    """

    def create_model(self) -> Model:
        model = Model('Knapsack')
        variables = [model.create_variable(f"x{i}") for i, item in enumerate(self.problem.items)]
        weight = Expression()
        value = Expression()
        for var, item in zip(variables, self.problem.items):
            weight += item.weight * var
            value += item.value * var
            model.add_constraint(var <= 1)
        model.add_constraint(weight <= self.problem.capacity)
        model.maximize(value)
        return model

    def solve(self) -> Solution:
        m = self.create_model()
        integer_solution = m.solve(self.timelimit)
        items = [item for (i, item) in enumerate(self.problem.items) if integer_solution.value(m.variables[i]) > 0]
        solution = Solution.from_items(items, not m.solver.interrupted)
        self.total_time = m.solver.total_time
        return solution
