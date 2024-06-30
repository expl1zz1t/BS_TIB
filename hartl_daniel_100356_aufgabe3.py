import matplotlib.pyplot as plt
import graphviz as gv
import numpy as np

class STATE:
    def __init__(self, name, num):
        self.name = name
        self.num = num
        return

class TRANSITION:
    def __init__(self, source, destination, name, rate):
        self.source = source
        self.destination = destination
        self.name = name
        self.rate = rate
        return
    
class MARKOV:
    def __init__(self, name, dt=1.0):
        self.nodes = []
        self.transitions = []
        self.name = name
        self.transition_matrix = None
        return
    
    def state(self, node):
        self.nodes.append(node)
        return
    
    def transition(self, edge):
        self.transitions.append(edge)
        return
    
    def build_transition_matrix(self):
        n = len(self.nodes)
        P = np.zeros((n, n))
        for t in self.transitions:
            i = t.source.num
            j = t.destination.num
            P[i, j] = t.rate
        for i in range(n):
            P[i, i] = 1 - np.sum(P[i])
        self.transition_matrix = P

    def simulate(self, hours):
        state = np.zeros(len(self.nodes))
        state[0] = 1  # Anfangszustand ist S0
        for _ in range(hours):
            state = np.dot(state, self.transition_matrix)
        return state

    def probability(self, hours):
        self.build_transition_matrix()
        result = self.simulate(hours)
        return result
    
    def plot(self):
        self.dot = gv.Digraph(self.name, format="png")
               
        for node in self.nodes:
            self.dot.node(node.name)
                
        for node in self.transitions:
            self.dot.edge(node.source.name, node.destination.name)
        
        return self.dot.render()    
     
  
#Beispiel    
B = MARKOV("Beispiel")
B_S1 = STATE('S1',0)
B_S2 = STATE('S2',1)
B.state(B_S1)
B.state(B_S2)
B.transition(TRANSITION(B_S1, B_S2, 'l12', 1000))
B.plot()

#Aufgabe 3
M = MARKOV("Markov Graph")
S1 = STATE('S1 Normal',1)
S2 = STATE('S2 Eine SPS',2)
S3 = STATE('S3 Beide SPS',3)
S4 = STATE('S4 Wartung',4)
S5 = STATE('S5 Ausgang',5)
S6 = STATE('S6 Eingang',6)

lam = 1 / 3000
mu  = 1 / 8

M.state(S1)
M.state(S2)
M.state(S3)
M.state(S4)
M.state(S5)
M.state(S6)

M.transition(TRANSITION(S1, S2, 'λ12', lam))
M.transition(TRANSITION(S1, S3, 'λ13', lam))
M.transition(TRANSITION(S2, S5, 'λ25', lam))
M.transition(TRANSITION(S3, S5, 'λ35', lam))
M.transition(TRANSITION(S2, S1, 'μ21', mu))
M.transition(TRANSITION(S3, S1, 'μ31', mu))
M.transition(TRANSITION(S5, S4, 'μ54', mu))
M.transition(TRANSITION(S4, S1, 'μ41', mu))
M.transition(TRANSITION(S4, S2, 'μ42', mu))
M.transition(TRANSITION(S4, S3, 'μ43', mu))

# Simulation
prob_40_days = M.probability(40 * 24)
prob_6_months = M.probability(6 * 30 * 24)
prob_12_years = M.probability(12 * 365 * 24)

print(f"Verfügbarkeit nach 40 Tagen: {prob_40_days[0]:.6f}")
print(f"Verfügbarkeit nach 6 Monaten: {prob_6_months[0]:.6f}")
print(f"Verfügbarkeit nach 12 Jahren: {prob_12_years[0]:.6f}")

print("Create Markov Graph")
M.plot()
