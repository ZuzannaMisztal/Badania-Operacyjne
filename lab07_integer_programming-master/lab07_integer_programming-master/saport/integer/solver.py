from copy import deepcopy

from saport.simplex.solution import Solution

from ..simplex import solver as lpsolver
import math
import time 


class Solver:
    """
        Naive branch and bound solver for integer programming problems


        Attributes
        ----------
        model : Model
            integer programming model to be solved
        timelimit: int
            what is the maximal solving time (in seconds)
        total_time: float
            how long it took to solve the problem
        start_time: float
            when the solving started
        interrupted: bool
            whether solving has been interrupted (by timeout)

        Methods
        -------
        start_timer():
            remember the starting time for the solver
        stop_timer():
            stores the total solving time
        wall_time() -> float:
            returns how long solver has been working
        timeout() -> bool:
            whether solver should stop working due to the timeout

        solve(model: Model, timelimit: int) -> Solution:
            solves the given model within a specified timelimit
        branch_and_bound(model: Model):
            processes given model in branch and bound fashion (recursively)
        find_float_assignment(solution: Solution):
            finds a variable with non-integer value in the current solution
            returns None if the solution is a correct integer solution
        model_with_new_constraint(self, model, constraint):
            creates a new model with an additional constraint
    """  

    def solve(self, model, timelimit):
        self.timelimit = timelimit
        self.total_time = None
        self.start_time = None
        self.interrupted = False

        self.model = model
        self.lower_bound = float('-inf')
        self.best_solution = None

        self.start_timer()
        self.branch_and_bound(model)
        self.stop_timer()

        return self.best_solution
           
    def branch_and_bound(self, model):
        #TODO: implement a branch and bound procedure
        # tip1: remember to check for the timeout and set te self.interrupted to True when it happens
        # tip2: remember to hande infeasible and unbounded models, check `simplex_examples` to know how to check for this condition
        if self.timeout():
            self.interrupted = True
            return

        lp_solution = lpsolver.Solver().solve(model)
        if not (lp_solution.is_bounded and lp_solution.is_feasible):
            return

        upper_bound = lp_solution.objective_value()
        if upper_bound <= self.lower_bound:
            return

        assignment = self.find_float_assignment(lp_solution)
        if assignment is None:
            if lp_solution.objective_value() > self.lower_bound:
                self.best_solution = lp_solution
                self.lower_bound = lp_solution.objective_value()
            return

        var, value = assignment
        new_model_1 = self.model_with_new_constraint(model, var <= math.floor(value))
        new_model_2 = self.model_with_new_constraint(model, var >= math.ceil(value))
        self.branch_and_bound(new_model_1)
        self.branch_and_bound(new_model_2)
        
    def find_float_assignment(self, solution: Solution):
        threshold = 0.00002
        for variable in solution.model.variables:
            assignment = solution.assignment[variable.index]
            is_int = abs(int(assignment) - assignment) < threshold
            if not is_int:
                return variable, assignment

    def model_with_new_constraint(self, model, constraint):
        new_model = deepcopy(model)
        new_model.add_constraint(constraint)
        return new_model

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        self.total_time = self.wall_time()

    def wall_time(self) -> float:
        return time.time() - self.start_time

    def timeout(self) -> bool:
        return self.wall_time() > self.timelimit
