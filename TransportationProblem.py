from gurobipy import Model, GRB, quicksum

def transport_optimization_simple(I, J, c, q, d, s):
    """
    Modèle d'optimisation simplifié sans modes de transport.

    I : liste des indices des origines (entiers)
    J : liste des indices des destinations (entiers)
    c : dict {(i,j): coût unitaire}
    q : dict {(i,j): capacité max}
    d : dict {j: demande}
    s : dict {i: offre}
    """

    model = Model("Transport_Optimization_Simple")

    # Variables de décision
    x = model.addVars(I, J, lb=0, name="x")

    # Objectif : minimiser le coût total
    model.setObjective(quicksum(c[i,j] * x[i,j] for i in I for j in J), GRB.MINIMIZE)

    # Contraintes de demande
    for j in J:
        model.addConstr(quicksum(x[i,j] for i in I) >= d[j], name=f"Demand_{j}")

    # Contraintes d'offre
    for i in I:
        model.addConstr(quicksum(x[i,j] for j in J) <= s[i], name=f"Supply_{i}")

    # Contraintes de capacité
    for i in I:
        for j in J:
            model.addConstr(x[i,j] <= q[i,j], name=f"Capacity_{i}_{j}")

    # Optimiser
    model.optimize()

    if model.status == GRB.OPTIMAL:
        solution = {(i,j): x[i,j].X for i in I for j in J}
        return solution,model
    else:
        print("Aucune solution optimale trouvée.")
        return None

# Exemple d'utilisation avec indices entiers
if __name__ == "__main__":
    # Origines : 0 = UsineA, 1 = EntrepotB
    I = [0, 1]
    # Destinations : 0 = Client1, 1 = Client2
    J = [0, 1]

    c = {
        (0,0): 10,
        (0,1): 12,
        (1,0): 11,
        (1,1): 13,
    }

    q = {
        (0,0): 100,
        (0,1): 90,
        (1,0): 60,
        (1,1): 40,
    }

    d = {
        0: 120,
        1: 100,
    }

    s = {
        0: 150,
        1: 100,
    }

    solution = transport_optimization_simple(I, J, c, q, d, s)

    if solution:
        print("Solution optimale :")
        for (i,j), val in solution.items():
            if val > 0:
                print(f"Transporter {val:.2f} unités de l'origine {i} vers la destination {j}")

