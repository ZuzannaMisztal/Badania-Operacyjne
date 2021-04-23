import logging
import saport.simplex.model as m

model = m.Model("Zad4")

x1 = model.create_variable("x1")
x2 = model.create_variable("x2")  # jeden zwój o długości 105, jeden 75
x3 = model.create_variable("x3")
x4 = model.create_variable("x4")
x5 = model.create_variable("x5")
x6 = model.create_variable("x6")
x7 = model.create_variable("x7")  # 2 zwoje 75, 1 zwój 35
x8 = model.create_variable("x8")
x9 = model.create_variable("x9")
x10 = model.create_variable("x10")
x11 = model.create_variable("x11")
x12 = model.create_variable("x12")
x13 = model.create_variable("x13")
x14 = model.create_variable("x14")
x15 = model.create_variable("x15")  # 5 zwojów 35

model.add_constraint(x1 + x2 + x3 + x4 == 150)
model.add_constraint(x2 + x5 + 2 * x6 + 2 * x7 + x8 + x9 + x10 == 200)
model.add_constraint(x3 + 2 * x4 + x7 + x8 + 2 * x9 + 3 * x10 + x11 + 2 * x12 + 3 * x13 + 4 * x14 + 5 * x15 == 150)

model.minimize(95 * x1 + 20 * x2 + 60 * x3 + 25 * x4 + 125 * x5 + 50 * x6 + 15 * x7 +
               90 * x8 + 55 * x9 + 20 * x10 + 165 * x11 + 130 * x12 + 95 * x13 + 60 * x14 + 25 * x15)

solution = model.solve()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.info(solution)
