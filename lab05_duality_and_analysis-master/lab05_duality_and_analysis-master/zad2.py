# remember to print the dual model (just print()) and the analysis results (analyser.interpret_results(solution, analysis_results))
# in case of doubt refer to examples 06 and 07

from saport.simplex.analyser import Analyser
from saport.simplex.model import Model

model = Model("Zad2")

x1 = model.create_variable("x1")
x2 = model.create_variable("x2")
x3 = model.create_variable("x3")

model.add_constraint(8 * x1 + 6 * x2 + x3 <= 960)
model.add_constraint(8 * x1 + 4 * x2 + 3 * x3 <= 800)
model.add_constraint(4 * x1 + 3 * x2 + x3 <= 320)

model.maximize(60 * x1 + 30 * x2 + 20 * x3)

dual = model.dual()

print(dual)

solution = model.solve()

analyser = Analyser()
analysis_result = analyser.analyse(solution)
analyser.interpret_results(solution, analysis_result)
