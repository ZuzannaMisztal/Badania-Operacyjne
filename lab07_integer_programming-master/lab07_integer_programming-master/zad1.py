from saport.integer.model import Model 

m = Model("Sense of Life")

x1 = m.create_variable("moules marinieres")
x2 = m.create_variable("pate de foie gras")
x3 = m.create_variable("beluga caviar")
x4 = m.create_variable("egg Benedictine")
x5 = m.create_variable("wafer_thin mint")
x6 = m.create_variable("salmon mousse")

m.add_constraint(2.15 * x1 + 2.75 * x2 + 3.35 * x3 + 3.55 * x4 + 4.20 * x5 + 5.80 * x6 <= 50)
m.add_constraint(x1 <= 5)
m.add_constraint(x2 <= 6)
m.add_constraint(x3 <= 7)
m.add_constraint(x4 <= 5)
m.add_constraint(x5 <= 1)
m.add_constraint(x6 <= 1)

m.maximize(3 * x1 + 4 * x2 + 4.5 * x3 + 4.65 * x4 + 8 * x5 + 9 * x6)

solution = m.solve()

print(m)
print(solution)
