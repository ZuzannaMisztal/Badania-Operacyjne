import saport.simplex.model as m

model = m.Model("Assignment 1")

x1 = model.create_variable("x1")
x2 = model.create_variable("x2")
x3 = model.create_variable("x3")

model.add_constraint(x1 + x2 + x3 <= 30)
model.add_constraint(x1 + 2*x2 + x3 >= 10)
model.add_constraint(2*x2 + x3 <= 20)

model.minimize(2 * x1 +  x2 + 3 * x3)

print(model)

model.solve()