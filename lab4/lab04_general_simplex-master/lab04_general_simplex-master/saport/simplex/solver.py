from copy import deepcopy

from . import model as m 
from .expressions import objective as o 
from .expressions import constraint as c
from .expressions import variable as v
from . import solution as s 
from . import tableaux as t
import numpy as np 


class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Solution:
            solves the given model and return the first solution
    """

    def solve(self, model):
        normal_model = self._normalize_model(model)
        if len(self.slack_variables) < len(normal_model.constraints):
            tableaux = self._presolve(normal_model)
        else:
            tableaux = self._basic_initial_tableaux(normal_model)

        self._optimize(tableaux)
        solution = tableaux.extract_solution()
        return self._translate_to_original_model(solution, model)

    def _optimize(self, tableaux):
        while not tableaux.is_optimal():
            pivot_col = tableaux.choose_entering_variable()
            if tableaux.is_unbounded(pivot_col):
                raise Exception("Linear Programming model is unbounded")
            pivot_row = tableaux.choose_leaving_variable(pivot_col)

            tableaux.pivot(pivot_row, pivot_col)

    def _presolve(self, model):
        """
            _presolve(model: Model) -> Tableaux:
                returns a initial tableaux for the second phase of simplex
        """
        presolve_model = self._create_presolve_model(model)
        tableaux = self._presolve_initial_tableaux(presolve_model)
        self._optimize(tableaux)

        if self._artifical_variables_are_positive(tableaux):
            raise Exception("Linear Programming model is unsolvable")

        basis = tableaux.extract_basis()
        tableaux = self._remove_artificial_variables(tableaux)
        tableaux = self._restore_original_cost_row(tableaux, model)
        tableaux = self._fix_cost_row_to_the_basis(tableaux, basis)
        return tableaux

    def _normalize_model(self, original_model):
        """
            _normalize_model(model: Model) -> Model:
                returns a normalized version of the given model 
        """

        model = deepcopy(original_model)
        self._change_objective_to_max(model)
        self._change_constraints_bounds_to_nonnegative(model)
        self.slack_variables = self._add_slack_variables(model)
        self.surplus_variables = self._add_surplus_variables(model)   
        return model

    def _create_presolve_model(self, normalized_model):
        presolve_model = deepcopy(normalized_model)
        self.artificial_variables = self._add_artificial_variables(presolve_model)
        return presolve_model    

    def _change_objective_to_max(self, model):
        if model.objective.type == o.ObjectiveType.MIN:
            model.objective.invert()

    def _change_constraints_bounds_to_nonnegative(self, model):
        for constraint in model.constraints:
            if constraint.bound < 0:
                constraint.invert()
    
    def _add_slack_variables(self, model):
        slack_variables = dict()
        for (i, constraint) in enumerate(model.constraints.copy()):
            if constraint.type == c.ConstraintType.LE:
                slack_var = model.create_variable(f"s{i}")
                slack_variables[slack_var] = i
                constraint.expression = constraint.expression + slack_var
        return slack_variables

    def _add_surplus_variables(self, model):
        surplus_variables = dict()
        for (i, constraint) in enumerate(model.constraints.copy()):
            if constraint.type == c.ConstraintType.GE:
                surp_var = model.create_variable(f"s{i}")
                surplus_variables[surp_var] = i
                constraint.expression = constraint.expression - surp_var
        return surplus_variables

    def _add_artificial_variables(self, model):
        artificial_variables = dict()
        for (i, constraint) in enumerate(model.constraints.copy()):
            if i not in self.slack_variables.values():
                art_var = model.create_variable(f"R{i}")
                artificial_variables[art_var] = i
                constraint.expression = constraint.expression + art_var
        return artificial_variables

    def _presolve_initial_tableaux(self, model):
        # TODO: create an initial tableaux for the artificial variables
        # - cost row should contain 1.0 for every artificial variable
        # - then you should subtract from it rows corresponding to the artificial variables
        # you may look at the _basic_initial_tableaux on how to create a tableaux
        cost_row = [0.0 for _ in range(len(model.variables) - len(self.artificial_variables))]
        cost_row = np.array(cost_row + [1.0 for _ in range(len(self.artificial_variables))] + [0.0])
        for i in self.artificial_variables.values():
            constraint = model.constraints[i]
            row = constraint.expression.factors(model) + [constraint.bound]
            cost_row = [cost_val - val for cost_val, val in zip(cost_row, row)]
        table = np.array([cost_row] + [c.expression.factors(model) + [c.bound] for c in model.constraints])
        return t.Tableaux(model, table)

    def _basic_initial_tableaux(self, model):
        cost_row = np.array((-1 * model.objective.expression).factors(model) + [0.0])
        table = np.array([cost_row] + [c.expression.factors(model) + [c.bound] for c in model.constraints])
        return t.Tableaux(model, table)

    def _artifical_variables_are_positive(self, tableaux):
        solution = tableaux.extract_solution().assignment
        artificials = solution[-len(self.artificial_variables):]
        return any(var > 0 for var in artificials)

    def _remove_artificial_variables(self, tableaux):
        # TODO: remove artificial variables from the tableaux
        to_delete = [i for i, _ in enumerate(tableaux.cost_factors())][-len(self.artificial_variables):]
        tableaux.table = np.delete(tableaux.table, to_delete, 1)
        x = 10
        return tableaux

    def _restore_original_cost_row(self, tableaux: t.Tableaux, model):
        # TODO: replace cost row in the tableaux with the original one
        cost_row = np.array((-1 * model.objective.expression).factors(model) + [0.0])
        tableaux.table[0] = cost_row
        return tableaux

    def _fix_cost_row_to_the_basis(self, tableaux, basis):
        # TODO: similarly to the way we have zeroed the artificial variables in the first phase
        #       now we have to subtract/add rows to the cost row to make the variables in basis
        #       equal zero in the cost row
        for row_index, column_index in enumerate(basis):
            factor = tableaux.cost_factors()[column_index]
            cost_row = [cost_val - factor * val for cost_val, val
                        in zip(tableaux.table[0], tableaux.table[row_index + 1])]
            tableaux.table[0] = cost_row
        return tableaux

    def _translate_to_original_model(self, solution, model):
        assignment = [solution.value(var) for var in model.variables]
        return s.Solution(model, assignment)
