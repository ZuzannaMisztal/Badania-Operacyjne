import saport.simplex.model as m

model = m.Model("Assignment 3")

# x1 - liczba porcji steków
# x2 - liczba porcji ziemniaków
x1 = model.create_variable("x1")
x2 = model.create_variable("x2")


model.add_constraint(5*x1 + 15*x2 >= 50)
model.add_constraint(20*x1 + 5*x2 >= 40)
model.add_constraint(15*x1 + 2*x2 <= 60)

model.minimize(8*x1 + 4*x2)

print(model)

model.solve()
