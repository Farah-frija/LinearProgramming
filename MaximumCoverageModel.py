from __future__ import annotations

import gurobipy as gp
from gurobipy import GRB


def maximum_coverage_problem(
        zone_poids: dict[int, int],
        site_coverage_cost: dict[int, list[set[int] | float]],
        budget: float
):
    try:
        # Parameters
        zones, poids = gp.multidict(zone_poids)

        sites, coverage, cost = gp.multidict(site_coverage_cost)

        # MIP  model formulation
        m = gp.Model("maximum_coverage")

        build = m.addVars(len(sites), vtype=GRB.BINARY, name="Build")
        is_covered = m.addVars(len(zones), vtype=GRB.BINARY, name="Is_covered")

        m.addConstrs((gp.quicksum(build[t] for t in sites if r in coverage[t]) >= is_covered[r]
                      for r in zones), name="Build2cover")
        m.addConstr(build.prod(cost) <= budget, name="budget")
        m.addConstr(build.sum() >= 1, name="at_least_one")

        m.setObjective(is_covered.prod(poids), GRB.MAXIMIZE)

        m.setParam(GRB.Param.PoolSolutions, 4)
        m.setParam(GRB.Param.PoolSearchMode, 2)
        m.setParam(GRB.Param.PoolGap, 0.001)

        m.optimize()

        print("le nombre de solution est : ", m.SolCount)

        # Checking the status of the model
        if m.status == GRB.OPTIMAL:
            print("Une solution optimale est trouvée")
        elif m.status == GRB.INFEASIBLE:
            print("infeasible")
        elif m.status == GRB.INF_OR_UNBD:
            print("error")

        # Display all solutions found in the solution pool

        solutions = []

        for k in range(m.SolCount):
            m.setParam(GRB.Param.SolutionNumber, k)
            print(f"\nSolution {k + 1}:")
            solution_k = {}
            locations_built_k = []
            for location in build.keys():
                if abs(build[location].getAttr(GRB.Attr.Xn) - 1) < 1e-6:
                    print(f"Build a cell location at location location {location}.")
                    locations_built_k.append(location)
            solution_k["locations_built"] = locations_built_k
            total_cost = sum(cost[location] * int(build[location].getAttr(GRB.Attr.Xn)) for location in range(len(sites)))
            solution_k["total_cost"] = total_cost
            budget_consumption = round(100 * total_cost / budget, 2)
            solution_k["budget_consumption"] = budget_consumption
            print(f"Percentage of budget consumed: {budget_consumption}%")
            total_poids = sum(poids[region] for region in range(len(zones)))
            solution_k["total_poids"] = total_poids
            coverage_percentage = round(100 * is_covered.prod(poids).getValue() / total_poids, 2)
            solution_k["coverage_percentage"] = coverage_percentage
            print(f"poids coverage: {coverage_percentage}%")
            solutions.append(solution_k)

        #return solutions
        sorted_solutions = sorted_array = sorted(solutions, key=lambda x: x['total_cost'])
        return sorted_solutions
    except Exception as e:
        raise Exception(e)

    solutions = cell_location_problem(
    {
        0: 523, 1: 690, 2: 420,
        3: 1010, 4: 1200, 5: 5850,
        6: 400, 7: 1008, 8: 950,
        9: 1100
    },
    {
        0: [{0, 1, 5, 9}, 4.2],
        1: [{0, 7, 8}, 6.1],
        2: [{2, 3, 4, 6, 9}, 5.2],
        3: [{2, 5, 6}, 5.5],
        4: [{0, 2, 6, 7, 8}, 4.8],
    }
    ,
    2
)
    print("*" * 50)
    print("*" * 50)
    print(solutions)
