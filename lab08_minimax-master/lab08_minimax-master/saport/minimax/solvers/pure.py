from dataclasses import dataclass
from .solver import AbstractSolver
from ..model import Game, Equilibrium, Strategy
from typing import List
import numpy as np


class PureSolver(AbstractSolver):

    def solve(self) -> List[Equilibrium]:
        #TODO: basic solver finding all pure equilibriums
        #      reminder: 
        #      if max of the column is the same as min of the row
        #      it is an equilibrium
        #      in case there is no pure equilibrium - should return an empty list
        result = []
        minimax = self.minimax()
        maximin = self.maximin()
        if minimax[1] == maximin[1]:
            strategy_a = Strategy.with_action(maximin[0], len(self.game.reward_matrix))
            strategy_b = Strategy.with_action(minimax[0], len(self.game.reward_matrix[0]))
            result.append(Equilibrium(minimax[1], strategy_a, strategy_b))
        return result

    def minimax(self):
        max_of_column = [max(column) for column in np.transpose(self.game.reward_matrix)]
        best = (0, max_of_column[0])
        for i, val in enumerate(max_of_column):
            if val < best[1]:
                best = (i, val)
        return best

    def maximin(self):
        min_of_row = [min(row) for row in self.game.reward_matrix]
        best = (0, min_of_row[0])
        for i, val in enumerate(min_of_row):
            if val > best[1]:
                best = (i, val)
        return best
