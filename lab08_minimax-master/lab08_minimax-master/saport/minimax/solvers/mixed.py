from dataclasses import dataclass
from .solver import AbstractSolver
from ..model import Game, Equilibrium, Strategy
from ...simplex import model as lpmodel
from ...simplex import solution as lpsolution
from ...simplex.expressions import expression as expr
import numpy as np
from typing import Tuple, List


class MixedSolver(AbstractSolver):

    def solve(self) -> Equilibrium:
        shifted_game, shift = self.shift_game_rewards()

        # don't remove this print, it will be graded :)
        print(f"- shifted game: \n{shifted_game}")

        a_model = self.create_max_model(shifted_game)
        b_model = self.create_min_model(shifted_game)       
        a_solution = a_model.solve()
        b_solution = b_model.solve()

        a_probabilities = self.extract_probabilities(a_solution)
        b_probabilities = self.extract_probabilities(b_solution)

        strategy_a = Strategy(a_probabilities)
        strategy_b = Strategy(b_probabilities)

        value = a_solution.objective_value() - shift
        equilibrium = Equilibrium(value, strategy_a, strategy_b)
        # TODO: the correct Equilibirum instead of None
        return equilibrium

    def shift_game_rewards(self) -> Tuple[Game, float]:
        shift = 0
        maximin = max(min(row) for row in self.game.reward_matrix)
        if maximin < 0:
            shift = - maximin
        return Game(self.game.reward_matrix + shift), shift

    def create_max_model(self, game: Game) -> lpmodel.Model:
        a_actions, b_actions = game.reward_matrix.shape

        a_model = lpmodel.Model("A")

        #TODO:
        # one variable for game value
        # + as many variables as there are actions available for player A
        # sum of those variables should be equal 1
        # for each column, value - column * actions <= 0
        # maximize value variable

        z = a_model.create_variable("z")
        action_variables = np.array([a_model.create_variable(f"x{i}") for i in range(1, a_actions + 1)])
        a_model.add_constraint(action_variables.sum() == 1)
        for column in np.transpose(game.reward_matrix):
            a_model.add_constraint(z + (expr.Expression.from_vectors(action_variables, column) * -1) <= 0)
        a_model.maximize(z)
        return a_model

    def create_min_model(self, game: Game) -> lpmodel.Model:
        a_actions, b_actions = game.reward_matrix.shape

        b_model = lpmodel.Model("B")
        
        #TODO:
        # one variable for game value
        # + as many variables as there are actions available for playerBA
        # sum of those variables should be equal 1
        # for each row, value - row * actions >= 0
        # minimize value variable

        z = b_model.create_variable("z")
        action_variables = np.array([b_model.create_variable(f"y{i}") for i in range(1, b_actions + 1)])
        b_model.add_constraint(action_variables.sum() == 1)
        for row in game.reward_matrix:
            b_model.add_constraint(z + (expr.Expression.from_vectors(action_variables, row) * -1) >= 0)
        b_model.minimize(z)
        return b_model

    def extract_probabilities(self, solution: lpsolution.Solution) -> List[float]:
        return [solution.value(x) for x in solution.model.variables if not solution.model.objective.depends_on_variable(solution.model, x)]

