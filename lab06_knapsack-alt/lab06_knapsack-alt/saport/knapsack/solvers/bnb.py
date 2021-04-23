from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
from typing import List


class AbstractBnbSolver(AbstractSolver):
    """
    An abstract branch-and-bound solver for the knapsack problems.

    Methods:
    --------
    upper_bound(left : List[Item], solution: Solution) -> float:
        given the list of still available items and the current solution,
        calculates the linear relaxation of the problem
    """
    
    def upper_bound(self, left : List[Item], solution: Solution) -> float:
        #TODO: implement the linear relaxation, i.e. assume you can take   
        #      fraction of the items in the backpack
        #      return the value of such a solution
        #      tip1: solution is your starting point
        #      tip2: left is the list of items you can still take
        weight_left = self.problem.capacity - solution.weight
        to_add = sorted(left, key=lambda x: x.value / x.weight, reverse=True)
        upper_bound = solution.value
        for item in to_add:
            if weight_left >= item.weight:
                upper_bound += item.value
            else:
                upper_bound += item.value * weight_left / item.weight
                break
        return upper_bound
        
    def solve(self) -> Solution:
        raise Exception("this is an abstract solver, don't try to run it!")