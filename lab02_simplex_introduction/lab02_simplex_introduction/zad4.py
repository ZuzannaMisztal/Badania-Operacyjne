import saport.simplex.model as m

model = m.Model("Assignment 4")

# x1 - produkcja samego zwoju 105cm = 105cm i 95cm odpadu
# x12 - produkcja naraz zwojów 105cm i 75cm = 180cm i 20cm odpadu
# x13 - produkcja naraz zwojów 105cm i 35cm = 140cm i 60cm odpadu
# x133 - produkcja naraz zwojów 105cm i 2*35cm = 175cm i 25cm odpadu
# x2 - produkcja samego zwoju 75cm = 75cm i 125cm odpadu
# x22 - produkcja naraz dwóch zwojów 75cm = 150cm i 50cm odpadu
# x223 - produkcja naraz zwojów 2*75cm i 35cm = 185cm i 15cm odpadu
# x23 - produkcja naraz zwojów 75cm i 35cm = 110cm i 90cm odpadu
# x233 - produkcja naraz zwojów 75cm i 2*35cm = 145cm i 55cm odpadu
# x2333 - produkcja naraz zwojów 75cm i 3*35cm = 180cm i 20cm odpadu
# x3 - produkcja samego zwoju 35cm = 35cm i 165cm odpadu
# x33 - produkcja dwóch zwojów 35cm = 70cm i 130cm odpadu
# x333 - produkcja trzech zwojów 35cm = 105xcm i 95cm odpadu
# x3333 - produkcja czterech zwojów 35cm = 140cm i 60cm odpadu
# x33333 - produkcja czterech zwojów 35cm = 175cm i 25cm odpadu
x1 = model.create_variable("x1")
x12 = model.create_variable("x12")
x13 = model.create_variable("x13")
x133 = model.create_variable("x133")
x2 = model.create_variable("x2")
x22 = model.create_variable("x22")
x223 = model.create_variable("x223")
x23 = model.create_variable("x23")
x233 = model.create_variable("x233")
x2333 = model.create_variable("x2333")
x3 = model.create_variable("x3")
x33 = model.create_variable("x33")
x333 = model.create_variable("x333")
x3333 = model.create_variable("x3333")
x33333 = model.create_variable("x33333")

model.add_constraint(x1 + x12 + x13 + x133 >= 150)
model.add_constraint(x12 + x2 + 2*x22 + 2*x223 + x23 + x233 + x2333 >= 200)
model.add_constraint(x13 + 2*x133 + x223 + x23 + 2*x233 + 3*x2333 + x3 + 2*x33 + 3*x333 + 4*x3333 + 5*x33333 >= 150)

model.minimize(95*x1 + 20*x12 + 60*x13 + 25*x133 + \
               125*x2 + 50*x22 + 15*x223 + 90*x23 + 55*x233 + 20*x2333 + \
               165*x3 + 130*x33 + 95*x333 + 60*x3333 + 25*x33333)

print(model)

model.solve()
