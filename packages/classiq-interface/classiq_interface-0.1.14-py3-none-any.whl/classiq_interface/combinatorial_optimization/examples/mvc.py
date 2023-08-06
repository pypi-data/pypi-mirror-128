import networkx as nx
import pyomo.core as pyo


def mvc(graph: nx.Graph, k: int) -> pyo.ConcreteModel:
    model = pyo.ConcreteModel()
    model.Nodes = pyo.Set(initialize=list(graph.nodes))
    model.Arcs = pyo.Set(initialize=list(graph.edges))
    model.x = pyo.Var(model.Nodes, domain=pyo.Binary)
    model.amount_constraint = pyo.Constraint(expr=sum(model.x.values()) == k)

    def obj_expression(model):
        # number of edges not covered
        return sum((1 - model.x[i]) * (1 - model.x[j]) for i, j in model.Arcs)

    model.cost = pyo.Objective(rule=obj_expression, sense=pyo.minimize)

    return model
