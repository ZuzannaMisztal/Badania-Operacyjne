import saport.simplex.model as m

model = m.Model("Assignment 2")

p1 = model.create_variable("P1")
p2 = model.create_variable("P2")
p3 = model.create_variable("P3")
p4 = model.create_variable("P4")

model.add_constraint(0.8*p1 + 2.4*p2 + 0.9*p3 + 0.4*p4 >= 1200)
model.add_constraint(0.6*p1 + 0.6*p2 + 0.3*p3 + 0.3*p4 >= 600)

model.minimize(9.6*p1 + 14.4*p2 + 10.8*p3 + 7.2*p4)

print(model)

model.solve()
