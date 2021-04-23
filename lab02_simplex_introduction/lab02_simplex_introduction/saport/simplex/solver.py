from copy import deepcopy
from . import model as m 
from .expressions import objective as o 
from .expressions import constraint as c

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
        for (i,val) in enumerate(self.assignment):
            text += f'\n\t- {self.model.variables[i].name} = {val}'
        return text

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
        solution = self._find_initial_solution(normal_model)
        tableaux = self._tableux(normal_model, solution)
        
        print("---")
        print("Normal model:")
        print(normal_model)
        print("---")
        print("Initial solution:")
        print(solution)
        print("---")
        print("Initial tableaux:")
        self._print_tableaux(normal_model, tableaux)

        return solution

    def _normalize_model(self, model):
        """
            _normalize_model(model: Model) -> Model:
                returns a normalized version of the given model 
        """
        if model.objective.type == o.ObjectiveType.MIN:
            model.objective.expression.atoms = [-1*a for a in model.objective.expression.atoms];
            model.objective.type = o.ObjectiveType.MAX
            self.objective_factor = 1
        else:
            self.objective_factor = -1
        
        self.slack_variables = dict()
        for (i,constraint) in enumerate(model.constraints):
            if constraint.type != c.ConstraintType.EQ:
                slack_var = model.create_variable(f"s{i}")
                self.slack_variables[slack_var.index] = i
                
                if constraint.type == c.ConstraintType.LE:
                    constraint.expression = constraint.expression + slack_var
                else:
                    constraint.expression = constraint.expression - slack_var

                constraint.type = c.ConstraintType.EQ 
        return model

    def _find_initial_solution(self, model):
        """
        _find_initial_solution(model: Model) -> Solution
            returns an initial solution for the given model
        """
        assignment = [0 for _ in model.variables]
        for (slack_index, constraint_index) in self.slack_variables.items():
            assignment[slack_index] = model.constraints[constraint_index].bound
        return Solution(model, assignment)

    def _tableux(self, model, solution):
        """
        _tableux(model: Model, solution: Solution) -> list[list[float]]
            returns a tableux for the given model and solution
        """
        cost_row = [1] + [0 for _ in model.variables] 
        for atom in model.objective.expression.atoms:
            cost_row[atom.var.index+1] = self.objective_factor * atom.factor
        cost_row.append(model.objective.evaluate(solution.assignment))

        base_rows = [[0] for _ in model.constraints]
        for (i,row) in enumerate(base_rows):
            row += [0 for _ in model.variables]
            for atom in model.constraints[i].expression.atoms:
                row[atom.var.index + 1] = atom.factor
            row.append(float(model.constraints[i].bound))

        return [cost_row] + base_rows 

    def _print_tableaux(self, model, tableux):
        def cell(x, w):
            return '{0: >{1}}'.format(x, w)

        header = ["base", "z"] + [var.name for var in model.variables] + ["rhs"]
        longest_col = max([len(h) for h in header])

        rows = [["z"]] + [[model.variables[i].name] for i in sorted(self.slack_variables.keys())]

        for (i,r) in enumerate(rows):
            r += [str(v) for v in tableux[i]]
            longest_col = max(longest_col, max([len(v) for v in r]))

        header = [cell(h, longest_col) for h in header]
        rows = [[cell(v, longest_col) for v in row] for row in rows]

        cell_sep = " | "
        print(cell_sep.join(header))
        for row in rows:
            print(cell_sep.join(row))

        
        
        
        
        
        

