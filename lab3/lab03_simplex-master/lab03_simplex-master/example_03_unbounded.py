import logging
from saport.simplex.model import Model
from saport.simplex.solver import UnboundedException


def run():
    model = Model("example_01_solvable")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(-1*x1 <= 150)
    model.add_constraint(-1*x2 <= 250)
    model.add_constraint(-2*x1 - x2 <= 500)

    model.maximize(8 * x1 + 5 * x2)

    try:
        solution = model.solve()
    except UnboundedException:
        logging.info("Congratulations! You found an unfesiable solution :)")
    else:
        raise AssertionError("This problem has no solution but your algorithm hasn't figured it out!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
