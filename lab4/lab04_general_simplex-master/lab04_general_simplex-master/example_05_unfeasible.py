import logging
from saport.simplex.model import Model 


def run():
    model = Model("example_05_unfeasible")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(x1 >= 150)
    model.add_constraint(x2 >= 250)
    model.add_constraint(2 * x1 + x2 <= 500)

    model.maximize(8 * x1 + 5 * x2)

    try:
        model.solve()
        raise AssertionError("Your algorithm found a solution to an unfeasible problem. This shouldn't happen...")
    except:
        logging.info("Congratulations! This problem is unfeasible and your algorithm has found that :)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
