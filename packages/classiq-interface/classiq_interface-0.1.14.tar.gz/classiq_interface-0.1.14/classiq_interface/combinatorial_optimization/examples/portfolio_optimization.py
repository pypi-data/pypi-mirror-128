from typing import List

import numpy as np
import pyomo.core as pyo


def portfolio_optimization(
    covariances: List[List[float]], returns: List[float], budget: int
) -> pyo.ConcreteModel:
    model = pyo.ConcreteModel()
    model.x = pyo.Var(range(len(returns)), domain=pyo.Binary)
    x_array = np.array(model.x.values())

    model.budget = pyo.Constraint(expr=(sum(x_array) == budget))

    model.risk = x_array @ covariances @ x_array
    model.profit = returns @ x_array

    model.cost = pyo.Objective(expr=model.risk - model.profit, sense=pyo.minimize)

    return model
